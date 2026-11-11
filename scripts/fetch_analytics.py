"""Lädt Marktdaten aus der Kraken-Futures-Analytics-API als 1-Minuten-Reihen und ergänzt das lokale Archiv.

Aufruf:
    python scripts/fetch_analytics.py                          # alle Arten bis jetzt laden oder ergänzen
    python scripts/fetch_analytics.py --arten liquidation-volume open-interest

Arten (Endpunkt charts/v1/analytics/{symbol}/{art}):
    liquidation-volume  liquidiertes Volumen je Minute, ohne Trennung nach Long und Short
    open-interest       offene Kontrakte als Open, High, Low, Close je Minute
    long-short-info     Anzahl und Anteil der Konten mit Long- bzw. Short-Position
    future-basis        Abstand des Perps zum Index (Basis)
Dazu der Spot-Index als 1m-Kerzen (charts/v1/spot), Art "spot".

Ablage: data/raw/{symbol}_{art}_1m.parquet, Spalte ts_open [ms, UTC], übrige Spalten je nach Art
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

ANALYTICS = "https://futures.kraken.com/api/charts/v1/analytics/{sym}/{art}?interval=60&since={a}&to={b}"
SPOT = "https://futures.kraken.com/api/charts/v1/spot/{sym}/1m?from={a}&to={b}"
ARTEN = ["liquidation-volume", "open-interest", "long-short-info", "future-basis", "spot"]
PAGE = 2000 * 60  # max. 2000 Werte je Abruf


def _json(url: str) -> dict:
    for versuch in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 + 2 * versuch)
    raise RuntimeError(f"Abruf fehlgeschlagen: {url}")


def _seite(sym: str, art: str, a: int) -> pd.DataFrame:
    b = a + PAGE - 60
    if art == "spot":
        c = _json(SPOT.format(sym=sym, a=a, b=b))["candles"]
        if not c:
            return pd.DataFrame()
        df = pd.DataFrame(c).rename(columns={"time": "ts_open"}).drop(columns="volume", errors="ignore")
        return df.astype(float).astype({"ts_open": "int64"})
    r = _json(ANALYTICS.format(sym=sym, art=art, a=a, b=b)).get("result", {})
    ts = r.get("timestamp", [])
    if not ts:
        return pd.DataFrame()
    d = r["data"]
    if isinstance(d, dict):                       # mehrere Reihen, z. B. longCount, shortCount
        df = pd.DataFrame(d)
    elif d and isinstance(d[0], list):            # OHLC als Liste
        df = pd.DataFrame(d, columns=["open", "high", "low", "close"])
    else:                                         # ein Wert je Minute
        df = pd.DataFrame({"wert": d})
    df = df.apply(pd.to_numeric, errors="coerce")
    df.insert(0, "ts_open", pd.Series(ts, dtype="int64") * 1000)
    return df


def laden(sym: str, art: str) -> None:
    pfad = RAW_DIR / f"{sym}_{art}_1m.parquet"
    alt = pd.read_parquet(pfad) if pfad.exists() else None
    start = int(pd.Timestamp(DATA_START, tz="UTC").timestamp())
    if alt is not None and len(alt):
        start = int(alt.ts_open.max() // 1000) + 60
    ende = int(time.time()) // 60 * 60 - 60
    starts = list(range(start, ende, PAGE))
    with ThreadPoolExecutor(6) as ex:
        seiten = list(ex.map(lambda a: _seite(sym, art, a), starts))
    teile = [x for x in [alt, *seiten] if x is not None and len(x)]
    if not teile:
        print(f"{art}: keine Daten")
        return
    df = pd.concat(teile).drop_duplicates("ts_open").sort_values("ts_open").reset_index(drop=True)
    df = df[df.ts_open < ende * 1000]
    df.to_parquet(pfad, index=False)
    luecken = (df.ts_open.diff().dropna() != 60_000).sum()
    erst, letzt = (pd.to_datetime(df.ts_open.iloc[i], unit="ms") for i in (0, -1))
    print(f"{sym} {art}: {len(df):,} Minuten von {erst} bis {letzt} UTC, Lücken: {luecken}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default=SYMBOL)
    ap.add_argument("--arten", nargs="+", default=ARTEN, choices=ARTEN)
    a = ap.parse_args()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for art in a.arten:
        laden(a.symbol, art)


if __name__ == "__main__":
    main()
