"""Lädt die Tageskerzen BTC-USD von Yahoo Finance als zusätzliche, längere BTC-Historie (H7c).

Aufruf:
    python scripts/fetch_yahoo_btc.py

Ablage: data/raw/BTC-USD_yahoo_1d.parquet (Spalten ts_open [ms, UTC, Tagesbeginn], open, high, low, close, volume)
Yahoo ist eine inoffizielle Schnittstelle. Krypto-Tageskerzen beginnen dort um 00:00 UTC.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab.config import RAW_DIR  # noqa: E402

URL = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD?period1=1410000000&period2={b}&interval=1d"


def main() -> None:
    req = urllib.request.Request(URL.format(b=int(time.time())), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        res = json.load(r)["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    df = pd.DataFrame(dict(ts_open=[t * 1000 for t in res["timestamp"]], open=q["open"], high=q["high"],
                           low=q["low"], close=q["close"], volume=q["volume"])).dropna()
    df = df[df.ts_open % 86_400_000 == 0]                 # nur Kerzen auf UTC-Tagesgrenzen
    heute = int(time.time()) // 86_400 * 86_400_000
    df = df[df.ts_open < heute].drop_duplicates("ts_open").sort_values("ts_open").reset_index(drop=True)
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(RAW_DIR / "BTC-USD_yahoo_1d.parquet", index=False)
    gaps = (df.ts_open.diff().dropna() != 86_400_000).sum()
    first, last = (pd.to_datetime(df.ts_open.iloc[i], unit="ms") for i in (0, -1))
    print(f"BTC-USD Yahoo: {len(df):,} Tage von {first.date()} bis {last.date()}, Lücken: {gaps}")


if __name__ == "__main__":
    main()
