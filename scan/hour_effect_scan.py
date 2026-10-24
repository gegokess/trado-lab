"""Scan für H8 (Uhrzeit-Effekt): Long zur Eröffnung von 21:00 UTC, Ausstieg zur Eröffnung von 23:00 UTC.

Aufruf:  python -m scan.hour_effect_scan        (Standard: In-Sample bis OOS_START)

Regel laut Laborbuch:
- Einstieg Long per Market zum Open der ersten Minute des Startfensters (Taker)
- Ausstieg per Market zum Open der ersten Minute nach dem Fenster (Taker)
- Not-SL per Stop-Market bei Einstieg − 1,5 × ATR14 der abgeschlossenen 1h-Kerzen (Taker), zugleich R
- Stop-Fill zum SL-Preis, bei einer Lücke unter den SL zum Open der Minute

Bewertet wird nur das Fenster 21:00 bis 23:00. Das Profil aller 24 Zwei-Stunden-Fenster und die
Aufteilung Werktag gegen Wochenende sind beschreibend und dienen nicht zur Auswahl.
"""
import numpy as np
import pandas as pd

from lab.config import TAKER_FEE
from lab.data import load_1m
from lab.report import summary
from scan.liquidity_sweep_scan import atr14, hourly

MIN_MS = 60_000


def _stunden(df: pd.DataFrame):
    """1m-Arrays als Matrix (Stunden × 60 Minuten). Setzt ein lückenloses Archiv ab voller Stunde voraus."""
    ts = df.ts_open.to_numpy(np.int64)
    if len(ts) % 60 or ts[0] % 3_600_000 or (np.diff(ts) != MIN_MS).any():
        raise ValueError("Archiv nicht lückenlos oder nicht an vollen Stunden ausgerichtet")
    n = len(ts) // 60
    o, h, l, c = (df[x].to_numpy(float).reshape(n, 60) for x in ("open", "high", "low", "close"))
    hs, _ = hourly(ts, df.open.to_numpy(), df.high.to_numpy(), df.low.to_numpy(), df.close.to_numpy())
    atr = atr14(hs).to_numpy()                 # gilt für die laufende Stunde, aus abgeschlossenen Stunden
    stunde0 = ts[::60]
    return stunde0, o, l, atr


def run(df: pd.DataFrame, start_h: int = 21, dauer_h: int = 2, sl_atr: float = 1.5,
        taker: float = TAKER_FEE) -> pd.DataFrame:
    stunde0, o, l, atr = _stunden(df)
    uhr = (stunde0 // 3_600_000) % 24
    idx = np.flatnonzero(uhr == start_h)
    idx = idx[idx + dauer_h < len(stunde0)]   # Ausstiegs-Open muss im Datensatz liegen
    idx = idx[~np.isnan(atr[idx])]

    entry = o[idx, 0]
    sl = entry - sl_atr * atr[idx]
    # Minuten des Fensters als eine Zeile je Trade
    fenster_l = np.concatenate([l[idx + j] for j in range(dauer_h)], axis=1)
    fenster_o = np.concatenate([o[idx + j] for j in range(dauer_h)], axis=1)
    getroffen = fenster_l <= sl[:, None]
    hit = getroffen.any(axis=1)
    erste = getroffen.argmax(axis=1)
    sl_fill = np.minimum(sl, fenster_o[np.arange(len(idx)), erste])
    exit_ = np.where(hit, sl_fill, o[idx + dauer_h, 0])

    risiko = entry - sl
    gebuehr = taker * (entry + exit_)
    return pd.DataFrame(dict(
        ts_open=stunde0[idx] * 1_000_000,
        exit_reason=np.where(hit, "sl", "zeit"),
        r_gross=(exit_ - entry) / risiko,
        r_net=(exit_ - entry - gebuehr) / risiko,
        pct_gross=(exit_ / entry - 1) * 100,
        pct_net=((exit_ - entry - gebuehr) / entry) * 100,
    ))


def kennzahlen(t: pd.DataFrame) -> dict:
    s = summary(t)
    s.pop("tp_quote", None)
    s.update(sl_quote=float((t.exit_reason == "sl").mean()), trefferquote=float((t.r_net > 0).mean()),
             pct_brutto=float(t.pct_gross.mean()), pct_netto=float(t.pct_net.mean()))
    return s


if __name__ == "__main__":
    pd.set_option("display.width", 250)
    df = load_1m()

    print("H8, Fenster 21:00 bis 23:00 UTC (bewertet)")
    h8 = run(df)
    print(pd.DataFrame([kennzahlen(h8)]).round(4).to_string(index=False))

    wtag = pd.to_datetime(h8.ts_open, unit="ns").dt.day_of_week
    teile = [dict(teil=name, **kennzahlen(h8[m])) for name, m in
             (("Werktag", wtag < 5), ("Wochenende", wtag >= 5))]
    print("\nWerktag gegen Wochenende (beschreibend)")
    print(pd.DataFrame(teile).round(4).to_string(index=False))

    print("\nProfil aller Zwei-Stunden-Fenster (beschreibend, nicht zur Auswahl)")
    prof = [dict(start=f"{h:02d}:00", **{k: v for k, v in kennzahlen(run(df, start_h=h)).items()
                                          if k in ("n", "pct_brutto", "pct_netto", "r_netto", "t_wert")})
            for h in range(24)]
    print(pd.DataFrame(prof).round(4).to_string(index=False))
