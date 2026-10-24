# trado-lab

Backtest-Labor für Trado. Handelsideen für den BTC-Perpetual PF_XBTUSD auf Kraken Futures werden hier mit festen Regeln geprüft: erst als schneller numba-Scan, dann realistisch mit [NautilusTrader](https://nautilustrader.io) inklusive Orders, Gebühren und Intrabar-Ausführung auf 1-Minuten-Kerzen.

## Einrichten

Voraussetzung: Python 3.13 und [uv](https://docs.astral.sh/uv/).

```bash
uv venv --python 3.13 .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
uv pip install -e .
python scripts/fetch_kraken.py       # lädt 1m-Kerzen ab 2023 nach data/raw (ca. 2 Mio. Kerzen, einige Minuten)
```

Erneut ausführen ergänzt nur die fehlenden Minuten.

## Benutzen

```bash
# schneller Scan einer Hypothese (In-Sample)
python -m scan.wick_fill_scan

# Nautilus-Backtest mit Parametern, Ergebnis landet in runs/
python -m lab.run wick_fill side=lower k_atr=1.5 sl_w=0.6

# finaler Out-of-Sample-Test (ab OOS_START in lab/config.py)
python -m lab.run wick_fill side=lower k_atr=1.5 sl_w=0.6 --oos
```

## Aufbau

| Pfad | Inhalt |
|---|---|
| `lab/config.py` | Symbol, Gebühren, Out-of-Sample-Grenze |
| `lab/data.py` | Archiv laden, Nautilus-Bars, Parquet-Katalog |
| `lab/instruments.py` | Kontrakt PF_XBTUSD |
| `lab/engine.py` | simuliertes Kraken-Venue und Backtest-Lauf |
| `lab/run.py` | Kommandozeile für Nautilus-Läufe |
| `lab/report.py` | Kennzahlen in R, t-Wert, Jahre |
| `scan/` | schnelle numba-Vorabtests |
| `strategies/` | Strategien für NautilusTrader |
| `runs/` | gespeicherte Ergebnisse |
| `LABORBUCH.md` | alle Hypothesen mit Regeln, Ergebnis und Entscheidung |
| `CLAUDE.md` | Arbeitsregeln für Claude |

## Neue Hypothese testen

1. Eintrag in LABORBUCH.md mit festen Regeln
2. Scan in `scan/<name>_scan.py`
3. Bei Erfolg Strategie `strategies/<name>.py` (Klasse erbt von `LabStrategy`, implementiert `handle_bar`)
4. `python -m lab.run <name> ...`, zum Schluss einmal `--oos`
