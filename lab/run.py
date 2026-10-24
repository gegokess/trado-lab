"""Nautilus-Backtest einer Strategie starten und Ergebnis unter runs/ ablegen.

Beispiel:
    python -m lab.run wick_fill side=lower k_atr=1.5 sl_w=0.6
    python -m lab.run wick_fill side=upper k_atr=2 --start 2024-01-01 --end 2025-01-01
    python -m lab.run wick_fill side=lower k_atr=1.5 --oos      # finaler Out-of-Sample-Test

Parameter im Format name=wert werden an die Strategie-Config durchgereicht.
"""
import argparse
import importlib
import json
import time
from datetime import datetime, timezone

import pandas as pd

from lab.config import OOS_START, RUNS_DIR
from lab.data import load_1m, to_bars
from lab.engine import run as run_engine
from lab.instruments import BAR_TYPE_1M, INSTRUMENT_ID
from lab.report import summary


def _parse(v: str):
    for cast in (int, float):
        try:
            return cast(v)
        except ValueError:
            pass
    return v


def load_strategy(name: str):
    """strategies/<name>.py muss genau eine LabStrategy-Klasse und ihre Config (Name + 'Config') enthalten."""
    mod = importlib.import_module(f"strategies.{name}")
    cls = next(v for k, v in vars(mod).items() if isinstance(v, type) and k.lower() == name.replace("_", ""))
    cfg = getattr(mod, cls.__name__ + "Config")
    return cls, cfg


def backtest(name: str, params: dict, start=None, end=None, oos=False, adaptive=True):
    cls, cfg = load_strategy(name)
    if oos:
        start, end = start or OOS_START, end
    df = load_1m(start, end, allow_oos=oos)
    strat = cls(cfg(instrument_id=INSTRUMENT_ID, bar_type=BAR_TYPE_1M, **params))
    t0 = time.time()
    engine = run_engine(strat, to_bars(df), adaptive_ordering=adaptive)
    trades = pd.DataFrame(strat.trades)
    meta = dict(strategie=name, params=params, start=str(pd.to_datetime(df.ts_open.iloc[0], unit="ms")),
                ende=str(pd.to_datetime(df.ts_open.iloc[-1], unit="ms")), oos=oos,
                adaptive_ordering=adaptive, laufzeit_s=round(time.time() - t0, 1))
    return trades, summary(trades), meta, engine


def save(trades, stats, meta) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    tag = "_".join(f"{k}{v}" for k, v in meta["params"].items())
    d = RUNS_DIR / f"{stamp}_{meta['strategie']}_{tag}{'_OOS' if meta['oos'] else ''}"
    d.mkdir(parents=True, exist_ok=True)
    trades.to_csv(d / "trades.csv", index=False)
    (d / "ergebnis.json").write_text(json.dumps(dict(meta=meta, kennzahlen=stats), indent=2, ensure_ascii=False))
    return str(d)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("strategy")
    ap.add_argument("params", nargs="*", help="name=wert")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--oos", action="store_true", help="Out-of-Sample-Zeitraum ab OOS_START rechnen")
    ap.add_argument("--no-adaptive", action="store_true", help="feste Reihenfolge O-H-L-C in der Kerze")
    ap.add_argument("--no-save", action="store_true")
    a = ap.parse_args()
    params = {k: _parse(v) for k, v in (p.split("=", 1) for p in a.params)}
    trades, stats, meta, _ = backtest(a.strategy, params, a.start, a.end, a.oos, not a.no_adaptive)
    print(json.dumps(dict(meta=meta, kennzahlen=stats), indent=2, ensure_ascii=False))
    if not a.no_save:
        print("gespeichert:", save(trades, stats, meta))
