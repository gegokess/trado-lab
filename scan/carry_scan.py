"""Auswertung für H13: BTC als Sicherheit, PF_XBTUSD short in gleicher Menge, Ertrag = Funding.

Aufruf:  python -m scan.carry_scan        (braucht data/raw/PF_XBTUSD_funding.parquet aus fetch_derivatives.py)

Echtes Kraken-Funding ab 2025-10. Die Regel hat keine Parameter, deshalb wird der ganze verfügbare Zeitraum
genutzt, auch der OOS-Teil. Positiver Satz heißt Longs zahlen, der Short erhält ihn.
"""
import numpy as np
import pandas as pd

from lab.config import RAW_DIR, SYMBOL, TAKER_FEE

STUNDEN_JAHR = 24 * 365


def main() -> None:
    f = pd.read_parquet(RAW_DIR / f"{SYMBOL}_funding.parquet")
    r = pd.Series(f.rate_rel.to_numpy(), index=pd.to_datetime(f.ts, unit="ms")).sort_index()
    tage = (r.index[-1] - r.index[0]).total_seconds() / 86_400
    brutto = r.sum()
    netto = brutto - 2 * TAKER_FEE
    print(f"Zeitraum {r.index[0]} bis {r.index[-1]} ({tage:.0f} Tage, {len(r)} Funding-Stunden)")
    print(f"Immer short: Funding brutto {brutto * 100:.2f} %, nach Öffnen und Schließen {netto * 100:.2f} %, "
          f"annualisiert {netto * 365 / tage * 100:.2f} % p.a.")
    print(f"Anteil Stunden mit negativem Funding {(r < 0).mean() * 100:.1f} %")
    m = r.resample("MS").sum() * 100
    print("Monatsertrag in %: " + ", ".join(f"{i:%Y-%m} {v:+.2f}" for i, v in m.items()))
    roll30 = r.rolling(30 * 24).sum().dropna() * 100
    print(f"schlechteste 30 Tage {roll30.min():+.2f} %, beste 30 Tage {roll30.max():+.2f} %")
    # beschreibend: nur short, wenn das Funding der Vorstunde positiv war
    pos = (r.shift(1) > 0).astype(float)
    wechsel = pos.diff().abs().fillna(0).sum()
    variante = (pos * r).sum() - wechsel * TAKER_FEE
    print(f"Variante nur bei positivem Vorstunden-Funding: {variante * 100:.2f} % ({int(wechsel)} Wechsel), "
          f"annualisiert {variante * 365 / tage * 100:.2f} % p.a.")


if __name__ == "__main__":
    main()
