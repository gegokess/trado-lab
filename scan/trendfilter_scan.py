"""Scan für H12: BTC long über dem 200-Tage-Schnitt, sonst flach, gemessen gegen Halten.

Aufruf:  python -m scan.trendfilter_scan

Tagesrenditen Schluss zu Schluss. Signal mit dem Schluss von Tag d, Position gilt für die Rendite von Tag d + 1.
Kosten: 3 bps je Wechsel (Taker), Funding mit festem Satz an jedem Long-Tag. Halten ohne Kosten.
"""
import numpy as np
import pandas as pd

from lab.config import FUNDING_RATE_1H, OOS_START, TAKER_FEE
from lab.data import load_1m
from scan.donchian_daily_scan import lade_yahoo, tageskerzen_kraken

REGELN = {"SMA200 (Haupttest)": ("sma", 200), "SMA50": ("sma", 50), "EMA150": ("ema", 150), "SMA125": ("sma", 125)}


def signal(close: pd.Series, art: str, n: int) -> pd.Series:
    ma = close.rolling(n).mean() if art == "sma" else close.ewm(span=n, adjust=False, min_periods=n).mean()
    return (close > ma).astype(float).where(ma.notna())


def strategie(close: pd.Series, pos: pd.Series) -> pd.Series:
    r = close.pct_change()
    p = pos.shift(1)                                     # Signal von gestern gilt heute
    wechsel = p.diff().abs().fillna(0)
    return (p * r - wechsel * TAKER_FEE - p * FUNDING_RATE_1H * 24).dropna()


def kennzahlen(r: pd.Series) -> dict:
    eq = (1 + r).cumprod()
    jahre = len(r) / 365
    return dict(rendite_pa=eq.iloc[-1] ** (1 / jahre) - 1, vola_pa=r.std() * np.sqrt(365),
                sharpe=r.mean() / r.std() * np.sqrt(365), max_verlust=(eq / eq.cummax() - 1).min())


def sharpe_diff_ci(a: pd.Series, b: pd.Series, n: int = 2000, block: int = 7, seed: int = 1):
    """Block-Bootstrap (Wochenblöcke, zirkulär) für Sharpe(a) − Sharpe(b) auf denselben Tagen."""
    x = np.column_stack([a.to_numpy(), b.to_numpy()])
    T = len(x)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        starts = rng.integers(0, T, int(np.ceil(T / block)))
        idx = (starts[:, None] + np.arange(block)).ravel()[:T] % T
        s = x[idx]
        sh = s.mean(0) / s.std(0)
        out.append((sh[0] - sh[1]) * np.sqrt(365))
    return np.quantile(out, [0.025, 0.975])


def auswerten(close: pd.Series, ab: str, bis: str, titel: str, mit_ci: bool):
    rows = []
    halten = close.pct_change()
    for name, (art, n) in REGELN.items():
        pos = signal(close, art, n)
        r = strategie(close, pos)
        r = r[(r.index >= ab) & (r.index < bis)]
        h = halten.reindex(r.index)
        k = kennzahlen(r)
        p = pos.shift(1).reindex(r.index)
        zeile = dict(regel=name, **k, im_markt=p.mean(), wechsel=int(p.diff().abs().sum()))
        if mit_ci and name.startswith("SMA200"):
            lo, hi = sharpe_diff_ci(r, h)
            zeile.update(sharpe_diff_lo=lo, sharpe_diff_hi=hi)
        rows.append(zeile)
    hk = kennzahlen(halten.reindex(r.index))
    rows.append(dict(regel="Halten", **hk, im_markt=1.0, wechsel=0))
    print(f"\n{titel}")
    print(pd.DataFrame(rows).round(3).to_string(index=False))


if __name__ == "__main__":
    pd.set_option("display.width", 220)
    y = lade_yahoo("2014-01-01", OOS_START)
    close = pd.Series(y.close.to_numpy(), index=pd.to_datetime(y.ts_open, unit="ms"))
    auswerten(close, "2015-01-01", OOS_START, "H12 Yahoo 2015 bis April 2026 (Hauptauswertung)", True)
    auswerten(close, "2015-01-01", "2023-01-01", "Teilzeitraum 2015 bis 2022", False)
    auswerten(close, "2023-01-01", OOS_START, "Teilzeitraum 2023 bis April 2026 (Yahoo)", False)
    kd = tageskerzen_kraken(load_1m())
    kc = pd.Series(kd.close.to_numpy(), index=pd.to_datetime(kd.ts_open, unit="ms"))
    # Kraken beginnt 2023, für den 200-Tage-Schnitt Yahoo-Schlüsse davor anhängen
    kc = pd.concat([close[close.index < kc.index[0]], kc])
    auswerten(kc, "2023-01-01", OOS_START, "Teilzeitraum 2023 bis April 2026 (Kraken-Schlüsse)", False)
