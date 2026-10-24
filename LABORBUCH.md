# Laborbuch

Jede Hypothese bekommt einen Eintrag, bevor gerechnet wird. Ergebnisse netto nach Gebühren (Maker 0,01 %, Taker 0,03 %).
Out-of-Sample ab 2026-05-01 ist gesperrt, bis die Parameter einer Hypothese final feststehen.

| Nr | Hypothese | Status | Ergebnis |
|---|---|---|---|
| H1 | Lange 1h-Wicks werden nach 20 % Füllung bis 80 % weiter gefüllt | abgelehnt | kein Edge, brutto ±0, netto −0,1 bis −0,2 R |

---

## H1: Wick-Füllung

**Idee (Gregor, 24.10.2026):** Lange Wicks auf 1h werden in der Regel wieder gefüllt. Entsteht die Wick innerhalb der Stunde und kommt der Kurs 20 % in die Wick zurück, läuft er weiter bis 80 %.

**Regeln** (strategies/wick_fill.py, scan/wick_fill_scan.py)

- Wick der laufenden Stunde: W = min(Open, Rebound-Hoch) − Tief (untere Wick, obere spiegelbildlich)
- Setup ab W ≥ k × ATR14 der abgeschlossenen 1h-Kerzen
- Einstieg per Stop-Market bei 20 % Füllung, TP Limit bei 80 %, SL Einstieg + sl_w × W
- Ein Trade pro Stunde, Einstiegsorder verfällt zur vollen Stunde, Zeitstopp 6 h

**Vorarbeit im Chat (vor Einrichtung des Repos, Daten Okt 2023 bis Okt 2026, auch OOS-Zeitraum berührt)**

- Fertige 1h-Kerzen: Wickspitze wird in 24 h genauso oft erreicht wie eine gleich weite Bewegung in die Gegenrichtung (z. B. 51 % zu 51 % bei k = 1,5). Keine Richtungsinformation
- Intrabar-Regel auf 1m, 36 Varianten: brutto ±0 R, netto durchweg negativ
- TP über 80 % hinaus (bis 300 % der Wick) und Stop auf Einstand, 132 Varianten: nur k = 2 mit rund 74 Trades positiv, t-Werte unter 1, hängt an 2 bis 3 Ausreißern, Jahre widersprüchlich. Als Zufall gewertet

**Abgleich Nautilus gegen numba-Scan (24.10.2026, In-Sample 2023-01 bis 2026-04, sl_w = 0,6)**

| Seite | k | Quelle | Trades | TP-Quote | R brutto | R netto | t-Wert |
|---|---|---|---|---|---|---|---|
| untere | 1,0 | numba | 1233 | 51,8 % | +0,02 | −0,12 | −4,1 |
| untere | 1,0 | Nautilus | 1262 | 52,1 % | +0,03 | −0,11 | −3,8 |
| untere | 1,5 | numba | 362 | 46,1 % | −0,07 | −0,18 | −3,3 |
| untere | 1,5 | Nautilus | 377 | 46,7 % | −0,07 | −0,17 | −3,2 |
| obere | 1,0 | numba | 1149 | 49,1 % | −0,03 | −0,19 | −6,5 |
| obere | 1,0 | Nautilus | 1188 | 49,6 % | −0,02 | −0,18 | −5,8 |
| obere | 1,5 | numba | 344 | 48,0 % | −0,02 | −0,14 | −2,5 |
| obere | 1,5 | Nautilus | 357 | 47,1 % | −0,03 | −0,15 | −2,6 |

Rund 98 % der Trades stimmen in Einstiegsminute und Ausstiegsgrund überein (Nautilus-Fills liegen erwartungsgemäß eine Minute später). Beide Wege liefern dasselbe Bild, der Scan ist damit als Vorfilter verlässlich.

**Entscheidung:** abgelehnt. Kein OOS-Test nötig. Offener Folgegedanke: Wick als Liquidity Sweep über ein vorheriges Swing-Hoch/-Tief mit Ziel jenseits der Wickspitze (eigene Hypothese, neu definieren).
