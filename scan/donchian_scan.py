"""Scan für H7 (Donchian-Ausbruch auf Tageskerzen), gepoolt über BTC, ETH und SOL.

Aufruf:  python -m scan.donchian_scan        (In-Sample bis OOS_START)

Regel laut Laborbuch, Long beschrieben, Short im gespiegelten Raum (Preise negiert, Hoch und Tief getauscht):
- Tageskerzen UTC aus dem 1m-Archiv
- Signal: Schluss von Tag d über dem höchsten Hoch der N Tage vor d
- Einstieg per Market zum Open von Tag d + 1 (Taker)
- Anfangs-SL am tiefsten Tief der M = N / 2 Tage vor dem Einstieg (Tage d − M + 1 bis d), R = Einstieg − SL
- der Stop wird zu jedem Tagesbeginn auf das Tief der letzten M abgeschlossenen Tage nachgezogen, nie zurück
- Ausstieg nur über den Stop (Stop-Market, Taker), Fill zum Stop oder bei einer Lücke zum Minuten-Open
- keine neue Position, solange eine offen ist. Funding als fester Satz über lab.report.add_funding

Annahmen gegenüber Nautilus:
- der Stop gilt schon in der Einstiegsminute
- eine am Ende des In-Sample-Zeitraums noch offene Position wird zum letzten Schluss bewertet (Grund "ende")
- Gebühren auf Basis der Fill-Preise, ohne Slippage
"""
import itertools

import numpy as np
import pandas as pd
from numba import njit

from lab.config import TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary

TAG = 1440
MAERKTE = ["PF_XBTUSD", "PF_ETHUSD", "PF_SOLUSD"]
RASTER = list(itertools.product(["long", "short"], [10, 20, 30]))


@njit(cache=True)
def _sim(o, l, c, dh, dl, dc, N, M, tak):
    nd = len(dh)
    out = np.full((2000, 6), np.nan)
    m = 0
    d = N
    while d < nd - 1:
        # Signal am Schluss von Tag d
        if dc[d] > dh[d - N:d].max():
            e_tag = d + 1
            i0 = e_tag * TAG
            e = o[i0]
            stop = dl[d - M + 1:d + 1].min()
            if e > stop:
                risk = e - stop
                ex = np.nan
                typ = 0
                i = i0
                n = len(o)
                while i < n:
                    if i % TAG == 0 and i > i0:
                        k = i // TAG
                        stop = max(stop, dl[k - M:k].min())
                    if l[i] <= stop:
                        ex = min(stop, o[i]); typ = -1
                        break
                    i += 1
                if np.isnan(ex):                    # Ende des Datensatzes
                    i = n - 1
                    ex = c[i]; typ = 0
                fee = (abs(e) + abs(ex)) * tak
                out[m, 0] = i0; out[m, 1] = i; out[m, 2] = typ
                out[m, 3] = e; out[m, 4] = ex; out[m, 5] = risk
                m += 1
                d = i // TAG                        # nächstes Signal frühestens am Schluss des Ausstiegstags
                continue
        d += 1
    return out[:m]


def run(df: pd.DataFrame, seite: str, N: int, tak: float = TAKER_FEE) -> pd.DataFrame:
    ts = df.ts_open.to_numpy(np.int64)
    if len(ts) % TAG or ts[0] % 86_400_000 or (np.diff(ts) != 60_000).any():
        raise ValueError("Archiv nicht lückenlos oder nicht an UTC-Tagen ausgerichtet")
    s = 1.0 if seite == "long" else -1.0
    o, h, l, c = (s * df[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    if seite == "short":
        h, l = l, h
    nd = len(o) // TAG
    dh, dl, dc = h.reshape(nd, TAG).max(1), l.reshape(nd, TAG).min(1), c.reshape(nd, TAG)[:, -1]
    r = _sim(o, l, c, dh, dl, dc, N, N // 2, tak)
    ei, xi = r[:, 0].astype(int), r[:, 1].astype(int)
    e, ex, risk = r[:, 3], r[:, 4], r[:, 5]
    fee = (np.abs(e) + np.abs(ex)) * tak
    t = pd.DataFrame(dict(
        ts_open=ts[ei] * 1_000_000, ts_close=(ts[xi] + 60_000) * 1_000_000, side=seite,
        entry=s * e, exit=s * ex, risk_px=risk,
        exit_reason=np.where(r[:, 2] == -1, "sl", "ende"),
        r_gross=(ex - e) / risk, r_net=(ex - e - fee) / risk, pct_net=(ex - e - fee) / np.abs(e) * 100))
    return add_funding(t)


if __name__ == "__main__":
    pd.set_option("display.width", 260)
    daten = {sym: load_1m(symbol=sym) for sym in MAERKTE}
    rows, einzel = [], []
    for seite, N in RASTER:
        alle = []
        for sym, df in daten.items():
            t = run(df, seite, N).assign(sym=sym)
            alle.append(t)
            s = summary(t)
            einzel.append(dict(seite=seite, N=N, sym=sym, n=s.get("n"), r_brutto=s.get("r_brutto"),
                               r_netto=s.get("r_netto"), t_wert=s.get("t_wert"), r_ohne_top3=s.get("r_ohne_top3"),
                               trefferquote=float((t.r_net > 0).mean()) if len(t) else np.nan,
                               tage=float(((t.ts_close - t.ts_open) / 8.64e13).mean()) if len(t) else np.nan,
                               r_funding=s.get("r_funding")))
        p = pd.concat(alle)
        rows.append(dict(seite=seite, N=N, trefferquote=float((p.r_net > 0).mean()),
                         tage=float(((p.ts_close - p.ts_open) / 8.64e13).mean()), **summary(p)))
    print("H7 gepoolt über", ", ".join(MAERKTE), "(In-Sample)")
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print("\nje Markt")
    print(pd.DataFrame(einzel).round(3).to_string(index=False))
