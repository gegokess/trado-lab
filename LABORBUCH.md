# Laborbuch

Jede Hypothese bekommt einen Eintrag, bevor gerechnet wird. Ergebnisse netto nach Gebühren (Maker 0,01 %, Taker 0,03 %).
Out-of-Sample ab 2026-05-01 ist gesperrt, bis die Parameter einer Hypothese final feststehen.

| Nr | Hypothese | Status | Ergebnis |
|---|---|---|---|
| H1 | Lange 1h-Wicks werden nach 20 % Füllung bis 80 % weiter gefüllt | abgelehnt | kein Edge, brutto ±0, netto −0,1 bis −0,2 R |
| H2 | Sweep eines unberührten Swing-Levels kehrt um, Ziel über der Wickbasis | abgelehnt | kein Edge, brutto ±0 bis +0,05, netto −0,006 bis −0,11 R |

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

---

## H2: Liquidity Sweep (Umkehr)

**Idee (Gregor, 24.10.2026):** Eine Wick, die ein vorheriges Swing-Tief durchsticht, holt dort ruhende Stops ab. Danach dreht der Kurs. Gehandelt wird gegen die Sweep-Richtung, also Long nach einem Sweep nach unten, mit Ziel oberhalb der Wickbasis. Abgrenzung zu H1: dort wurde die Wick weiter gefüllt, hier wird die Füllung gegen die Wickrichtung gehandelt und ein Sweep-Filter verlangt.

**Regeln** (strategies/liquidity_sweep.py, scan/liquidity_sweep_scan.py), untere Seite beschrieben, obere spiegelbildlich

- Swing-Tief: abgeschlossene 1h-Kerze, deren Tief strikt unter den Tiefs der sw Stunden davor und danach liegt, nutzbar erst ab der Bestätigung sw Stunden später
- unberührt: keine abgeschlossene Stunde seit der Entstehung hat unter dem Level gehandelt, ein berührtes Level fällt dauerhaft weg
- Referenzlevel S der laufenden Stunde: das höchste unberührte Swing-Tief unterhalb des Stundenopens
- Wick der laufenden Stunde wie in H1: Oberkante T = min(Open, Rebound-Hoch), W = T − Tief
- Setup: W ≥ k_atr × ATR14 der abgeschlossenen 1h-Kerzen und Tief < S ≤ T, der Sweep liegt also innerhalb der Wick
- Einstieg Long bei Tief + entry_w × W (Taker), gedacht als Rückeroberung eines Teils der Wick: per Stop-Market, solange der Kurs noch darunter liegt, sonst per Market (siehe Befund zum Einstieg unten)
- TP als ruhende Limit-Order bei T + tp_w × W (Maker), SL per Stop-Market bei Tief − sl_w × W (Taker)
- ein Trade pro Stunde, nicht ausgelöste Einstiegsorder verfällt zur vollen Stunde, Zeitstopp 6 h

**Vorab festgelegtes Raster** (In-Sample 2023-01-01 bis 2026-04-30, 16 Varianten): Seite untere/obere, k_atr 1,0/1,5, entry_w 0,3/0,5, tp_w 0,5/1,0. Fest: sl_w = 0,2, sw = 3, Zeitstopp 360 min.

**Abgleich Nautilus gegen numba-Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04, entry_w = 0,3, tp_w = 0,5)

| Seite | k | Quelle | Trades | TP-Quote | R brutto | R netto | t-Wert |
|---|---|---|---|---|---|---|---|
| untere | 1,0 | numba | 541 | 66,9 % | +0,05 | −0,02 | −0,8 |
| untere | 1,0 | Nautilus | 549 | 67,4 % | +0,05 | −0,02 | −0,6 |
| untere | 1,5 | numba | 205 | 62,9 % | +0,01 | −0,04 | −0,8 |
| untere | 1,5 | Nautilus | 211 | 63,0 % | +0,01 | −0,04 | −0,9 |
| obere | 1,0 | numba | 503 | 62,0 % | −0,02 | −0,11 | −3,2 |
| obere | 1,0 | Nautilus | 515 | 62,1 % | −0,02 | −0,11 | −3,3 |
| obere | 1,5 | numba | 191 | 63,4 % | +0,05 | −0,01 | −0,1 |
| obere | 1,5 | Nautilus | 198 | 62,6 % | +0,04 | −0,02 | −0,3 |

96 bis 97 % der Nautilus-Trades stimmen in Einstiegsminute und Ausstiegsgrund mit dem Scan überein. Anders als bei H1 liegt der Fill auf derselben Minute wie der Scan-Zeitstempel, weil der Einstieg per Market aus dem Signal der Vorminute erfolgt und nicht als ruhende Stop-Order auf einen Trigger wartet. Nautilus-Läufe in runs/, Scan über das volle Raster per `python -m scan.liquidity_sweep_scan`.

**Raster (16 Varianten, In-Sample):** kein Netto-Ergebnis über null. Bestes Netto −0,006 R (obere Seite, k = 1,5, tp_w = 0,5), bestes Brutto +0,05 R, t-Werte zwischen −3,3 und −0,1. Die Variante mit tp_w = 1,0 ist durchweg schlechter als tp_w = 0,5.

**Befund zum Einstieg:** entry_w ist in dieser Regel wirkungslos. Das Setup wird erst gültig, wenn der Rebound die Wick auf mindestens k × ATR aufgespannt hat, und dann liegt der Kurs schon über L + entry_w × W. Der Einstieg entartet damit zum Market-Einstieg am Rebound, die Werte 0,3 und 0,5 liefern dieselben Trades. Das Raster enthält faktisch 8 Regeln, nicht 16.

**Entscheidung:** abgelehnt. Kein OOS-Test, die Parameter sind nie in den brutto klar positiven Bereich gekommen. Der Sweep hebt die Trefferquote deutlich (62 bis 67 % statt 47 bis 52 % bei H1), aber das Verhältnis aus engem SL (0,2 W) und nahem Ziel (0,5 W über der Wickbasis) frisst die Quote auf: brutto bleibt bestenfalls die Hälfte der Gebühren übrig. Die obere Seite mit k = 1,0 ist mit t = −3,3 klar negativ, dort ist der Sweep nach oben kein Umkehrsignal.

Offener Folgegedanke: Einstieg nicht am Rebound, sondern auf einem Rücklauf unter die Wickbasis (Limit bei T − x × W, also Maker statt Taker und engeres Risiko bei gleichem Ziel). Das ist eine andere Regel und braucht einen eigenen Eintrag.
