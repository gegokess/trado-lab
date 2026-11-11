"""Schneller numba-Scan für H1 (Wick-Füllung), gleiche Regel wie strategies/wick_fill.py.

Aufruf:  python -m scan.wick_fill_scan            (Standard: In-Sample bis OOS_START)
Annahmen gegenüber Nautilus: SL vor TP, wenn beide in derselben Minute liegen; kein Ausstieg in der Einstiegsminute.
"""
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import arrays, load_1m
from lab.report import summary


def hourly_atr(ts_ms, o, h, l, c, n=14):
    """ATR der abgeschlossenen Stunden, je Minute (für die laufende Stunde gilt der Wert aus den 14 Stunden davor)."""
    hid = ts_ms // 3_600_000
    hs = pd.DataFrame({"h": hid, "o": o, "hi": h, "lo": l, "c": c}).groupby("h").agg(
        hi=("hi", "max"), lo=("lo", "min"), c=("c", "last"))
    pc = hs.c.shift(1).fillna(hs.c)
    tr = np.maximum(hs.hi - hs.lo, np.maximum((hs.hi - pc).abs(), (hs.lo - pc).abs()))
    return tr.rolling(n).mean().shift(1).reindex(hid).to_numpy(), hid


@njit(cache=True)
def _sim(o, h, l, c, hid, atr, k, fin, fout, s, hold, absp, tak, mak, mspan, mshare):
    n = len(o)
    out = np.full((50000, 5), np.nan)
    m = 0
    cur = -1
    O = L = P = HM = 0.0
    inpos = False
    e = tp = sl = risk = 0.0
    dl = ei = 0
    used = -1
    for i in range(n):
        if inpos:
            ex = np.nan
            typ = 0
            if h[i] >= sl:
                ex = max(sl, o[i]); typ = -1
            elif l[i] <= tp:
                ex = tp; typ = 1
            elif i >= dl:
                ex = c[i]; typ = 0
            if not np.isnan(ex):
                fee = absp[ei] * tak + absp[i] * (mak if typ == 1 else tak)
                out[m, 0] = ei; out[m, 1] = typ
                out[m, 2] = (e - ex) / risk; out[m, 3] = (e - ex - fee) / risk; out[m, 4] = (e - ex - fee) / absp[ei]
                m += 1
                inpos = False
        if hid[i] != cur:
            cur = hid[i]; O = o[i]; L = l[i]; P = c[i]; HM = h[i]
            continue
        if not inpos and not np.isnan(atr[i]) and used != cur:
            T = min(O, P); W = T - L
            if W > 0 and W >= k * atr[i] and HM - L >= mspan and W >= mshare * (HM - L):
                E = T - fin * W
                if l[i] <= E and o[i] > T - fout * W:
                    e = min(E, o[i]); tp = T - fout * W; sl = E + s * W; risk = sl - e
                    inpos = True; ei = i; dl = i + hold; used = cur
        if l[i] < L:
            L = l[i]; P = c[i]
        else:
            P = max(P, h[i])
        HM = max(HM, h[i])
    return out[:m]


def run(df: pd.DataFrame, side: str, k: float, fill_in=0.2, fill_out=0.8, sl_w=0.6, hold_min=360,
        maker=MAKER_FEE, taker=TAKER_FEE, min_span=0.0, min_share=0.0) -> pd.DataFrame:
    ts, o, h, l, c = arrays(df)
    if side == "upper":          # Spiegeln: obere Wick wird zur unteren
        o, h, l, c = -o, -l, -h, -c
    atr, hid = hourly_atr(ts, *(arrays(df)[1:]))
    r = _sim(o, h, l, c, hid, atr, k, fill_in, fill_out, sl_w, hold_min, np.abs(df.open.to_numpy()), taker, maker,
             min_span, min_share)
    reason = np.where(r[:, 1] == 1, "tp", np.where(r[:, 1] == -1, "sl", "zeit"))
    return pd.DataFrame(dict(ts_open=ts[r[:, 0].astype(int)] * 1_000_000, exit_reason=reason,
                             r_gross=r[:, 2], r_net=r[:, 3], pct_net=r[:, 4] * 100))


def raster_h6(df):
    """H16 (LABORBUCH.md): Spanne ab 60 USD, Wick ab 65 %, Einstieg 10 %, SL Oberkante + Puffer, Zeitstopp 24 h."""
    rows = []
    for side, sl_w, fout in itertools.product(["lower", "upper"], [0.10, 0.15, 0.20, 0.30], [0.8, 1.0]):
        t = run(df, side, 0.0, fill_in=0.1, fill_out=fout, sl_w=sl_w, hold_min=1440, min_span=60.0, min_share=0.65)
        rows.append(dict(side=side, sl_w=sl_w, fill_out=fout, **summary(t)))
    return rows


if __name__ == "__main__":
    import sys
    df = load_1m()
    rows = []
    if "--h6" in sys.argv:
        rows = raster_h6(df)
    else:
        for side, k, sl_w in itertools.product(["lower", "upper"], [1.0, 1.5, 2.0], [0.3, 0.6]):
            rows.append(dict(side=side, k=k, sl_w=sl_w, **summary(run(df, side, k, sl_w=sl_w))))
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
