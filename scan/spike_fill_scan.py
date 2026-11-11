"""Schneller numba-Scan für H9 (Wick nach Spike zur Hälfte füllen), gleiche Regel wie strategies/spike_fill.py.

Aufruf:  TRADO_SYMBOL=PF_ETHUSD python -m scan.spike_fill_scan      (Standard: In-Sample bis OOS_START)
Untere Seite: Spike nach unten, Einstieg Short. Obere Seite über gespiegelte Preise, Einstieg Long.
Annahmen gegenüber Nautilus: Einstieg nur in einer roten Minute (Hoch vor Tief), Stop vor Ziel in derselben Minute,
kein Ausstieg in der Einstiegsminute, Slippage als Anteil vom Preis auf Stop- und Market-Orders.
r_gross enthält die Slippage, aber keine Gebühren.
"""
import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import arrays, load_1m
from lab.report import summary


@njit(cache=True)
def _sim(o, h, l, c, spike, rb_min, fin, fout, sl_w, window, hold, cooldown, slip, tak, mak):
    n = len(o)
    out = np.full((n // 15 + 1, 5), np.nan)
    m = 0
    i = 1500
    last = -10**9
    while i < n - 6:
        S = max(h[i - 4], h[i - 3], h[i - 2], h[i - 1], h[i])
        if l[i] > min(l[i - 4], l[i - 3], l[i - 2], l[i - 1]) or S - l[i] < spike * abs(S) or i - last < cooldown:
            i += 1
            continue
        last = i
        L = l[i]
        iL = i
        for q in range(i + 1, min(i + 6, n)):
            if l[q] < L:
                L = l[q]
                iL = q
        M = S - L
        RH = L
        j = -1
        E = 0.0
        RHe = 0.0
        for q in range(iL + 1, min(iL + 1 + window, n)):
            if l[q] < L:
                break
            if h[q] > RH:
                RH = h[q]
            W = RH - L
            if W >= rb_min * M and l[q] <= RH - fin * W and c[q] < o[q]:
                j = q
                E = min(RH - fin * W, o[q]) - slip * abs(o[q])
                RHe = RH
                break
        if j >= 0 and j + 1 < n:
            W = RHe - L
            SL = RHe + sl_w * W
            T = RHe - fout * W
            risk = SL - E
            ex = 0.0
            typ = 0
            k = -1
            for q in range(j + 1, min(j + 1 + hold, n)):
                if h[q] >= SL:
                    ex = max(SL, o[q]) + slip * abs(SL)
                    typ = -1
                    k = q
                    break
                if l[q] <= T:
                    ex = T
                    typ = 1
                    k = q
                    break
            if k < 0:
                k = min(j + hold, n - 1)
                ex = c[k] + slip * abs(c[k])
            if risk > 0:
                fee = abs(E) * tak + abs(ex) * (mak if typ == 1 else tak)
                out[m, 0] = j
                out[m, 1] = typ
                out[m, 2] = (E - ex) / risk
                out[m, 3] = (E - ex - fee) / risk
                out[m, 4] = (E - ex - fee) / abs(E)
                m += 1
        i += cooldown
    return out[:m]


def run(df: pd.DataFrame, side: str, spike=0.02, rb_min=0.3, fill_in=0.1, fill_out=0.5, sl_w=0.1, window=180,
        hold_min=4320, cooldown=15, slip=0.0002, maker=MAKER_FEE, taker=TAKER_FEE) -> pd.DataFrame:
    ts, o, h, l, c = arrays(df)
    if side == "upper":          # Spiegeln: Spike nach oben wird zum Spike nach unten
        o, h, l, c = -o, -l, -h, -c
    r = _sim(o, h, l, c, spike, rb_min, fill_in, fill_out, sl_w, window, hold_min, cooldown, slip, taker, maker)
    reason = np.where(r[:, 1] == 1, "tp", np.where(r[:, 1] == -1, "sl", "zeit"))
    return pd.DataFrame(dict(ts_open=ts[r[:, 0].astype(int)] * 1_000_000, exit_reason=reason,
                             r_gross=r[:, 2], r_net=r[:, 3], pct_net=r[:, 4] * 100, side=side))


if __name__ == "__main__":
    df = load_1m()
    rows = []
    t = {s: run(df, s) for s in ("lower", "upper")}
    t["beide"] = pd.concat(t.values())
    for side, tr in t.items():
        rows.append(dict(side=side, **summary(tr)))
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
