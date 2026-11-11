"""Scan für H7c: Regel von H7 auf Tageskerzen, hier auf der längeren BTC-Historie von Yahoo (2015 bis 2022).

Aufruf:  python -m scan.donchian_daily_scan

Die Regel entscheidet nur zum Tageswechsel, innerhalb eines Tages liegt der Stop fest. Deshalb reicht die
Tageskerze: Stop getroffen, wenn das Tagestief ihn erreicht, Fill zum Stop oder bei einer Eröffnung darunter
zum Open. Die Uhrzeit des Ausstiegs ist unbekannt, für das Funding wird die Tagesmitte angesetzt.

Ablauf:
1. Kontrolle: Tagesrechnung auf Kraken-Tageskerzen 2023 bis April 2026 gegen den 1m-Scan von H7
2. Qualitätsprüfung: Yahoo gegen Kraken, gleiche Tage 2023 bis April 2026
3. Haupttest Long N = 10 auf Yahoo 2015 bis 2022, dazu die übrigen Zellen und der Gesamtzeitraum beschreibend
"""
import numpy as np
import pandas as pd

from lab.config import OOS_START, RAW_DIR, TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary
from scan.donchian_scan import RASTER
from scan.donchian_scan import run as run_1m

TAG_MS = 86_400_000


def tageskerzen_kraken(df1m: pd.DataFrame) -> pd.DataFrame:
    g = df1m.assign(tag=df1m.ts_open // TAG_MS * TAG_MS).groupby("tag")
    return g.agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                 close=("close", "last")).reset_index().rename(columns=dict(tag="ts_open"))


def lade_yahoo(start: str, ende: str) -> pd.DataFrame:
    d = pd.read_parquet(RAW_DIR / "BTC-USD_yahoo_1d.parquet")
    lo, hi = (pd.Timestamp(x, tz="UTC").value // 1_000_000 for x in (start, ende))
    if hi > pd.Timestamp(OOS_START, tz="UTC").value // 1_000_000:
        raise ValueError("Zeitraum reicht in die Out-of-Sample-Periode")
    return d[(d.ts_open >= lo) & (d.ts_open < hi)].reset_index(drop=True)


def run(d: pd.DataFrame, seite: str, N: int, tak: float = TAKER_FEE) -> pd.DataFrame:
    s = 1.0 if seite == "long" else -1.0
    o, h, l, c = (s * d[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    if seite == "short":
        h, l = l, h
    ts = d.ts_open.to_numpy(np.int64)
    M, nd = N // 2, len(o)
    rows = []
    t = N
    while t < nd - 1:
        if c[t] > h[t - N:t].max():
            k0 = t + 1
            e, stop = o[k0], l[t - M + 1:t + 1].min()
            if e > stop:
                risk, ex, grund, k = e - stop, None, "sl", k0
                while k < nd:
                    if k > k0:
                        stop = max(stop, l[k - M:k].min())
                    if l[k] <= stop:
                        ex = min(stop, o[k])
                        break
                    k += 1
                if ex is None:
                    k, ex, grund = nd - 1, c[nd - 1], "ende"
                fee = (abs(e) + abs(ex)) * tak
                rows.append(dict(ts_open=int(ts[k0]) * 1_000_000, ts_close=(int(ts[k]) + TAG_MS // 2) * 1_000_000,
                                 side=seite, entry=s * e, exit=s * ex, risk_px=risk, exit_reason=grund,
                                 r_gross=(ex - e) / risk, r_net=(ex - e - fee) / risk,
                                 pct_net=(ex - e - fee) / abs(e) * 100))
                t = k
                continue
        t += 1
    cols = ["ts_open", "ts_close", "side", "entry", "exit", "risk_px", "exit_reason", "r_gross", "r_net", "pct_net"]
    return add_funding(pd.DataFrame(rows, columns=cols))


def kennzahlen(t: pd.DataFrame) -> dict:
    s = summary(t)
    s.pop("tp_quote", None)
    if len(t):
        s.update(treffer=float((t.r_net > 0).mean()), tage=float(((t.ts_close - t.ts_open) / 8.64e13).mean()))
    return s


if __name__ == "__main__":
    pd.set_option("display.width", 260)

    # 1. Kontrolle gegen den 1m-Scan
    df1m = load_1m()
    kd = tageskerzen_kraken(df1m)
    print("1. Kontrolle Tagesrechnung gegen 1m-Scan, Kraken 2023 bis April 2026")
    for seite, N in RASTER:
        a, b = run(kd, seite, N), run_1m(df1m, seite, N)
        m = a.merge(b, on="ts_open", suffixes=("_tag", "_1m"))
        print(f"  {seite:5} N={N:2}: Tage {len(a)}, 1m {len(b)}, gleicher Einstieg {len(m)}, "
              f"max |dR| {np.abs(m.r_net_tag - m.r_net_1m).max():.4f}")

    # 2. Yahoo gegen Kraken
    y = lade_yahoo("2023-01-01", OOS_START)
    m = y.merge(kd, on="ts_open", suffixes=("_y", "_k"))
    print(f"\n2. Yahoo gegen Kraken, {len(m)} gemeinsame Tage, mittlere absolute Abweichung in %:")
    print("  " + ", ".join(f"{c} {((m[c + '_y'] / m[c + '_k'] - 1).abs().mean() * 100):.3f}"
                           for c in ("open", "high", "low", "close")))
    rows = []
    for seite, N in RASTER:
        a, b = run(y, seite, N), run(kd, seite, N)
        rows.append(dict(seite=seite, N=N, n_yahoo=len(a), n_kraken=len(b),
                         r_netto_yahoo=a.r_net.mean(), r_netto_kraken=b.r_net.mean(),
                         gleicher_einstieg=len(a.merge(b, on="ts_open"))))
    print(pd.DataFrame(rows).round(3).to_string(index=False))

    # 3. Haupttest und Beschreibung
    y15 = lade_yahoo("2014-11-01", "2023-01-01")              # Vorlauf für die ersten Signale 2015
    y15_ab = pd.Timestamp("2015-01-01", tz="UTC").value
    print("\n3. Yahoo 2015 bis 2022 (Einstiege ab 2015-01-01), Haupttest ist Long N = 10")
    rows = []
    for seite, N in RASTER:
        t = run(y15, seite, N)
        t = t[t.ts_open >= y15_ab]
        rows.append(dict(seite=seite, N=N, **kennzahlen(t)))
    print(pd.DataFrame(rows).round(3).to_string(index=False))

    print("\nGesamtzeitraum Yahoo 2015 bis April 2026, beschreibend")
    yall = lade_yahoo("2014-11-01", OOS_START)
    rows = []
    for seite, N in RASTER:
        t = run(yall, seite, N)
        t = t[t.ts_open >= y15_ab]
        k = kennzahlen(t)
        rows.append(dict(seite=seite, N=N, **{x: k.get(x) for x in ("n", "r_netto", "t_wert", "r_ohne_top3", "treffer")}))
    print(pd.DataFrame(rows).round(3).to_string(index=False))
