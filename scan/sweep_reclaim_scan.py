"""Schneller numba-Scan für H4 und H5, gleiche Regel wie strategies/sweep_reclaim.py.

Beides sind Varianten von H3 (Rücklauf-Einstieg) mit je einer zusätzlichen Zutat, gesteuert über
zwei Schalter:

- reclaim=True  (H4): Setup nur gültig, wenn das Einstiegslevel strikt über dem gesweepten Level liegt
- lvl_tf=4      (H5): Swing-Tiefs werden auf 4h-Kerzen bestimmt statt auf 1h

Mit reclaim=False und lvl_tf=1 muss dieses Modul H3 exakt reproduzieren, das ist der Korrektheitstest
(python -m scan.sweep_reclaim_scan --pruefe).

Aufruf:
    python -m scan.sweep_reclaim_scan           # beide Raster, In-Sample bis OOS_START
    python -m scan.sweep_reclaim_scan --pruefe  # nur der Abgleich gegen H3

Annahmen gegenüber Nautilus wie in H3: die Einstiegs-Limit-Order füllt genau auf ihrem Level, SL vor
TP bei gleicher Minute, kein Ausstieg in der Einstiegsminute, Platzierung entscheidet der Schlusskurs
der Vorminute, Gebühren auf Basis des Minuten-Opens.
"""
import argparse
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import arrays, load_1m
from lab.report import summary


def ohlc(ts_ms, o, h, l, c, tf_h=1):
    """OHLC je Kerze von tf_h Stunden und der Kerzenindex je Minute."""
    bid = ts_ms // (tf_h * 3_600_000)
    hs = pd.DataFrame({"b": bid, "op": o, "hi": h, "lo": l, "cl": c}).groupby("b").agg(
        op=("op", "first"), hi=("hi", "max"), lo=("lo", "min"), cl=("cl", "last"))
    return hs, bid


def atr14(hs, n=14):
    """ATR der abgeschlossenen Kerzen, Definition wie in H1 bis H3 (Wert gilt für die laufende Kerze)."""
    pc = hs.cl.shift(1).fillna(hs.cl)
    tr = np.maximum(hs.hi - hs.lo, np.maximum((hs.hi - pc).abs(), (hs.lo - pc).abs()))
    return tr.rolling(n).mean().shift(1)


def levels_per_hour(hs1, hsl, sw, tf_h):
    """Je 1h-Stunde das höchste unberührte Swing-Tief des Level-Zeitrahmens unterhalb des Stundenopens.

    Swing-Tief bei Level-Kerze t: lo[t] liegt strikt unter den Tiefs der sw Kerzen davor und danach,
    nutzbar erst ab der Bestätigung mit Kerze t+sw, und es fällt dauerhaft weg, sobald eine
    abgeschlossene Level-Kerze darunter gehandelt hat. Für tf_h = 1 ist das die Definition aus H2.
    """
    lol = hsl.lo.to_numpy()
    pos = {b: i for i, b in enumerate(hsl.index.to_numpy())}
    op1 = hs1.op.to_numpy()
    out = np.full(len(op1), np.nan)
    aktiv: list[float] = []
    fertig = -1                                  # letzte eingearbeitete Level-Kerze
    for i, stunde in enumerate(hs1.index.to_numpy()):
        p = pos.get(stunde // tf_h)
        if p is None:
            continue
        while fertig < p - 1:                    # alle inzwischen abgeschlossenen Level-Kerzen
            fertig += 1
            t = fertig - sw
            if t - sw >= 0 and lol[t] < lol[t - sw:t].min() and lol[t] < lol[t + 1:t + sw + 1].min():
                aktiv.append(lol[t])
            aktiv = [s for s in aktiv if s <= lol[fertig]]
        unten = [s for s in aktiv if s < op1[i]]
        if unten:
            out[i] = max(unten)
    return pd.Series(out, index=hs1.index)


@njit(cache=True)
def _sim(o, h, l, c, hid, atr, swp, k, pb, ftp, s, hold, rec, absp, tak, mak):
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
                # H4: der Einstieg muss über dem gesweepten Level bleiben
                if (rec == 0 or S < E) and c[i - 1] > E and c[i - 1] < Z and l[i] <= E:
                    e = E; tp = Z; sl = L - s * W; risk = e - sl
                    inpos = True; ei = i; dl = i + hold; used = cur
        if l[i] < L:
            L = l[i]; P = c[i]
        else:
            P = max(P, h[i])
    return out[:m]


def run(df: pd.DataFrame, side: str, k: float, pb_w=0.2, tp_w=0.5, sl_w=0.2, sw=3, hold_min=360,
        reclaim=False, lvl_tf=1, maker=MAKER_FEE, taker=TAKER_FEE) -> pd.DataFrame:
    ts, o, h, l, c = arrays(df)
    if side == "upper":          # Spiegeln: Sweep eines Swing-Hochs wird zum Sweep eines Swing-Tiefs
        o, h, l, c = -o, -l, -h, -c
    hs1, hid = ohlc(ts, o, h, l, c, 1)
    hsl = hs1 if lvl_tf == 1 else ohlc(ts, o, h, l, c, lvl_tf)[0]
    atr = atr14(hs1).reindex(hid).to_numpy()
    swp = levels_per_hour(hs1, hsl, sw, lvl_tf).reindex(hid).to_numpy()
    r = _sim(o, h, l, c, hid, atr, swp, k, pb_w, tp_w, sl_w, hold_min, 1 if reclaim else 0,
             np.abs(df.open.to_numpy()), taker, maker)
    reason = np.where(r[:, 1] == 1, "tp", np.where(r[:, 1] == -1, "sl", "zeit"))
    return pd.DataFrame(dict(ts_open=ts[r[:, 0].astype(int)] * 1_000_000, exit_reason=reason,
                             r_gross=r[:, 2], r_net=r[:, 3], pct_net=r[:, 4] * 100))


def _raster(df, reclaim, lvl_tf):
    rows = []
    for side, k, pw, tw in itertools.product(["lower", "upper"], [1.0, 1.5], [0.2, 0.4], [0.5, 1.0]):
        rows.append(dict(side=side, k=k, pb_w=pw, tp_w=tw,
                         **summary(run(df, side, k, pb_w=pw, tp_w=tw, reclaim=reclaim, lvl_tf=lvl_tf))))
    return pd.DataFrame(rows).round(3)


def _pruefe(df):
    """Mit beiden Schaltern aus muss dieses Modul H3 Trade für Trade reproduzieren."""
    from scan.sweep_pullback_scan import run as h3
    ok = True
    for side, k, pw, tw in itertools.product(["lower", "upper"], [1.0, 1.5], [0.2, 0.4], [0.5, 1.0]):
        a = h3(df, side, k, pb_w=pw, tp_w=tw)
        b = run(df, side, k, pb_w=pw, tp_w=tw, reclaim=False, lvl_tf=1)
        gleich = len(a) == len(b) and a.ts_open.equals(b.ts_open) and np.allclose(a.r_net, b.r_net)
        ok &= gleich
        if not gleich:
            print(f"ABWEICHUNG {side} k={k} pb={pw} tp={tw}: H3 {len(a)} Trades, hier {len(b)}")
    print("H3 wird exakt reproduziert" if ok else "H3 wird NICHT reproduziert")
    return ok


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pruefe", action="store_true", help="nur den Abgleich gegen H3 rechnen")
    a = ap.parse_args()
    df = load_1m()
    pd.set_option("display.width", 250)
    if a.pruefe:
        _pruefe(df)
    else:
        print("##### H4: reclaim=True, Level aus 1h #####")
        print(_raster(df, True, 1).to_string())
        print()
        print("##### H5: reclaim=False, Level aus 4h #####")
        print(_raster(df, False, 4).to_string())
