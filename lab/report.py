"""Einheitliche Auswertung von Trade-Listen (aus Scan oder Nautilus)."""
import numpy as np
import pandas as pd

from lab.config import FUNDING_RATE_1H

NS_PRO_STUNDE = 3_600_000_000_000


def add_funding(trades: pd.DataFrame, rate_1h: float = FUNDING_RATE_1H) -> pd.DataFrame:
    """Rechnet festes Funding anteilig zur Haltedauer ein und zieht es von r_net und pct_net ab.

    Braucht ts_open, ts_close [ns], side, entry und den Risikoabstand risk_px. Fehlt risk_px
    (ältere Läufe), wird er aus r_gross zurückgerechnet. Ergebnis zusätzlich in r_funding.
    """
    if len(trades) == 0 or "r_funding" in trades:
        return trades
    t = trades.copy()
    sign = np.where(t.side == "long", 1.0, -1.0)
    stunden = (t.ts_close - t.ts_open) / NS_PRO_STUNDE
    kosten_px = sign * rate_1h * stunden * t.entry           # positiv = Kosten für die Position
    if "risk_px" in t:
        risk = t.risk_px
    else:
        risk = (sign * (t.exit - t.entry) / t.r_gross).where(t.r_gross.abs() > 1e-9)
    t["r_funding"] = -kosten_px / risk
    t["r_net"] = t.r_net + t.r_funding
    if "pct_net" in t:
        t["pct_net"] = t.pct_net - kosten_px / t.entry * 100
    return t


def summary(trades: pd.DataFrame, r_col: str = "r_net") -> dict:
    """Kennzahlen für eine Trade-Liste mit Spalten ts_open [ns], r_gross, r_net, exit_reason."""
    if len(trades) == 0:
        return dict(n=0)
    r = trades[r_col].to_numpy()
    years = pd.to_datetime(trades.ts_open, unit="ns").dt.year
    se = r.std(ddof=1) / np.sqrt(len(r)) if len(r) > 1 else np.nan
    top3 = np.sort(r)[-3:].sum() if len(r) > 3 else np.nan
    out = dict(
        n=len(r),
        tp_quote=float((trades.exit_reason == "tp").mean()),
        r_brutto=float(trades.r_gross.mean()),
        r_netto=float(r.mean()),
        t_wert=float(r.mean() / se) if se and se > 0 else np.nan,
        r_ohne_top3=float((r.sum() - top3) / (len(r) - 3)) if len(r) > 3 else np.nan,
    )
    if "r_funding" in trades:
        out["r_funding"] = float(trades.r_funding.mean())
    for y, g in trades.groupby(years):
        out[f"r_{y}"] = float(g[r_col].mean())
    return out


def table(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.round(3)
