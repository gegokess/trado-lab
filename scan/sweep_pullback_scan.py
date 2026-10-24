"""Schneller numba-Scan für H3 (Liquidity Sweep mit Rücklauf-Einstieg), gleiche Regel wie
strategies/sweep_pullback.py.

Aufruf:  python -m scan.sweep_pullback_scan        (Standard: In-Sample bis OOS_START)

Gerechnet wird immer im gespiegelten Raum als Long nach einem Sweep nach unten, die obere Seite
entsteht durch Negieren der Preise. Die Definition von Swing-Tief, unberührt und Referenzlevel wird
unverändert aus H2 übernommen.

Annahmen gegenüber Nautilus:
- die Einstiegs-Limit-Order füllt genau auf ihrem Level, ein Eröffnungssprung darunter bringt keinen
  besseren Preis (konservativ)
- SL vor TP, wenn beide in derselben Minute liegen
- kein Ausstieg in der Einstiegsminute
- ob die Order platziert wird, entscheidet der Schlusskurs der Vorminute, nicht der laufenden
- Gebühren auf Basis des Minuten-Opens
"""
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import arrays, load_1m
from lab.report import summary
from scan.liquidity_sweep_scan import atr14, hourly, swing_lows


@njit(cache=True)
def _sim(o, h, l, c, hid, atr, swp, k, pb, ftp, s, hold, absp, tak, mak):
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
                fee = absp[ei] * mak + absp[i] * (mak if typ == 1 else tak)
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
                E = T - pb * W; Z = T + ftp * W
                # Limit muss unter dem letzten Schlusskurs liegen (echte Maker-Order) und das Ziel offen sein
                if c[i - 1] > E and c[i - 1] < Z and l[i] <= E:
                    e = E; tp = Z; sl = L - s * W; risk = e - sl
                    inpos = True; ei = i; dl = i + hold; used = cur
        if l[i] < L:
            L = l[i]; P = c[i]
        else:
            P = max(P, h[i])
    return out[:m]


def run(df: pd.DataFrame, side: str, k: float, pb_w=0.2, tp_w=0.5, sl_w=0.2, sw=3, hold_min=360,
        maker=MAKER_FEE, taker=TAKER_FEE) -> pd.DataFrame:
    ts, o, h, l, c = arrays(df)
    if side == "upper":          # Spiegeln: Sweep eines Swing-Hochs wird zum Sweep eines Swing-Tiefs
        o, h, l, c = -o, -l, -h, -c
    hs, hid = hourly(ts, o, h, l, c)
    atr = atr14(hs).reindex(hid).to_numpy()
    swp = swing_lows(hs, sw).reindex(hid).to_numpy()
    r = _sim(o, h, l, c, hid, atr, swp, k, pb_w, tp_w, sl_w, hold_min,
             np.abs(df.open.to_numpy()), taker, maker)
    reason = np.where(r[:, 1] == 1, "tp", np.where(r[:, 1] == -1, "sl", "zeit"))
    return pd.DataFrame(dict(ts_open=ts[r[:, 0].astype(int)] * 1_000_000, exit_reason=reason,
                             r_gross=r[:, 2], r_net=r[:, 3], pct_net=r[:, 4] * 100))


if __name__ == "__main__":
    df = load_1m()
    rows = []
    for side, k, pw, tw in itertools.product(["lower", "upper"], [1.0, 1.5], [0.2, 0.4], [0.5, 1.0]):
        rows.append(dict(side=side, k=k, pb_w=pw, tp_w=tw,
                         **summary(run(df, side, k, pb_w=pw, tp_w=tw))))
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string())
