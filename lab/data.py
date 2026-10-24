"""Zugriff auf das lokale Kursarchiv, als DataFrame, numpy-Arrays (Scans) oder Nautilus-Bars."""
import numpy as np
import pandas as pd
from nautilus_trader.model import Bar, Price, Quantity

from lab.config import CATALOG_DIR, OOS_START, RAW_DIR, SYMBOL
from lab.instruments import BAR_TYPE_1M, pf_xbtusd

MIN_NS = 60_000_000_000


def load_1m(start: str | None = None, end: str | None = None, allow_oos: bool = False) -> pd.DataFrame:
    """1m-Kerzen [start, end) in UTC. Ohne allow_oos=True endet der Zeitraum spätestens bei OOS_START."""
    path = RAW_DIR / f"{SYMBOL}_1m.parquet"
    if not path.exists():
        raise FileNotFoundError("Kein Archiv gefunden. Erst `python scripts/fetch_kraken.py` ausführen.")
    df = pd.read_parquet(path)
    lo = pd.Timestamp(start, tz="UTC").value // 1_000_000 if start else None
    hi = pd.Timestamp(end, tz="UTC").value // 1_000_000 if end else None
    oos = pd.Timestamp(OOS_START, tz="UTC").value // 1_000_000
    if not allow_oos:
        if hi is not None and hi > oos:
            raise ValueError(f"Zeitraum reicht in die Out-of-Sample-Periode (ab {OOS_START}). allow_oos=True nur für den finalen Test.")
        hi = oos if hi is None else hi
    if lo is not None:
        df = df[df.ts_open >= lo]
    if hi is not None:
        df = df[df.ts_open < hi]
    return df.reset_index(drop=True)


def arrays(df: pd.DataFrame):
    """(ts_open_ms, open, high, low, close) als numpy-Arrays für numba-Scans."""
    return (df.ts_open.values.astype(np.int64), df.open.values, df.high.values, df.low.values, df.close.values)


def to_bars(df: pd.DataFrame) -> list[Bar]:
    """Nautilus-Bars. ts_event = Kerzenbeginn, ts_init = Kerzenende, damit keine Kerze vor ihrem Abschluss sichtbar ist."""
    ts = df.ts_open.values.astype(np.int64) * 1_000_000
    o, h, l, c, v = (df[x].values for x in ("open", "high", "low", "close", "volume"))
    return [
        Bar(BAR_TYPE_1M, Price(o[i], 0), Price(h[i], 0), Price(l[i], 0), Price(c[i], 0),
            Quantity(round(v[i], 4), 4), int(ts[i]), int(ts[i] + MIN_NS))
        for i in range(len(df))
    ]


def write_catalog(df: pd.DataFrame) -> None:
    """Schreibt Instrument und Bars in den Nautilus-Parquet-Katalog (für BacktestNode / spätere Nutzung)."""
    from nautilus_trader.persistence import ParquetDataCatalog

    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    cat = ParquetDataCatalog(str(CATALOG_DIR))
    cat.write_instruments([pf_xbtusd()])
    cat.write_bars(to_bars(df))
    print(f"Katalog geschrieben: {CATALOG_DIR}")
