"""Zentrale Einstellungen für alle Tests. Änderungen hier betreffen jeden Lauf."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CATALOG_DIR = DATA_DIR / "catalog"
RUNS_DIR = ROOT / "runs"

# Markt
SYMBOL = "PF_XBTUSD"          # Kraken Futures, linearer BTC-Perpetual
VENUE = "KRAKEN"
DATA_START = "2023-01-01"     # Beginn des Datenarchivs (UTC)

# Gebühren Kraken Futures, Gregors Stufe 5 (Stand 11.10.2026), als Anteil des Positionswerts
MAKER_FEE = 0.0001            # 0,01 %  Limit/Post-Only, TP als ruhende Limit-Order
TAKER_FEE = 0.0003            # 0,03 %  Market, Stop-Market (Einstieg per Stop, SL)

# Funding als fester Satz je Stunde, Anteil des Positionswerts, positiv heißt Longs zahlen und Shorts erhalten.
# Festlegung Gregor 24.10.2026: Mittel des Kraken-Fundings PF_XBTUSD vom 2026-01-01 bis 2026-10-24
# (relativeFundingRate, 7.113 Stunden, entspricht +2,85 % p.a.). Echte Kraken-Werte gibt es nur rund ein Jahr
# rückwirkend, deshalb gilt der Satz für den ganzen Testzeitraum. Neu berechnen mit scripts/fetch_derivatives.py
FUNDING_RATE_1H = 3.26e-06

# Out-of-Sample: alles ab diesem Zeitpunkt ist für Scans und Parametersuche gesperrt.
# Pro Hypothese wird dieser Zeitraum genau einmal mit den final festgelegten Parametern gerechnet.
OOS_START = "2026-05-01"
