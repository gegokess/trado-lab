"""Lädt Funding und Open Interest von Kraken Futures und ergänzt das lokale Archiv (Vorarbeit V1).

Aufruf:
    python scripts/fetch_derivatives.py

Ablage in data/raw:
- PF_XBTUSD_funding.parquet: ts [ms, UTC, Beginn der Funding-Stunde], rate_rel (Anteil des
  Positionswerts je Stunde, positiv heißt Longs zahlen), rate_abs (Kraken-Feld fundingRate)
- PF_XBTUSD_oi.parquet: ts [ms, UTC, Stundenbeginn], oi_open, oi_high, oi_low, oi_close

Wichtig: Der Funding-Endpunkt liefert nur etwa das letzte Jahr (rollierend). Ältere Werte gibt
es bei Kraken nicht mehr. Das Skript hängt deshalb an das bestehende Archiv an und sollte
regelmäßig laufen, damit die Historie wächst. Open Interest reicht bis März 2023 zurück.
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lab.config import DATA_START, RAW_DIR, SYMBOL  # noqa: E402

URL_FUNDING = "https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol={sym}"
URL_OI = "https://futures.kraken.com/api/charts/v1/analytics/{sym}/open-interest?interval=3600&since={a}"


def _get(url: str) -> dict:
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return json.load(r)
        except Exception:
            time.sleep(2 + 2 * attempt)
    raise RuntimeError(f"Abruf fehlgeschlagen: {url}")


def _merge(path: Path, new: pd.DataFrame) -> pd.DataFrame:
    old = pd.read_parquet(path) if path.exists() else None
    df = pd.concat([x for x in (old, new) if x is not None and len(x)])
    df = df.drop_duplicates("ts", keep="last").sort_values("ts").reset_index(drop=True)
    df.to_parquet(path, index=False)
    return df


def funding(sym: str) -> pd.DataFrame:
    rates = _get(URL_FUNDING.format(sym=sym))["rates"]
    df = pd.DataFrame(rates)
    df = pd.DataFrame(dict(
        ts=(pd.to_datetime(df.timestamp, utc=True) - pd.Timestamp(0, tz="UTC")) // pd.Timedelta(milliseconds=1),
        rate_rel=df.relativeFundingRate.astype(float),
        rate_abs=df.fundingRate.astype(float),
    ))
    return _merge(RAW_DIR / f"{sym}_funding.parquet", df)


def open_interest(sym: str) -> pd.DataFrame:
    path = RAW_DIR / f"{sym}_oi.parquet"
    a = int(pd.Timestamp(DATA_START, tz="UTC").timestamp())
    if path.exists():
        a = int(pd.read_parquet(path).ts.max() // 1000) + 3600
    teile = []
    while a < time.time() - 3600:
        r = _get(URL_OI.format(sym=sym, a=a))["result"]
        if not r or not r["timestamp"]:
            break
        ts = [t * 1000 if t < 1e11 else t for t in r["timestamp"]]
        teile.append(pd.DataFrame(r["data"], columns=["oi_open", "oi_high", "oi_low", "oi_close"],
                                  dtype=float).assign(ts=ts))
        a = int(ts[-1] // 1000) + 3600      # nächster Abschnitt, Kraken liefert je Abruf nur einen Teil
    new = pd.concat(teile) if teile else pd.DataFrame(columns=["ts"])
    return _merge(path, new[["ts", "oi_open", "oi_high", "oi_low", "oi_close"]] if len(new) else new)


def _info(name: str, df: pd.DataFrame) -> None:
    first, last = (pd.to_datetime(df.ts.iloc[i], unit="ms") for i in (0, -1))
    gaps = (df.ts.diff().dropna() != 3_600_000).sum()
    print(f"{name}: {len(df):,} Stunden von {first} bis {last} UTC, Lücken: {gaps}")


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    _info(f"{SYMBOL} Funding", funding(SYMBOL))
    _info(f"{SYMBOL} Open Interest", open_interest(SYMBOL))


if __name__ == "__main__":
    main()
