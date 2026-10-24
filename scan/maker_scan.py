"""Scan für H10: die kleinen Brutto-Effekte aus H8 und H9 mit Limit-Orders (Maker) statt Market.

Aufruf:  python -m scan.maker_scan        (In-Sample bis OOS_START)

Füllmodell: Eine Limit-Order füllt nur, wenn eine Minute den Preis echt durchhandelt (Kauf: Tief < Limit,
Verkauf: Hoch > Limit). Mit --beruehrung reicht Berührung (optimistische Obergrenze, nur beschreibend).
Liegen Stop und Limit-Ausstieg in derselben Minute, zählt der Stop. Gebühren auf die Fill-Preise.

H10a: Kauf-Limit zum Open 21:00 UTC, gültig 60 min, Not-SL 1,5 ATR, Verkauf-Limit zum Open 23:00, gültig 30 min,
      danach Market. R = 1,5 ATR
H10b: Richtung gegen die Rendite 21:00 bis 21:30, Limit zum Open 21:30, gültig 15 min, Schließen per Limit zum
      Open 22:00, gültig 15 min, danach Market. Kein Stop, R = ATR
"""
import argparse

import numpy as np
import pandas as pd

from lab.config import MAKER_FEE, TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary
from scan.liquidity_sweep_scan import atr14, hourly

TAG = 1440


def tagesergebnis(o, h, l, atr_tag, seite: int, ein_m: int, ein_fenster: int, aus_m: int, aus_fenster: int,
                  sl_atr: float | None, beruehrung: bool) -> pd.DataFrame:
    """Je Tag das Ergebnis einer Seite (+1 Long, −1 Short) mit Limit-Ein- und -Ausstieg."""
    nd = len(o) // TAG
    rows = []
    for d in range(nd):
        i0, x0 = d * TAG + ein_m, d * TAG + aus_m
        if x0 + aus_fenster >= len(o) or np.isnan(atr_tag[d]):
            rows.append(dict(gefuellt=False))
            continue
        L = o[i0]
        # Füllung des Einstiegs
        f = None
        for j in range(i0, i0 + ein_fenster):
            durch = (l[j] < L or (beruehrung and l[j] <= L)) if seite > 0 else (h[j] > L or (beruehrung and h[j] >= L))
            if durch:
                f = j
                break
        if f is None:
            rows.append(dict(gefuellt=False, markt=seite * (o[x0] - o[i0])))
            continue
        sl = None if sl_atr is None else L - seite * sl_atr * atr_tag[d]
        ex, art, k = None, None, f
        # bis zum Beginn des Ausstiegsfensters nur der Stop
        while k < x0 + aus_fenster:
            if sl is not None and ((seite > 0 and l[k] <= sl) or (seite < 0 and h[k] >= sl)):
                ex = sl if k == f else (min(sl, o[k]) if seite > 0 else max(sl, o[k]))
                art = "sl"
                break
            if k >= x0:
                X = o[x0]
                if (seite > 0 and (h[k] > X or (beruehrung and h[k] >= X))) or \
                   (seite < 0 and (l[k] < X or (beruehrung and l[k] <= X))):
                    ex, art = X, "limit"
                    break
            k += 1
        if ex is None:
            k, ex, art = x0 + aus_fenster, o[x0 + aus_fenster], "markt"
        fee = L * MAKER_FEE + ex * (MAKER_FEE if art == "limit" else TAKER_FEE)
        rows.append(dict(gefuellt=True, e=L, x=ex, art=art, fi=f, xi=k, brutto=seite * (ex - L), fee=fee,
                         markt=seite * (o[x0] - o[i0])))
    return pd.DataFrame(rows)


def trades(r: pd.DataFrame, ts, seite_vec, risk_tag) -> pd.DataFrame:
    m = r.gefuellt.to_numpy(bool)
    r = r[m]
    s = np.asarray(seite_vec)[m]
    risk = np.asarray(risk_tag)[m]
    t = pd.DataFrame(dict(ts_open=ts[r.fi.astype(int)] * 1_000_000, ts_close=(ts[r.xi.astype(int)] + 60_000) * 1_000_000,
                          side=np.where(s > 0, "long", "short"), entry=r.e, exit=r.x, risk_px=risk,
                          exit_reason=np.where(r.art == "limit", "tp", np.where(r.art == "sl", "sl", "zeit")),
                          r_gross=r.brutto / risk, r_net=(r.brutto - r.fee) / risk,
                          pct_net=(r.brutto - r.fee) / r.e * 100, bps_brutto=r.brutto / r.e * 1e4))
    t = add_funding(t)
    t["bps_netto"] = t.pct_net * 100
    return t.reset_index(drop=True)


def kennzahlen(t: pd.DataFrame, n_tage: int) -> dict:
    s = summary(t)
    s.pop("tp_quote", None)
    s.update(fuellquote=len(t) / n_tage, limit_ausstieg=float((t.exit_reason == "tp").mean()),
             sl_quote=float((t.exit_reason == "sl").mean()),
             bps_brutto=float(t.bps_brutto.mean()), bps_netto=float(t.bps_netto.mean()),
             t_bps=float(t.bps_netto.mean() / (t.bps_netto.std(ddof=1) / np.sqrt(len(t)))))
    return s


def mischen(a: pd.DataFrame, b: pd.DataFrame, s: np.ndarray) -> pd.DataFrame:
    """Je Tag Ergebnis a (Long) oder b (Short) nach Richtung s."""
    cols = a.columns.union(b.columns)
    a, b = a.reindex(columns=cols), b.reindex(columns=cols)
    out = b.copy()
    out.loc[s > 0] = a.loc[s > 0]
    out["gefuellt"] = out.gefuellt.fillna(False).astype(bool)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--beruehrung", action="store_true", help="Füllung schon bei Berührung (optimistisch)")
    a = ap.parse_args()
    pd.set_option("display.width", 260)
    df = load_1m()
    ts = df.ts_open.to_numpy(np.int64)
    if ts[0] % 86_400_000 or len(ts) % TAG or (np.diff(ts) != 60_000).any():
        raise ValueError("Archiv nicht lückenlos oder nicht tagesweise ausgerichtet")
    o, h, l = (df[x].to_numpy(float) for x in ("open", "high", "low"))
    hs, _ = hourly(ts, o, h, l, df.close.to_numpy(float))
    atr = atr14(hs)
    nd = len(o) // TAG
    stunde = lambda m: (ts[np.arange(nd) * TAG + m]) // 3_600_000  # noqa: E731
    modus = "Berührung (optimistisch)" if a.beruehrung else "Durchhandeln (Haupttest)"

    # H10a
    atr_a = atr.reindex(stunde(21 * 60)).to_numpy()
    ra = tagesergebnis(o, h, l, atr_a, +1, 21 * 60, 60, 23 * 60, 30, 1.5, a.beruehrung)
    ta = trades(ra, ts, np.ones(nd), 1.5 * atr_a)
    print(f"H10a Long 21 bis 23 UTC mit Limit-Orders, Füllung {modus}")
    print(pd.DataFrame([kennzahlen(ta, nd)]).round(3).to_string(index=False))
    m = ra.gefuellt.to_numpy(bool)
    mk = ra.markt / o[np.arange(nd) * TAG + 21 * 60] * 1e4
    print(f"  Market-Variante brutto an gefüllten Tagen {mk[m].mean():.2f} bps, an nicht gefüllten {mk[~m].mean():.2f} bps")

    # H10b
    atr_b = atr.reindex(stunde(21 * 60 + 30)).to_numpy()
    rich = np.where(o[np.arange(nd) * TAG + 21 * 60 + 30] < o[np.arange(nd) * TAG + 21 * 60], 1, -1)
    rl = tagesergebnis(o, h, l, atr_b, +1, 21 * 60 + 30, 15, 22 * 60, 15, None, a.beruehrung)
    rs = tagesergebnis(o, h, l, atr_b, -1, 21 * 60 + 30, 15, 22 * 60, 15, None, a.beruehrung)
    rb = mischen(rl, rs, rich)
    tb = trades(rb, ts, rich, atr_b)
    print(f"\nH10b Umkehr der vorletzten halben Stunde mit Limit-Orders, Füllung {modus}")
    print(pd.DataFrame([kennzahlen(tb, nd)]).round(3).to_string(index=False))
    m = rb.gefuellt.to_numpy(bool)
    mk = rb.markt / o[np.arange(nd) * TAG + 21 * 60 + 30] * 1e4
    print(f"  Market-Variante brutto an gefüllten Tagen {mk[m].mean():.2f} bps, an nicht gefüllten {mk[~m].mean():.2f} bps")

    rng = np.random.default_rng(42)
    werte = np.array([trades(mischen(rl, rs, z := rng.choice([-1, 1], nd)), ts, z, atr_b).r_net.mean()
                      for _ in range(1000)])
    print(f"  Zufallsrichtung, 1.000 Läufe: Mittel R netto {werte.mean():.4f}, 95-%-Quantil {np.quantile(werte, 0.95):.4f}, "
          f"H10b {tb.r_net.mean():.4f}, Anteil Läufe ≥ H10b {(werte >= tb.r_net.mean()).mean():.3f}")
