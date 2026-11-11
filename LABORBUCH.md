# Laborbuch

Jede Hypothese bekommt einen Eintrag, bevor gerechnet wird. Ergebnisse netto nach Gebühren (Maker 0,01 %, Taker 0,03 %).
Out-of-Sample ab 2026-05-01 ist gesperrt, bis die Parameter einer Hypothese final feststehen.

| Nr | Hypothese | Status | Ergebnis |
|---|---|---|---|
| H1 | Lange 1h-Wicks werden nach 20 % Füllung bis 80 % weiter gefüllt | abgelehnt | kein Edge, brutto ±0, netto −0,1 bis −0,2 R |
| H2 | Sweep eines unberührten Swing-Levels kehrt um, Ziel über der Wickbasis | abgelehnt | kein Edge, brutto ±0 bis +0,05, netto −0,006 bis −0,11 R |
| H3 | Wie H2, aber Einstieg per Limit auf einem Rücklauf unter die Wickbasis | abgelehnt | besser als H2, aber in Nautilus netto −0,008 bis −0,078 R |
| H4 | Wie H3, aber der Einstieg muss über dem gesweepten Level liegen | abgelehnt | erster messbarer Effekt (+0,02 R, obere Seite +0,05 R), aber nicht signifikant |
| H5 | Wie H3, aber Swing-Level aus 4h-Kerzen statt 1h | abgelehnt | klar schlechter als H3, −0,10 R im Mittel |
| H6 | ETH: Wick ab 60 USD Kerzenspanne, Stop knapp über der Wick-Oberkante, Ziel 80 oder 100 % | abgelehnt | Scan netto −0,26 bis +0,17 R, Nautilus t-Werte unter 0,5, ohne Top 3 bei null |
| H7 | ETH: Limit-Short beim Rücklauf bis 10 bis 15 % vor den Open nach Bewegung ab 30 USD, Ziel 50 % | abgelehnt | alle 48 Varianten schon brutto negativ, netto −0,09 bis −0,40 R |
| H8 | ETH: freie Parametersuche über Rücklauf-Setups mit Filtern und Trade-Management | abgelehnt | kein über Zeiträume stabiler Vorteil, beste Varianten kippen außerhalb des Suchzeitraums |
| H9 | ETH und BTC: Wick nach Spike ab 2 % in höchstens 5 Minuten zur Hälfte füllen | abgelehnt | Scan +0,10 bis +0,17 R, Nautilus −0,15 bis +0,04 R, ohne Top 3 überall ≤ 0 |
| H10 | Wie H9, aber weiterer Stop und Laufenlassen | OOS bestanden, nur BTC obere Seite, Beobachtung | In-Sample +0,13 R (t 4,3), OOS 17 Trades +0,11 R (t 1,0) |
| H11 | H10 (BTC obere Seite) häufiger: kleinere Spikes, längere Spikes, SOL und XRP | abgelehnt | mehr Trades nur mit deutlich weniger R pro Trade, SOL und XRP ohne Effekt |
| H12 | H10-Trades mit Liquidationen im Spike laufen besser (Short-Squeeze als Ursache) | nicht gestützt | mehr Liquidationen +0,07 R besser, t 1,1, Kriterium (+0,1 R, t > 2) verfehlt |
| H13 | H10 nur, wenn vor dem Spike die Shorts überwiegen (Premium oder Kontenverhältnis) | geplant | offen |
| H14 | Long-Liquidationskaskade nach unten, Long auf den Rücklauf | geplant | offen |
| H15 | Extremes Premium bzw. Funding kehrt sich über 1 bis 3 Tage um | geplant, braucht Funding im Lab | offen |
| H16 | BTC-Trend auf Tagesbasis als zweites Standbein mit wenigen Trades | geplant | offen |

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

- Einstieg nur zulassen, wenn der Rücklauf über dem gesweepten Level S bleibt: als H4 geprüft, erster messbarer Effekt, aber nicht signifikant
- Swing-Level aus 4h statt 1h: als H5 geprüft, klar schlechter

---

## H4: Rücklauf-Einstieg mit erhaltener Rückeroberung

**Idee (Gregor, 24.10.2026):** In H3 darf die Einstiegs-Limit-Order unter dem gesweepten Level S liegen, wenn S hoch in der Wick sitzt. Dann ist die Rückeroberung des Levels beim Einstieg schon wieder verloren und das Setup widerspricht seiner eigenen Begründung. H4 verlangt, dass der Einstieg über S bleibt.

**Regeln** (strategies/sweep_reclaim.py, scan/sweep_reclaim_scan.py, Schalter reclaim = True, lvl_tf = 1)

- alles wie H3, zusätzlich: Setup nur gültig, wenn S < T − pb_w × W, also das Einstiegslevel strikt über dem gesweepten Level liegt
- die Bedingung ersetzt eine Prüfung über den Zeitverlauf: da die Limit-Order über S liegt, füllt sie zwangsläufig, bevor der Kurs S wieder unterschreitet

**Vorab festgelegtes Raster:** identisch zu H3, damit die Zahlen direkt vergleichbar sind (16 Varianten, Seite untere/obere, k_atr 1,0/1,5, pb_w 0,2/0,4, tp_w 0,5/1,0, fest sl_w = 0,2, sw = 3, Zeitstopp 360 min).

**Korrektheitsprüfung:** mit reclaim = False und lvl_tf = 1 reproduzieren Scan und Strategie H3 Trade für Trade, über alle 16 Varianten im Scan und in drei Nautilus-Läufen. Die verallgemeinerte Level-Mechanik ist damit abgesichert (`python -m scan.sweep_reclaim_scan --pruefe`).

**Wirkung des Filters, Scan über alle 16 Varianten gegen H3**

| | Mittel netto gegen H3 | besser in | Trades gegenüber H3 |
|---|---|---|---|
| alle 16 Varianten | +0,019 R | 10 von 16 | 73 % |
| nur untere Seite | −0,010 R | 3 von 8 | |
| nur obere Seite | +0,047 R | 7 von 8 | |

Der Filter wirkt nur auf der oberen Seite, also beim Sweep eines Swing-Hochs. Dort verbessert er 7 von 8 Varianten, auf der unteren Seite ist er neutral bis schädlich. Er entfernt insgesamt 27 % der Trades, und die entfernten sind im Schnitt Verlierer.

**Abgleich Nautilus gegen numba-Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04)

| Seite | k | pb_w | tp_w | Quelle | Trades | TP-Quote | R brutto | R netto | t-Wert | R ohne Top 3 |
|---|---|---|---|---|---|---|---|---|---|---|
| obere | 1,5 | 0,2 | 1,0 | numba | 117 | 35,9 % | +0,10 | +0,058 | +0,7 | +0,03 |
| obere | 1,5 | 0,2 | 1,0 | Nautilus | 104 | 31,7 % | +0,05 | +0,008 | +0,1 | −0,03 |
| obere | 1,5 | 0,4 | 0,5 | numba | 43 | 41,9 % | +0,13 | +0,070 | +0,5 | −0,01 |
| obere | 1,5 | 0,4 | 0,5 | Nautilus | 47 | 42,6 % | +0,14 | +0,085 | +0,6 | +0,02 |
| untere | 1,0 | 0,2 | 0,5 | numba | 355 | 54,6 % | +0,02 | −0,021 | −0,5 | −0,03 |
| untere | 1,0 | 0,2 | 0,5 | Nautilus | 325 | 54,5 % | +0,02 | −0,021 | −0,5 | −0,03 |

Deckung 71 bis 91 % bei Versatz +1 Minute, 89 bis 91 % im Fenster 0 bis 10 Minuten, wie bei H3. Der Scan rechnet die stärkste Variante deutlich zu gut: +0,058 R im Scan gegen +0,008 R in Nautilus.

**Entscheidung H4:** abgelehnt als handelbare Regel, aber der Filter selbst ist der erste Befund im Labor, der messbar in die richtige Richtung wirkt. In Nautilus bleibt nur eine Variante netto positiv (obere Seite, k = 1,5, pb_w = 0,4, tp_w = 0,5: +0,085 R) und die hat 47 Trades in 40 Monaten bei t = 0,6. Das ist die beste von 16 Zellen und damit kein Nachweis. Brutto ist mit +0,14 R der höchste Wert im Labor bisher.

**Kein OOS-Test, bewusst.** Der OOS-Zeitraum ab 2026-05-01 umfasst knapp sechs Monate. Bei 47 Trades in 40 Monaten wären das etwa 7 Trades, bei der 117er-Variante etwa 15. Damit ist keine Entscheidung möglich, der Zeitraum bleibt für eine Hypothese mit genug Trades reserviert.

Festhalten für künftige Hypothesen: die Bedingung Einstieg über dem gesweepten Level gehört auf der oberen Seite in jede Sweep-Regel, sie kostet 27 % der Trades und bringt im Mittel +0,05 R. Offener Folgegedanke: dieselbe Geometrie mit deutlich mehr Trades, etwa Wick und Level auf 15m statt 1h, damit eine Variante überhaupt in den Bereich statistischer Aussagekraft kommt.

---

## H5: Rücklauf-Einstieg mit Swing-Leveln aus 4h

**Idee (Gregor, 24.10.2026):** Swing-Level aus 1h-Kerzen sind häufig und flach. An einem Level aus einem höheren Zeitrahmen liegt mehr ruhende Liquidität, der Sweep sollte dort aussagekräftiger sein.

**Regeln** (strategies/sweep_reclaim.py, scan/sweep_reclaim_scan.py, Schalter reclaim = False, lvl_tf = 4)

- alles wie H3, aber Swing-Tiefs werden auf 4h-Kerzen bestimmt: eine 4h-Kerze, deren Tief strikt unter den Tiefs der sw 4h-Kerzen davor und danach liegt, bestätigt sw × 4 Stunden später
- unberührt wird gegen abgeschlossene 4h-Kerzen geprüft
- Wick, ATR14 und alle Ein- und Ausstiegslevel bleiben auf 1h beziehungsweise 1m, nur die Herkunft von S ändert sich

**Vorab festgelegtes Raster:** identisch zu H3 und H4 (16 Varianten).

**Abgleich Nautilus gegen numba-Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04)

| Seite | k | pb_w | tp_w | Quelle | Trades | R brutto | R netto | t-Wert |
|---|---|---|---|---|---|---|---|---|
| untere | 1,5 | 0,4 | 0,5 | numba | 53 | +0,04 | +0,001 | +0,0 |
| untere | 1,5 | 0,4 | 0,5 | Nautilus | 53 | −0,04 | −0,081 | −0,6 |
| obere | 1,0 | 0,2 | 0,5 | numba | 197 | +0,03 | −0,022 | −0,4 |
| obere | 1,0 | 0,2 | 0,5 | Nautilus | 170 | −0,02 | −0,064 | −1,0 |

**Wirkung gegen H3, Scan über alle 16 Varianten:** Mittel −0,097 R, besser in nur 2 von 16 Zellen, 52 % der Trades von H3. Auf der unteren Seite ist keine einzige Variante besser als H3.

**Entscheidung H5:** abgelehnt. Die Annahme, an 4h-Leveln liege mehr ruhende Liquidität und der Sweep sei dort aussagekräftiger, bestätigt sich nicht, das Gegenteil tritt ein. Im Scan ist keine Variante netto über +0,001 R, in Nautilus sind beide nachgerechneten Varianten klar negativ, und die schlechteste Zelle (obere Seite, k = 1,5, pb_w = 0,4) liegt mit −0,37 bis −0,42 R bei t = −2,8 deutlich im Minus. Kein OOS-Test.

Mögliche Erklärung, nicht geprüft: ein 4h-Swing-Tief wird seltener unberührt gesweept, und wenn doch, ist der Durchstich Teil einer größeren Bewegung statt eines Stop-Hunts. Die Umkehrannahme passt dort nicht.

---

## H6: Wick-Füllung ETH mit Stop an der Oberkante

**Idee (Gregor, 11.11.2026):** Eine große 1h-Kerze spannt sich innerhalb der Stunde auf, läuft zurück und füllt die Wick danach wieder. Läuft der Kurs über die Wick-Oberkante hinaus, ist die Idee widerlegt. Der Stop sitzt deshalb knapp über der Oberkante und nicht im gleichen Abstand wie das Ziel.

**Markt:** PF_ETHUSD auf Kraken Futures, erste Hypothese außerhalb von BTC. Das Symbol ist per Umgebungsvariable TRADO_SYMBOL umschaltbar, Standard bleibt PF_XBTUSD.

**Regeln** (strategies/wick_fill.py und scan/wick_fill_scan.py, erweitert um min_span und min_share)

- Wick der laufenden Stunde wie H1: W = min(Open, Rebound-Hoch) − Tief, obere Wick spiegelbildlich mit Long
- Setup nur, solange die bisherige Spanne der Stunde (Hoch − Tief) mindestens 60 USD beträgt und W mindestens 65 % dieser Spanne ausmacht. Keine ATR-Bedingung (k_atr = 0)
- Einstieg per Stop-Market bei 10 % Füllung (fill_in = 0,1)
- TP als Limit bei fill_out × W, SL per Stop-Market bei Oberkante + Puffer, also sl_w = 0,1 + Puffer
- Ein Trade pro Stunde, nicht ausgelöste Einstiegsorder verfällt zur vollen Stunde, Zeitstopp 24 h (hold_min = 1440)

**Vorab festgelegtes Raster** (16 Varianten)

- Seite: untere und obere
- Puffer über der Oberkante: 0, 5, 10 und 20 % von W, also sl_w = 0,10 / 0,15 / 0,20 / 0,30
- Ziel: fill_out = 0,8 und 1,0

**Vorarbeit im Chat (11.11.2026, eigene Skripte außerhalb des Labors, PF_ETHUSD 1m von 2023-01 bis 2026-11)**

- Ziel 45 % Füllung mit Stop im gleichen Abstand: Wick-Größe über ATR, Prozent vom Kurs und Kerzenspanne in USD variiert. Der Hang zur Füllung ist messbar (bei 10 bis 30 USD Spanne 57 % Ziel zuerst gegen 43 %), wird aber von den Gebühren aufgefressen. Bei großen Wicks ab etwa 2,75 % vom Kurs verschwindet er
- Stop an der Oberkante, Spanne ab 60 USD, In-Sample bis 2026-04: Trefferquote rund 7 Prozentpunkte über einem Zufallsverlauf, netto +0,18 bis +0,30 R bei 344 Trades, t-Werte 1,4 bis 2,0. Bei Spanne ab 40 USD liegt dieselbe Regel bei null
- Insgesamt rund 60 Varianten angesehen. Das Raster oben stammt aus dieser Suche und ist damit nicht unabhängig
- Der OOS-Zeitraum wurde dabei berührt: 10 Trades der Variante ab 60 USD gesehen, überwiegend Verluste. Ein Lauf mit --oos ist für H6 deshalb keine saubere Prüfung mehr. Belastbar wäre nur das Mitprotokollieren neuer Fälle ab 12.11.2026
- Abweichungen der Chat-Skripte von dieser Regel: Setup wurde einmal ausgelöst und nicht laufend neu geprüft, Einstieg war auch nach Ablauf der Stunde möglich

**Scan über das Raster** (11.11.2026, In-Sample 2023-01 bis 2026-04, `TRADO_SYMBOL=PF_ETHUSD python -m scan.wick_fill_scan --h6`)

- Untere Wick (Short): 180 bis 187 Trades, brutto +0,03 bis +0,16 R, netto −0,26 bis −0,01 R, keine Variante positiv
- Obere Wick (Long): 89 Trades, brutto +0,15 bis +0,35 R, netto −0,05 bis +0,17 R, beste Variante sl_w = 0,30 und fill_out = 0,8 mit t = 1,05. 2026 in 7 von 8 Varianten um −1 R
- Jahre widersprüchlich, 2023 mit wenigen Trades durchgehend um −1 R

**Nautilus, die zwei Varianten aus der Chat-Vorarbeit** (runs/20261111-*_PF_ETHUSD_*)

| Seite | sl_w | fill_out | Trades | TP-Quote | R brutto | R netto | t-Wert | ohne Top 3 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| untere | 0,15 | 1,0 | 193 | 19,7 % | +0,29 | +0,09 | +0,46 | −0,00 | −1,20 | +0,19 | −0,12 | +1,52 |
| untere | 0,20 | 0,8 | 196 | 26,0 % | +0,09 | −0,05 | −0,36 | −0,11 | −1,15 | +0,03 | −0,20 | +0,81 |
| obere | 0,15 | 1,0 | 90 | 24,4 % | +0,35 | +0,16 | +0,47 | −0,04 | −1,15 | +0,49 | +0,12 | −1,27 |
| obere | 0,20 | 0,8 | 91 | 31,9 % | +0,23 | +0,09 | +0,45 | −0,02 | −0,30 | +0,20 | +0,14 | −1,20 |

Nautilus rechnet etwas besser als der Scan (z. B. untere Seite 0,15/1,0: +0,09 gegen −0,04 R), die Abweichung liegt im Bereich weniger großer Gewinner. Nach Abzug der 3 besten Trades bleibt in keiner Variante etwas übrig.

**Entscheidung H6:** abgelehnt. Mit den Labor-Regeln (Setup laufend geprüft, Einstiegsorder verfällt zur vollen Stunde, Fills über Nautilus) verschwindet der Vorteil aus der Chat-Vorarbeit. Dort lag er bei +0,18 bis +0,30 R mit 344 Trades. Er hängt also an Details der Umsetzung, vor allem am Einstieg nach Ablauf der Stunde, und ist kein robuster Effekt. Die TP-Quote liegt zwar über einem Zufallsverlauf, das reicht nach Gebühren aber nicht. Kein OOS-Test, der Zeitraum ist für H6 ohnehin berührt.

Festhalten: Der Hang von ETH-Wicks zur Füllung ist auf 1h messbar (Chat-Vorarbeit), aber klein. Bei kleinen Wicks fressen ihn die Gebühren, bei großen verschwindet er. Ein enger Stop an der Wick-Oberkante verbessert das Chance-Risiko-Verhältnis, macht die Regel aber empfindlich für Ausführungsdetails.

---

## H7: Limit-Short beim Rücklauf zum Open (ETH)

**Idee (Gregor, 11.11.2026):** Der Kurs bewegt sich innerhalb einer Stunde mindestens 30 USD vom Open weg und läuft in derselben Stunde bis auf 10 bis 15 % der Bewegung an den Open zurück. Dort Einstieg gegen den Rücklauf, Ziel 50 % Füllung, Stop leicht über dem Open.

**Regeln** (Skript außerhalb des Repos, Labordaten PF_ETHUSD, In-Sample 2023-01 bis 2026-04)

- Bewegung M = Open − bisheriges Extrem der Stunde, Setup ab M ≥ 30 USD, obere Seite spiegelbildlich mit Long
- Limit-Order bei Open − f × M (Maker), läuft bei neuem Extrem mit, nur innerhalb der Stunde
- Ziel Limit bei Open − 0,5 × M, Stop bei Open + s × M (Taker)
- Raster: f = 0,10 und 0,15, s = 0 / 0,05 / 0,10 / 0,15 / 0,20 / 0,30, Stundenende glattstellen, Stop auf Einstieg oder weiterlaufen lassen (72 Varianten)

**Ergebnis:** Alle Varianten schon brutto negativ (−0,03 bis −0,13 R), netto −0,09 bis −0,40 R bei t-Werten um −3 bis −5. Die Trefferquote liegt in jeder Variante leicht unter der eines Zufallsverlaufs mit gleichem Chance-Risiko-Verhältnis. Fast alle Trades entscheiden sich in 2 bis 11 Minuten.

**Entscheidung H7:** abgelehnt. Ein Rücklauf bis kurz vor den Open hat Schwung und läuft meist durch den Open, statt wieder halb in die Kerze zu fallen. Kein OOS-Test.

---

## H8: Freie Parametersuche über Rücklauf-Setups (ETH)

**Anlass (11.11.2026):** Nach H6 und H7 bewusst breite Suche, um zu sehen, ob irgendeine Variante der Wick- und Rücklauf-Idee trägt. Diese Suche verletzt das Protokoll mit wenigen vorab genannten Varianten absichtlich und ist deshalb nur als Erkundung zu werten.

**Vorgehen** (Skripte außerhalb des Repos, Labordaten PF_ETHUSD)

- Zwei Einstiegsarten: Limit beim Rücklauf (wie H7) oder Stop-Order nach der Umkehr (Rücklaufhoch − p × M)
- Variiert: Mindestbewegung 10 bis 100 USD, Mindest-Rücklauf 50 bis 95 %, Einstieg, Ziel 40 bis 100 %, Stop über Open bzw. Rücklaufhoch, Einstiegsfenster, Seite, Slippage 0 / 0,2 / 0,5 / 1 USD
- Gesucht auf 2023 bis 2024, geprüft auf 2025 bis 2026-04, insgesamt rund 25.000 Varianten
- Danach Filter (12 h ruhig, kein neues 24h-Extrem, Bewegung in höchstens 10 Minuten), Trade-Management (Nachziehen, Teilgewinn, Zeitstopp) und Hebel für mehr Trades (Grenze in ATR, 30m-Perioden, gleitender Startpunkt)

**Befunde**

- Ein erster Durchlauf sah sehr gut aus, das lag an einem Fehler: Stop-Einstiege wurden nicht zum schlechteren Eröffnungskurs der Folgeminute gefüllt. Nach Korrektur und mit 0,50 USD Slippage liegen die 20 besten Varianten aus 2023 bis 2024 im Prüfzeitraum bei −0,04 R
- Einstieg nach der Umkehr ist klar besser als Limit in den Rücklauf (18 % gegen 1 % der Varianten positiv)
- Kleine Bewegungen haben brutto einen leichten Vorteil, Gebühren und Slippage kosten bei 1 bis 3 USD Risiko aber 0,3 bis 0,5 R
- Ungewöhnlich große oder sehr schnelle Bewegungen (ab 2 × ATR, in höchstens 10 Minuten) füllen sich deutlich schlechter, diese Filter verschlechtern jede Variante
- Kein neues 24h-Extrem plus ruhige 12 h davor verbessert um etwa +0,02 R, macht aber keine Variante robust positiv
- Feste Ziele schlagen jedes Nachziehen und jeden Teilgewinn, Zeitstopp ändert kaum etwas
- Auf einen Zeitraum optimierte Varianten verlieren im jeweils anderen (beste auf 2025 bis 2026-04: +0,55 R, in 2023 bis 2024: −0,31 R)

**OOS-Zeitraum berührt:** Für drei Kandidaten wurde der Zeitraum ab 2026-05-01 gerechnet: Long-Variante ab 50 USD (2 Trades, −2,6 R), häufige Variante ab 30 USD (50 Trades, −0,32 R), Filter-Kandidaten (4 bis 19 Trades, −0,16 bis +0,44 R).

**Entscheidung H8:** abgelehnt. Kein Rücklauf-Setup auf ETH 1h trägt über Zeiträume und realistische Ausführung. Die Lehren daraus fließen in H9 ein: Einstieg erst nach der Umkehr, nur große Bewegungen, bescheidenes Ziel.

---

## H9: Wick nach Spike zur Hälfte füllen (ETH und BTC)

**Idee (Gregor, 11.11.2026):** Nach einem Liquidations-Spike wie am 2026-11-08 um 21:55 UTC (ETH −155 USD in einer Minute) wird die Wick gefüllt, wenn man nach dem Ende der Erholung einsteigt und Geduld hat.

**Markt:** PF_ETHUSD und PF_XBTUSD, beide Richtungen

**Regeln** (scan/spike_fill_scan.py, strategies/spike_fill.py, untere Seite, obere spiegelbildlich)

- Spike: Tief einer Minute ist das tiefste der letzten 5 Minuten und liegt mindestens 2 % unter dem Hoch S dieser 5 Minuten. Läuft der Spike in den nächsten 5 Minuten weiter, gilt das neue Tief L. M = S − L
- Nach einem Spike frühestens 15 Minuten später wieder ein neuer
- Erholung: Erholungshoch RH seit dem Tief, W = RH − L. Setup gültig ab W ≥ 0,3 × M, verfällt bei neuem Tief nach den ersten 5 Minuten oder 180 Minuten nach dem Tief
- Einstieg Short per Stop-Market bei RH − 0,1 × W, nachdem die Erholung gestoppt hat
- TP als Limit bei RH − 0,5 × W (halbe Füllung zurück zum Tief), SL per Stop-Market bei RH + 0,1 × W
- Zeitstopp 72 h
- Gebühren wie immer, im Scan 0,02 % Slippage auf Stop- und Market-Orders

**Feste Parameter:** spike = 0,02, rb_min = 0,3, fill_in = 0,1, fill_out = 0,5, sl_w = 0,1, window = 180, hold_min = 4320. Keine weitere Variation im Labor.

**Vorarbeit im Chat (11.11.2026, liq.py außerhalb des Repos, 2023-01 bis 2026-11):** 40 vorab festgelegte Kombinationen je Markt (Spike 1 / 1,5 / 2 / 3 %, mit und ohne Volumenfilter, drei Muster mit fünf Ausstiegen). Nur dieses Muster war in beiden Märkten und allen Zeiträumen positiv:

| Markt | Trades | R 2023 bis 2024 | R 2025 bis 2026-04 | R ab 2026-05 | nur 1. Spike je Tag |
|---|---|---|---|---|---|
| ETH | 567 | +0,04 | +0,16 | +0,18 (51) | +0,08, t 1,1 |
| BTC | 270 | +0,07 | +0,44 | +0,02 (22) | +0,11, t 1,0 |

- Verwandte Muster negativ: Limit-Short bei 50 % Erholung −0,01 bis −0,13 R, Long auf die Erholung −0,11 bis −0,33 R, Volumenfilter verschlechtert
- Der OOS-Zeitraum wurde in der Vorarbeit mitgerechnet (zusammen mit allen Kombinationen, nicht zur Auswahl genutzt). Der Lauf mit --oos im Labor ist deshalb keine unberührte Prüfung, sondern die realistische Nachrechnung desselben Zeitraums
- Spikes kommen gehäuft (ETH an 59 Tagen drei oder mehr), die effektive Stichprobe ist deutlich kleiner als die Zahl der Trades
- Echte Bestätigung nur durch Mitprotokollieren neuer Fälle ab 2026-11-12, falls der Nautilus-Test trägt

**Scan im Labor** (11.11.2026, In-Sample 2023-01 bis 2026-04, `TRADO_SYMBOL=... python -m scan.spike_fill_scan`)

| Markt | Seite | Trades | TP-Quote | R brutto | R netto | t-Wert |
|---|---|---|---|---|---|---|
| ETH | untere | 312 | 50,6 % | +0,12 | −0,01 | −0,2 |
| ETH | obere | 204 | 65,7 % | +0,43 | +0,28 | +3,4 |
| BTC | untere | 133 | 51,1 % | +0,16 | +0,03 | +0,3 |
| BTC | obere | 115 | 66,1 % | +0,46 | +0,32 | +2,9 |

Der Scan reproduziert die Vorarbeit genau (ETH beide Seiten 516 Trades, +0,105 R, BTC 248 Trades, +0,166 R). Die Trennung nach Seiten war nicht vorab festgelegt.

**Nautilus** (runs/20261111-2004*_spike_fill_*)

| Markt | Seite | Trades | TP-Quote | R brutto | R netto | t-Wert | ohne Top 3 | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ETH | untere | 324 | 44,8 % | +0,04 | −0,11 | −1,5 | −0,16 | −0,26 | −0,27 | −0,00 | +0,10 |
| ETH | obere | 223 | 42,2 % | +0,05 | −0,15 | −1,6 | −0,23 | +0,12 | −0,09 | −0,27 | −0,24 |
| BTC | untere | 138 | 35,5 % | +0,02 | −0,12 | −1,1 | −0,18 | −0,18 | −0,17 | −0,10 | +0,48 |
| BTC | obere | 124 | 50,8 % | +0,20 | +0,04 | +0,4 | −0,01 | +0,16 | +0,11 | −0,20 | −0,10 |

**Warum Scan und Nautilus so weit auseinanderliegen**

- Nur rund zwei Drittel der Scan-Trades haben in Nautilus ein Gegenstück. Die fehlenden sind die besten Scan-Trades (ETH obere Seite +0,36 R). Der Scan steigt in der Minute ein, in der die Erholung ihr Hoch macht und wieder fällt, und unterstellt dafür die Reihenfolge Hoch vor Tief. Nautilus kann die Stop-Order erst nach Abschluss der Minute auf das neue Niveau setzen
- In Spike-Phasen springt der Kurs oft in derselben Minute über Einstieg und Stop. Die Stop-Order nach dem Einstieg wird dann von der Börse abgelehnt und die Position sofort geschlossen, mit Verlusten bis etwa −4 R. Der Scan prüft den Stop erst ab der Folgeminute
- Auch bei gemeinsamen Trades rechnet Nautilus schlechter (ETH obere Seite +0,24 R im Scan, −0,03 R in Nautilus)

**Fehler beim Bau der Strategie, behoben vor der Wertung:** Spike-Erkennung prüfte zunächst eine falsche Pufferlänge (0 Trades). Ein abgelehnter Stop nach dem Einstieg ließ Positionen ungeschützt 72 h laufen (Einzeltrades bis −55 R). Jetzt schließt die Strategie bei abgelehnter Ausstiegsorder sofort per Market.

**Entscheidung H9:** abgelehnt. Realistisch ausgeführt ist die Regel auf beiden Märkten und beiden Seiten nicht positiv, die einzige knapp positive Zelle (BTC obere Seite) hängt an den drei besten Trades. Kein OOS-Lauf, kein Protokoll-Skript.

Festhalten für künftige Hypothesen: Scans mit sehr engen Einstiegen und Stops (unter etwa 0,3 % vom Kurs) und Einstieg in der Minute der Umkehr überschätzen das Ergebnis deutlich, weil die Reihenfolge innerhalb einer Minute angenommen wird. Das betrifft auch die Chat-Vorarbeit zu H6 bis H8. Solche Regeln nur mit Nautilus bewerten oder mit Trade-Ticks rechnen.

---

## H10: Spike-Füllung mit weiterem Stop und Laufenlassen (ETH und BTC)

**Idee (Gregor, 11.11.2026):** H9 ist in Nautilus vor allem am engen Stop gescheitert, der in Spike-Minuten übersprungen wird. Mit mehr Abstand und der Möglichkeit, Gewinner laufen zu lassen, könnte die Regel tragen.

**Regeln** (strategies/spike_fill.py, erweitert um sl_ref, trail_start, trail_w)

- Spike, Erholung und Einstieg unverändert wie H9 (spike = 0,02, rb_min = 0,3, fill_in = 0,1, window = 180, cooldown = 15)
- Stop wahlweise über dem Erholungshoch (sl_ref = rh: RH + sl_w × W) oder über dem Spike-Start (sl_ref = start: S + sl_w × M)
- Laufenlassen (trail_w > 0): kein festes Ziel. Sobald der Kurs trail_start × W vom Erholungshoch Richtung Tief gelaufen ist, Stop auf den tatsächlichen Einstieg, danach nach jeder Minute auf bestes Niveau + trail_w × W nachziehen, nur in Gewinnrichtung
- Zeitstopp 72 h, Gebühren wie immer, nur Nautilus (der Scan überschätzt solche Regeln, siehe H9)

**Vorab festgelegtes Raster** (9 Kombinationen je Markt und Seite, 36 Läufe, nur In-Sample bis OOS_START)

- Stop: rh mit sl_w = 0,3, rh mit sl_w = 0,5, start mit sl_w = 0,1
- Ausstieg: festes Ziel fill_out = 0,5, festes Ziel fill_out = 1,0, Laufenlassen mit trail_start = 0,5 und trail_w = 0,5

**Nautilus, In-Sample 2023-01 bis 2026-04** (runs/20261111-2100_spike_fill_H10_raster, R netto)

| Markt | Seite | Stop | Ziel 50 % | Ziel 100 % | laufen lassen |
|---|---|---|---|---|---|
| ETH | untere | rh 0,3 / rh 0,5 / start 0,1 | −0,04 / −0,04 / −0,02 | −0,04 / −0,05 / −0,02 | −0,05 / −0,05 / −0,03 |
| ETH | obere | rh 0,3 / rh 0,5 / start 0,1 | −0,06 / +0,01 / +0,02 | −0,08 / +0,02 / +0,04 | −0,16 / −0,05 / −0,01 |
| BTC | untere | rh 0,3 / rh 0,5 / start 0,1 | −0,18 / −0,13 / −0,11 | −0,17 / −0,08 / −0,07 | −0,03 / −0,02 / −0,06 |
| BTC | obere | rh 0,3 / rh 0,5 / start 0,1 | +0,07 / +0,13 / +0,13 | +0,27 / +0,25 / +0,21 | −0,01 / +0,05 / +0,10 |

- Jeder weitere Stop verbessert gegenüber H9 (dort −0,11 bis −0,15 R bei ETH)
- Laufenlassen ist in 10 von 12 Gruppen schlechter als ein festes Ziel, wie schon in H8
- ETH bleibt auf beiden Seiten bei null oder leicht negativ, BTC untere Seite negativ
- BTC obere Seite (Spike nach oben, Long nach dem Ende des Rücksetzers) ist in 8 von 9 Varianten positiv. Bestwerte: start 0,1 mit Ziel 50 % +0,13 R bei t = 4,3, TP-Quote 85 %, alle Jahre positiv (+0,16 / +0,11 / +0,12 / +0,16). Start 0,1 mit Ziel 100 % +0,21 R bei t = 3,3. Nur erster Trade je Tag: +0,13 R (t 3,3) bzw. +0,21 R (t 2,5). Rund 3 Trades pro Monat
- Prüfung auf Fills in der Einstiegsminute (Reihenfolge innerhalb der Minute angenommen): Bei BTC obere Seite tragen die länger laufenden Trades das Ergebnis (+0,11 bis +0,41 R, t bis 3,1). Trades mit Ausstieg in der ersten Minute liegen um null

**Einordnung:** 36 Zellen gerechnet, die positive Gruppe ist eine von vier Markt-Seiten-Kombinationen und hat auf ETH kein Gegenstück. Das spricht gegen einen allgemeinen Effekt. Für BTC ist es dennoch das stärkste Ergebnis im Labor bisher. Nächster Schritt laut Protokoll: eine Variante festlegen und einmal mit --oos rechnen (Zeitraum ab 2026-05 für diese Regel unberührt, in der H9-Vorarbeit aber mit engem Stop bereits gesehen).

**Finale Variante für den OOS-Test (festgelegt 2026-11-11 vor dem Lauf):** PF_XBTUSD, side = upper, sl_ref = start, sl_w = 0,1, fill_out = 0,5, sonst wie H9. Auswahlgrund: in allen vier Jahren positiv, höchster t-Wert. Einmaliger Lauf mit --oos ab 2026-05-01.

**OOS-Lauf** (2026-11-11, runs/20261111-203112_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5_OOS, 2026-05-01 bis 2026-11-11)

| Zeitraum | Trades | TP-Quote | R brutto | R netto | t-Wert | ohne Top 3 |
|---|---|---|---|---|---|---|
| In-Sample 2023-01 bis 2026-04 | 124 | 84,7 % | +0,16 | +0,13 | 4,3 | +0,11 |
| OOS 2026-05 bis 2026-11 | 17 | 88,2 % | +0,14 | +0,11 | 1,0 | +0,04 |

- 15 Gewinner mit +0,08 bis +0,51 R, 2 Verlierer mit je −1,04 R, Summe +1,9 R
- Profil mit hoher Trefferquote und kleinen Gewinnen: typischer Gewinn rund +0,25 R gegen −1 R Verlust. Die Gewinnschwelle liegt bei etwa 80 % Treffern. Sinkt die Trefferquote um wenige Prozentpunkte, wird die Regel negativ
- Trades gehäuft in wenigen Phasen (Juni und August 2026)

**Entscheidung H10:** OOS bestanden für BTC obere Seite mit Stop über dem Spike-Start und Ziel 50 %. Wegen kleiner OOS-Stichprobe, fehlendem Gegenstück auf ETH und dem engen Abstand zur Gewinnschwelle noch kein Einsatz in Trado. Nächster Schritt: neue Fälle ab 2026-11-12 mitprotokollieren (Paper), Entscheidung nach etwa 30 weiteren Trades.

---

## H11: Mehr Trades für die H10-Regel

**Ziel (Gregor, 11.11.2026):** Die H10-Regel (BTC, Spike nach oben, Stop über Spike-Start, Ziel 50 %) handelt nur etwa 3-mal im Monat. Gesucht sind mehr Trades ohne schlechteres Ergebnis pro Trade.

**Basis:** strategies/spike_fill.py mit side = upper, sl_ref = start, sl_w = 0,1, fill_out = 0,5, sonst wie H9. In-Sample BTC: 124 Trades, +0,134 R, t 4,3.

**Vorab festgelegte Läufe** (nur Nautilus, nur In-Sample bis OOS_START, je ein Hebel gegenüber der Basis)

- Kleinere Spikes: spike = 0,015 und 0,0175 (BTC)
- Längere Spikes: Spike-Dauer span = 10 und 15 Minuten statt 5, neuer Parameter span (BTC)
- Weitere Märkte: PF_SOLUSD (Tick 0,01) und PF_XRPUSD (Tick 0,0001) mit der Basisregel, Kontrakte neu in lab/instruments.py

**Übernahmekriterium:** R netto pro Trade nicht unter +0,13 und R pro Monat höher als bei der Basis. Der OOS-Zeitraum ist für die H10-Regel verbraucht, übernommene Hebel gelten nur nach Papier-Beobachtung als bestätigt.

**Ergebnis** (2026-11-11, Nautilus, In-Sample 2023-01 bis 2026-04, runs/20261111-204*)

| Lauf | Trades | Trades pro Monat | TP-Quote | R netto | t-Wert | R gesamt | 2023 | 2024 | 2025 | 2026 |
|---|---|---|---|---|---|---|---|---|---|---|
| Basis BTC (2 %, 5 Min.) | 124 | 3,1 | 84,7 % | +0,134 | 4,3 | +16,6 | +0,16 | +0,11 | +0,12 | +0,16 |
| BTC spike = 0,015 | 269 | 6,7 | 76,2 % | +0,022 | 0,8 | +5,9 | +0,06 | +0,03 | −0,07 | +0,03 |
| BTC spike = 0,0175 | 174 | 4,4 | 79,3 % | +0,064 | 2,1 | +11,1 | +0,07 | +0,05 | +0,07 | +0,09 |
| BTC span = 10 | 171 | 4,3 | 81,3 % | +0,061 | 1,9 | +10,4 | +0,05 | +0,08 | −0,03 | +0,19 |
| BTC span = 15 | 207 | 5,2 | 84,5 % | +0,043 | 1,6 | +8,9 | +0,05 | +0,06 | −0,05 | +0,12 |
| SOL Basis | 672 | 16,8 | 68,8 % | −0,027 | −1,3 | −18,1 | −0,05 | −0,01 | −0,03 | +0,03 |
| XRP Basis | 592 | 14,8 | 70,3 % | +0,000 | 0,0 | +0,0 | +0,13 | −0,03 | −0,03 | +0,01 |

- Jeder BTC-Hebel bringt 40 bis 120 % mehr Trades, halbiert aber mindestens das R pro Trade. Der Gesamtgewinn sinkt in allen Fällen gegenüber der Basis
- Die zusätzlichen Trades sind also deutlich schlechter als die der Basis, die 2-%-Grenze in 5 Minuten trennt gute von mittelmäßigen Fällen
- SOL und XRP zeigen keinen Effekt. 2 % sind dort im Verhältnis zur üblichen Schwankung kleiner als bei BTC, ein an die Volatilität angepasster Schwellenwert wurde nicht getestet

**Entscheidung H11:** abgelehnt, die H10-Regel bleibt unverändert. Mit ETH, SOL und XRP gibt es jetzt drei Märkte ohne den Effekt. Das erhöht den Verdacht, dass H10 auf BTC eine Eigenheit oder ein Zufallstreffer ist, und spricht umso mehr für die Papier-Beobachtung vor jedem Einsatz.

---

## H12: Liquidationen als Ursache der H10-Regel

**Idee (Forum-Input, 11.11.2026):** Ein Vorteil entsteht dort, wo jemand zu einem schlechten Preis handeln muss. Bei H10 wäre das ein Short-Squeeze: Liquidierte Shorts kaufen zu jedem Preis, der Spike schießt über, danach läuft ein Teil zurück. Trifft das zu, laufen H10-Trades mit Liquidationen im Spike besser als solche ohne. Ein Unterschied würde H10 erklären, kein Unterschied wäre eine Warnung vor einem Zufallstreffer.

**Daten:** Kraken Futures Analytics, liquidation-volume für PF_XBTUSD als 1-Minuten-Werte ab 2023 (scripts/fetch_analytics.py). Der Wert trennt nicht nach Long und Short. Bei einem Spike nach oben werden aber fast nur Shorts liquidiert.

**Regeln** (festgelegt 2026-11-11 vor dem Rechnen, keine neue Strategie, Auswertung der vorhandenen H10-Trades)

- Trades: finale H10-Variante, In-Sample runs/20261111-204153_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5 (124 Trades), OOS runs/20261111-203112_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5_OOS (17 Trades)
- Spike-Minuten je Trade: Minuten vor dem Einstieg, deren Hoch das höchste der letzten 5 Minuten ist und mindestens 2 % über dem Tief dieser 5 Minuten liegt. Gesucht wird bis 190 Minuten vor dem Einstieg, verwendet wird die letzte zusammenhängende Gruppe (Abstand höchstens 5 Minuten)
- Liquidationsfenster: 4 Minuten vor der ersten bis 1 Minute nach der letzten Spike-Minute
- Kennzahl L: Summe des Liquidationsvolumens im Fenster
- Aufteilung 1: L = 0 gegen L > 0
- Aufteilung 2: L unter gegen ab dem Median der In-Sample-Trades
- Keine weiteren Schnitte und keine Suche nach Schwellen

**Kriterium:** Der Mechanismus gilt als gestützt, wenn in beiden Aufteilungen die Gruppe mit mehr Liquidationen um mindestens 0,1 R besser ist und in mindestens einer Aufteilung der t-Wert der Differenz (Welch) über 2 liegt. Nur dann werden die OOS-Trades einmal mit derselben Aufteilung (Median aus In-Sample) geprüft, dort zählt nur die Richtung. Ein Filter für den spike-bot folgt daraus erst nach Papier-Beobachtung.

**Ergebnis** (2026-11-11, runs/20261111-2200_h12_liquidationen, R netto aus den Nautilus-Trades)

| Aufteilung (In-Sample) | wenig Liquidationen | viel Liquidationen | Differenz | t-Wert |
|---|---|---|---|---|
| L = 0 / L > 0 | 1 Trade | 123 Trades, +0,133 R | nicht auswertbar | |
| L unter / ab Median (7,9 BTC) | 62 Trades, +0,099 R, TP 84 % | 62 Trades, +0,169 R, TP 86 % | +0,07 R | 1,1 |

- Aufteilung 1 ist nicht auswertbar: In 123 von 124 Spikes gab es bei Kraken Liquidationen. Ein Spike ohne Liquidationen kommt praktisch nicht vor
- Aufteilung 2 zeigt die erwartete Richtung, aber zu schwach. Das Kriterium ist verfehlt
- Liquidationsvolumen und Spike-Höhe hängen eng zusammen (Korrelation 0,63, Spike im Mittel 2,6 % gegen 3,4 %). L misst also zu einem großen Teil nur die Größe des Spikes
- Kraken ist ein kleiner Teil des Perp-Markts. Die Liquidationen auf Binance, Bybit und OKX, die einen Squeeze treiben, sind in diesen Daten nicht enthalten

Nicht vorab festgelegt, nur zur Beschreibung (keine Grundlage für Entscheidungen):

- Nach Quartilen von L steigt das R von +0,07 über +0,13 und +0,14 auf +0,20, die Rangkorrelation von L mit R liegt aber bei 0,01
- Nach Spike-Höhe geteilt (Median) +0,06 R gegen +0,21 R. Das wäre eine eigene Hypothese mit eigenem Test
- Das Auswertungsskript hat die OOS-Trades in einem Durchlauf mitberechnet, obwohl sie laut Regel nur bei erfülltem Kriterium dran waren. OOS lag die Richtung umgekehrt (8 Trades +0,27 R gegen 9 Trades −0,03 R). Bei so wenigen Trades sagt das nichts, es wird hier nur der Vollständigkeit halber genannt

**Entscheidung H12:** Mechanismus mit Kraken-Daten nicht gestützt, aber auch nicht widerlegt, weil Kraken die marktweiten Liquidationen kaum abbildet. H10 bleibt unverändert in der Papier-Beobachtung. H13 baut auf H12 auf und wird zurückgestellt, bis es marktweite Liquidationsdaten gibt oder H14 bzw. H15 etwas Neues zeigen.

---

## H13 bis H16: geplante Hypothesen aus dem Forum-Input

Grundsatz: Jede Regel beginnt bei einem Marktteilnehmer, der zu einem schlechten Preis handeln muss. Die Regeln unten sind Entwürfe und werden vor dem jeweiligen Lauf endgültig festgelegt.

- H13 Positionierung vor dem Spike: H10 nur, wenn vor dem Spike-Start die Shorts überwiegen. Messgrößen Basis bzw. Perp minus Spot im Mittel der 60 Minuten davor und das Kontenverhältnis aus long-short-info. Nur sinnvoll, wenn H12 den Mechanismus stützt
- H14 Long-Liquidationskaskade: Liquidationsvolumen in höchstens 5 Minuten weit über dem Üblichen bei fallendem Kurs, Long auf den Rücklauf nach dem Muster von H10. Auslöser ist hier der Mechanismus, nicht die Kerzenform
- H15 Premium- bzw. Funding-Extrem: Basis über mehrere Stunden extrem, danach 1 bis 3 Tage gegen die Mehrheit. Voraussetzung ist eine Funding-Simulation im Lab. Funding-Raten gibt es bei Kraken nur für etwa ein Jahr, die Basis ab 2023
- H16 Trend auf Tagesbasis: BTC-Momentum mit wenigen Trades pro Jahr als zweites Standbein, das unabhängig von H10 funktioniert
