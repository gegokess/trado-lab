"""H28: Trendfilter rückwirkend auf alle vorhandenen Trade-Listen (LABORBUCH.md).

Aufruf:  python -m scan.h28_trendfilter

Jeder Trade bekommt den 4h-Trend beim Einstieg nach T1 (EMA wie Trado) und T2 (Marktstruktur).
Ausgabe je Lauf: R aller Trades, mit dem Trend, gegen den Trend, gemischt. Ergebnis in runs/<zeit>_h28_trendfilter.
"""
import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from lab.config import OOS_START, RAW_DIR, RUNS_DIR

H4 = 14_400_000
SWING_K = 5
MIN_TRADES = 30
AUSGESCHLOSSEN = ("_OOS", "h22_liquidationen", "h28_trendfilter")


def kerzen_4h(symbol: str) -> pd.DataFrame:
    df = pd.read_parquet(RAW_DIR / f"{symbol}_1m.parquet")
    df["ts"] = df.ts_open // H4 * H4
    return df.groupby("ts").agg(high=("high", "max"), low=("low", "min"), close=("close", "last")).reset_index()


def trend_reihen(h4: pd.DataFrame) -> pd.DataFrame:
    """Trend je 4h-Kerze, gültig ab ihrem Schluss (ts + 4h)."""
    c = h4.close
    e20, e50 = c.ewm(span=20, adjust=False).mean(), c.ewm(span=50, adjust=False).mean()
    t1 = np.where((e20 > e50) & (c > e50), 1, np.where((e20 < e50) & (c < e50), -1, 0))
    t1[:50] = 0
    # Swings k = 5, bekannt erst nach Schluss der k-ten Kerze danach
    hi, lo, n, k = h4.high.to_numpy(), h4.low.to_numpy(), len(h4), SWING_K
    t2 = np.zeros(n, dtype=int)
    sh, sl = [], []                                   # bekannte Swing-Hochs und -Tiefs (Preis)
    for i in range(n):
        j = i - k                                     # Kandidat, der mit Kerze i bestätigt wird
        if j >= k:
            fenster_h, fenster_l = hi[j - k:i + 1], lo[j - k:i + 1]
            if hi[j] == fenster_h.max() and (fenster_h == hi[j]).sum() == 1:
                sh.append(hi[j])
            if lo[j] == fenster_l.min() and (fenster_l == lo[j]).sum() == 1:
                sl.append(lo[j])
        if len(sh) >= 2 and len(sl) >= 2:
            if sh[-1] > sh[-2] and sl[-1] > sl[-2]:
                t2[i] = 1
            elif sh[-1] < sh[-2] and sl[-1] < sl[-2]:
                t2[i] = -1
    return pd.DataFrame({"gueltig_ab": h4.ts + H4, "t1": t1, "t2": t2})


def laeufe() -> list[tuple[str, str, pd.DataFrame]]:
    """(Name, Symbol, Trades) je Lauf, das H20-Raster je Zelle aufgeteilt."""
    out = []
    for d in sorted(RUNS_DIR.iterdir()):
        f = d / "trades.csv"
        if not f.exists() or any(x in d.name for x in AUSGESCHLOSSEN):
            continue
        t = pd.read_csv(f)
        if "symbol" in t and t.symbol.nunique() > 1 or "stop" in t:
            for keys, g in t.groupby([c for c in ("symbol", "stop", "ausstieg", "seite") if c in t]):
                out.append((f"{d.name} | {' / '.join(map(str, keys))}", g.symbol.iloc[0], g))
            continue
        meta = d / "ergebnis.json"
        sym = json.loads(meta.read_text()).get("meta", {}).get("symbol") if meta.exists() else None
        sym = sym or next((s for s in ("PF_ETHUSD", "PF_SOLUSD", "PF_XRPUSD") if s in d.name), "PF_XBTUSD")
        out.append((d.name, sym, t))
    return out


def welch(a: pd.Series, b: pd.Series) -> float:
    if len(a) < 2 or len(b) < 2:
        return np.nan
    return (a.mean() - b.mean()) / np.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))


def main() -> None:
    grenze = pd.Timestamp(OOS_START, tz="UTC").value
    trends = {}
    zeilen = []
    for name, sym, t in laeufe():
        t = t[t.ts_open < grenze].copy()
        if len(t) < MIN_TRADES:
            continue
        if sym not in trends:
            trends[sym] = trend_reihen(kerzen_4h(sym))
        tr = trends[sym]
        ein_ms = (t.ts_open // 1_000_000).to_numpy()
        idx = np.searchsorted(tr.gueltig_ab.to_numpy(), ein_ms, side="right") - 1
        richtung = np.where(t.side == "long", 1, -1)
        for td in ("t1", "t2"):
            tw = np.where(idx >= 0, tr[td].to_numpy()[np.clip(idx, 0, None)], 0)
            mit, gegen, gem = (tw * richtung == 1), (tw * richtung == -1), tw == 0
            r = t.r_net
            zeilen.append(dict(lauf=name, symbol=sym, trend=td, n=len(t), r_alle=r.mean(),
                               n_mit=mit.sum(), r_mit=r[mit].mean(), n_gegen=gegen.sum(), r_gegen=r[gegen].mean(),
                               n_gemischt=gem.sum(), r_gemischt=r[gem].mean(),
                               diff_mit_gegen=r[mit].mean() - r[gegen].mean(), t_diff=welch(r[mit], r[gegen])))
    e = pd.DataFrame(zeilen)
    pd.set_option("display.width", 250, "display.max_colwidth", 70, "display.max_rows", 200)
    for td in ("t1", "t2"):
        d = e[e.trend == td]
        besser = (d.r_mit > d.r_alle).mean()
        print(f"\n{td}: {len(d)} Läufe, mit Trend besser als alle in {besser:.0%}, "
              f"Median Differenz mit gegen gegen {d.diff_mit_gegen.median():+.3f} R, "
              f"Anteil Trades mit Trend {d.n_mit.sum() / d.n.sum():.0%}")
        print(d.drop(columns=["trend"]).round(3).to_string(index=False))
    out = RUNS_DIR / (datetime.now(timezone.utc).strftime("%Y%m%d-%H%M") + "_h28_trendfilter")
    out.mkdir(exist_ok=True)
    e.to_csv(out / "ergebnis.csv", index=False)
    print(f"\nGespeichert: {out}")


if __name__ == "__main__":
    main()
