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

# Kontraktdaten je Symbol: Basiswährung, Preisstellen, Tick, Mengenschritt
# Tick laut https://futures.kraken.com/derivatives/api/v3/instruments (Stand 11.11.2026)
SPECS = {
    "PF_XBTUSD": dict(base="BTC", price_precision=0, tick="1", size_precision=4, size_inc="0.0001"),
    "PF_ETHUSD": dict(base="ETH", price_precision=1, tick="0.1", size_precision=3, size_inc="0.001"),
    "PF_SOLUSD": dict(base="SOL", price_precision=2, tick="0.01", size_precision=2, size_inc="0.01"),
    "PF_XRPUSD": dict(base="XRP", price_precision=4, tick="0.0001", size_precision=0, size_inc="1"),
}

INSTRUMENT_ID = InstrumentId.from_str(f"{SYMBOL}.{VENUE}")
BAR_TYPE_1M = BarType.from_str(f"{SYMBOL}.{VENUE}-1-MINUTE-LAST-EXTERNAL")


def instrument() -> CryptoPerpetual:
    """Kontrakt für das eingestellte SYMBOL (lab/config.py)."""
    return perpetual(SYMBOL)


def pf_xbtusd() -> CryptoPerpetual:
    return perpetual("PF_XBTUSD")


def perpetual(symbol: str) -> CryptoPerpetual:
    """Kraken-Perpetual laut SPECS, linear, 1 Kontrakt = 1 Einheit der Basiswährung.

    PF_XBTUSD: Tick 1 USD, Mengen in 0,0001. PF_ETHUSD: Tick 0,1 USD, Mengen in 0,001.

    Margin wie Kraken-Retail-Stufe Europa (Initial 10 %, Maintenance 5 %), Werte aus
    https://futures.kraken.com/derivatives/api/v3/instruments (Stand 24.10.2026).
    Gebühren hängen am Venue (lab/engine.py), nicht am Instrument.
    """
    sp = SPECS[symbol]
    return CryptoPerpetual(
        instrument_id=InstrumentId.from_str(f"{symbol}.{VENUE}"),
        raw_symbol=Symbol(symbol),
        base_currency=Currency.from_str(sp["base"]),
        quote_currency=Currency.from_str("USD"),
        settlement_currency=Currency.from_str("USD"),
        is_inverse=False,
        price_precision=sp["price_precision"],
        size_precision=sp["size_precision"],
        price_increment=Price.from_str(sp["tick"]),
        size_increment=Quantity.from_str(sp["size_inc"]),
        ts_event=0,
        ts_init=0,
        margin_init=Decimal("0.10"),
        margin_maint=Decimal("0.05"),
    )
