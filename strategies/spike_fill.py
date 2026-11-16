"""Hypothese H19: Wick nach Spike zur Hälfte füllen (LABORBUCH.md).

Regel (untere Seite: Spike nach unten, Short; obere Seite spiegelbildlich mit Long):
- Spike: Tief der Minute ist das tiefste der letzten 5 Minuten und liegt mind. spike × S unter dem Hoch S dieser 5 Minuten
- Neues Tief in den 5 Minuten danach verlängert den Spike, später verfällt das Setup. M = S − L
- Erholungshoch RH seit dem Tief, W = RH − L. Ab W >= rb_min × M liegt eine Stop-Market-Order bei RH − fill_in × W
- TP als Post-Only-Limit bei RH − fill_out × W (Maker), SL per Stop-Market bei RH + sl_w × W (Taker)
- Setup verfällt window Minuten nach dem Tief, Zeitstopp hold_min Minuten, nächster Spike frühestens cooldown Minuten später
- Während eine Position offen ist, werden keine neuen Spikes gehandelt (im Scan können sich Trades überlappen)

Erweiterung H21: span = Anzahl Minuten, in denen der Spike entstehen darf (Standard 5)

Erweiterung H20:
- sl_ref = "start": SL über dem Spike-Start bei S + sl_w × M statt über dem Erholungshoch
- trail_w > 0: kein festes Ziel. Ab trail_start × W Füllung Stop auf den tatsächlichen Einstieg, danach nach jeder
  Minute auf bestes Niveau + trail_w × W nachziehen (nur in Gewinnrichtung). R bleibt auf das Anfangsrisiko bezogen

Erweiterung H30:
- tps = "0.5:0.5,1.0:0.3,1.5:0.2": Teilziele als Füllgrad:Anteil der Menge, je als Post-Only-Limit. Ersetzt fill_out
- be_nach_tp1: nach dem ersten Teilziel Stop für die Restmenge auf den tatsächlichen Einstieg
- trail15: nach dem ersten Teilziel Stop nach jeder abgeschlossenen 15m-Kerze unter das letzte bekannte
  15m-Swing-Tief (k = 2) nachziehen, nur in Gewinnrichtung (Long, Short spiegelbildlich)
"""
from collections import deque

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Bar, BarType, InstrumentId, OrderSide, Price, Quantity

from strategies.base import LabStrategy

MIN_NS = 60_000_000_000


class SpikeFillConfig(StrategyConfig):
    def __init__(self, *, instrument_id: InstrumentId, bar_type: BarType,
                 side: str = "lower",      # "lower" = Spike nach unten -> Short, "upper" = Spike nach oben -> Long
                 spike: float = 0.02, rb_min: float = 0.3, fill_in: float = 0.1, fill_out: float = 0.5,
                 sl_w: float = 0.1, window: int = 180, hold_min: int = 4320, cooldown: int = 15,
                 qty: str = "0.01", sl_ref: str = "rh", trail_start: float = 0.5, trail_w: float = 0.0,
                 span: int = 5, tps: str = "", be_nach_tp1: bool = False, trail15: bool = False, **_kw) -> None:
        super().__init__()
        self.instrument_id, self.bar_type, self.side = instrument_id, bar_type, side
        self.spike, self.rb_min, self.fill_in, self.fill_out, self.sl_w = spike, rb_min, fill_in, fill_out, sl_w
        self.window, self.hold_min, self.cooldown, self.qty = window, hold_min, cooldown, qty
        self.sl_ref, self.trail_start, self.trail_w = sl_ref, trail_start, trail_w
        self.span = span
        self.tps, self.be_nach_tp1, self.trail15 = tps, be_nach_tp1, trail15


class SpikeFill(LabStrategy):
    def __init__(self, config: SpikeFillConfig):
        super().__init__(config)
        c = config
        self.sg = 1.0 if c.side == "lower" else -1.0
        self.entry_side = OrderSide.SELL if c.side == "lower" else OrderSide.BUY
        self.highs = deque(maxlen=max(5, config.span))
        self.lows = deque(maxlen=max(5, config.span))
        self.n = 0                  # Zähler der Minuten
        self.last_spike = -10**9
        self.setup = None           # dict mit S, L, M, RH, i_spike, i_low
        self.levels = None          # platzierte (E, TP, SL) im Originalraum
        self.entry_ts = None
        self.last_close = None
        self.pend = None            # Erholungshoch und W (gespiegelt) der platzierten Einstiegsorder
        self.trade = None           # Zustand zum Nachziehen während der Position
        self.sl_order = None
        self.tp_ids = []            # Teilziel-Orders (H30), erste Order löst Stop auf Einstieg aus
        self.rest = None            # nach dem ersten Teilziel: dict(E, sl) im gespiegelten Raum
        self.m15 = []               # gespiegelte Hochs abgeschlossener 15m-Kerzen
        self.m15_h = None           # laufendes Hoch der aktuellen 15m-Kerze

    def on_start(self):
        self.instrument = self.cache.instrument(self.config.instrument_id)
        self.subscribe_bars(self.config.bar_type)

    # Hilfsfunktionen -------------------------------------------------------------
    def _px(self, x: float) -> Price:
        return self.instrument.make_price(x)

    def _flat(self) -> bool:
        return self.portfolio.is_net_flat(self.config.instrument_id)

    def _mirror(self, o, h, l, c):
        if self.sg > 0:
            return o, h, l, c
        return -o, -l, -h, -c

    def _unmirror(self, x):
        return x if self.sg > 0 else -x

    def _cancel_entry(self):
        if self.levels is not None and self._flat():
            self.cancel_all_orders(self.config.instrument_id)
        self.levels = None

    # Ablauf je abgeschlossener Minute ------------------------------------------
    def handle_bar(self, bar: Bar):
        c = self.config
        o, h, l, cl = (float(bar.open), float(bar.high), float(bar.low), float(bar.close))
        self.last_close = cl
        mo, mh, ml, mc = self._mirror(o, h, l, cl)
        self.n += 1
        self._kerze15(bar, mh, mc)

        # Zeitstopp
        if self.entry_ts is not None and not self._flat() and bar.ts_init - self.entry_ts >= c.hold_min * MIN_NS:
            self.close_all_positions(c.instrument_id)
            self.cancel_all_orders(c.instrument_id)
        if not self._flat():
            if self.trade is not None:
                self._trail(ml)
            self.highs.append(mh)
            self.lows.append(ml)
            return

        s = self.setup
        if s is not None:
            if ml < s["L"]:
                if self.n - s["i_spike"] <= 5:          # Spike läuft noch weiter
                    s["L"], s["RH"], s["M"] = ml, ml, s["S"] - ml
                    s["i_low"] = self.n
                    self._cancel_entry()
                else:                                    # neues Tief nach dem Spike: Setup verfällt
                    self._cancel_entry()
                    self.setup = s = None
            else:
                s["RH"] = max(s["RH"], mh)
            if s is not None and self.n - s["i_low"] > c.window:
                self._cancel_entry()
                self.setup = s = None

        # Neuen Spike erkennen (nur ohne laufendes Setup)
        if s is None and len(self.lows) >= c.span - 1 and self.n - self.last_spike >= c.cooldown:
            prev_h, prev_l = list(self.highs)[-(c.span - 1):], list(self.lows)[-(c.span - 1):]
            S = max(max(prev_h), mh)
            if ml <= min(prev_l) and S - ml >= c.spike * abs(S):
                self.last_spike = self.n
                self.setup = {"S": S, "L": ml, "M": S - ml, "RH": ml, "i_spike": self.n, "i_low": self.n}
        self.highs.append(mh)
        self.lows.append(ml)

        s = self.setup
        if s is None or s["i_low"] == self.n:
            return
        W = s["RH"] - s["L"]
        if W <= 0 or W < c.rb_min * s["M"]:
            return
        mE = s["RH"] - c.fill_in * W
        mTP = s["RH"] - c.fill_out * W
        mSL = (s["RH"] + c.sl_w * W) if c.sl_ref == "rh" else (s["S"] + c.sl_w * s["M"])
        new = tuple(self._px(self._unmirror(x)) for x in (mE, mTP, mSL))
        if self.levels == new:
            return
        self._cancel_entry()
        qty = Quantity.from_str(c.qty)
        if mc <= mE:      # Kurs schon unter dem Einstiegslevel: sofort Market
            order = self.order_factory.market(c.instrument_id, self.entry_side, qty)
        else:             # Stop-Market (TP/SL folgen in handle_position_opened)
            order = self.order_factory.stop_market(c.instrument_id, self.entry_side, qty, trigger_price=new[0])
        self.submit_order(order)
        self.levels = new
        self.pend = dict(RH=s["RH"], W=W)
        self.plan = dict(entry=float(new[0]), sl=float(new[2]), tp=None if c.trail_w > 0 else float(new[1]),
                         spike_pct=s["M"] / abs(s["S"]) * 100)

    def handle_position_opened(self, event):
        """Sofort nach dem Einstieg: TP als Post-Only-Limit (Maker), SL als Stop-Market (Taker), beide reduce-only."""
        c = self.config
        self.entry_ts = event.ts_event
        self.levels = None
        self.setup = None
        exit_side = OrderSide.BUY if self.entry_side == OrderSide.SELL else OrderSide.SELL
        qty = Quantity.from_str(c.qty)
        tp, sl = self.plan["tp"], self.plan["sl"]
        px = float(event.avg_px_open)
        ziele = self._teilziele(qty)
        if ziele:
            tp = float(ziele[0][0])
        # Fill nach einem Kurssprung jenseits von Ziel oder Stop: TP (Post-Only) bzw. SL würden nicht greifen, sofort schließen
        beyond_tp = tp is not None and ((px <= tp) if self.sg > 0 else (px >= tp))
        beyond_sl = (px >= sl) if self.sg > 0 else (px <= sl)
        if beyond_tp or beyond_sl:
            self.close_all_positions(c.instrument_id)
            return
        if ziele:
            self.tp_ids, self.tp_mengen = [], {}
            for preis, menge in ziele:
                o = self.order_factory.limit(c.instrument_id, exit_side, menge, preis, post_only=True, reduce_only=True)
                self.tp_ids.append(o.client_order_id)
                self.tp_mengen[o.client_order_id] = menge
                self.submit_order(o)
        elif tp is not None:
            self.submit_order(self.order_factory.limit(c.instrument_id, exit_side, qty, self._px(tp),
                                                       post_only=True, reduce_only=True))
        self.sl_order = self.order_factory.stop_market(c.instrument_id, exit_side, qty, trigger_price=self._px(sl),
                                                       reduce_only=True)
        self.submit_order(self.sl_order)
        if c.trail_w > 0:
            mE = px if self.sg > 0 else -px
            self.trade = dict(E=mE, RH=self.pend["RH"], W=self.pend["W"], best=mE, active=False,
                              sl=sl if self.sg > 0 else -sl)

    def _trail(self, ml: float):
        """Nach jeder Minute: bestes Niveau fortschreiben, ab trail_start Stop auf Einstieg und nachziehen."""
        c, t = self.config, self.trade
        t["best"] = min(t["best"], ml)
        if not t["active"] and t["best"] <= t["RH"] - c.trail_start * t["W"]:
            t["active"] = True
        if not t["active"]:
            return
        ns = min(t["E"], t["best"] + c.trail_w * t["W"])
        tick = self.instrument.price_increment.as_double()
        if ns >= t["sl"] - tick:
            return
        exit_side = OrderSide.BUY if self.entry_side == OrderSide.SELL else OrderSide.SELL
        if self.sl_order is not None and self.sl_order.is_open:
            self.cancel_order(self.sl_order)
        self.sl_order = self.order_factory.stop_market(c.instrument_id, exit_side, Quantity.from_str(c.qty),
                                                       trigger_price=self._px(self._unmirror(ns)), reduce_only=True)
        self.submit_order(self.sl_order)
        t["sl"] = ns

    # Teilziele und Rest (H30) ------------------------------------------------------
    def _teilziele(self, qty: Quantity) -> list:
        """[(Preis, Menge)] aus tps, Füllgrad vom Rücklauf-Tief bzw. -Hoch aus. Rest der Rundung geht ans letzte Ziel."""
        c = self.config
        if not c.tps:
            return []
        teile = [tuple(float(x) for x in t.split(":")) for t in c.tps.split(",")]
        voll = abs(sum(a for _, a in teile) - 1.0) < 1e-9     # Summe 100 %: Rundungsrest ans letzte Ziel
        gesamt = qty.as_double()
        out, vergeben = [], 0.0
        for k, (fuell, anteil) in enumerate(teile):
            m = round(gesamt * anteil, self.instrument.size_precision)
            if voll and k == len(teile) - 1:
                m = round(gesamt - vergeben, self.instrument.size_precision)
            vergeben += m
            mpx = self.pend["RH"] - fuell * self.pend["W"]
            out.append((self._px(self._unmirror(mpx)), self.instrument.make_qty(m)))
        return out

    def on_order_filled(self, event):
        super().on_order_filled(event)
        self._guard(self._nach_fill, event)

    def on_order_updated(self, event):
        self._guard(self._menge_zuruecksetzen, event)

    def _menge_zuruecksetzen(self, event):
        """Nautilus 2.0.0rc7 setzt offene Reduce-Only-Orders nach jedem Teil-Fill auf die ganze Restposition hoch.
        Dann würde das zweite Ziel alles schließen. Teilziele daher auf ihre geplante Menge zurücksetzen."""
        oid = event.client_order_id
        soll = getattr(self, "tp_mengen", {}).get(oid)
        if soll is None or event.quantity <= soll:
            return
        o = self.cache.order(oid)
        if o is not None and o.is_open:
            self.modify_order(oid, quantity=soll)

    def _nach_fill(self, event):
        c = self.config
        if not self.tp_ids or event.client_order_id not in self.tp_ids or self._flat():
            return
        if event.client_order_id != self.tp_ids[0]:
            return
        if not (c.be_nach_tp1 or c.trail15):
            return
        pos = self.cache.positions_open(instrument_id=c.instrument_id)[0]
        e = float(pos.avg_px_open)
        self.rest = dict(E=e if self.sg > 0 else -e, sl=None)
        self._setze_stop(self.rest["E"], pos.quantity)

    def _setze_stop(self, msl: float, menge):
        """Stop der Restmenge auf msl (gespiegelter Raum) setzen, alten Stop stornieren."""
        exit_side = OrderSide.BUY if self.entry_side == OrderSide.SELL else OrderSide.SELL
        if self.sl_order is not None and self.sl_order.is_open:
            self.cancel_order(self.sl_order)
        self.sl_order = self.order_factory.stop_market(self.config.instrument_id, exit_side, menge,
                                                       trigger_price=self._px(self._unmirror(msl)), reduce_only=True)
        self.submit_order(self.sl_order)
        self.rest["sl"] = msl

    def _kerze15(self, bar: Bar, mh: float, mc: float):
        """15m-Kerzen aus 1m-Bars (gespiegelte Hochs). Nach jedem Schluss ggf. den Rest-Stop nachziehen."""
        self.m15_h = mh if self.m15_h is None else max(self.m15_h, mh)
        if bar.ts_init % (15 * MIN_NS) != 0:
            return
        self.m15.append(self.m15_h)
        self.m15_h = None
        if len(self.m15) > 50:
            self.m15 = self.m15[-50:]
        if not (self.config.trail15 and self.rest is not None and not self._flat()):
            return
        x = self.m15
        for j in range(len(x) - 3, 1, -1):                  # letztes bekanntes Swing-Hoch (gespiegelt) mit k = 2
            if x[j] > max(x[j - 2], x[j - 1], x[j + 1], x[j + 2]):
                ns = x[j]
                tick = self.instrument.price_increment.as_double()
                if ns < self.rest["sl"] - tick and ns > mc:
                    pos = self.cache.positions_open(instrument_id=self.config.instrument_id)
                    if pos:
                        self._setze_stop(ns, pos[0].quantity)
                break

    def handle_position_closed(self, event):
        self.entry_ts = None
        self.trade = None
        self.sl_order = None
        self.tp_ids = []
        self.rest = None
        self.cancel_all_orders(self.config.instrument_id)

    def on_order_rejected(self, event):
        self._guard(self._handle_rejected, event)

    def _handle_rejected(self, event):
        """Abgelehnter TP oder SL bei offener Position (Kurs schon jenseits des Niveaus): sofort per Market schließen."""
        if not self._flat():
            self.cancel_all_orders(self.config.instrument_id)
            self.close_all_positions(self.config.instrument_id)
