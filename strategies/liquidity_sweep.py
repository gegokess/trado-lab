"""Hypothese H2: Ein Sweep eines unberührten Swing-Levels kehrt um.

Regel (untere Seite, obere Seite spiegelbildlich mit Short):
- Swing-Tief: abgeschlossene 1h-Kerze, deren Tief strikt unter den Tiefs der sw Stunden davor und
  danach liegt, nutzbar erst ab der Bestätigung sw Stunden später
- ein Swing-Tief fällt dauerhaft weg, sobald eine abgeschlossene Stunde darunter gehandelt hat
- Referenzlevel S der laufenden Stunde: höchstes unberührtes Swing-Tief unterhalb des Stundenopens
- in der laufenden Stunde: Open O, Tief L, höchstes Hoch nach L = Rebound P, Oberkante T = min(O, P), Wick W = T - L
- Setup aktiv, wenn W >= k_atr * ATR14 der abgeschlossenen 1h-Kerzen und L < S <= T
- Einstieg Long bei L + entry_w * W. Sobald das Setup gültig ist, hat der Rebound dieses Level in der
  Regel schon überholt, der Einstieg erfolgt dann per Market (Taker), sonst per Stop-Market
- TP als Limit bei T + tp_w * W (Maker), SL per Stop-Market bei L - sl_w * W (Taker)
- ein Trade pro Stunde, nicht ausgelöste Einstiegsorder verfällt zur vollen Stunde
- Zeitstopp nach hold_min Minuten (Market)
"""
from collections import deque

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Bar, BarType, InstrumentId, OrderSide, Price, Quantity

from strategies.base import LabStrategy

HOUR_NS = 3_600_000_000_000
MIN_NS = 60_000_000_000


class LiquiditySweepConfig(StrategyConfig):
    def __init__(self, *, instrument_id: InstrumentId, bar_type: BarType,
                 side: str = "lower",      # "lower" = Sweep eines Swing-Tiefs -> Long, "upper" -> Short
                 k_atr: float = 1.0, entry_w: float = 0.3, tp_w: float = 0.5, sl_w: float = 0.2,
                 sw: int = 3, hold_min: int = 360, qty: str = "0.01", **_kw) -> None:
        super().__init__()
        self.instrument_id, self.bar_type, self.side = instrument_id, bar_type, side
        self.k_atr, self.entry_w, self.tp_w, self.sl_w = k_atr, entry_w, tp_w, sl_w
        self.sw, self.hold_min, self.qty = sw, hold_min, qty


class LiquiditySweep(LabStrategy):
    def __init__(self, config: LiquiditySweepConfig):
        super().__init__(config)
        c = config
        self.sg = 1.0 if c.side == "lower" else -1.0   # Rechnen im gespiegelten Raum für die obere Seite
        self.entry_side = OrderSide.BUY if c.side == "lower" else OrderSide.SELL
        self.hour = None
        self.O = self.L = self.P = None
        self.h_hi = self.h_lo = self.h_close = None
        self.prev_close = None
        self.trs = deque(maxlen=14)
        self.lows = deque(maxlen=2 * c.sw + 1)   # gespiegelte Tiefs der letzten abgeschlossenen Stunden
        self.aktiv: list[float] = []             # unberührte, bestätigte Swing-Tiefs (gespiegelt)
        self.S = None
        self.used = False
        self.levels = None          # aktuell platzierte (E, TP, SL) im Originalraum
        self.entry_ts = None

    def on_start(self):
        self.instrument = self.cache.instrument(self.config.instrument_id)
        self.subscribe_bars(self.config.bar_type)

    # Hilfsfunktionen -------------------------------------------------------------
    def _px(self, x: float) -> Price:
        return self.instrument.make_price(x)

    def _atr(self):
        return sum(self.trs) / 14 if len(self.trs) == 14 else None

    def _flat(self) -> bool:
        return self.portfolio.is_net_flat(self.config.instrument_id)

    def _cancel_entry(self):
        if self.levels is not None and self._flat():
            self.cancel_all_orders(self.config.instrument_id)
        self.levels = None

    def _close_hour(self):
        """ATR fortschreiben und die Swing-Tiefs mit der abgeschlossenen Stunde pflegen."""
        sw = self.config.sw
        pc = self.prev_close if self.prev_close is not None else self.h_close
        self.trs.append(max(self.h_hi - self.h_lo, abs(self.h_hi - pc), abs(self.h_lo - pc)))
        self.prev_close = self.h_close
        m_lo = self.h_lo if self.sg > 0 else -self.h_hi
        self.lows.append(m_lo)
        if len(self.lows) == 2 * sw + 1:
            kand = self.lows[sw]
            if all(kand < self.lows[j] for j in range(2 * sw + 1) if j != sw):
                self.aktiv.append(kand)
        self.aktiv = [s for s in self.aktiv if s <= m_lo]   # abgeholte Liquidität fällt weg

    # Ablauf je abgeschlossener Minute ------------------------------------------
    def handle_bar(self, bar: Bar):
        c = self.config
        o, h, l, cl = (float(bar.open), float(bar.high), float(bar.low), float(bar.close))
        hid = bar.ts_event // HOUR_NS
        mo, mh, ml, mc = self._mirror(o, h, l, cl)

        # Zeitstopp
        if self.entry_ts is not None and not self._flat() and bar.ts_init - self.entry_ts >= c.hold_min * MIN_NS:
            self.close_all_positions(c.instrument_id)
            self.cancel_all_orders(c.instrument_id)

        # Neue Stunde: Swing-Level und ATR fortschreiben, Wick zurücksetzen, Einstiegsorder verfallen lassen
        if hid != self.hour:
            if self.hour is not None:
                self._close_hour()
            self.hour, self.used = hid, False
            self.h_hi, self.h_lo, self.h_close = h, l, cl
            self._cancel_entry()
            self.O, self.L, self.P = mo, ml, mc
            unten = [s for s in self.aktiv if s < mo]
            self.S = max(unten) if unten else None
        else:
            self.h_hi, self.h_lo, self.h_close = max(self.h_hi, h), min(self.h_lo, l), cl
            if ml < self.L:
                self.L, self.P = ml, mc   # neues Tief: Rebound beginnt neu (Reihenfolge in der Minute unbekannt)
            else:
                self.P = max(self.P, mh)

        if self.used or not self._flat():
            return
        atr = self._atr()
        if atr is None or self.S is None:
            return
        T = min(self.O, self.P)
        W = T - self.L
        if W <= 0 or W < c.k_atr * atr or not (self.L < self.S <= T):
            self._cancel_entry()
            return
        mE, mTP, mSL = self.L + c.entry_w * W, T + c.tp_w * W, self.L - c.sl_w * W
        if mc >= mTP:          # Ziel schon erreicht, kein Einstieg mehr sinnvoll
            self._cancel_entry()
            return
        E, TP, SL = (self._unmirror(x) for x in (mE, mTP, mSL))
        new = (self._px(E), self._px(TP), self._px(SL))
        if self.levels == new:
            return
        self._cancel_entry()
        qty = Quantity.from_str(c.qty)
        if mc >= mE:   # Rebound hat das Einstiegslevel schon überholt, das ist der Normalfall
            order = self.order_factory.market(c.instrument_id, self.entry_side, qty)
        else:          # Kurs noch unter dem Level: Stop-Market (Brackets erlauben keinen Stop-Einstieg)
            order = self.order_factory.stop_market(c.instrument_id, self.entry_side, qty, trigger_price=new[0])
        self.submit_order(order)
        self.levels = new
        self.plan = dict(entry=float(new[0]), sl=float(new[2]), tp=float(new[1]), wick=W, atr=atr,
                         sweep=self._unmirror(self.S))

    def handle_position_opened(self, event):
        """Sofort nach dem Einstieg: TP als Post-Only-Limit (Maker), SL als Stop-Market (Taker), beide reduce-only."""
        c = self.config
        self.used = True
        self.entry_ts = event.ts_event
        self.levels = None
        exit_side = OrderSide.SELL if self.entry_side == OrderSide.BUY else OrderSide.BUY
        qty = Quantity.from_str(c.qty)
        tp = self.order_factory.limit(c.instrument_id, exit_side, qty, self._px(self.plan["tp"]),
                                      post_only=True, reduce_only=True)
        sl = self.order_factory.stop_market(c.instrument_id, exit_side, qty, trigger_price=self._px(self.plan["sl"]),
                                            reduce_only=True)
        self.submit_order(tp)
        self.submit_order(sl)

    def handle_position_closed(self, event):
        self.entry_ts = None
        self.cancel_all_orders(self.config.instrument_id)

    def _mirror(self, o, h, l, c):
        if self.sg > 0:
            return o, h, l, c
        return -o, -l, -h, -c

    def _unmirror(self, x):
        return x if self.sg > 0 else -x
