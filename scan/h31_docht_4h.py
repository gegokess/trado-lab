"""H31: Docht-Füllung auf 4h, 1:1-Bracket zum halben Docht gegen Kontrollen ohne Docht (LABORBUCH.md).

Aufruf:  python -m scan.h31_docht_4h            In-Sample bis OOS_START
         python -m scan.h31_docht_4h --oos      einmalig ab OOS_START (nur für Treffer-Zellen gedacht)

Zellen: ETH und BTC × oberer und unterer Docht × alle Ereignisse und nur mit Sweep.
"""
import argparse
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE as FEE_MAKER, TAKER_FEE as FEE_TAKER, OOS_START, RAW_DIR, RUNS_DIR

H4 = 14_400_000
HALTEN_KERZEN = 3
SWEEP_N = 20
N_KONTROLLE = 10


@njit(cache=True)
def bracket(high, low, close, i, richtung, einstieg, d, n_min):
    """1:1-Bracket ab Minute i. Ziel und Stop in derselben Minute zählen als Stop. Rückgabe (R, Ziel getroffen, Ende)."""
    ziel, stop = einstieg + richtung * d, einstieg - richtung * d
    ende = min(len(high) - 1, i + n_min - 1)
    for j in range(i, ende + 1):
        s = low[j] <= stop if richtung == 1 else high[j] >= stop
        z = high[j] >= ziel if richtung == 1 else low[j] <= ziel
        if s:
            return -1.0, 0, j
        if z:
            return 1.0, 1, j
    return richtung * (close[ende] - einstieg) / d, 0, ende


def auswerten(symbol: str, oos: bool, rng) -> tuple[list, list]:
    m1 = pd.read_parquet(RAW_DIR / f"{symbol}_1m.parquet")
    grenze = pd.Timestamp(OOS_START, tz="UTC").value // 1_000_000
    ts = m1.ts_open.to_numpy()
    high, low, close = (m1[c].to_numpy() for c in ("high", "low", "close"))
    h4 = m1.assign(ts=m1.ts_open // H4 * H4).groupby("ts").agg(
        open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last")).reset_index()
    o, h, l, c = h4.open, h4.high, h4.low, h4.close
    tr = np.maximum(h - l, np.maximum((h - c.shift()).abs(), (l - c.shift()).abs()))
    h4["atr"] = tr.rolling(14).mean().shift(1)
    koerper = (c - o).abs()
    oben_d, unten_d = h - np.maximum(o, c), np.minimum(o, c) - l
    vor_h, vor_l = h.shift(1).rolling(SWEEP_N).max(), l.shift(1).rolling(SWEEP_N).min()
    ev = {
        1: (oben_d >= h4.atr) & (oben_d > koerper),            # oberer Docht: Long auf die Füllung
        -1: (unten_d >= h4.atr) & (unten_d > koerper),          # unterer Docht: Short auf die Füllung
    }
    sweep = {1: (h > vor_h) & (c < vor_h), -1: (l < vor_l) & (c > vor_l)}
    dist = {1: np.maximum(o, c) + 0.5 * oben_d - c, -1: c - (np.minimum(o, c) - 0.5 * unten_d)}
    jahr = pd.to_datetime(h4.ts, unit="ms").dt.year
    start_ms = h4.ts + H4                                      # Einstieg zum Schluss = Beginn der nächsten Kerze
    im_teil = (start_ms >= grenze) if oos else (start_ms < grenze)
    gueltig = im_teil & h4.atr.notna() & (start_ms + HALTEN_KERZEN * H4 <= ts[-1])
    n_min = HALTEN_KERZEN * 240

    zeilen, trades = [], []
    for richtung in (1, -1):
        for nur_sweep in (False, True):
            maske = ev[richtung] & gueltig & (sweep[richtung] if nur_sweep else True)
            maske &= dist[richtung] > 0
            idx = np.flatnonzero(maske.to_numpy())
            kandidaten = {y: np.flatnonzero((~ev[richtung] & gueltig & (jahr == y)).to_numpy()) for y in jahr.unique()}
            rs, kr, frei_ab = [], [], -1
            for k in idx:
                i = int(np.searchsorted(ts, start_ms.iloc[k]))
                if i <= frei_ab or i >= len(ts):
                    continue
                e, d = float(c.iloc[k]), float(dist[richtung].iloc[k])
                r, ziel, ende = bracket(high, low, close, i, richtung, e, d, n_min)
                frei_ab = ende
                aus = e + richtung * d if ziel else close[ende] if r not in (-1.0,) else e - richtung * d
                gebuehr = (FEE_TAKER * e + (FEE_MAKER if ziel else FEE_TAKER) * aus) / d
                rs.append((r, r - gebuehr))
                trades.append(dict(symbol=symbol, seite="oben" if richtung == 1 else "unten", sweep=bool(sweep[richtung].iloc[k]),
                                   nur_sweep=nur_sweep, ts=int(start_ms.iloc[k]), einstieg=e, d=d, d_atr=d / h4.atr.iloc[k],
                                   r_brutto=r, r_netto=r - gebuehr))
                # Kontrollen: gleicher Abstand in ATR, gleiche Richtung, Schluss ohne Ereignis aus demselben Jahr
                pool = kandidaten[jahr.iloc[k]]
                for kk in rng.choice(pool, N_KONTROLLE):
                    ik = int(np.searchsorted(ts, start_ms.iloc[kk]))
                    if ik >= len(ts):
                        continue
                    dk = d / h4.atr.iloc[k] * h4.atr.iloc[kk]
                    kr.append(bracket(high, low, close, ik, richtung, float(c.iloc[kk]), float(dk), n_min)[0])
            a = np.array(rs) if rs else np.zeros((0, 2))
            kr = np.array(kr)
            t = np.nan
            if len(a) > 1 and len(kr) > 1:
                t = (a[:, 0].mean() - kr.mean()) / np.sqrt(a[:, 0].var(ddof=1) / len(a) + kr.var(ddof=1) / len(kr))
            zeilen.append(dict(symbol=symbol, seite="oben" if richtung == 1 else "unten",
                               auswahl="nur Sweep" if nur_sweep else "alle", n=len(a),
                               treffer=(a[:, 0] == 1).mean() if len(a) else np.nan,
                               r_brutto=a[:, 0].mean() if len(a) else np.nan, r_netto=a[:, 1].mean() if len(a) else np.nan,
                               n_kontrolle=len(kr), r_kontrolle=kr.mean() if len(kr) else np.nan,
                               treffer_kontrolle=(kr == 1).mean() if len(kr) else np.nan, t_diff=t))
    return zeilen, trades


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oos", action="store_true")
    a = ap.parse_args()
    rng = np.random.default_rng(31)
    zeilen, trades = [], []
    for sym in ("PF_ETHUSD", "PF_XBTUSD"):
        z, t = auswerten(sym, a.oos, rng)
        zeilen += z
        trades += t
    e = pd.DataFrame(zeilen)
    e["treffer_zelle"] = (e.t_diff >= 2.5) & (e.r_netto > 0)
    pd.set_option("display.width", 220)
    print(e.round(3).to_string(index=False))
    out = RUNS_DIR / (datetime.now(timezone.utc).strftime("%Y%m%d-%H%M") + "_h31_docht_4h" + ("_OOS" if a.oos else ""))
    out.mkdir(exist_ok=True)
    e.to_csv(out / "ergebnis.csv", index=False)
    pd.DataFrame(trades).to_csv(out / "trades.csv", index=False)
    print(f"Gespeichert: {out}")


if __name__ == "__main__":
    main()
