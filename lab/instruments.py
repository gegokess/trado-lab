"""Kontraktdefinitionen für Nautilus."""
from decimal import Decimal

from nautilus_trader.model import (
    BarType,
    CryptoPerpetual,
    Currency,
    InstrumentId,
    Price,
    Quantity,
    Symbol,
)

from lab.config import SYMBOL, VENUE

INSTRUMENT_ID = InstrumentId.from_str(f"{SYMBOL}.{VENUE}")
BAR_TYPE_1M = BarType.from_str(f"{SYMBOL}.{VENUE}-1-MINUTE-LAST-EXTERNAL")


def pf_xbtusd() -> CryptoPerpetual:
    """Kraken PF_XBTUSD: linear, 1 Kontrakt = 1 BTC, Tick 1 USD, Mengen in 0,0001.

    Margin wie Kraken-Retail-Stufe Europa (Initial 10 %, Maintenance 5 %), Werte aus
    https://futures.kraken.com/derivatives/api/v3/instruments (Stand 24.10.2026).
    Gebühren hängen am Venue (lab/engine.py), nicht am Instrument.
    """
    return CryptoPerpetual(
        instrument_id=INSTRUMENT_ID,
        raw_symbol=Symbol(SYMBOL),
        base_currency=Currency.from_str("BTC"),
        quote_currency=Currency.from_str("USD"),
        settlement_currency=Currency.from_str("USD"),
        is_inverse=False,
        price_precision=0,
        size_precision=4,
        price_increment=Price.from_str("1"),
        size_increment=Quantity.from_str("0.0001"),
        ts_event=0,
        ts_init=0,
        margin_init=Decimal("0.10"),
        margin_maint=Decimal("0.05"),
    )
