"""Scan für H9 (Intraday-Momentum am Ende der US-Sitzung, nach Shen, Urquhart und Wang 2022).

Aufruf:  python -m scan.intraday_momentum_scan        (In-Sample bis OOS_START)

Regeln laut Laborbuch, Zeiten fest in EST = UTC − 5 (Hauptvariante) oder New Yorker Ortszeit (beschreibend):
- r_ONFH = Open(Öffnung + 30 min) / Open(Schluss des Vortags) − 1, Öffnung 9:15, Schluss 17:00
- r_SLH  = Open(16:30) / Open(16:00) − 1
- Einstieg Market zum Open der Minute 16:30, Ausstieg Market zum Open der Minute 17:00, beide Taker
- Signal A: Long bei r_ONFH > 0, sonst Short. Signal B: Long bei r_SLH < 0, sonst Short
- Signal C: Long bei r_ONFH > 0 und r_SLH < 0, Short bei r_ONFH ≤ 0 und r_SLH ≥ 0, sonst kein Trade
- R = ATR14 der abgeschlossenen 1h-Kerzen zum Einstieg (nur Normierung, kein Stop)
"""
import numpy as np
import pandas as pd

from lab.config import TAKER_FEE
from lab.data import load_1m
from lab.report import add_funding, summary
from scan.liquidity_sweep_scan import atr14, hourly

MIN_MS = 60_000


def tage(df: pd.DataFrame, zeitzone: str | None) -> pd.DataFrame:
    """Je Handelstag die benötigten Preise. zeitzone=None heißt fest UTC − 5 wie in der Studie."""
    ts = df.ts_open.to_numpy(np.int64)
    t0 = ts[0]
    if (np.diff(ts) != MIN_MS).any():
        raise ValueError("Archiv nicht lückenlos")
    o, v = df.open.to_numpy(float), df.volume.to_numpy(float)
    hs, _ = hourly(ts, o, df.high.to_numpy(), df.low.to_numpy(), df.close.to_numpy())
    atr = atr14(hs)                                        # Index = Stunden-ID, gilt für die laufende Stunde

    lokal = pd.to_datetime(ts, unit="ms", utc=True)
    lokal = lokal.tz_convert(zeitzone) if zeitzone else lokal - pd.Timedelta(hours=5)
    datum = pd.Series(lokal.normalize().tz_localize(None) if zeitzone else lokal.normalize().tz_localize(None))
    minute = lokal.hour * 60 + lokal.minute
    idx = pd.DataFrame(dict(datum=datum.values, minute=np.asarray(minute), i=np.arange(len(ts))))

    def preis_index(m: int) -> pd.Series:
        return idx[idx.minute == m].set_index("datum").i

    i_open30 = preis_index(9 * 60 + 45)
    i_slh0 = preis_index(16 * 60)
    i_ein = preis_index(16 * 60 + 30)
    i_aus = preis_index(17 * 60)
    i_vorschluss = i_aus.copy()
    i_vorschluss.index = i_vorschluss.index + pd.Timedelta(days=1)      # Schluss des Vortags
    t = pd.concat(dict(vs=i_vorschluss, o30=i_open30, s0=i_slh0, ein=i_ein, aus=i_aus), axis=1).dropna().astype(int)
    t = t[t.vs < t.o30]
    t["r_onfh"] = o[t.o30] / o[t.vs] - 1
    t["r_slh"] = o[t.ein] / o[t.s0] - 1
    t["vol_fh"] = [v[a - 30:a].sum() for a in t.o30]
    t["atr"] = atr.reindex(ts[t.ein] // 3_600_000).to_numpy()
    t["e"], t["x"] = o[t.ein], o[t.aus]
    t["ts_open"], t["ts_close"] = ts[t.ein] * 1_000_000, ts[t.aus] * 1_000_000
    return t.dropna()


def trades(t: pd.DataFrame, richtung: np.ndarray, tak: float = TAKER_FEE) -> pd.DataFrame:
    """richtung: +1 Long, −1 Short, 0 kein Trade, je Tag."""
    m = richtung != 0
    t, s = t[m], richtung[m].astype(float)
    brutto = s * (t.x - t.e)
    fee = (t.e + t.x) * tak
    out = pd.DataFrame(dict(ts_open=t.ts_open, ts_close=t.ts_close, side=np.where(s > 0, "long", "short"),
                            entry=t.e, exit=t.x, risk_px=t.atr, exit_reason="zeit",
                            r_gross=brutto / t.atr, r_net=(brutto - fee) / t.atr,
                            pct_net=(brutto - fee) / t.e * 100, bps_brutto=brutto / t.e * 1e4))
    out = add_funding(out)
    out["bps_netto"] = out.pct_net * 100
    return out.reset_index(drop=True)


def signale(t: pd.DataFrame) -> dict:
    a = np.where(t.r_onfh > 0, 1, -1)
    b = np.where(t.r_slh < 0, 1, -1)
    c = np.where((t.r_onfh > 0) & (t.r_slh < 0), 1, np.where((t.r_onfh <= 0) & (t.r_slh >= 0), -1, 0))
    return dict(A=a, B=b, C=c)


def kennzahlen(x: pd.DataFrame) -> dict:
    s = summary(x)
    s.pop("tp_quote", None)
    b = x.bps_netto
    s.update(bps_brutto=float(x.bps_brutto.mean()), bps_netto=float(b.mean()),
             t_bps=float(b.mean() / (b.std(ddof=1) / np.sqrt(len(b)))), treffer=float((x.r_net > 0).mean()),
             long_anteil=float((x.side == "long").mean()))
    return s


if __name__ == "__main__":
    pd.set_option("display.width", 280)
    df = load_1m()

    for name, zz in (("fest UTC − 5 (Haupttest)", None), ("New York mit Sommerzeit (beschreibend)", "America/New_York")):
        t = tage(df, zz)
        sig = signale(t)
        print(f"\nH9, {name}, {len(t)} Tage")
        print(pd.DataFrame([dict(signal=k, **kennzahlen(trades(t, v))) for k, v in sig.items()]).round(3).to_string(index=False))

        if zz is None:
            c = sig["C"]
            tc = trades(t, c)
            # Kontrolle Marktrichtung: an denselben Tagen immer Long
            immer_long = kennzahlen(trades(t, np.where(c != 0, 1, 0)))
            print(f"\nKontrolle immer Long an denselben {int((c != 0).sum())} Tagen: "
                  f"{immer_long['bps_netto']:.2f} bps netto, R netto {immer_long['r_netto']:.4f}")
            # Kontrolle Zufallsrichtung
            rng = np.random.default_rng(42)
            werte = []
            for _ in range(1000):
                zr = np.where(c != 0, rng.choice([-1, 1], len(c)), 0)
                werte.append(trades(t, zr).r_net.mean())
            werte = np.array(werte)
            print(f"Kontrolle Zufallsrichtung, 1.000 Läufe: Mittel R netto {werte.mean():.4f}, "
                  f"95-%-Quantil {np.quantile(werte, 0.95):.4f}, Signal C {tc.r_net.mean():.4f}, "
                  f"Anteil Läufe ≥ C {(werte >= tc.r_net.mean()).mean():.3f}")
            # beschreibend: Volumen der ersten halben Stunde
            terz = pd.qcut(t.vol_fh.rank(method="first"), 3, labels=["niedrig", "mittel", "hoch"])
            rows = []
            for k in ("niedrig", "mittel", "hoch"):
                m = (terz == k).to_numpy()
                x = trades(t[m], c[m])
                rows.append(dict(volumen=k, n=len(x), bps_netto=x.bps_netto.mean(), r_netto=x.r_net.mean(),
                                 t=x.r_net.mean() / (x.r_net.std(ddof=1) / np.sqrt(len(x)))))
            print("\nSignal C nach Volumen der ersten halben Stunde (beschreibend)")
            print(pd.DataFrame(rows).round(3).to_string(index=False))
            wt = pd.to_datetime(tc.ts_open, unit="ns").dt.day_of_week
            print(f"Signal C Werktage {tc[wt < 5].bps_netto.mean():.2f} bps (n {int((wt < 5).sum())}), "
                  f"Wochenende {tc[wt >= 5].bps_netto.mean():.2f} bps (n {int((wt >= 5).sum())})")
