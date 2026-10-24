"""Hypothese H7: Donchian-Ausbruch auf Tageskerzen (Zeitreihen-Momentum).

Regel (Long beschrieben, Short spiegelbildlich):
- Tageskerzen UTC aus den 1m-Bars
- Signal: Schluss von Tag d über dem höchsten Hoch der N Tage vor d
- Einstieg per Market zum Beginn von Tag d + 1 (Taker). Die Order geht mit dem Schluss der letzten
  Minute von Tag d raus und füllt zum Open der ersten Minute von Tag d + 1
- Anfangs-SL per Stop-Market am tiefsten Tief der M = N / 2 Tage d − M + 1 bis d, R = Einstieg − SL
- mit jedem Tagesschluss wird der Stop auf das Tief der letzten M abgeschlossenen Tage nachgezogen, nie zurück
- Ausstieg nur über den Stop, keine neue Position, solange eine offen ist
"""
from collections import deque

from nautilus_trader.config import StrategyConfig
from nautilus_trader.model import Bar, BarType, InstrumentId, OrderSide, Quantity

from strategies.base import LabStrategy

MIN_NS = 60_000_000_000
TAG_MIN = 1440


class DonchianConfig(StrategyConfig):
    def __init__(self, *, instrument_id: InstrumentId, bar_type: BarType,
                 side: str = "long", N: int = 10, qty: str = "0.01", **_kw) -> None:
        super().__init__()
        self.instrument_id, self.bar_type, self.side = instrument_id, bar_type, side
        self.N, self.qty = N, qty


class Donchian(LabStrategy):
    def __init__(self, config: DonchianConfig):
        super().__init__(config)
        c = config
        self.sg = 1.0 if c.side == "long" else -1.0       # gespiegelter Raum für Short
        self.entry_side = OrderSide.BUY if c.side == "long" else OrderSide.SELL
        self.exit_side = OrderSide.SELL if c.side == "long" else OrderSide.BUY
        self.M = c.N // 2
        self.highs = deque(maxlen=c.N + 1)                 # gespiegelte Tageshochs, inklusive des letzten Tages
        self.lows = deque(maxlen=c.N + 1)
        self.d_hi = self.d_lo = None
        self.stop = None                                   # aktueller Stop im gespiegelten Raum
        self.wartet = False                                # Einstiegsorder unterwegs

    def on_start(self):
        self.instrument = self.cache.instrument(self.config.instrument_id)
        self.subscribe_bars(self.config.bar_type)

    def _flat(self) -> bool:
        return self.portfolio.is_net_flat(self.config.instrument_id)

    def _real(self, x: float) -> float:
        return x * self.sg

    def _setze_stop(self, m_stop: float):
        c = self.config
        self.cancel_all_orders(c.instrument_id)
        self.stop = m_stop
        order = self.order_factory.stop_market(c.instrument_id, self.exit_side, Quantity.from_str(c.qty),
                                               trigger_price=self.instrument.make_price(self._real(m_stop)),
                                               reduce_only=True)
        self.submit_order(order)

    def handle_bar(self, bar: Bar):
        c = self.config
        h, l, cl = float(bar.high), float(bar.low), float(bar.close)
        mh, ml, mc = (h, l, cl) if self.sg > 0 else (-l, -h, -cl)
        self.d_hi = mh if self.d_hi is None else max(self.d_hi, mh)
        self.d_lo = ml if self.d_lo is None else min(self.d_lo, ml)
        if (bar.ts_event // MIN_NS + 1) % TAG_MIN:
            return                                         # Tag noch nicht abgeschlossen

        # Tagesschluss: Signal mit den N Tagen davor prüfen, dann den Tag in die Historie aufnehmen
        signal = len(self.highs) >= c.N and mc > max(list(self.highs)[-c.N:])
        self.highs.append(self.d_hi)
        self.lows.append(self.d_lo)
        self.d_hi = self.d_lo = None

        if not self._flat():
            neu = min(list(self.lows)[-self.M:])
            if neu > self.stop:
                self._setze_stop(neu)
            return
        if signal and not self.wartet and len(self.lows) >= self.M:
            sl = min(list(self.lows)[-self.M:])
            self.plan = dict(sl=self._real(sl), N=c.N)
            self.stop = sl
            self.wartet = True
            self.submit_order(self.order_factory.market(c.instrument_id, self.entry_side, Quantity.from_str(c.qty)))

    def handle_position_opened(self, event):
        self.wartet = False
        e = float(event.avg_px_open) * self.sg
        if e <= self.stop:                                 # Eröffnung schon unter dem Stop: sofort raus
            self.close_all_positions(self.config.instrument_id)
            return
        self._setze_stop(self.stop)

    def handle_position_closed(self, event):
        self.cancel_all_orders(self.config.instrument_id)
        self.stop = None
