"""H30: Teilziele und nachgezogener Stop für die H20-Regel, Nautilus-Läufe A0 bis A3 (LABORBUCH.md).

Aufruf:  python -m scan.h30_teilziele          In-Sample bis OOS_START
         python -m scan.h30_teilziele --oos A2  einmaliger OOS-Lauf einer Variante gegen A0

Eigener Treiber statt lab.run, weil die Teilziel-Parameter Doppelpunkte enthalten (unter Windows nicht als
Ordnername erlaubt). Ablage wie lab.run unter runs/<zeit>_h30_<Variante>[_OOS].
"""
import argparse
import json
from datetime import datetime, timezone

import pandas as pd

from lab.config import RUNS_DIR
from lab.run import backtest

BASIS = dict(side="upper", sl_ref="start", sl_w=0.1, fill_out=0.5)
VARIANTEN = {
    "A0": dict(),
    "A1": dict(tps="0.5:0.5,1.0:0.3,1.5:0.2", be_nach_tp1=True),
    "A2": dict(tps="0.5:0.5,1.0:0.5", be_nach_tp1=True),
    "A3": dict(tps="0.5:0.5", trail15=True),
}


def lauf(name: str, oos: bool) -> dict:
    trades, stats, meta, _ = backtest("spike_fill", {**BASIS, **VARIANTEN[name]}, oos=oos)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    d = RUNS_DIR / f"{stamp}_h30_{name}{'_OOS' if oos else ''}"
    d.mkdir(parents=True, exist_ok=True)
    trades.to_csv(d / "trades.csv", index=False)
    (d / "ergebnis.json").write_text(json.dumps(dict(meta=meta, kennzahlen=stats), indent=2, ensure_ascii=False))
    return dict(variante=name, r_summe=float(trades.r_net.sum()) if len(trades) else 0.0, **stats)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--oos", help="Variante für den einmaligen OOS-Lauf")
    a = ap.parse_args()
    namen = ["A0", a.oos] if a.oos else list(VARIANTEN)
    e = pd.DataFrame([lauf(n, bool(a.oos)) for n in namen])
    pd.set_option("display.width", 250)
    print(e.round(3).to_string(index=False))


if __name__ == "__main__":
    main()
