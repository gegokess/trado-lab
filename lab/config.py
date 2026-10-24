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

# Out-of-Sample: alles ab diesem Zeitpunkt ist für Scans und Parametersuche gesperrt.
# Pro Hypothese wird dieser Zeitraum genau einmal mit den final festgelegten Parametern gerechnet.
OOS_START = "2026-05-01"
