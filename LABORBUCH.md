# Laborbuch

Jede Hypothese bekommt einen Eintrag, bevor gerechnet wird. Ergebnisse netto nach Gebühren (Maker 0,01 %, Taker 0,03 %).
Out-of-Sample ab 2026-05-01 ist gesperrt, bis die Parameter einer Hypothese final feststehen.

| Nr | Hypothese | Status | Ergebnis |
|---|---|---|---|
| H1 | Lange 1h-Wicks werden nach 20 % Füllung bis 80 % weiter gefüllt | abgelehnt | kein Edge, brutto ±0, netto −0,1 bis −0,2 R |
| H2 | Sweep eines unberührten Swing-Levels kehrt um, Ziel über der Wickbasis | abgelehnt | kein Edge, brutto ±0 bis +0,05, netto −0,006 bis −0,11 R |
| H3 | Wie H2, aber Einstieg per Limit auf einem Rücklauf unter die Wickbasis | abgelehnt | besser als H2, aber in Nautilus netto −0,008 bis −0,078 R |

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

Folgegedanke Einstieg auf einem Rücklauf unter die Wickbasis statt am Rebound: als H3 geprüft, ebenfalls abgelehnt.

---

## H3: Liquidity Sweep mit Rücklauf-Einstieg

**Idee (Gregor, 24.10.2026):** Wie H2, aber der Einstieg wartet nicht auf den Rebound, sondern auf einen Rücklauf unter die Wickbasis. Das ergibt eine ruhende Limit-Order statt eines Market-Einstiegs (Maker statt Taker) und ein engeres Risiko bei unverändertem Ziel. H2 hat gezeigt, dass das Signal mit 62 bis 67 % Trefferquote Substanz hat und nur am Verhältnis von Risiko zu Ziel scheitert, genau dort setzt H3 an.

**Regeln** (strategies/sweep_pullback.py, scan/sweep_pullback_scan.py), untere Seite beschrieben, obere spiegelbildlich

- Swing-Tief, unberührt und Referenzlevel S: Definition unverändert aus H2, der Scan importiert sie aus scan/liquidity_sweep_scan.py
- Wick der laufenden Stunde: Oberkante T = min(Open, Rebound-Hoch), W = T − Tief
- Setup: W ≥ k_atr × ATR14 der abgeschlossenen 1h-Kerzen und Tief < S ≤ T
- Einstieg Long als ruhende Limit-Order bei T − pb_w × W (Maker, Post-Only), platziert nur solange der letzte Schlusskurs darüber liegt
- TP als ruhende Limit-Order bei T + tp_w × W (Maker), SL per Stop-Market bei Tief − sl_w × W (Taker)
- Einstiegsorder wird gelöscht, sobald das Setup erlischt, und verfällt zur vollen Stunde
- ein Trade pro Stunde, Zeitstopp 6 h
- Risiko und Ziel: (1 − pb_w + sl_w) × W gegen (pb_w + tp_w) × W, bei pb_w = 0,2 und tp_w = 0,5 also 1,0 W gegen 0,7 W, in H2 war es 1,2 W gegen 0,5 W

**Vorab festgelegtes Raster** (In-Sample 2023-01-01 bis 2026-04-30, 16 Varianten): Seite untere/obere, k_atr 1,0/1,5, pb_w 0,2/0,4, tp_w 0,5/1,0. Fest: sl_w = 0,2, sw = 3, Zeitstopp 360 min.

**Abgleich Nautilus gegen numba-Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04)

| Seite | k | pb_w | tp_w | Quelle | Trades | TP-Quote | R brutto | R netto | t-Wert | R ohne Top 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| untere | 1,5 | 0,2 | 0,5 | numba | 152 | 51,3 % | +0,04 | +0,005 | +0,1 | −0,01 |
| untere | 1,5 | 0,2 | 0,5 | Nautilus | 142 | 50,0 % | +0,02 | −0,008 | −0,1 | −0,02 |
| untere | 1,5 | 0,4 | 0,5 | numba | 90 | 42,2 % | +0,06 | +0,013 | +0,1 | −0,03 |
| untere | 1,5 | 0,4 | 0,5 | Nautilus | 93 | 40,9 % | +0,02 | −0,019 | −0,2 | −0,06 |
| obere | 1,5 | 0,2 | 1,0 | numba | 155 | 33,5 % | +0,05 | +0,009 | +0,1 | −0,01 |
| obere | 1,5 | 0,2 | 1,0 | Nautilus | 139 | 29,5 % | +0,00 | −0,041 | −0,5 | −0,07 |
| untere | 1,0 | 0,2 | 0,5 | numba | 425 | 54,6 % | +0,01 | −0,034 | −0,8 | −0,04 |
| untere | 1,0 | 0,2 | 0,5 | Nautilus | 391 | 53,7 % | −0,00 | −0,047 | −1,1 | −0,05 |
| obere | 1,0 | 0,2 | 0,5 | numba | 405 | 53,1 % | −0,03 | −0,081 | −1,9 | −0,09 |
| obere | 1,0 | 0,2 | 0,5 | Nautilus | 359 | 52,4 % | −0,03 | −0,078 | −1,8 | −0,08 |

**Raster (16 Varianten, In-Sample, Scan):** drei Varianten netto knapp positiv (+0,005 bis +0,013 R), alle mit t-Werten um 0,1 und alle negativ ohne die drei besten Trades. In Nautilus gerechnet kippen alle drei ins Minus. Die übrigen 13 Varianten sind schon im Scan netto negativ und der Scan rechnet H3 systematisch zu gut (siehe unten), deshalb wurden sie nicht einzeln in Nautilus nachgerechnet.

**Befund zum Scan als Vorfilter:** für H3 ist der Scan deutlich unzuverlässiger als für H1 und H2. Deckung mit Nautilus nur 70 bis 89 % bei einem Versatz von +1 Minute (88 bis 94 % in einem Fenster von 0 bis 10 Minuten), gegenüber 96 bis 98 % bei H1 und H2. Der Scan nimmt rund 8 % mehr Trades und liegt netto 0,01 bis 0,05 R zu hoch. Grund ist die ruhende Einstiegsorder: der Scan füllt sie schon in der Minute, in der das Setup entsteht, Nautilus erst ab der Folgeminute, und die Order wandert mit der Wick mit. Für Hypothesen mit Limit-Einstieg ist der Scan also nur zur Vorauswahl der Größenordnung brauchbar, entschieden wird in Nautilus.

Der Versatz von +1 Minute entspricht dem Verhalten bei H1 (ruhende Stop-Order) und nicht dem von H2, wo der Market-Einstieg auf derselben Minute fällt.

**Entscheidung:** abgelehnt. Kein OOS-Test. Der Rücklauf-Einstieg wirkt in die erwartete Richtung: brutto steigt gegenüber H2 von +0,05 auf +0,06 R im Scan, das Risiko sinkt von 1,2 W auf 1,0 W und die Einstiegsgebühr halbiert sich von Taker auf Maker. Das reicht aber nicht über null. Der Preis dafür ist sichtbar: die Limit-Order füllt nur in etwa jedem dritten Setup der H2-Grundgesamtheit (142 gegenüber 198 Trades bei k = 1,5), und die TP-Quote fällt von 63 % auf 50 %, weil der Rücklauf oft gleich bis in den Stop durchläuft.

Damit ist die Idee Sweep als Umkehrsignal in zwei Einstiegsvarianten geprüft und beide Male netto negativ. Weitere Varianten derselben Geometrie sind nicht aussichtsreich, ohne eine neue Zutat. Offene Folgegedanken für eigene Einträge:

- Einstieg nur zulassen, wenn der Rücklauf über dem gesweepten Level S bleibt, also die Rückeroberung erhalten bleibt. In H3 darf der Einstieg unter S liegen, wenn S hoch in der Wick sitzt
- Sweep auf einem höheren Zeitrahmen (Swing-Level aus 4h statt 1h), damit mehr ruhende Liquidität am Level liegt
