"""Einheitliche Auswertung von Trade-Listen (aus Scan oder Nautilus)."""
import numpy as np
import pandas as pd


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
    for y, g in trades.groupby(years):
        out[f"r_{y}"] = float(g[r_col].mean())
    return out


def table(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    return df.round(3)
