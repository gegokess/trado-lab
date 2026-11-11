"""Scan für H15: SMC-Kette. Sweep eines 1h-Swings auf 15m, MSS auf 5m, Einstieg per Limit in der FVG-Mitte.

Aufruf:  python -m scan.smc_kette_scan                (Füllung nur bei Durchhandeln, Haupttest)
         python -m scan.smc_kette_scan --beruehrung   (Füllung bei Berührung, beschreibend)

Regeln laut Laborbuch, Long beschrieben, Short spiegelbildlich. Swings der 1h- und 5m-Kerzen mit Trados
find_swings (1h k = 5, 5m k = 2), nutzbar erst nach Schluss der k-ten Folgekerze.
"""
import argparse

import numpy as np
import pandas as pd

from lab import trado_features as tf
from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary
from scan.minuten_sim import ausstieg

M5, M15, H1 = 300_000, 900_000, 3_600_000
CRV, SL_PUFFER_ATR, MSS_KERZEN, MSS_ALTER_MS, ORDER_MIN, ZEITSTOPP_MIN = 2.5, 0.1, 12, 4 * H1, 60, 1440
T_GRENZE = 2.24


def swings(bars: pd.DataFrame, k: int, ms: int):
    """(Bestätigungszeit, Preis, Kerzenbeginn) für Hochs und Tiefs."""
    hi, lo = tf.structure.find_swings(bars.high, bars.low, bars.ts, k)
    best = lambda s: int(bars.ts.iloc[s.idx + k]) + ms  # noqa: E731  Schluss der k-ten Folgekerze
    return ([(best(s), s.price, int(s.ts)) for s in hi], [(best(s), s.price, int(s.ts)) for s in lo])


def setups(df: pd.DataFrame, stufen: dict) -> list[dict]:
    b1, b15, b5 = tf.resample(df, H1), tf.resample(df, M15), tf.resample(df, M5)
    atr1 = pd.Series(tf.indicators.atr(b1.high, b1.low, b1.close, 14), index=b1.ts + H1)  # gilt ab Kerzenschluss
    sh1, sl1 = swings(b1, 5, H1)
    sh5, sl5 = swings(b5, 2, M5)
    ts5 = b5.ts.to_numpy()
    out = []
    for s, levels_alle, mss_swings in ((1, sl1, sh5), (-1, sh1, sl5)):
        lv_i, aktiv = 0, np.empty(0)
        mss_t = np.array([x[0] for x in mss_swings])
        t15, lo15, hi15, cl15 = (b15[x].to_numpy() for x in ("ts", "low", "high", "close"))
        for j in range(len(b15)):
            T, Te = int(t15[j]), int(t15[j]) + M15
            neu = []
            while lv_i < len(levels_alle) and levels_alle[lv_i][0] <= T:
                neu.append(levels_alle[lv_i][1])
                lv_i += 1
            if neu:
                aktiv = np.concatenate([aktiv, neu])
            lo, hi, cl = lo15[j], hi15[j], cl15[j]
            if s > 0:
                treffer = lo < aktiv
                sweep = bool((cl > aktiv[treffer]).any())
                extrem = lo
            else:
                treffer = hi > aktiv
                sweep = bool((cl < aktiv[treffer]).any())
                extrem = hi
            if treffer.any():
                aktiv = aktiv[~treffer]
            if not sweep:
                continue
            stufen["sweep"] += 1
            # MSS-Level: jüngster bestätigter 5m-Swing in Gegenrichtung, höchstens 4 h alt
            k = np.searchsorted(mss_t, Te, side="right") - 1
            if k < 0 or mss_swings[k][2] < Te - MSS_ALTER_MS:
                continue
            mss_lvl = mss_swings[k][1]
            b = np.searchsorted(ts5, Te)
            mss_b = None
            for bi in range(b, min(b + MSS_KERZEN, len(b5))):
                if (s > 0 and b5.low.iloc[bi] < extrem) or (s < 0 and b5.high.iloc[bi] > extrem):
                    break
                if (s > 0 and b5.close.iloc[bi] > mss_lvl) or (s < 0 and b5.close.iloc[bi] < mss_lvl):
                    mss_b = bi
                    break
            if mss_b is None:
                continue
            stufen["mss"] += 1
            # FVG zwischen Sweep und MSS
            start = np.searchsorted(ts5, T)
            fvg = None
            for i in range(max(start, 2), mss_b + 1):
                if s > 0 and b5.low.iloc[i] > b5.high.iloc[i - 2]:
                    fvg = (b5.high.iloc[i - 2], b5.low.iloc[i])
                if s < 0 and b5.high.iloc[i] < b5.low.iloc[i - 2]:
                    fvg = (b5.high.iloc[i], b5.low.iloc[i - 2])
            if fvg is None:
                continue
            stufen["fvg"] += 1
            e = (fvg[0] + fvg[1]) / 2
            atr = atr1[atr1.index <= Te].iloc[-1] if (atr1.index <= Te).any() else np.nan
            sl = extrem - s * SL_PUFFER_ATR * atr
            schluss = b5.close.iloc[mss_b]
            if np.isnan(atr) or s * (schluss - e) <= 0 or s * (e - sl) <= 0:
                continue
            out.append(dict(s=s, t_order=int(ts5[mss_b]) + M5, e=e, sl=sl, tp=e + s * CRV * abs(e - sl),
                            extrem=extrem))
    return sorted(out, key=lambda x: x["t_order"])


def simulieren(df: pd.DataFrame, liste: list[dict], beruehrung: bool) -> pd.DataFrame:
    ts = df.ts_open.to_numpy(np.int64)
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    t0, frei_ab, rows = ts[0], 0, []
    for z in liste:
        m0 = int((z["t_order"] - t0) // 60_000)
        if m0 < frei_ab or m0 + ORDER_MIN + ZEITSTOPP_MIN >= len(o):
            continue
        s, e = z["s"], z["e"]
        for m in range(m0, m0 + ORDER_MIN):
            if s > 0:
                if l[m] < e or (beruehrung and l[m] <= e):
                    break
            elif h[m] > e or (beruehrung and h[m] >= e):
                break
        else:
            continue
        xi, x, art = ausstieg(o, h, l, c, m, s, z["sl"], z["tp"], m + ZEITSTOPP_MIN)
        rows.append(dict(i=m, xi=xi, s=s, e=e, x=x, art=art, sl=z["sl"], tp=z["tp"]))
        frei_ab = xi + 1
    return pd.DataFrame(rows)


def trades(r: pd.DataFrame, ts) -> pd.DataFrame:
    risk = (r.e - r.sl).abs()
    brutto = r.s * (r.x - r.e)
    fee = r.e * MAKER_FEE + r.x * np.where(r.art == 1, MAKER_FEE, TAKER_FEE)
    t = pd.DataFrame(dict(ts_open=ts[r.i] * 1_000_000, ts_close=(ts[r.xi] + 60_000) * 1_000_000,
                          side=np.where(r.s > 0, "long", "short"), entry=r.e, exit=r.x, risk_px=risk,
                          exit_reason=np.where(r.art == 1, "tp", np.where(r.art == -1, "sl", "zeit")),
                          r_gross=brutto / risk, r_net=(brutto - fee) / risk, pct_net=(brutto - fee) / r.e * 100))
    return add_funding(t)


def zufall(df: pd.DataFrame, r: pd.DataFrame, rng) -> float:
    o, h, l, c = (df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    rows = []
    for z in r.itertuples():
        s = rng.choice([-1, 1])
        d = abs(z.e - z.sl)
        sl, tp = z.e - s * d, z.e + s * CRV * d
        xi, x, art = ausstieg(o, h, l, c, z.i, s, sl, tp, z.i + ZEITSTOPP_MIN)
        rows.append(dict(i=z.i, xi=xi, s=s, e=z.e, x=x, art=art, sl=sl, tp=tp))
    return trades(pd.DataFrame(rows), df.ts_open.to_numpy(np.int64)).r_net.mean()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--beruehrung", action="store_true")
    a = ap.parse_args()
    pd.set_option("display.width", 250)
    df = load_1m()
    ts = df.ts_open.to_numpy(np.int64)
    stufen = dict(sweep=0, mss=0, fvg=0)
    liste = setups(df, stufen)
    r = simulieren(df, liste, a.beruehrung)
    t = trades(r, ts)
    print(f"H15 SMC-Kette, Füllung {'Berührung' if a.beruehrung else 'Durchhandeln (Haupttest)'}")
    print(f"Stufen: Sweeps {stufen['sweep']}, davon MSS {stufen['mss']}, davon mit FVG {stufen['fvg']}, "
          f"gültige Orders {len(liste)}, gefüllte Trades {len(t)}")
    k = summary(t)
    k.update(long_anteil=float((t.side == "long").mean()), h_mittel=float(((t.ts_close - t.ts_open) / 3.6e12).mean()),
             risiko_bps=float((t.risk_px / t.entry).median() * 1e4))
    print(pd.DataFrame([k]).round(3).to_string(index=False))
    for seite in ("long", "short"):
        g = t[t.side == seite]
        print(f"  {seite}: n {len(g)}, R netto {g.r_net.mean():.3f}, TP-Quote {(g.exit_reason == 'tp').mean():.3f}")
    if not a.beruehrung:
        rng = np.random.default_rng(42)
        werte = np.array([zufall(df, r, rng) for _ in range(1000)])
        print(f"Zufallsrichtung, 1.000 Läufe: Mittel R netto {werte.mean():.4f}, 95-%-Quantil {np.quantile(werte, 0.95):.4f}, "
              f"H15 {t.r_net.mean():.4f}, Anteil Läufe ≥ H15 {(werte >= t.r_net.mean()).mean():.3f}")
