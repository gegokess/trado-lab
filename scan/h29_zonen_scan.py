"""H29 Stufe 1: Zonen-Setups mit dem Trend, Scan brutto gegen verschobene Kontrollzonen (LABORBUCH.md).

Aufruf:  python -m scan.h29_zonen_scan [--symbol PF_XBTUSD]

Zonen Z1 bis Z4, Setups S1 (Rücklauf) und S2 (Ausbruch und Retest), Trend T1 (4h-EMA) und T2 (4h-Struktur),
Long und Short. Messgröße ist ein 1:1-Bracket ohne Gebühren. Kontrolle: je Zone 5 um 1 bis 3 ATR verschobene
Zonen gleicher Breite mit denselben Regeln. Nur In-Sample bis OOS_START.
"""
import argparse
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from numba import njit

from lab.config import OOS_START, RAW_DIR, RUNS_DIR
from scan.h28_trendfilter import trend_reihen

MIN, H4, TAG = 60_000, 14_400_000, 86_400_000
N_KONTROLLE = 5
HALTEN = 72 * 60
SL_PUFFER = 0.25
VORLAUF_TAGE = 100


# ---------------------------------------------------------------- Ergebnis eines Brackets
@njit(cache=True)
def bracket(high, low, close, i, richtung, einstieg, stop, halten):
    """1:1-Bracket ab Minute i. Stop in Minute i zählt, Ziel erst ab i + 1. Rückgabe (R, Ende-Index)."""
    r = abs(einstieg - stop)
    ziel = einstieg + richtung * r
    if richtung == 1 and low[i] <= stop or richtung == -1 and high[i] >= stop:
        return -1.0, i
    n = len(high)
    ende = min(n - 1, i + halten)
    for j in range(i + 1, ende + 1):
        if richtung == 1:
            if low[j] <= stop:
                return -1.0, j
            if high[j] >= ziel:
                return 1.0, j
        else:
            if high[j] >= stop:
                return -1.0, j
            if low[j] <= ziel:
                return 1.0, j
    return richtung * (close[ende] - einstieg) / r, ende


@njit(cache=True)
def letzte_beruehrung(high, low, a, niveau, richtung, rueck):
    """Letzter Index < a, an dem das Niveau berührt wurde (Long: Tief ≤ Niveau, Short: Hoch ≥ Niveau), sonst -1."""
    for j in range(a - 1, max(-1, a - rueck - 1), -1):
        if richtung == 1 and low[j] <= niveau or richtung == -1 and high[j] >= niveau:
            return j
    return -1


@njit(cache=True)
def s1_ausloeser(high, low, a, b, niveau, abstand, richtung, rueck):
    """Erste Berührungen in [a, b), vor denen sich der Kurs seit der letzten Berührung mindestens `abstand` entfernt hatte."""
    out = []
    lt = letzte_beruehrung(high, low, a, niveau, richtung, rueck)
    weit = False
    if lt >= 0:
        for j in range(lt + 1, a):
            if richtung == 1 and high[j] >= niveau + abstand or richtung == -1 and low[j] <= niveau - abstand:
                weit = True
                break
    for t in range(a, b):
        if richtung == 1 and high[t] >= niveau + abstand or richtung == -1 and low[t] <= niveau - abstand:
            if not (richtung == 1 and low[t] <= niveau or richtung == -1 and high[t] >= niveau):
                weit = True
        if richtung == 1 and low[t] <= niveau or richtung == -1 and high[t] >= niveau:
            if weit:
                out.append(t)
            weit = False
    return out


# ---------------------------------------------------------------- Zonen
def swings(h4: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    """Swing-Hochs und -Tiefs mit dem Zeitpunkt, ab dem sie bekannt sind (Schluss der k-ten Kerze danach)."""
    hi, lo = h4.high.to_numpy(), h4.low.to_numpy()
    rows = []
    for j in range(k, len(h4) - k):
        fh, fl = hi[j - k:j + k + 1], lo[j - k:j + k + 1]
        if hi[j] == fh.max() and (fh == hi[j]).sum() == 1:
            rows.append((h4.ts.iloc[j + k] + H4, h4.ts.iloc[j], hi[j]))
        if lo[j] == fl.min() and (fl == lo[j]).sum() == 1:
            rows.append((h4.ts.iloc[j + k] + H4, h4.ts.iloc[j], lo[j]))
    return pd.DataFrame(rows, columns=["bekannt", "ts", "preis"]).sort_values("bekannt").reset_index(drop=True)


def z1(sw: pd.DataFrame, t: int, atr: float) -> list[tuple[float, float]]:
    d = sw[(sw.bekannt <= t) & (sw.ts >= t - VORLAUF_TAGE * TAG)].preis.sort_values().to_numpy()
    zonen, gruppe = [], []
    for p in d:
        if gruppe and (p - gruppe[-1] > 0.5 * atr or p - gruppe[0] > atr):
            if len(gruppe) >= 3:
                zonen.append((gruppe[0], gruppe[-1]))
            gruppe = []
        gruppe.append(p)
    if len(gruppe) >= 3:
        zonen.append((gruppe[0], gruppe[-1]))
    return zonen


def z2(tage: pd.DataFrame, wochen: pd.DataFrame, t: int, atr: float) -> list[tuple[float, float]]:
    out = []
    vt = tage[tage.ts == t // TAG * TAG - TAG]
    wbeginn = (t // TAG - (pd.Timestamp(t, unit="ms").day_of_week)) * TAG
    vw = wochen[wochen.ts == wbeginn - 7 * TAG]
    for d in (vt, vw):
        if len(d):
            for p in (d.high.iloc[0], d.low.iloc[0]):
                out.append((p - 0.1 * atr, p + 0.1 * atr))
    return out


def z3(kurs: float, atr: float, schritt: float) -> list[tuple[float, float]]:
    a, b = kurs - 15 * atr, kurs + 15 * atr
    return [(p * 0.999, p * 1.001) for p in np.arange(np.ceil(a / schritt) * schritt, b, schritt)]


STUFE = np.log(1.0025)


def z4(m1: pd.DataFrame, t: int) -> list[tuple[float, float]]:
    d = m1[(m1.ts_open >= t - 30 * TAG) & (m1.ts_open < t)]
    if len(d) < 1000:
        return []
    tp = (d.high + d.low + d.close) / 3
    b = np.floor(np.log(tp.to_numpy()) / STUFE).astype(np.int64)
    vol = pd.Series(d.volume.to_numpy()).groupby(b).sum()
    vol = vol.reindex(range(vol.index.min(), vol.index.max() + 1), fill_value=0.0)
    grenze = vol[vol > 0].quantile(0.9)
    v = vol.to_numpy()
    out = []
    for i, (stufe, x) in enumerate(vol.items()):
        if x > grenze and x == v[max(0, i - 2):i + 3].max():
            out.append((float(np.exp(stufe * STUFE)), float(np.exp((stufe + 1) * STUFE))))
    return out


# ---------------------------------------------------------------- Hauptlauf
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default="PF_XBTUSD")
    a = ap.parse_args()
    schritt = {"PF_XBTUSD": 1000.0, "PF_ETHUSD": 50.0}[a.symbol]

    m1 = pd.read_parquet(RAW_DIR / f"{a.symbol}_1m.parquet")
    grenze = pd.Timestamp(OOS_START, tz="UTC").value // 1_000_000
    m1 = m1[m1.ts_open < grenze + HALTEN * MIN].reset_index(drop=True)
    ts = m1.ts_open.to_numpy()
    high, low, close = (m1[c].to_numpy() for c in ("high", "low", "close"))

    g = m1.assign(ts=m1.ts_open // H4 * H4).groupby("ts")
    h4 = g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"), close=("close", "last")).reset_index()
    tr = np.maximum(h4.high - h4.low, np.maximum((h4.high - h4.close.shift()).abs(), (h4.low - h4.close.shift()).abs()))
    h4["atr"] = tr.rolling(14).mean()
    tage = m1.assign(ts=m1.ts_open // TAG * TAG).groupby("ts").agg(high=("high", "max"), low=("low", "min")).reset_index()
    wt = pd.to_datetime(m1.ts_open, unit="ms")
    wochen = m1.assign(ts=((m1.ts_open // TAG) - wt.dt.dayofweek.to_numpy()) * TAG).groupby("ts") \
        .agg(high=("high", "max"), low=("low", "min")).reset_index()
    sw = swings(h4)
    trend = trend_reihen(h4[["ts", "high", "low", "close"]])
    # Trend je Minute: Wert der zuletzt geschlossenen 4h-Kerze
    k_idx = np.searchsorted(trend.gueltig_ab.to_numpy(), ts, side="right") - 1
    trend_min = {td: np.where(k_idx >= 0, trend[td].to_numpy()[np.clip(k_idx, 0, None)], 0) for td in ("t1", "t2")}

    rng = np.random.default_rng(29)
    rueck = VORLAUF_TAGE * 1440
    ereignisse = []                       # (setup, zone, richtung, kontrolle, t_index, einstieg, stop)
    z4_cache = {}
    start = int(h4.ts.iloc[0]) + VORLAUF_TAGE * TAG
    for bi in range(len(h4) - 1):
        t0 = int(h4.ts.iloc[bi])
        if t0 < start or t0 >= grenze:
            continue
        atr = float(h4.atr.iloc[bi - 1])           # ATR der zuletzt geschlossenen 4h-Kerze
        kurs = float(h4.close.iloc[bi - 1])
        a_i, b_i = np.searchsorted(ts, t0), np.searchsorted(ts, t0 + H4)
        blo, bhi = low[a_i:b_i].min(), high[a_i:b_i].max()
        tag = t0 // TAG * TAG
        if tag not in z4_cache:
            z4_cache = {tag: z4(m1, tag)}
        zonen = {"Z1": z1(sw, t0, atr), "Z2": z2(tage, wochen, t0, atr), "Z3": z3(kurs, atr, schritt), "Z4": z4_cache[tag]}
        for zname, zl in zonen.items():
            for (lo, hi) in zl:
                if hi - lo > 3 * atr or abs((lo + hi) / 2 - kurs) > 15 * atr:
                    continue
                versch = [0.0] + list(rng.uniform(1, 3, N_KONTROLLE) * rng.choice([-1, 1], N_KONTROLLE) * atr)
                for kk, dv in enumerate(versch):
                    zlo, zhi = lo + dv, hi + dv
                    # S1 Rücklauf: Long an der Oberkante, Short an der Unterkante
                    if blo <= zhi:                      # nur Zonen, die in diesem Block berührt werden
                        for t in s1_ausloeser(high, low, a_i, b_i, zhi, atr, 1, rueck):
                            ereignisse.append(("S1", zname, 1, kk, t, zhi, zlo - SL_PUFFER * atr))
                    if bhi >= zlo:
                        for t in s1_ausloeser(high, low, a_i, b_i, zlo, atr, -1, rueck):
                            ereignisse.append(("S1", zname, -1, kk, t, zlo, zhi + SL_PUFFER * atr))
                    # S2 Ausbruch dieser 4h-Kerze und Retest in den folgenden 12 4h-Kerzen
                    o4, c4 = h4.open.iloc[bi], h4.close.iloc[bi]
                    for richtung, ok, niveau, stop in ((1, o4 < zlo and c4 > zhi, zhi, zlo - SL_PUFFER * atr),
                                                       (-1, o4 > zhi and c4 < zlo, zlo, zhi + SL_PUFFER * atr)):
                        if not ok:
                            continue
                        c_i, d_i = b_i, min(len(ts), np.searchsorted(ts, t0 + 13 * H4))
                        seg = low[c_i:d_i] <= niveau if richtung == 1 else high[c_i:d_i] >= niveau
                        if seg.any():
                            ereignisse.append(("S2", zname, richtung, kk, c_i + int(seg.argmax()), niveau, stop))
    e = pd.DataFrame(ereignisse, columns=["setup", "zone", "richtung", "kontrolle", "i", "einstieg", "stop"])
    e = e[ts[e.i] < grenze].sort_values("i").reset_index(drop=True)
    print(f"{len(e):,} Berührungen vor Trendfilter")

    zeilen, trades = [], []
    for td in ("t1", "t2"):
        mit = trend_min[td][e.i.to_numpy()] == e.richtung.to_numpy()
        d = e[mit]
        for (setup, zone, richtung), gz in d.groupby(["setup", "zone", "richtung"]):
            res = {}
            for kk, gk in gz.groupby("kontrolle"):
                frei_ab, rs = -1, []
                for row in gk.itertuples():
                    if row.i <= frei_ab:
                        continue                          # je Zelle und Kontrollreihe nur ein Trade gleichzeitig
                    r, ende = bracket(high, low, close, row.i, row.richtung, row.einstieg, row.stop, HALTEN)
                    rs.append(r)
                    frei_ab = ende
                    if kk == 0:
                        trades.append(dict(trend=td, setup=setup, zone=zone, richtung=richtung, ts=int(ts[row.i]),
                                           einstieg=row.einstieg, stop=row.stop, r=r))
                res[kk] = np.array(rs)
            echt = res.get(0, np.array([]))
            kon = np.concatenate([v for k, v in res.items() if k > 0]) if len(res) > 1 else np.array([])
            t_diff = np.nan
            if len(echt) > 1 and len(kon) > 1:
                t_diff = (echt.mean() - kon.mean()) / np.sqrt(echt.var(ddof=1) / len(echt) + kon.var(ddof=1) / len(kon))
            zeilen.append(dict(trend=td, setup=setup, zone=zone, seite="long" if richtung == 1 else "short",
                               n=len(echt), r=echt.mean() if len(echt) else np.nan,
                               treffer=(echt > 0).mean() if len(echt) else np.nan,
                               n_kontrolle=len(kon), r_kontrolle=kon.mean() if len(kon) else np.nan, t_diff=t_diff))
    erg = pd.DataFrame(zeilen)
    erg["weiter"] = (erg.t_diff >= 3) & (erg.r > 0)
    pd.set_option("display.width", 200)
    print(erg.round(3).to_string(index=False))
    out = RUNS_DIR / (datetime.now(timezone.utc).strftime("%Y%m%d-%H%M") + f"_h29_zonen_scan_{a.symbol}")
    out.mkdir(exist_ok=True)
    erg.to_csv(out / "ergebnis.csv", index=False)
    pd.DataFrame(trades).to_csv(out / "trades.csv", index=False)
    print(f"Gespeichert: {out}")


if __name__ == "__main__":
    main()
