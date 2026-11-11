"""Scan für H6 (Fib-Pullback im Trend), Struktur-Features exakt wie Trado (lab/trado_features.py).

Aufruf:  python -m scan.fib_pullback_scan                    (BTC, In-Sample bis OOS_START, volles Raster)
         python -m scan.fib_pullback_scan --symbol PF_ETHUSD (Gegenprobe auf einem anderen Markt)

Regel laut Laborbuch, Long beschrieben, Short im gespiegelten Raum (Preise negiert):
- Stunde t nutzt die Features, die Trado zum Zeitpunkt t sieht: trend_4h aufwärts, Fib-Impuls aufwärts und valid
- Einstieg Limit (Maker) am Fib-Level q. Die Order liegt in Minute i nur, wenn der Schluss der Vorminute
  über dem Level und höchstens 1 ATR (1h, Trado-Definition) darüber liegt. Sonst gilt sie als gelöscht
- SL Stop-Market bei Ursprung − 0,25 ATR (Taker), TP Limit am Extrem oder an der Extension −0,27 (Maker)
- CRV-Filter mit Trados Formel (rr_net_of_fees, 2 bps Slippage auf den SL): mindestens 1,5, sonst keine Order
- ein Trade je Impuls, nur eine Position zur Zeit, Zeitstopp 72 h zum Minutenschluss (Taker)
- Funding als fester Satz über lab.report.add_funding

Annahmen gegenüber Nautilus:
- die Limit-Order füllt genau auf ihrem Level, eine Lücke darunter bringt keinen besseren Preis
- liegt in der Füllminute auch der SL, zählt der Trade als SL (konservativ), TP erst ab der Folgeminute
- SL vor TP, wenn beide in derselben Minute liegen
- Gebühren auf Basis der Fill-Preise, ohne Slippage (wie alle bisherigen Scans)
"""
import argparse
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab import trado_features as tf
from lab.config import MAKER_FEE, SYMBOL, TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary

SL_PUFFER_ATR = 0.25
ZEITSTOPP_MIN = 72 * 60
MIN_RR = 1.5
SLIPPAGE = 0.0002          # Trado fees.slippage_bps = 2, nur für den CRV-Filter


def stundenplan(f: pd.DataFrame, seite: str, q: str, tp_modus: str) -> pd.DataFrame:
    """Je Stunde Level, SL, TP, ATR und Impuls-Kennung im gespiegelten Raum, nan wenn kein Setup."""
    up = seite == "long"
    s = 1.0 if up else -1.0
    ok = (f.trend_4h == ("aufwärts" if up else "abwärts")) & (f.fib_dir == ("up" if up else "down")) & \
        (f.valid == True)  # noqa: E712
    origin, extreme, atr = s * f.origin, s * f.extreme, f.atr
    rng = extreme - origin
    lvl = s * f[f"l{q}"]
    sl = origin - SL_PUFFER_ATR * atr
    tp = extreme if tp_modus == "extrem" else extreme + 0.27 * rng
    # Trados CRV netto, mit echten (positiven) Preisen für die Gebühren
    c_in = (lvl * s) * MAKER_FEE
    c_sl = (sl * s) * (TAKER_FEE + SLIPPAGE)
    c_tp = (tp * s) * MAKER_FEE
    rr = (tp - lvl - c_in - c_tp) / (lvl - sl + c_in + c_sl)
    ok &= (rr >= MIN_RR) & (lvl > sl)
    imp = pd.factorize(f.origin_ts.astype(str) + "_" + f.extreme_ts.astype(str))[0]
    idm = np.where(f.idm_status == "gesweept", 1, np.where(f.idm_status == "offen", 0, -1))
    return pd.DataFrame(dict(stunde=f.ts // tf.H1, ok=ok.to_numpy(), lvl=lvl, sl=sl, tp=tp, atr=atr,
                             imp=imp, idm=idm, rr=rr))


@njit(cache=True)
def _sim(o, h, l, c, hid, h0, ok, lvl, sl, tp, atr, imp, mak, tak, absp, hold):
    n = len(o)
    out = np.full((20000, 8), np.nan)
    m = 0
    inpos = False
    e = s_ = t_ = 0.0
    ei = dl = 0
    benutzt = np.zeros(imp.max() + 2, np.bool_)
    for i in range(1, n):
        if inpos:
            ex = np.nan
            typ = 0
            if l[i] <= s_:
                ex = min(s_, o[i]); typ = -1
            elif i > ei and h[i] >= t_:
                ex = t_; typ = 1
            elif i >= dl:
                ex = c[i]; typ = 0
            if not np.isnan(ex):
                fee = abs(e) * mak + abs(ex) * (mak if typ == 1 else tak)
                risk = e - s_
                out[m, 0] = ei; out[m, 1] = i; out[m, 2] = typ
                out[m, 3] = (ex - e) / risk; out[m, 4] = (ex - e - fee) / risk
                out[m, 5] = e; out[m, 6] = ex; out[m, 7] = risk
                m += 1
                inpos = False
            continue
        k = hid[i] - h0
        if k < 0 or k >= len(ok) or not ok[k] or benutzt[imp[k]]:
            continue
        L = lvl[k]
        if c[i - 1] > L and c[i - 1] - L <= atr[k] and l[i] <= L:
            e = L; s_ = sl[k]; t_ = tp[k]
            inpos = True; ei = i; dl = i + hold
            benutzt[imp[k]] = True
            if l[i] <= s_:                            # SL schon in der Füllminute: konservativ als Verlust
                fee = abs(e) * mak + abs(s_) * tak
                risk = e - s_
                out[m, 0] = i; out[m, 1] = i; out[m, 2] = -1
                out[m, 3] = -1.0; out[m, 4] = (s_ - e - fee) / risk
                out[m, 5] = e; out[m, 6] = s_; out[m, 7] = risk
                m += 1
                inpos = False
    return out[:m]


def run(df: pd.DataFrame, f: pd.DataFrame, seite: str, q: str, tp_modus: str) -> pd.DataFrame:
    ts = df.ts_open.to_numpy(np.int64)
    s = 1.0 if seite == "long" else -1.0
    o, h, l, c = (s * df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    if seite == "short":
        h, l = l, h                                   # gespiegelt: Hoch und Tief tauschen
    plan = stundenplan(f, seite, q, tp_modus)
    h0 = int(plan.stunde.iloc[0])
    voll = pd.DataFrame(dict(stunde=np.arange(h0, int(plan.stunde.iloc[-1]) + 1))).merge(plan, how="left")
    voll["ok"] = voll.ok.fillna(False).astype(bool)
    voll = voll.fillna(dict(imp=-1, idm=-1))
    imp = voll.imp.to_numpy(np.int64)
    imp = np.where(imp < 0, imp.max() + 1, imp)
    r = _sim(o, h, l, c, ts // tf.H1, h0, voll.ok.to_numpy(), voll.lvl.to_numpy(float), voll.sl.to_numpy(float),
             voll.tp.to_numpy(float), voll.atr.to_numpy(float), imp, MAKER_FEE, TAKER_FEE,
             df.open.to_numpy(float), ZEITSTOPP_MIN)
    ei, xi = r[:, 0].astype(int), r[:, 1].astype(int)
    idm = voll.idm.to_numpy()[ts[ei] // tf.H1 - h0]
    t = pd.DataFrame(dict(
        ts_open=ts[ei] * 1_000_000, ts_close=(ts[xi] + 60_000) * 1_000_000, side=seite,
        entry=s * r[:, 5], exit=s * r[:, 6], risk_px=r[:, 7],
        exit_reason=np.where(r[:, 2] == 1, "tp", np.where(r[:, 2] == -1, "sl", "zeit")),
        r_gross=r[:, 3], r_net=r[:, 4], pct_net=r[:, 4] * r[:, 7] / np.abs(r[:, 5]) * 100,
        idm=np.where(idm == 1, "gesweept", np.where(idm == 0, "offen", "keins"))))
    return add_funding(t)


RASTER = list(itertools.product(["long", "short"], ["0.618", "0.786", "0.882"], ["extrem", "ext027"]))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--symbol", default=SYMBOL)
    a = ap.parse_args()
    df = load_1m(symbol=a.symbol)
    f = tf.load(a.symbol, df)
    pd.set_option("display.width", 260)
    rows, teile = [], []
    for seite, q, tpm in RASTER:
        t = run(df, f, seite, q, tpm)
        rows.append(dict(seite=seite, q=q, tp=tpm, h_mittel=round(((t.ts_close - t.ts_open) / 3.6e12).mean(), 1)
                         if len(t) else np.nan, **summary(t)))
        for name, g in t.groupby("idm"):
            teile.append(dict(seite=seite, q=q, tp=tpm, idm=name, n=len(g), r_brutto=g.r_gross.mean(),
                              r_netto=g.r_net.mean()))
    print(f"H6 Scan {a.symbol}, In-Sample")
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print("\nAufteilung nach Inducement beim Einstieg (beschreibend)")
    print(pd.DataFrame(teile).round(3).to_string(index=False))
