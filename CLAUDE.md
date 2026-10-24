# trado-lab: Regeln für die Zusammenarbeit

Backtest-Labor für Gregors Trading-Bot Trado (BTC-Perpetual PF_XBTUSD auf Kraken Futures).
Ziel: Hypothesen mit festen Regeln prüfen, bevor etwas in Trado übernommen wird.

## Setup in einer neuen Sitzung

```bash
uv venv --python 3.13 .venv && . .venv/bin/activate
uv pip install -e .
python scripts/fetch_kraken.py        # 1m-Archiv ab 2023 laden oder ergänzen (data/ ist nicht im Git)
```

## Markt und Kosten (nicht ohne Rücksprache ändern)

- Daten: Kraken Futures Charts-API, 1m-Kerzen PF_XBTUSD, Zeitstempel = Kerzenbeginn UTC
- Gebühren Gregor, Stufe 5: Maker 0,01 %, Taker 0,03 % (lab/config.py)
- Einstieg per Stop-Market ist Taker, TP als ruhende Limit-Order Maker, SL als Stop-Market Taker
- Funding als fester Satz `FUNDING_RATE_1H` (Mittel Kraken 2026, lab/config.py), anteilig zur Haltedauer über `add_funding` in lab/report.py. In Nautilus-Läufen automatisch, in Scans selbst aufrufen. Echte Werte nur ab 2025-10 (`python scripts/fetch_derivatives.py`)

## Testprotokoll

1. Hypothese mit festen Regeln in LABORBUCH.md eintragen, bevor gerechnet wird
2. Schneller Scan in `scan/` (numba) über wenige, vorab genannte Varianten, nur In-Sample
3. Nur wenn der Scan brutto klar positiv ist: Strategie in `strategies/` für NautilusTrader bauen und mit `python -m lab.run` rechnen
4. Out-of-Sample ab `OOS_START` (lab/config.py) genau einmal je Hypothese mit final festgelegten Parametern (`--oos`)
5. Ergebnis, Anzahl getesteter Varianten und Entscheidung im Laborbuch festhalten

Bewertung immer netto nach Gebühren in R, mit t-Wert, Ergebnis ohne die 3 besten Trades und Aufteilung nach Jahren (lab/report.py).
Positive Einzelvarianten aus großen Rastern sind zunächst Zufallsverdacht.

## Code-Konventionen

- Strategien erben von `strategies.base.LabStrategy` und implementieren `handle_bar`, nicht `on_bar`. Sie setzen vor dem Einstieg `self.plan = dict(sl=..., tp=...)`
- Config-Klassen für NautilusTrader 2.x mit explizitem `__init__` (siehe strategies/wick_fill.py)
- Bars: `ts_event` = Kerzenbeginn, `ts_init` = Kerzenende. Fills und `ts_opened` liegen daher eine Minute hinter dem Scan-Zeitstempel
- Bestehende Dateien gezielt ändern statt komplett neu zu schreiben
- Dokumentation und Kommentare auf Deutsch, Aufzählungen ohne fettes Startwort und ohne Punkt am Ende
- Ergebnisse in `runs/` werden committet (trades.csv, ergebnis.json), Rohdaten nicht

## NautilusTrader-Version

2.0.0rc7 (Release Candidate, laut Doku nicht für Live-Handel mit echtem Geld gedacht). API weicht von 1.x ab:
`portfolio.is_net_flat`, `order_factory.bracket` erlaubt keinen Stop-Einstieg, Fehler in Handlern werden sonst nur geloggt.
