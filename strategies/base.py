"""Gemeinsame Basis: einheitliches Trade-Protokoll in R und harte Fehler statt stiller Log-Einträge."""
from nautilus_trader.trading import Strategy


class LabStrategy(Strategy):
    """Unterklassen implementieren handle_bar und optional handle_position_opened / handle_position_closed.

    Vor jedem Einstieg setzt die Strategie self.plan = dict(sl=..., tp=..., **Zusatzinfos).
    Beim Schließen der Position entsteht daraus eine Zeile in self.trades mit Brutto- und Netto-Ergebnis
    in R (R = Risiko vom tatsächlichen Einstieg bis zum geplanten SL) und in % vom Positionswert.
    Jede Exception in einem Handler wird gespeichert, lab.engine.run bricht dann mit Fehler ab.
    """

    def __init__(self, config):
        super().__init__(config)
        self.trades: list[dict] = []
        self.plan: dict | None = None
        self.error: BaseException | None = None
        self._fees = 0.0
        self._exit_reason = None

    # Schutz gegen still geschluckte Fehler ---------------------------------------
    def _guard(self, fn, *args):
        if self.error is not None:
            return
        try:
            fn(*args)
        except BaseException as exc:  # noqa: BLE001
            self.error = exc
            raise

    def on_bar(self, bar):
        self._guard(self.handle_bar, bar)

    def on_position_opened(self, event):
        self._guard(self.handle_position_opened, event)

    def on_position_closed(self, event):
        self._guard(self._log_trade, event)
        self._guard(self.handle_position_closed, event)

    def on_order_filled(self, event):
        self._guard(self._track_fill, event)

    # Von Unterklassen zu implementieren --------------------------------------------
    def handle_bar(self, bar):
        raise NotImplementedError

    def handle_position_opened(self, event):
        pass

    def handle_position_closed(self, event):
        pass

    # Protokoll ----------------------------------------------------------------------
    def _track_fill(self, event):
        self._fees += float(event.commission.as_double())
        # Der letzte Fill vor dem Schließen bestimmt den Ausstiegsgrund
        self._exit_reason = {"LIMIT": "tp", "STOP_MARKET": "sl", "MARKET": "zeit"}.get(
            str(event.order_type).split(".")[-1], str(event.order_type))

    def _log_trade(self, event):
        p = self.plan or {}
        qty = float(event.peak_qty)
        e, x = float(event.avg_px_open), float(event.avg_px_close)
        sign = 1 if str(event.entry).endswith("BUY") else -1
        gross = sign * (x - e) * qty
        risk = abs(e - p.get("sl", e)) * qty or float("nan")
        self.trades.append(dict(
            ts_open=event.ts_opened, ts_close=event.ts_closed, side="long" if sign > 0 else "short",
            entry=e, exit=x, qty=qty, risk_px=abs(e - p.get("sl", e)), exit_reason=self._exit_reason or "",
            r_gross=gross / risk, r_net=(gross - self._fees) / risk,
            pct_net=(gross - self._fees) / (e * qty) * 100, fees=self._fees,
            **{k: v for k, v in p.items() if k not in ("entry", "sl")},
        ))
        self.plan, self._fees, self._exit_reason = None, 0.0, None
