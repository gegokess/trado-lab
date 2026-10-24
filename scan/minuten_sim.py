"""Gemeinsamer Ausstieg auf 1m-Kerzen für H14 und H15: Stop, Ziel und Zeitstopp ab einer Einstiegsminute.

Konventionen wie in den übrigen Scans: Stop vor Ziel in derselben Minute, Stop gilt schon in der
Einstiegsminute, Ziel erst ab der Folgeminute und nur bei Durchhandeln (Limit, Maker).
"""
import numpy as np
from numba import njit


@njit(cache=True)
def ausstieg(o, h, l, c, i0, s, sl, tp, ende):
    """s = +1 Long, −1 Short. Rückgabe (Ausstiegsminute, Preis, Art: 1 Ziel, −1 Stop, 0 Zeit)."""
    n = len(o)
    ende = min(ende, n - 1)
    for i in range(i0, ende + 1):
        if s > 0:
            if l[i] <= sl:
                return i, (sl if i == i0 else min(sl, o[i])), -1
            if i > i0 and not np.isnan(tp) and h[i] > tp:
                return i, tp, 1
        else:
            if h[i] >= sl:
                return i, (sl if i == i0 else max(sl, o[i])), -1
            if i > i0 and not np.isnan(tp) and l[i] < tp:
                return i, tp, 1
    return ende, c[ende], 0
