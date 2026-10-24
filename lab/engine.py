"""Backtest-Engine mit simuliertem Kraken-Futures-Venue."""
from decimal import Decimal

from nautilus_trader.backtest import BacktestEngine
from nautilus_trader.common import LogLevel
from nautilus_trader.config import BacktestEngineConfig, LoggerConfig
from nautilus_trader.execution import MakerTakerFeeModel
from nautilus_trader.model import AccountType, Currency, Money, OmsType, TraderId, Venue

from lab.config import MAKER_FEE, TAKER_FEE, VENUE
from lab.instruments import pf_xbtusd

USD = Currency.from_str("USD")
KRAKEN = Venue(VENUE)


def run(strategy, bars, *, adaptive_ordering: bool = True, start_balance: float = 1_000_000,
        log_level: LogLevel = LogLevel.ERROR) -> BacktestEngine:
    """Spielt die Bars gegen das Venue ab und gibt die Engine (für Reports) zurück.

    adaptive_ordering: innerhalb einer Kerze wird zuerst das Extrem angelaufen, das näher am Open liegt.
    Bei False immer Open, High, Low, Close (für Shorts konservativ, für Longs optimistisch).
    Startkapital ist bewusst groß, damit Margin nie bindet. Ergebnisse werden in R ausgewertet.
    """
    engine = BacktestEngine(config=BacktestEngineConfig(
        trader_id=TraderId("TRADO-LAB-001"),
        logging=LoggerConfig(stdout_level=log_level),
    ))
    engine.add_venue(
        venue=KRAKEN,
        oms_type=OmsType.NETTING,
        account_type=AccountType.MARGIN,
        starting_balances=[Money(start_balance, USD)],
        base_currency=USD,
        default_leverage=Decimal(10),
        fee_model=MakerTakerFeeModel(maker_rate=Decimal(str(MAKER_FEE)), taker_rate=Decimal(str(TAKER_FEE))),
        bar_execution=True,
        bar_adaptive_high_low_ordering=adaptive_ordering,
    )
    engine.add_instrument(pf_xbtusd())
    engine.add_data(bars)
    engine.add_strategy(strategy)
    engine.run()
    if getattr(strategy, "error", None) is not None:
        raise RuntimeError("Strategie ist im Lauf abgestürzt") from strategy.error
    return engine
