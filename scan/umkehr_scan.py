"""Ereignisstudie für H11: kehrt BTC nach einer sehr starken Bewegung um?

Aufruf:  python -m scan.umkehr_scan        (In-Sample bis OOS_START)

Definition laut Laborbuch:
- Stundenpreise p_t = Open der Minute zur vollen Stunde t
- Bewegung r_L = p_t / p_(t−L) − 1, Maßstab σ_L = σ_1h × √L mit σ_1h = Standardabweichung der 1h-Renditen
  der 720 Stunden vor Beginn der Bewegung (nur Vergangenheit)
- Ereignis bei |r_L| ≥ k × σ_L, Entballung: je Zelle höchstens ein Ereignis in 24 h
- Folgerendite über H Stunden ab p_t, mit Vorzeichen gegen die Bewegung (positiv = Umkehr)
- Zelle zählt nur bei t ≥ 3,3 brutto (Bonferroni, 54 Zellen) und netto positiv nach 6 bps (zweimal Taker)
"""
import itertools

import numpy as np
import pandas as pd

from lab.config import TAKER_FEE
from lab.data import load_1m

L_WERTE, K_WERTE, H_WERTE = (1, 4, 24), (2, 3, 4), (1, 4, 24)
T_GRENZE = 3.3
KOSTEN_BPS = 2 * TAKER_FEE * 1e4


def stundenpreise(df: pd.DataFrame) -> pd.Series:
    ts = df.ts_open.to_numpy(np.int64)
    m = ts % 3_600_000 == 0
    return pd.Series(df.open.to_numpy(float)[m], index=pd.to_datetime(ts[m], unit="ms"))


def ereignisse(p: pd.Series, L: int, k: float, H: int) -> pd.DataFrame:
    r1 = p.pct_change()
    sig1 = r1.rolling(720).std().shift(L)                 # Volatilität vor Beginn der Bewegung
    rL = p / p.shift(L) - 1
    fwd = p.shift(-H) / p - 1
    d = pd.DataFrame(dict(rL=rL, z=rL / (sig1 * np.sqrt(L)), fwd=fwd)).dropna()
    rows = []
    for richtung, maske in (("Fall", d.z <= -k), ("Anstieg", d.z >= k)):
        letzte = None
        for t, r in d[maske].iterrows():
            if letzte is not None and t - letzte < pd.Timedelta(hours=24):
                continue
            letzte = t
            rows.append(dict(t=t, richtung=richtung, z=r.z, umkehr_bps=-np.sign(r.rL) * r.fwd * 1e4))
    return pd.DataFrame(rows)


def zelle(e: pd.DataFrame) -> dict:
    x = e.umkehr_bps
    n = len(x)
    se = x.std(ddof=1) / np.sqrt(n) if n > 1 else np.nan
    return dict(n=n, bps_brutto=x.mean() if n else np.nan, t=x.mean() / se if n > 1 else np.nan,
                bps_netto=x.mean() - KOSTEN_BPS if n else np.nan, treffer=(x > 0).mean() if n else np.nan)


if __name__ == "__main__":
    pd.set_option("display.width", 220)
    p = stundenpreise(load_1m())
    rows, alle = [], {}
    for L, k, H in itertools.product(L_WERTE, K_WERTE, H_WERTE):
        e = ereignisse(p, L, k, H)
        for richtung in ("Fall", "Anstieg"):
            sub = e[e.richtung == richtung] if len(e) else e
            alle[(L, k, H, richtung)] = sub
            rows.append(dict(L=L, k=k, H=H, richtung=richtung, **zelle(sub)))
    tab = pd.DataFrame(rows)
    tab["zaehlt"] = (tab.t >= T_GRENZE) & (tab.bps_netto > 0)
    print(f"H11 Ereignisstudie, {len(p)} Stunden In-Sample, Kosten {KOSTEN_BPS:.0f} bps je Runde")
    print(tab.round(2).to_string(index=False))
    print(f"\nZellen mit t ≥ {T_GRENZE} und netto positiv: {int(tab.zaehlt.sum())} von {len(tab)}")
    print(f"Zellen mit t ≥ 2 (ohne Korrektur, beschreibend): {int((tab.t >= 2).sum())}, mit t ≤ −2: {int((tab.t <= -2).sum())}")
    for _, r in tab[tab.zaehlt | (tab.t >= 2)].iterrows():
        sub = alle[(r.L, r.k, r.H, r.richtung)]
        jahre = sub.groupby(sub.t.dt.year).umkehr_bps.agg(["size", "mean"]).round(1)
        print(f"\nL={r.L} k={r.k} H={r.H} {r.richtung}: je Jahr (Anzahl, bps brutto)\n{jahre.T.to_string()}")
