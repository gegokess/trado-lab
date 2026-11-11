"""Aufruf: python scan/h22_liquidationen.py .

H22: Liquidationen im Spike als Ursache der H20-Regel (Auswertung vorhandener H20-Trades)."""
import json, sys
from pathlib import Path
import numpy as np, pandas as pd

ROOT = Path(sys.argv[1])
IS = ROOT / "runs/20261111-204153_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5/trades.csv"
OOS = ROOT / "runs/20261111-203112_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5_OOS/trades.csv"
p = pd.read_parquet(ROOT / "data/raw/PF_XBTUSD_1m.parquet")
liq = pd.read_parquet(ROOT / "data/raw/PF_XBTUSD_liquidation-volume_1m.parquet")
p = p.merge(liq, on="ts_open", how="left").fillna({"wert": 0.0})
ts = p.ts_open.to_numpy(); h = p.high.to_numpy(); lo = p.low.to_numpy(); L = p.wert.to_numpy()
# Spike-Minute: Hoch ist das höchste der letzten 5 Minuten und >= 2 % über dem Tief dieser 5 Minuten
hmax = pd.Series(h).rolling(5).max().to_numpy(); lmin = pd.Series(lo).rolling(5).min().to_numpy()
spike = (h >= hmax) & (h - lmin >= 0.02 * lmin)

def kennzahl(t_ein_ns):
    i = np.searchsorted(ts, t_ein_ns // 1_000_000) - 1        # letzte abgeschlossene Minute vor dem Fill
    idx = [j for j in range(max(0, i - 190), i + 1) if spike[j]]
    if not idx:
        return np.nan, None, None
    gruppe = [idx[-1]]
    for j in reversed(idx[:-1]):
        if gruppe[0] - j <= 5:
            gruppe.insert(0, j)
        else:
            break
    a, b = gruppe[0] - 4, gruppe[-1] + 1
    return L[a:b + 1].sum(), ts[gruppe[0]], ts[gruppe[-1]]

def lade(pfad, teil):
    t = pd.read_csv(pfad)
    t[["L", "spike_erst", "spike_letzt"]] = [kennzahl(x) for x in t.ts_open]
    t["teil"] = teil
    t["zeit_ein"] = pd.to_datetime(t.ts_open, unit="ns")
    return t

def welch(a, b):
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))

t = pd.concat([lade(IS, "IS"), lade(OOS, "OOS")], ignore_index=True)
med = t[t.teil == "IS"].L.median()
zeilen = []
for teil in ["IS", "OOS"]:
    d = t[t.teil == teil]
    for name, ohne, mit in [("L = 0 / L > 0", d.L == 0, d.L > 0), (f"L < Median / L >= Median ({med:.2f} BTC)", d.L < med, d.L >= med)]:
        a, b = d[ohne].r_net, d[mit].r_net
        zeilen.append(dict(teil=teil, aufteilung=name, n_wenig=len(a), r_wenig=a.mean(), tp_wenig=(d[ohne].exit_reason == "tp").mean(),
                           n_viel=len(b), r_viel=b.mean(), tp_viel=(d[mit].exit_reason == "tp").mean(),
                           differenz=b.mean() - a.mean(), t_diff=welch(b, a)))
erg = pd.DataFrame(zeilen)
pd.set_option("display.width", 200)
print("ohne Spike gefunden:", t.L.isna().sum())
print(t.groupby("teil").L.describe().round(2))
print(erg.round(3).to_string(index=False))
# Jahre und Spike-Stärke zur Einordnung (In-Sample)
d = t[t.teil == "IS"].copy(); d["viel"] = d.L >= med; d["jahr"] = d.zeit_ein.dt.year
print(d.pivot_table(index="jahr", columns="viel", values="r_net", aggfunc=["count", "mean"]).round(3))
print("Spike-Stärke im Mittel (wenig/viel):", d.groupby("viel").spike_pct.mean().round(2).to_dict())
print("Korrelation L mit spike_pct:", round(d.L.corr(d.spike_pct), 2), " Rang-Korr L mit r_net:", round(d.L.rank().corr(d.r_net.rank()), 3))
out = ROOT / "runs/20261111-2200_h22_liquidationen"; out.mkdir(exist_ok=True)
t.drop(columns="zeit_ein").to_csv(out / "trades.csv", index=False)
erg.to_csv(out / "ergebnis.csv", index=False)
