"""Prüfung für V2: liefert lab/trado_features.py dasselbe wie Trado selbst?

Aufruf:  python -m scan.pruefe_trado_features
Voraussetzung: Trado-Repo unter TRADO_DIR (Standard ../trado) und `uv pip install -e ".[pruefung]"`

Prüft zwei Glieder der Kette:
1. Kerzen: 1h und 4h, im Labor aus 1m-Kerzen gebildet, gegen Trados echte Kraken-Kerzen in trado/data/sample
2. Features: an zufälligen Zeitpunkten Trados compute_features (mit Trado-Config-Standardwerten) gegen
   lab.trado_features, beide auf denselben Kerzen

Die Beispieldaten liegen im Out-of-Sample-Zeitraum. Das ist hier zulässig, weil nur Code verglichen und
nichts gehandelt oder ausgewertet wird.
"""
import sys

import numpy as np
import pandas as pd

from lab import trado_features as tf
from lab.data import load_1m

sys.path.insert(0, str(tf.TRADO_DIR))
from bot.config import Config  # noqa: E402
from bot.features.snapshot import compute_features  # noqa: E402

FELDER = ["fib_dir", "origin", "extreme", "valid", "extended", "range_atr",
          "l0.5", "l0.618", "l0.786", "l0.882", "idm_price", "idm_status", "trend_4h"]


def pruefe_kerzen(df1m: pd.DataFrame) -> bool:
    ok = True
    for name, ms in (("1h", tf.H1), ("4h", tf.H4)):
        # Die letzte Kerze im Sample wurde noch während ihrer Laufzeit gespeichert und ist unvollständig
        ref = pd.read_csv(tf.TRADO_DIR / "data" / "sample" / f"PF_XBTUSD_{name}.csv").iloc[:-1]
        lab = tf.resample(df1m, ms)
        m = ref.merge(lab, on="ts", suffixes=("_trado", "_lab"))
        abw = {c: int((m[f"{c}_trado"] != m[f"{c}_lab"]).sum()) for c in ("open", "high", "low", "close")}
        vol = float((m.volume_trado - m.volume_lab).abs().max())
        print(f"Kerzen {name}: {len(m)} von {len(ref)} gemeinsam, Abweichungen OHLC {abw}, max. Volumenabweichung {vol:.4f}")
        ok &= len(m) == len(ref) and not any(abw.values()) and vol < 0.01
    return ok


def trado_werte(cfg: Config, h1: pd.DataFrame, h4: pd.DataFrame, t: int) -> dict:
    p = h1[h1.ts <= t - tf.H1].tail(cfg.data.history_candles).reset_index(drop=True)
    h = h4[h4.ts <= t - tf.H4].tail(cfg.data.history_candles).reset_index(drop=True)
    f = compute_features(cfg, p, h)
    fib, idm = f["fib"] or {}, f["inducement"]
    out = dict(fib_dir=fib.get("direction"), origin=fib.get("origin"), extreme=fib.get("extreme"),
               valid=fib.get("valid"), extended=fib.get("extended"), range_atr=fib.get("range_atr"),
               idm_price=idm.get("price"), idm_status=idm["status"], trend_4h=f["higher"]["ema_trend"])
    out.update({f"l{q}": v for q, v in fib.get("levels", {}).items()})
    return out


def pruefe_features(df1m: pd.DataFrame, n: int = 300, seed: int = 1) -> bool:
    cfg = Config()
    assert (cfg.data.history_candles, cfg.data.min_candles) == (tf.WINDOW, tf.MIN_CANDLES)
    assert (cfg.features.swing_lookback, cfg.features.minor_swing_lookback) == (tf.SWING_K, tf.MINOR_K)
    assert (cfg.features.fib_ratios, cfg.features.fib_min_range_atr) == (tf.FIB_RATIOS, tf.FIB_MIN_RANGE_ATR)
    h1, h4 = tf.resample(df1m, tf.H1), tf.resample(df1m, tf.H4)
    zeiten = np.random.default_rng(seed).choice(h1.ts.to_numpy()[tf.WINDOW * 4:] + tf.H1, n, replace=False)
    lab = pd.DataFrame(tf._chunk((h1, h4, np.sort(zeiten)))).set_index("ts")
    fehler = 0
    for t in np.sort(zeiten):
        a, b = trado_werte(cfg, h1, h4, int(t)), lab.loc[int(t)]
        diff = [k for k in FELDER if not (a.get(k) == b.get(k) or (pd.isna(a.get(k)) and pd.isna(b.get(k))))]
        fehler += bool(diff)
        if diff:
            print(pd.to_datetime(t, unit="ms"), "Abweichung in", {k: (a.get(k), b.get(k)) for k in diff})
    print(f"Features: {n - fehler} von {n} Zeitpunkten identisch")
    return fehler == 0


if __name__ == "__main__":
    df = load_1m("2023-01-01", None, allow_oos=True)
    ok = pruefe_kerzen(df) & pruefe_features(df)
    print("Ergebnis:", "bestanden" if ok else "NICHT bestanden")
    sys.exit(0 if ok else 1)
