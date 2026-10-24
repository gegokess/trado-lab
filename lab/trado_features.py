"""Struktur-Features exakt wie in Trado (Vorarbeit V2): Swings, Fib-Retracement, Inducement, 4h-EMA-Trend.

Die Funktionen kommen unverändert aus dem Trado-Repo (bot/features/structure.py und indicators.py) und
werden direkt aus den Dateien geladen. Ein im Labor bestätigtes Setup ist damit in Trado dieselbe Regel.
Pfad zum Trado-Repo: Umgebungsvariable TRADO_DIR, sonst der Nachbarordner ../trado.

Nachbildung von trado/bot/features/snapshot.py:compute_features, zeitpunktgenau je volle Stunde:
- primär 1h, höher 4h, je die letzten WINDOW abgeschlossenen Kerzen (Trado: data.history_candles = 600)
- Features erst ab MIN_CANDLES Kerzen je Zeitebene (Trado: data.min_candles = 250)
- Swings k = 5, Inducement k = 2, Fib-Level 0,5/0,618/0,786/0,882, Impuls mindestens 2 ATR (Trado-Standard)
- ema_trend der 4h-Kerzen wie in snapshot._tf_block

Zeile mit ts = t (ms, UTC) enthält, was Trado zum Zeitpunkt t aus den bis dahin geschlossenen Kerzen sieht.
Ergebnisse werden in data/features zwischengespeichert, der Schlüssel enthält einen Hash der Trado-Dateien.
"""
from __future__ import annotations

import hashlib
import importlib.util
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd

from lab.config import DATA_DIR, ROOT

TRADO_DIR = Path(os.environ.get("TRADO_DIR", ROOT.parent / "trado"))
FEATURE_DIR = DATA_DIR / "features"

WINDOW = 600
MIN_CANDLES = 250
SWING_K = 5
MINOR_K = 2
FIB_RATIOS = [0.5, 0.618, 0.786, 0.882]
FIB_MIN_RANGE_ATR = 2.0
H1, H4 = 3_600_000, 14_400_000


def _load(name: str):
    path = TRADO_DIR / "bot" / "features" / f"{name}.py"
    if not path.exists():
        raise FileNotFoundError(f"Trado nicht gefunden unter {TRADO_DIR}. TRADO_DIR setzen oder Repo daneben klonen.")
    spec = importlib.util.spec_from_file_location(f"trado_{name}", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod                     # nötig für die Dataclass in structure.py
    spec.loader.exec_module(mod)
    return mod


structure = _load("structure")
indicators = _load("indicators")


def trado_hash() -> str:
    h = hashlib.sha256()
    for name in ("structure", "indicators"):
        h.update((TRADO_DIR / "bot" / "features" / f"{name}.py").read_bytes())
    h.update(f"{WINDOW},{MIN_CANDLES},{SWING_K},{MINOR_K},{FIB_RATIOS},{FIB_MIN_RANGE_ATR}".encode())
    return h.hexdigest()[:10]


def resample(df1m: pd.DataFrame, ms: int) -> pd.DataFrame:
    """Kerzen im festen UTC-Raster aus 1m-Kerzen, nur vollständige. Spalten wie in Trado: ts, open, high, low, close, volume."""
    g = df1m.assign(ts=df1m.ts_open // ms * ms).groupby("ts")
    out = g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                close=("close", "last"), volume=("volume", "sum"), n=("open", "size")).reset_index()
    return out[out.n == ms // 60_000].drop(columns="n").reset_index(drop=True)


def ema_trend(df: pd.DataFrame) -> str:
    """Wie trado/bot/features/snapshot.py:_tf_block, nur der Teil für ema_trend."""
    e20 = indicators.ema(df["close"], 20)[-1]
    e50 = indicators.ema(df["close"], 50)[-1]
    close = float(df["close"].iloc[-1])
    if np.isnan(e50):
        return "unklar"
    if e20 > e50 and close > e50:
        return "aufwärts"
    if e20 < e50 and close < e50:
        return "abwärts"
    return "gemischt"


def primary_features(p: pd.DataFrame) -> dict:
    """Fib und Inducement eines 1h-Fensters, Aufrufe wie in compute_features."""
    atr_p = float(indicators.atr(p["high"], p["low"], p["close"], 14)[-1])
    out = dict(atr=atr_p)
    if not (atr_p > 0):
        return out
    highs, lows = structure.find_swings(p["high"], p["low"], p["ts"], SWING_K)
    fib = structure.fib_retracement(p, highs, lows, atr_p, FIB_RATIOS, FIB_MIN_RANGE_ATR)
    idm = structure.inducement(p, fib, MINOR_K)
    if fib:
        out.update(fib_dir=fib["direction"], origin=fib["origin"], extreme=fib["extreme"],
                   origin_ts=fib["origin_ts"], extreme_ts=fib["extreme_ts"], valid=fib["valid"],
                   extended=fib["extended"], range_atr=fib["range_atr"],
                   **{f"l{q}": v for q, v in fib["levels"].items()})
    out.update(idm_price=idm.get("price"), idm_status=idm["status"])
    return out


def _chunk(args) -> list[dict]:
    h1, h4, times = args
    rows = []
    ts1, ts4 = h1.ts.to_numpy(), h4.ts.to_numpy()
    for t in times:
        i = np.searchsorted(ts1, t - H1, side="right")          # 1h-Kerzen mit Beginn ≤ t − 1h sind geschlossen
        j = np.searchsorted(ts4, t - H4, side="right")
        if i < MIN_CANDLES or j < MIN_CANDLES:
            continue
        p = h1.iloc[max(0, i - WINDOW):i].reset_index(drop=True)
        h = h4.iloc[max(0, j - WINDOW):j].reset_index(drop=True)
        rows.append(dict(ts=int(t), trend_4h=ema_trend(h), **primary_features(p)))
    return rows


def compute(df1m: pd.DataFrame, workers: int = 2) -> pd.DataFrame:
    h1, h4 = resample(df1m, H1), resample(df1m, H4)
    times = h1.ts.to_numpy() + H1                                 # jede volle Stunde nach einem Kerzenschluss
    teile = np.array_split(times, workers * 8)
    with ProcessPoolExecutor(workers) as ex:
        rows = [r for teil in ex.map(_chunk, [(h1, h4, t) for t in teile]) for r in teil]
    return pd.DataFrame(rows)


def load(symbol: str, df1m: pd.DataFrame, workers: int = 2) -> pd.DataFrame:
    """Features für das ganze 1m-Archiv eines Symbols, aus dem Zwischenspeicher oder neu berechnet."""
    FEATURE_DIR.mkdir(parents=True, exist_ok=True)
    last = int(df1m.ts_open.iloc[-1])
    path = FEATURE_DIR / f"{symbol}_trado_{trado_hash()}_{last}.parquet"
    if path.exists():
        return pd.read_parquet(path)
    f = compute(df1m, workers)
    f.to_parquet(path, index=False)
    return f
