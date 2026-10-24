"""Lädt 1-Minuten-Kerzen von Kraken Futures und aktualisiert das lokale Archiv.

Aufruf:
    python scripts/fetch_kraken.py              # Archiv anlegen oder bis jetzt ergänzen
    python scripts/fetch_kraken.py --catalog    # zusätzlich den Nautilus-Katalog neu schreiben

Ablage: data/raw/PF_XBTUSD_1m.parquet (Spalten ts_open [ms, UTC], open, high, low, close, volume)
"""
import argparse
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab.config import DATA_START, RAW_DIR, SYMBOL  # noqa: E402

URL = "https://futures.kraken.com/api/charts/v1/trade/{sym}/1m?from={a}&to={b}"
PAGE = 2000 * 60  # Kraken liefert max. 2000 Kerzen je Abruf


def _get(sym: str, a: int) -> list[dict]:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(URL.format(sym=sym, a=a, b=a + PAGE - 1), timeout=30) as r:
                return json.load(r)["candles"]
        except Exception:
            time.sleep(2 + 2 * attempt)
    raise RuntimeError(f"Abruf fehlgeschlagen ab {a}")


def fetch(sym: str, start_s: int, end_s: int) -> pd.DataFrame:
    starts = list(range(start_s, end_s, PAGE))
    with ThreadPoolExecutor(6) as ex:
        pages = list(ex.map(lambda a: _get(sym, a), starts))
    rows = [c for p in pages for c in p]
    if not rows:
        return pd.DataFrame(columns=["ts_open", "open", "high", "low", "close", "volume"])
    df = pd.DataFrame(rows).rename(columns={"time": "ts_open"})
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    return df[["ts_open", "open", "high", "low", "close", "volume"]]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default=SYMBOL)
    ap.add_argument("--catalog", action="store_true", help="Nautilus-Katalog danach neu schreiben")
    a = ap.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = RAW_DIR / f"{a.symbol}_1m.parquet"
    old = pd.read_parquet(path) if path.exists() else None
    start = int(pd.Timestamp(DATA_START, tz="UTC").timestamp())
    if old is not None and len(old):
        start = int(old.ts_open.max() // 1000) + 60
    end = int(time.time()) // 60 * 60 - 60  # nur abgeschlossene Minuten

    new = fetch(a.symbol, start, end) if start < end else None
    df = pd.concat([x for x in (old, new) if x is not None and len(x)])
    df = df.drop_duplicates("ts_open").sort_values("ts_open").reset_index(drop=True)
    df = df[df.ts_open < end * 1000]
    df.to_parquet(path, index=False)

    gaps = (df.ts_open.diff().dropna() != 60_000).sum()
    first, last = (pd.to_datetime(df.ts_open.iloc[i], unit="ms") for i in (0, -1))
    print(f"{a.symbol}: {len(df):,} Kerzen von {first} bis {last} UTC, Lücken: {gaps}")

    if a.catalog:
        from lab.data import write_catalog
        write_catalog(df)


if __name__ == "__main__":
    main()
