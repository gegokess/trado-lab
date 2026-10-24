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
| V1 | Funding-Historie und Funding-Simulation im Labor | erledigt | fester Satz aus dem Kraken-Mittel 2026 (+2,85 % p.a.), Kontrolle bestanden |
| V2 | Struktur-Definitionen aus Trado übernehmen, ETH- und SOL-Perps laden | offen | |
| H6 | Limit am Fib-Level eines 1h-Impulses in Richtung des 4h-Trends | offen | |
| H7 | Donchian-Ausbruch auf Tageskerzen (Zeitreihen-Momentum) | offen | |
| H8 | Long von 21:00 bis 23:00 UTC schlägt die Gebühren | abgelehnt | Effekt brutto bestätigt (+0,068 %, t = 3,4), netto −0,019 R |

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

## V1: Funding im Labor

**Zweck:** H6 und H7 halten Positionen über Stunden bis Wochen. Ohne Funding wären die Ergebnisse dort systematisch verzerrt.

- Historie über `GET https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol=PF_XBTUSD` nach data/raw laden, analog zu scripts/fetch_kraken.py
- Abrechnung stündlich auf den Positionswert, im Scan und in Nautilus gleich gerechnet
- Ergebnisspalte r_funding getrennt von den Gebühren ausweisen, damit sichtbar bleibt, welcher Anteil vom Funding kommt
- Kontrolle: H2 bis H5 mit Funding neu rechnen. Bei Haltedauern unter 6 h muss sich das Ergebnis um weniger als 0,005 R ändern, sonst ist die Abrechnung falsch

**Stand 24.10.2026:** `python scripts/fetch_derivatives.py` lädt Funding und Open Interest nach data/raw und hängt bei jedem Lauf an das bestehende Archiv an.

- Funding: Der Endpunkt liefert nur das letzte Jahr rollierend, aktuell ab 2025-10-15 (8.972 Stunden, 7 Lücken). Ältere Kraken-Werte gibt es nicht mehr, auch nicht über die Charts-API (dort erst ab 2026-02). Im Mittel des letzten Jahres rund +3,4 % p.a., Longs zahlen
- Open Interest: stündlich lückenlos ab 2023-03-07 über die Charts-API (Analytics open-interest). Damit sind Hypothesen mit Open Interest doch rückwirkend testbar, anders als bisher angenommen
- Das Skript sollte regelmäßig laufen, spätestens alle elf Monate, sonst entstehen beim Funding Lücken, die sich nicht mehr schließen lassen

Zur Wahl standen Ersatzdaten einer anderen Börse, ein Stresstest mit festem Satz oder beides.

**Entscheidung Gregor (24.10.2026):** fester Satz aus dem Mittel des Kraken-Fundings 2026 für den ganzen Testzeitraum.

- `FUNDING_RATE_1H = 3.26e-06` in lab/config.py, Mittel vom 2026-01-01 bis 2026-10-24 über 7.113 Stunden, entspricht +2,85 % p.a. Positiv heißt Longs zahlen und Shorts erhalten
- Monatsmittel 2026 annualisiert zur Einordnung: Januar +7,7 %, Februar bis April −0,8 bis −3,4 %, Mai und Juni um 0, Juli bis Oktober +5,4 bis +9,7 %. 64 % der Stunden positiv
- Abrechnung anteilig zur Haltedauer: Funding in Preis = Vorzeichen × Satz × Stunden × Einstieg, als r_funding ausgewiesen und von r_net und pct_net abgezogen (`add_funding` in lab/report.py)
- Nautilus-Läufe über `python -m lab.run` rechnen Funding automatisch ein, die Strategien schreiben dafür den Risikoabstand risk_px ins Trade-Protokoll. Ältere Läufe ohne risk_px werden aus r_gross zurückgerechnet
- Scans rechnen Funding nicht automatisch, neue Scans mit Haltedauer über einige Stunden (H6, H7) ziehen `add_funding` selbst heran
- Grenze der Methode: Ein fester Satz bildet keine Phasen mit überhitztem Funding ab. Hypothesen, die gerade solche Phasen handeln, brauchen echte Werte und damit das Kraken-Jahr ab 2025-10

**Kontrolle:** alle 14 gespeicherten Nautilus-Läufe aus H1 bis H5 mit Funding neu ausgewertet. Größte Änderung 0,0015 R (H4, obere Seite, mittlere Haltedauer 2,4 bis 3,5 h), Longs verlieren leicht, Shorts gewinnen leicht. Damit deutlich unter der Grenze von 0,005 R, die Abrechnung ist plausibel. Ein neuer Nautilus-Lauf der H4-Variante (obere Seite, k = 1,5, pb_w = 0,4) liefert r_funding = +0,0015 R, identisch zur Nachrechnung. Für H8 läge der Effekt bei rund −0,001 R und ändert die Entscheidung nicht.

**Status V1:** erledigt.

---

## V2: Gemeinsame Definitionen und weitere Märkte

**Zweck:** Eine im Labor bestätigte Regel soll in Trado exakt dieselbe Regel sein. Das Labor bestimmt Swings bisher mit sw = 3 und strikt auf beiden Seiten, Trado mit k = 5 und Gleichstand zugunsten des ersten Hochs.

- `find_swings`, `zigzag`, `fib_retracement`, `inducement` und `atr` aus trado/bot/features importieren statt nachzubauen, für H6 Pflicht
- Zeitpunktgenau rechnen: ein Swing ist erst nutzbar, wenn die k-te Folgekerze geschlossen ist. Fib und Inducement werden zu jedem Zeitpunkt nur aus bis dahin bestätigten Swings gebildet
- Test: Für zehn zufällige Zeitpunkte aus data/sample von Trado müssen Fib-Level und Inducement im Labor identisch zum Trado-Snapshot sein
- PF_ETHUSD und PF_SOLUSD ab 2023 als 1m-Archiv laden. Sie dienen als Gegenprobe für finale Parameter, ohne den OOS-Zeitraum von BTC zu verbrauchen

---

## H6: Fib-Pullback im Trend

**Idee (Vorschlag von Claude, von Gregor freigegeben, 24.10.2026):** Trado lässt Opus Pullbacks im Trend an Fib 0,618 bis 0,882 vorschlagen, mit dem Trend der höheren Zeitebene als Filter. Diese Regel ist der Kern dessen, was der Bot handeln soll, und wurde im Labor bisher nicht geprüft. H6 ist die deterministische Fassung davon. Abgrenzung zu H1 bis H5: dort wurde gegen die Wick und ohne Trendfilter gehandelt, hier wird mit dem Trend nach einem Rücklauf eingestiegen.

**Regeln** (strategies/fib_pullback.py, scan/fib_pullback_scan.py), Long beschrieben, Short spiegelbildlich

- Zeitebenen wie Trado: primär 1h, höher 4h, Swings k = 5, Inducement k = 2, Impuls mindestens 2 × ATR14 (1h), alle Definitionen aus V2
- Trendfilter: ema_trend der abgeschlossenen 4h-Kerzen ist aufwärts (EMA20 > EMA50 und Schluss > EMA50, Definition aus Trados Snapshot)
- Setup: jüngster Fib-Impuls auf 1h ist aufwärts und valid, der letzte 1h-Schluss liegt über dem Einstiegslevel
- Einstieg Long als ruhende Limit-Order (Post-Only, Maker) beim Fib-Level q
- Die Order liegt nur, solange der Kurs höchstens 1 ATR vom Level entfernt ist. Das bildet Trados Abstandsgrenze und das stündlich neu vorgeschlagene Setup nach. Entfernt sich der Kurs weiter, wird sie gelöscht und bei Rückkehr neu gelegt
- SL per Stop-Market bei Ursprung (1,0) − 0,25 ATR (Taker)
- TP als ruhende Limit-Order am Extrem (0) oder an der Extension −0,27 (Maker)
- Filter wie Trados Risiko-Engine: CRV bis TP netto nach Gebühren mindestens 1,5, sonst kein Setup. Bei q = 0,618 mit TP am Extrem fallen dadurch die meisten Setups weg, das ist gewollt und entspricht dem Bot
- Setup erlischt, wenn ein Schluss den Ursprung bricht, der 4h-Trend kippt oder ein neuer Impuls den alten ersetzt
- ein Trade je Impuls, keine offene Position in die Gegenrichtung, Zeitstopp 72 h
- Abweichung von Trado bewusst: ein Ziel statt TP-Aufteilung 50/30/20

**Vorab festgelegtes Raster** (In-Sample 2023-01-01 bis 2026-04-30, 12 Varianten): Seite Long/Short, q 0,618/0,786/0,882, TP Extrem/−0,27. Fest: SL-Puffer 0,25 ATR, Zeitstopp 72 h, Funding aus V1.

**Vorab festgelegte Aufteilung, keine zusätzlichen Varianten:** Innerhalb jeder Zelle werden die Trades getrennt nach Inducement beim Einstieg gesweept oder offen ausgewiesen. Das beantwortet, ob die Inducement-Regel aus dem trade-setup-Skill etwas bringt, ohne das Raster zu verdoppeln.

**Erfolgskriterium, vor dem Rechnen festgelegt:** Eine Zelle gilt als Kandidat für den OOS-Test, wenn sie in Nautilus netto über null liegt, t ≥ 2,5 erreicht (wegen 12 Zellen), ohne die drei besten Trades positiv bleibt, in mindestens zwei der drei vollen Jahre 2023 bis 2025 positiv ist und auf ETH mit denselben Parametern dasselbe Vorzeichen zeigt.

**Folgen für Trado:** Besteht eine Zelle, wird sie als harte Regel in `STRATEGIE-REGELN` eingetragen (Punkte 1, 2, 6, 9). Fällt H6 durch, ist das ein Befund gegen die Grundannahme des System-Prompts und sollte vor dem weiteren Paper-Betrieb besprochen werden.

---

## H7: Donchian-Ausbruch auf Tageskerzen

**Idee (Vorschlag von Claude, von Gregor freigegeben, 24.10.2026):** Zeitreihen-Momentum ist bei BTC der am besten belegte Effekt. Quantpedia fand für 2015 bis 2022, dass Käufe am N-Tage-Hoch besser abschnitten als Halten, mit den besten Werten bei kurzen Lookbacks. Abgrenzung zu allen bisherigen Hypothesen: Einstieg beim Ausbruch statt beim Rücklauf, Haltedauer Tage bis Wochen, weite Stops und damit geringe Gebührenlast in R.

**Regeln** (strategies/donchian.py, scan/donchian_scan.py), Long beschrieben, Short spiegelbildlich und getrennt ausgewertet

- Tageskerzen UTC aus dem 1m-Archiv
- Signal: Schlusskurs von Tag d über dem höchsten Hoch der N Tage vor d
- Einstieg per Market zur Eröffnung von d + 1 (Taker)
- Anfangs-SL per Stop-Market am tiefsten Tief der M Tage vor dem Einstieg, M = N / 2. R = Einstieg − Anfangs-SL
- Ausstieg: Der Stop wird täglich auf das M-Tage-Tief nachgezogen und nie zurückgesetzt. Kein festes Ziel
- keine neue Position, solange eine offen ist
- Funding aus V1 verpflichtend

**Vorab festgelegtes Raster** (In-Sample 2023-01-01 bis 2026-04-30, 6 Varianten): Seite Long/Short, N 10/20/30.

**Statistische Einschränkung, vorab benannt:** Je Seite und Variante sind in 40 Monaten grob 10 bis 30 Trades zu erwarten. BTC allein reicht für eine Aussage nicht. Ausgewertet wird deshalb gepoolt über BTC, ETH und SOL (V2) mit identischen Parametern, BTC wird zusätzlich einzeln gezeigt.

**Erfolgskriterium:** gepoolt netto über null mit t ≥ 2, ohne die drei besten Trades je Markt positiv, auf mindestens zwei der drei Märkte einzeln positiv. Bei Trendfolge ist eine Trefferquote um 35 bis 45 % normal und kein Ablehnungsgrund.

**Folgen für Trado:** Trado kann diesen Setup-Typ heute nicht abbilden (kein Stop-Entry, kein Nachziehen, Verfall nach einer Stunde, der Prompt lehnt Ausbrüche ab). Besteht H7, braucht der Bot einen zweiten, rein regelbasierten Ausführungspfad ohne LLM-Vorschlag.

---

## H8: Uhrzeit-Effekt am Abend UTC

**Idee (Vorschlag von Claude, von Gregor freigegeben, 24.10.2026):** Quantpedia fand für 2015 bis 2022 die stärksten Stundenrenditen bei BTC um 22 und 23 UTC und keine signifikant negative Stunde. Geprüft wird, ob der Effekt 2023 bis 2026 noch besteht und ob er Taker-Gebühren auf beiden Seiten trägt.

**Regeln** (scan/hour_effect_scan.py, Nautilus nur bei positivem Scan)

- Long per Market zur Eröffnung der 21:00-Kerze UTC (Taker)
- Ausstieg per Market zur Eröffnung der 23:00-Kerze UTC (Taker)
- Not-SL per Stop-Market bei Einstieg − 1,5 × ATR14 (1h), dient zugleich als R
- jeder Tag ein Trade, auch am Wochenende

**Vorab festgelegt:** genau eine Regel, das Fenster 21:00 bis 23:00 aus der Quelle. Kein Raster.

**Nur beschreibend, nicht zur Auswahl:** mittlere Netto-Rendite aller 24 Zwei-Stunden-Fenster als Profil, dazu Werktage gegen Wochenende. Ein anderes Fenster, das dort gut aussieht, ist kein Ergebnis von H8, sondern bräuchte eine eigene Hypothese und eine Bestätigung auf ETH.

**Erfolgskriterium:** netto über null, t ≥ 2, in jedem der Jahre 2023, 2024 und 2025 positiv. Als Gebührenschwelle muss die mittlere Brutto-Rendite über 0,06 % je Trade liegen (zweimal Taker).

**Folgen für Trado:** Auch bei knappem Scheitern netto kann ein brutto stabiler Effekt als Zeitfilter dienen (Punkt 10 der `STRATEGIE-REGELN`), zum Beispiel keine Shorts zwischen 21 und 23 UTC.

**Ergebnis Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04, `python -m scan.hour_effect_scan`)

| Teil | Trades | R brutto | R netto | t-Wert | R ohne Top 3 | % brutto | % netto | SL-Quote |
|---|---|---|---|---|---|---|---|---|
| alle Tage | 1216 | +0,052 | −0,019 | −1,0 | −0,030 | +0,068 | +0,008 | 10,9 % |
| Werktage | 869 | +0,049 | −0,006 | −0,3 | −0,017 | +0,076 | +0,016 | 7,7 % |
| Wochenende | 347 | +0,061 | −0,050 | −1,1 | −0,088 | +0,046 | −0,014 | 19,0 % |

R netto je Jahr: 2023 −0,033, 2024 −0,010, 2025 −0,001, 2026 (bis April) −0,057.

- Brutto ist der Effekt deutlich: +0,068 % je Trade bei t = 3,4 (in R +0,052 bei t = 2,8), und in jedem Jahr positiv (2023 +0,052 %, 2024 +0,088 %, 2025 +0,079 %, 2026 +0,019 %). Das ist zugleich eine Bestätigung außerhalb des Zeitraums der Quelle (2015 bis 2022)
- Die Gebührenschwelle von 0,06 % wird knapp überschritten, netto bleiben +0,008 % mit t = 0,4. In R gerechnet ist das Ergebnis negativ, weil ruhige Tage mit kleinem ATR und damit kleinem R stärker gewichtet sind
- Im Profil aller 24 Zwei-Stunden-Fenster ist 21:00 das mit Abstand beste Fenster, als einziges netto in Prozent positiv. Alle übrigen 23 Fenster sind netto negativ, 22:00 und 17:00 brutto noch leicht positiv
- Am Wochenende ist der Effekt schwächer und der Not-SL greift fast dreimal so oft. Grund ist der kleinere ATR am Wochenende, der Stop liegt dann enger

**Entscheidung H8:** abgelehnt als handelbare Regel. Das Erfolgskriterium (netto über null in R, t ≥ 2, jedes Jahr positiv) ist klar verfehlt. Ein Nautilus-Lauf ist nicht nötig, weil Ein- und Ausstieg reine Market-Orders zu festen Zeiten sind und solche Regeln bei H2 zu 96 bis 98 % mit dem Scan übereinstimmten. Kein OOS-Test.

Festhalten für Trado und künftige Hypothesen:

- Der Abend-Effekt ist brutto real und stabil. Als Zeitfilter in `STRATEGIE-REGELN` Punkt 10 brauchbar, etwa keine neuen Shorts zwischen 21:00 und 23:00 UTC und Long-Setups mit Einstieg vor 21:00 bevorzugen
- Er reicht nicht, um zwei Taker-Gebühren zu tragen. Offener Folgegedanke als eigene Hypothese: Einstieg und Ausstieg per Limit (Maker) rund um 21:00 und 23:00, mit dem Risiko nicht gefüllter Orders. Bei zweimal Maker läge die Kostenschwelle bei 0,02 % statt 0,06 %
