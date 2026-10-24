"""Schneller numba-Scan für H2 (Liquidity Sweep, Umkehr), gleiche Regel wie strategies/liquidity_sweep.py.

Aufruf:  python -m scan.liquidity_sweep_scan        (Standard: In-Sample bis OOS_START)

Gerechnet wird immer im gespiegelten Raum als Long nach einem Sweep nach unten, die obere Seite
entsteht durch Negieren der Preise. Annahmen gegenüber Nautilus: SL vor TP, wenn beide in derselben
Minute liegen, kein Ausstieg in der Einstiegsminute, Gebühren auf Basis des Minuten-Opens.
"""
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import arrays, load_1m
from lab.report import summary


def hourly(ts_ms, o, h, l, c):
    """1h-OHLC und Stundenindex je Minute, aus den (ggf. gespiegelten) 1m-Arrays."""
    hid = ts_ms // 3_600_000
    hs = pd.DataFrame({"h": hid, "op": o, "hi": h, "lo": l, "cl": c}).groupby("h").agg(
        op=("op", "first"), hi=("hi", "max"), lo=("lo", "min"), cl=("cl", "last"))
    return hs, hid


def atr14(hs, n=14):
    """ATR der abgeschlossenen Stunden, Definition wie in H1 (der Wert gilt für die laufende Stunde)."""
    pc = hs.cl.shift(1).fillna(hs.cl)
    tr = np.maximum(hs.hi - hs.lo, np.maximum((hs.hi - pc).abs(), (hs.lo - pc).abs()))
    return tr.rolling(n).mean().shift(1)


def swing_lows(hs, sw):
    """Je Stunde das höchste unberührte Swing-Tief unterhalb des Stundenopens (nan wenn keines).

    Swing-Tief bei Stunde t: lo[t] liegt strikt unter den Tiefs der sw Stunden davor und danach.
    Nutzbar erst ab Stunde t+sw+1 (vorher nicht bestätigt), und es fällt dauerhaft weg, sobald
    eine abgeschlossene Stunde darunter gehandelt hat.
    """
    lo, op = hs.lo.to_numpy(), hs.op.to_numpy()
    out = np.full(len(lo), np.nan)
    aktiv: list[float] = []
    for i in range(len(lo)):
        t = i - 1 - sw                       # Kandidat, der mit Stunde i-1 bestätigt ist
        if t - sw >= 0 and lo[t] < lo[t - sw:t].min() and lo[t] < lo[t + 1:t + sw + 1].min():
            aktiv.append(lo[t])
        if i:
            aktiv = [s for s in aktiv if s <= lo[i - 1]]
        unten = [s for s in aktiv if s < op[i]]
        if unten:
            out[i] = max(unten)
    return pd.Series(out, index=hs.index)


@njit(cache=True)
def _sim(o, h, l, c, hid, atr, swp, k, fin, ftp, s, hold, absp, tak, mak):
    n = len(o)
    out = np.full((50000, 5), np.nan)
    m = 0
    cur = -1
    O = L = P = 0.0
    inpos = False
    e = tp = sl = risk = 0.0
    dl = ei = 0
    used = -1
    for i in range(n):
        if inpos:
            ex = np.nan
            typ = 0
            if l[i] <= sl:
                ex = min(sl, o[i]); typ = -1
            elif h[i] >= tp:
                ex = tp; typ = 1
            elif i >= dl:
                ex = c[i]; typ = 0
            if not np.isnan(ex):
                fee = absp[ei] * tak + absp[i] * (mak if typ == 1 else tak)
                out[m, 0] = ei; out[m, 1] = typ
                out[m, 2] = (ex - e) / risk; out[m, 3] = (ex - e - fee) / risk; out[m, 4] = (ex - e - fee) / absp[ei]
                m += 1
                inpos = False
        if hid[i] != cur:
            cur = hid[i]; O = o[i]; L = l[i]; P = c[i]
            continue
        if not inpos and not np.isnan(atr[i]) and not np.isnan(swp[i]) and used != cur:
            T = min(O, P); W = T - L; S = swp[i]
            if W > 0 and W >= k * atr[i] and L < S and S <= T:
                E = L + fin * W; Z = T + ftp * W
                if h[i] >= E and o[i] < Z and c[i] < Z:
                    e = max(E, o[i]); tp = Z; sl = L - s * W; risk = e - sl
                    inpos = True; ei = i; dl = i + hold; used = cur
        if l[i] < L:
            L = l[i]; P = c[i]
        else:
            P = max(P, h[i])
    return out[:m]


def run(df: pd.DataFrame, side: str, k: float, entry_w=0.3, tp_w=0.5, sl_w=0.2, sw=3, hold_min=360,
        maker=MAKER_FEE, taker=TAKER_FEE) -> pd.DataFrame:
    ts, o, h, l, c = arrays(df)
    if side == "upper":          # Spiegeln: Sweep eines Swing-Hochs wird zum Sweep eines Swing-Tiefs
        o, h, l, c = -o, -l, -h, -c
    hs, hid = hourly(ts, o, h, l, c)
    atr = atr14(hs).reindex(hid).to_numpy()
    swp = swing_lows(hs, sw).reindex(hid).to_numpy()
    r = _sim(o, h, l, c, hid, atr, swp, k, entry_w, tp_w, sl_w, hold_min,
             np.abs(df.open.to_numpy()), taker, maker)
    reason = np.where(r[:, 1] == 1, "tp", np.where(r[:, 1] == -1, "sl", "zeit"))
    return pd.DataFrame(dict(ts_open=ts[r[:, 0].astype(int)] * 1_000_000, exit_reason=reason,
                             r_gross=r[:, 2], r_net=r[:, 3], pct_net=r[:, 4] * 100))


if __name__ == "__main__":
    df = load_1m()
    rows = []
    for side, k, ew, tw in itertools.product(["lower", "upper"], [1.0, 1.5], [0.3, 0.5], [0.5, 1.0]):
        rows.append(dict(side=side, k=k, entry_w=ew, tp_w=tw,
                         **summary(run(df, side, k, entry_w=ew, tp_w=tw))))
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
