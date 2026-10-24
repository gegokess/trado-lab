"""Hypothese H1: Lange 1h-Wicks werden nach teilweiser Füllung weiter gefüllt.

Regel (untere Wick, obere Wick spiegelbildlich mit Long):
- In der laufenden Stunde: Open O, Tief L, höchstes Hoch nach L = Rebound P
- Wick W = min(O, P) - L, Oberkante T = min(O, P)
- Setup aktiv, wenn W >= k * ATR14 der abgeschlossenen 1h-Kerzen
- Einstieg Short per Stop-Market bei T - fill_in * W (Taker)
- TP als Limit bei T - fill_out * W (Maker), SL per Stop-Market bei Einstieg + sl_w * W (Taker)
- Ein Trade pro Stunde, nicht ausgelöste Einstiegsorder verfällt zur vollen Stunde
- Zeitstopp nach hold_min Minuten (Market)
"""
from collections import deque
from decimal import Decimal

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Bar, BarType, InstrumentId, OrderSide, OrderType, Price, Quantity

from strategies.base import LabStrategy

HOUR_NS = 3_600_000_000_000
MIN_NS = 60_000_000_000


class WickFillConfig(StrategyConfig):
    def __init__(self, *, instrument_id: InstrumentId, bar_type: BarType,
                 side: str = "lower",      # "lower" = untere Wick -> Short, "upper" = obere Wick -> Long
                 k_atr: float = 1.5, fill_in: float = 0.2, fill_out: float = 0.8,
                 sl_w: float = 0.6, hold_min: int = 360, qty: str = "0.01", **_kw) -> None:
        super().__init__()
        self.instrument_id, self.bar_type, self.side = instrument_id, bar_type, side
        self.k_atr, self.fill_in, self.fill_out, self.sl_w = k_atr, fill_in, fill_out, sl_w
        self.hold_min, self.qty = hold_min, qty


class WickFill(LabStrategy):
    def __init__(self, config: WickFillConfig):
        super().__init__(config)
        c = config
        self.sg = 1.0 if c.side == "lower" else -1.0   # Rechnen im gespiegelten Raum für obere Wicks
        self.entry_side = OrderSide.SELL if c.side == "lower" else OrderSide.BUY
        self.hour = None
        self.O = self.L = self.P = None
        self.h_hi = self.h_lo = self.h_close = None
        self.prev_close = None
        self.trs = deque(maxlen=14)
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

    # Ablauf je abgeschlossener Minute ------------------------------------------
    def handle_bar(self, bar: Bar):
        c = self.config
        o, h, l, cl = (float(bar.open), float(bar.high), float(bar.low), float(bar.close))
        hid = bar.ts_event // HOUR_NS

        # Zeitstopp
        if self.entry_ts is not None and not self._flat() and bar.ts_init - self.entry_ts >= c.hold_min * MIN_NS:
            self.close_all_positions(c.instrument_id)
            self.cancel_all_orders(c.instrument_id)

        # Neue Stunde: ATR fortschreiben, Wick-Zustand zurücksetzen, offene Einstiegsorder verfallen lassen
        if hid != self.hour:
            if self.hour is not None:
                pc = self.prev_close if self.prev_close is not None else self.h_close
                self.trs.append(max(self.h_hi - self.h_lo, abs(self.h_hi - pc), abs(self.h_lo - pc)))
                self.prev_close = self.h_close
            self.hour, self.used = hid, False
            self.h_hi, self.h_lo, self.h_close = h, l, cl
            self._cancel_entry()
            # Wick-Zustand im gespiegelten Raum: untere Wick wie gehabt, obere über negierte Preise
            mo, mh, ml, mc = self._mirror(o, h, l, cl)
            self.O, self.L, self.P = mo, ml, mc
        else:
            self.h_hi, self.h_lo, self.h_close = max(self.h_hi, h), min(self.h_lo, l), cl
            mo, mh, ml, mc = self._mirror(o, h, l, cl)
            if ml < self.L:
                self.L, self.P = ml, mc   # neues Tief: Rebound beginnt neu (Reihenfolge in der Minute unbekannt)
            else:
                self.P = max(self.P, mh)

        if self.used or not self._flat():
            return
        atr = self._atr()
        if atr is None:
            return
        T = min(self.O, self.P)
        W = T - self.L
        if W <= 0 or W < c.k_atr * atr:
            self._cancel_entry()
            return
        mE, mTP = T - c.fill_in * W, T - c.fill_out * W
        mSL = mE + c.sl_w * W
        E, TP, SL = (self._unmirror(x) for x in (mE, mTP, mSL))
        if mc <= mTP:          # Ziel schon erreicht, kein Einstieg mehr sinnvoll
            self._cancel_entry()
            return
        new = (self._px(E), self._px(TP), self._px(SL))
        if self.levels == new:
            return
        self._cancel_entry()
        qty = Quantity.from_str(c.qty)
        if mc <= mE:   # Kurs schon unter dem Einstiegslevel (Sprung): sofort Market
            order = self.order_factory.market(c.instrument_id, self.entry_side, qty)
        else:          # Stop-Market (Brackets erlauben keinen Stop-Einstieg, TP/SL folgen in on_position_opened)
            order = self.order_factory.stop_market(c.instrument_id, self.entry_side, qty, trigger_price=new[0])
        self.submit_order(order)
        self.levels = new
        self.plan = dict(entry=float(new[0]), sl=float(new[2]), tp=float(new[1]), wick=W, atr=atr)

    def handle_position_opened(self, event):
        """Sofort nach dem Einstieg: TP als Post-Only-Limit (Maker), SL als Stop-Market (Taker), beide reduce-only."""
        c = self.config
        self.used = True
        self.entry_ts = event.ts_event
        self.levels = None
        exit_side = OrderSide.BUY if self.entry_side == OrderSide.SELL else OrderSide.SELL
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
