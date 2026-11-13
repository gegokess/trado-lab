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
| V2 | Struktur-Definitionen aus Trado übernehmen, ETH- und SOL-Perps laden | erledigt | Features an 300 von 300 Zeitpunkten identisch zu Trado |
| H6 | Limit am Fib-Level eines 1h-Impulses in Richtung des 4h-Trends | abgelehnt | schon brutto negativ, auf BTC, ETH und SOL, gepoolt −0,07 R brutto |
| H7 | Donchian-Ausbruch auf Tageskerzen (Zeitreihen-Momentum) | abgelehnt | BTC Long N = 10 in Nautilus +0,30 R bei t = 1,5 (40 Trades), Short negativ |
| H7c | H7 auf längerer BTC-Historie (Yahoo BTC-USD, 2015 bis 2022) | Kriterium erfüllt, Signal ohne Mehrwert | Long N = 10 +0,91 R bei t = 3,1, Zufallseinstiege mit gleichem Stop sind genauso gut |
| H9 | Intraday-Momentum: Rendite seit US-Öffnung bestimmt die Richtung der letzten halben Stunde | abgelehnt | Effekt 2023 bis 2026 verschwunden, brutto +1,9 bps, netto −4,1 bps, nicht besser als Zufall |
| H10 | Die kleinen Brutto-Effekte aus H8 und H9 mit Limit-Orders (Maker) statt Market handeln | abgelehnt | negative Auswahl der Fills frisst die Ersparnis, H10a +1,6 bps netto bei t = 0,8, H10b negativ |
| H11 | Nach einer sehr starken Bewegung kehrt BTC um (Ereignisstudie, dann Regel) | abgelehnt | 0 von 54 Zellen, nach Fällen nur der allgemeine Aufwärtstrend |
| H12 | Trendfilter: BTC long über dem 200-Tage-Schnitt, sonst flach, gemessen gegen Halten | abgelehnt | Sharpe 1,13 gegen 1,12, Unterschied nicht gesichert, größter Verlust −70 % statt −83 % |
| H13 | Carry: BTC als Sicherheit, Perp short, Funding vereinnahmen | abgelehnt | +3,3 % p.a., unter dem US-Leitzins von 3,75 bis 4,00 % |
| H14 | Liquidationskaskade: starker Open-Interest-Aufbau bei Seitwärtskurs, dann Ausbruch aus der 24-h-Range | abgelehnt | −0,18 R bei 75 Trades, schlechter als dieselbe Regel ohne Open Interest |
| H15 | SMC-Kette: Sweep eines 1h-Swings, MSS auf 5m, Einstieg im FVG | abgelehnt | −0,14 R bei 119 Trades, nicht besser als Zufallsrichtung |
| H8 | Long von 21:00 bis 23:00 UTC schlägt die Gebühren | abgelehnt | Effekt brutto bestätigt (+0,068 %, t = 3,4), netto −0,019 R |
| H16 | ETH: Wick ab 60 USD Kerzenspanne, Stop knapp über der Wick-Oberkante, Ziel 80 oder 100 % | abgelehnt | Scan netto −0,26 bis +0,17 R, Nautilus t-Werte unter 0,5, ohne Top 3 bei null |
| H17 | ETH: Limit-Short beim Rücklauf bis 10 bis 15 % vor den Open nach Bewegung ab 30 USD, Ziel 50 % | abgelehnt | alle 48 Varianten schon brutto negativ, netto −0,09 bis −0,40 R |
| H18 | ETH: freie Parametersuche über Rücklauf-Setups mit Filtern und Trade-Management | abgelehnt | kein über Zeiträume stabiler Vorteil, beste Varianten kippen außerhalb des Suchzeitraums |
| H19 | ETH und BTC: Wick nach Spike ab 2 % in höchstens 5 Minuten zur Hälfte füllen | abgelehnt | Scan +0,10 bis +0,17 R, Nautilus −0,15 bis +0,04 R, ohne Top 3 überall ≤ 0 |
| H20 | Wie H19, aber weiterer Stop und Laufenlassen | OOS bestanden, nur BTC obere Seite, Beobachtung | In-Sample +0,13 R (t 4,3), OOS 17 Trades +0,11 R (t 1,0) |
| H21 | H20 (BTC obere Seite) häufiger: kleinere Spikes, längere Spikes, SOL und XRP | abgelehnt | mehr Trades nur mit deutlich weniger R pro Trade, SOL und XRP ohne Effekt |
| H22 | H20-Trades mit Liquidationen im Spike laufen besser (Short-Squeeze als Ursache) | nicht gestützt | mehr Liquidationen +0,07 R besser, t 1,1, Kriterium (+0,1 R, t > 2) verfehlt |
| H23 | H20 nur, wenn vor dem Spike die Shorts überwiegen (Premium oder Kontenverhältnis) | geplant | offen |
| H24 | Long-Liquidationskaskade nach unten, Long auf den Rücklauf | geplant | offen |
| H25 | Extremes Premium bzw. Funding kehrt sich über 1 bis 3 Tage um | geplant | offen |
| H26 | BTC-Trend auf Tagesbasis als zweites Standbein mit wenigen Trades | entfällt | bereits durch H7, H7c und H12 abgedeckt |
| H27 | H20 mit Entscheidung alle 10 Sekunden statt nach Kerzenschluss | geplant, lokal als H17 begonnen, noch nicht in main | offen |
| H28 | Trendfilter rückwirkend auf alle vorhandenen Trade-Listen: nur mit dem 4h-Trend handeln | T2 formal erfüllt, T1 nicht | Struktur-Filter hebt R in 76 % der Läufe, Median +0,06 R, macht aber keine Strategie tragfähig |
| H29 | Zonen-Setups mit dem Trend (Rücklauf in Zone, Ausbruch und Retest), danach Stop- und Ziel-Varianten | abgelehnt in Stufe 1 | 0 von 32 Zellen besser als verschobene Kontrollzonen, bester t-Wert 1,3 |

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

**Umsetzung (24.10.2026)**

- lab/trado_features.py lädt structure.py und indicators.py direkt aus dem Trado-Repo (Umgebungsvariable TRADO_DIR, sonst Nachbarordner ../trado) und bildet compute_features zeitpunktgenau nach: je volle Stunde die letzten 600 geschlossenen 1h- und 4h-Kerzen, Features ab 250 Kerzen je Zeitebene, Standardwerte aus Trados Config
- Zwischenspeicher in data/features, der Dateiname enthält einen Hash der Trado-Dateien. Ändert sich Trado, wird neu gerechnet. Rechenzeit rund 25 s je Markt
- lab.data.load_1m hat den Parameter symbol, scripts/fetch_kraken.py --symbol lädt weitere Märkte

**Prüfung** (`python -m scan.pruefe_trado_features`, braucht `uv pip install -e ".[pruefung]"`)

- Kerzen: 1h und 4h aus dem 1m-Archiv gegen Trados echte Kraken-Kerzen in trado/data/sample, 1.199 und 599 Kerzen, OHLC und Volumen ohne Abweichung. Die jeweils letzte Kerze im Sample ist unvollständig gespeichert und bleibt außen vor
- Features: an 300 zufälligen Zeitpunkten (2023 bis 2026) Trados eigenes compute_features gegen das Labor, Fib-Richtung, Ursprung, Extrem, valid, extended, alle Level, Inducement und 4h-ema_trend in allen 300 Fällen identisch
- Daten: PF_ETHUSD und PF_SOLUSD ab 2023-01-01 geladen, je rund 2,0 Mio. 1m-Kerzen ohne Lücken

**Status V2:** erledigt.

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

**Ergebnis Scan BTC** (24.10.2026, In-Sample 2023-02 bis 2026-04, Features ab 250 4h-Kerzen, `python -m scan.fib_pullback_scan`)

| Seite | q | TP | Trades | TP-Quote | R brutto | R netto | t-Wert | R ohne Top 3 | Haltedauer h |
|---|---|---|---|---|---|---|---|---|---|
| Long | 0,618 | Extrem | 2 | | | | | | |
| Long | 0,618 | −0,27 | 232 | 28,9 % | −0,02 | −0,056 | −0,6 | −0,085 | 17,5 |
| Long | 0,786 | Extrem | 226 | 25,2 % | −0,04 | −0,110 | −1,0 | −0,154 | 7,1 |
| Long | 0,786 | −0,27 | 222 | 21,6 % | +0,04 | −0,033 | −0,3 | −0,091 | 8,6 |
| Long | 0,882 | Extrem | 198 | 14,6 % | −0,20 | −0,310 | −2,3 | −0,397 | 4,3 |
| Long | 0,882 | −0,27 | 195 | 12,8 % | −0,12 | −0,237 | −1,5 | −0,347 | 5,1 |
| Short | 0,618 | Extrem | 2 | | | | | | |
| Short | 0,618 | −0,27 | 193 | 32,6 % | +0,04 | +0,014 | +0,1 | −0,019 | 19,2 |
| Short | 0,786 | Extrem | 172 | 20,3 % | −0,20 | −0,271 | −2,3 | −0,331 | 9,2 |
| Short | 0,786 | −0,27 | 167 | 17,4 % | −0,14 | −0,208 | −1,5 | −0,286 | 10,3 |
| Short | 0,882 | Extrem | 153 | 15,0 % | −0,11 | −0,218 | −1,3 | −0,329 | 6,5 |
| Short | 0,882 | −0,27 | 151 | 12,6 % | −0,07 | −0,182 | −0,9 | −0,326 | 7,1 |

Bei q = 0,618 mit TP am Extrem lässt der CRV-Filter wie erwartet fast nichts durch. Funding macht je Trade nur ±0,004 R aus, Gebühren rund 0,06 R.

**Gegenprobe ETH und SOL, beschreibend:** dasselbe Raster ohne Änderung. Auf ETH keine Zelle netto positiv (bestes −0,039 R), auf SOL drei knapp positiv (Long 0,618/−0,27 mit +0,074 R bei t = 0,8, Long 0,786/−0,27 mit +0,012 R und Long 0,618/Extrem mit nur 15 Trades), auf BTC sind dieselben Zellen negativ. Über alle drei Märkte und 36 Zellen gepoolt (5.858 Trades, Zellen überlappen sich): brutto −0,074 R, netto −0,132 R. Long und Short gleich schlecht.

**Aufteilung nach Inducement, gepoolt über alle Märkte:** Einstieg nach gesweeptem Inducement brutto −0,14 R (1.236 Trades), bei offenem Inducement −0,02 R (801), ohne Inducement im Impuls −0,06 R (3.821). Der gesweepte Köder, der im trade-setup-Skill als gutes Zeichen gilt, ist hier die schlechteste Gruppe.

**Entscheidung H6:** abgelehnt. Keine Zelle erreicht das Erfolgskriterium, die beste auf BTC liegt bei +0,014 R mit t = 0,1. Die Regel ist schon vor Gebühren negativ, und das auf allen drei Märkten. Nach Testprotokoll kein Nautilus-Lauf und kein OOS-Test. Varianten getestet: 12 je Markt, 36 insgesamt.

Besonders deutlich: Je tiefer der Einstieg im Retracement (0,882 statt 0,618), desto schlechter. Das spricht dagegen, dass am 0,882 ein Umkehrpunkt liegt, und eher dafür, dass ein tiefer Rücklauf auf 1h oft in einen Bruch des Ursprungs übergeht.

**Folgen für Trado, zu besprechen:**

- Der Kern dessen, was der System-Prompt Opus nahelegt (Pullback im Trend an Fib 0,618 bis 0,882, Inducement als Timing), hat in seiner regelbasierten Form keinen Vorteil. Was Opus darüber hinaus beiträgt, lässt sich im Labor nicht messen, nur im Paper-Betrieb
- Fib-Level und Inducement sollten in `STRATEGIE-REGELN` nicht als Einstiegsgrund stehen. Der Prompt sagt schon, sie seien kein Beleg für eine höhere Trefferquote, das ist jetzt auch gemessen
- Geprüft ist nur diese Geometrie: 1h-Impulse, SL am Ursprung, TP am Extrem oder −0,27, 4h-ema_trend als Filter. Andere Zeitebenen oder Stops wären eigene Hypothesen

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

**Ergebnis Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04, `python -m scan.donchian_scan`)

Gepoolt über BTC, ETH und SOL:

| Seite | N | Trades | Treffer | Tage im Trade | R brutto | R netto | t-Wert | R ohne Top 3 | Funding R |
|---|---|---|---|---|---|---|---|---|---|
| Long | 10 | 117 | 41,9 % | 9,5 | +0,281 | +0,266 | +1,9 | +0,083 | −0,008 |
| Long | 20 | 64 | 43,8 % | 19,7 | +0,448 | +0,431 | +1,3 | −0,022 | −0,012 |
| Long | 30 | 45 | 40,0 % | 26,9 | +0,724 | +0,706 | +1,2 | −0,064 | −0,015 |
| Short | 10 | 101 | 21,8 % | 8,0 | −0,152 | −0,152 | −2,3 | −0,237 | +0,006 |
| Short | 20 | 58 | 25,9 % | 14,8 | −0,172 | −0,169 | −1,9 | −0,267 | +0,008 |
| Short | 30 | 39 | 33,3 % | 19,8 | −0,181 | −0,176 | −1,8 | −0,289 | +0,008 |

Long je Markt, R netto (R ohne Top 3 des Markts):

| N | BTC | ETH | SOL |
|---|---|---|---|
| 10 | +0,298 (+0,022) | +0,171 (−0,216) | +0,334 (−0,040) |
| 20 | +0,384 (−0,190) | −0,062 (−0,375) | +1,026 (−0,110) |
| 30 | +0,358 (−0,390) | +0,014 (−0,331) | +1,820 (−0,277) |

R netto Long N = 10 je Jahr: 2023 +0,63, 2024 +0,37, 2025 +0,01, 2026 bis April −0,30.

- Gebühren spielen hier keine Rolle (rund 0,015 R je Trade), weil der Stop im Median 7,7 % entfernt liegt. Funding kostet die Longs 0,008 bis 0,015 R
- Typisches Trendfolge-Profil: Trefferquote um 40 %, das Ergebnis hängt an wenigen großen Gewinnern (BTC Long N = 10: bester Trade +4,6 R im Januar 2023, die drei besten zusammen tragen fast den ganzen Gewinn)
- Long ist auf allen drei Märkten positiv, Short auf allen drei negativ. Im Testzeitraum stieg BTC um rund 360 %. Ein Teil des Long-Ergebnisses ist damit schlicht Marktrichtung, nicht Ausbruchslogik. BTC Long N = 10 war 33 % der Zeit investiert
- Die Jahreszahlen fallen von 2023 nach 2026 deutlich ab, im Einklang mit dem flacheren Markt seit 2025

**Entscheidung H7:** abgelehnt nach dem vorab festgelegten Kriterium. Die beste Zelle (Long N = 10) erreicht gepoolt t = 1,9 statt 2 und ist ohne die drei besten Trades auf ETH und SOL negativ. Erfüllt ist nur die Bedingung, auf mindestens zwei Märkten einzeln positiv zu sein. Kein Nautilus-Lauf, weil Market-Einstieg und Stop-Ausstieg im Scan verlässlich sind (vgl. H2) und die Entscheidung nicht an der Ausführungsgenauigkeit hängt. Kein OOS-Test. Varianten getestet: 6 gepoolte Zellen auf drei Märkten.

Einordnung: Unter allen bisherigen Hypothesen ist das der erste Befund mit klar positivem Brutto-Ergebnis über mehrere Märkte. Das Problem ist die Stichprobe, nicht die Richtung. 117 Trades mit stark schiefer Verteilung reichen für t ≥ 2 nicht. Die Short-Seite ist dagegen eindeutig und kann ruhen.

Offener Folgegedanke, eigener Eintrag nötig: dieselbe Long-Regel mit N = 10 als einzige Zelle auf weiteren Kraken-Perps, die nicht in H7 vorkamen. Das erweitert die Stichprobe unabhängig von der Auswahl, die hier getroffen wurde.

**Nachtrag 24.10.2026, nur BTC:** Gregor hat festgelegt, dass ausschließlich BTC zählt, auch nicht als Gegenprobe. Der Folgegedanke mit weiteren Perps entfällt. Maßgeblich für H7 ist damit BTC allein.

**Nautilus-Lauf BTC** (24.10.2026, In-Sample 2023-01 bis 2026-04, strategies/donchian.py, `python -m lab.run donchian side=long N=10`)

| Seite | N | Quelle | Trades | R brutto | R netto | t-Wert | R ohne Top 3 | Funding R |
|---|---|---|---|---|---|---|---|---|
| Long | 10 | numba | 40 | +0,318 | +0,298 | +1,5 | +0,022 | −0,011 |
| Long | 10 | Nautilus | 40 | +0,318 | +0,298 | +1,5 | +0,022 | −0,011 |
| Long | 20 | numba | 22 | +0,405 | +0,384 | +0,9 | −0,190 | −0,015 |
| Long | 20 | Nautilus | 21 | +0,413 | +0,391 | +0,9 | −0,213 | −0,015 |
| Long | 30 | numba | 17 | +0,382 | +0,358 | +0,8 | −0,390 | −0,019 |
| Long | 30 | Nautilus | 16 | +0,410 | +0,385 | +0,8 | −0,414 | −0,019 |
| Short | 10 | Nautilus | 33 | −0,296 | −0,297 | −2,9 | −0,427 | +0,007 |
| Short | 20 | Nautilus | 17 | −0,245 | −0,240 | −1,3 | −0,515 | +0,011 |
| Short | 30 | Nautilus | 12 | −0,140 | −0,133 | −0,7 | −0,412 | +0,011 |

- Deckung Trade für Trade: alle Nautilus-Trades haben im Scan denselben Einstiegszeitpunkt und denselben Ausstieg, die Abweichung je Trade liegt unter 0,001 R. Der Einstiegspreis weicht in einigen Fällen um Bruchteile eines Dollars ab
- Der einzige Unterschied: Bei N = 20 und N = 30 ist am Ende des In-Sample-Zeitraums eine Position offen. Der Scan bewertet sie zum letzten Schluss, Nautilus zählt sie nicht. Short ist in beiden Quellen identisch
- Für Tagesregeln mit Market-Einstieg und Stop-Ausstieg ist der Scan damit exakt

**Entscheidung H7 bleibt:** abgelehnt. Auf BTC allein erreicht die beste Zelle (Long N = 10) netto +0,30 R bei t = 1,5 mit 40 Trades. Ohne die drei besten Trades bleiben +0,02 R, die drei besten tragen rund 93 % des Gewinns. Kein OOS-Test: Bei rund einem Trade pro Monat kämen im OOS-Zeitraum etwa sechs Trades zusammen, das entscheidet nichts. Die Richtung ist positiv, die Stichprobe auf BTC ab 2023 reicht für einen Nachweis nicht.

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

---

## H7c: Donchian-Ausbruch auf längerer BTC-Historie

**Idee (Gregor, 24.10.2026):** H7 zeigt auf BTC ab 2023 eine positive Long-Seite, die Stichprobe von 40 Trades reicht aber nicht für einen Nachweis. Kraken liefert für BTC keine Futures-Daten vor 2023. Als zusätzlicher Backtest dient deshalb eine andere BTC-Kursreihe mit längerer Historie. Es bleibt bei BTC, kein anderer Coin.

**Daten**

- Yahoo Finance BTC-USD, Tageskerzen UTC, Historie ab September 2014 (`python scripts/fetch_yahoo_btc.py`)
- Spot-Index statt Perpetual. Für eine Tagesregel ohne Intraday-Logik ist das gleichwertig, Funding gibt es im Spot nicht, wird aber wie in H7 als fester Satz abgezogen (für Longs vorsichtig)
- Testzeitraum 2015-01-01 bis 2022-12-31. Er überschneidet sich nicht mit dem Zeitraum von H7 und enthält zwei Bärenmärkte (2018, 2022)
- Qualitätsprüfung vorab: Yahoo-Tageskerzen gegen die aus Kraken-1m gebildeten Tageskerzen 2023 bis April 2026 vergleichen

**Regeln:** unverändert aus H7 (strategies/donchian.py). Auf Tageskerzen ist die Regel exakt rechenbar, weil alle Entscheidungen zum Tageswechsel fallen und der Stop innerhalb eines Tages fest liegt: Stop getroffen, wenn das Tagestief ihn erreicht, Fill zum Stop oder bei einer Eröffnung darunter zum Open. Kontrolle: die Tagesrechnung muss auf den Kraken-Daten 2023 bis April 2026 dieselben Trades liefern wie der 1m-Scan von H7.

**Vorab festgelegt**

- Haupttest genau eine Zelle: Long N = 10, die beste Zelle aus H7. Weil sie dort ausgewählt wurde, zählt nur dieser neue Zeitraum als Bestätigung
- die übrigen fünf Zellen aus H7 nur beschreibend
- Erfolgskriterium: netto über null, t ≥ 2, ohne die drei besten Trades positiv. Zusätzlich beschreibend die Jahre einzeln und der Gesamtzeitraum 2015 bis April 2026
- Gebühren wie Kraken: Einstieg und Stop je Taker 0,03 %

**Folgen:** Besteht Long N = 10 auf 2015 bis 2022, ist H7 auf BTC als Kandidat für den OOS-Test ab Mai 2026 bestätigt (der OOS-Zeitraum ist dann aber erst nach einigen Monaten mehr Daten aussagekräftig). Fällt sie durch, ist H7 endgültig verworfen.

**Ergebnis** (24.10.2026, `python -m scan.donchian_daily_scan`)

Kontrollen:

- Tagesrechnung gegen 1m-Scan auf Kraken 2023 bis April 2026: in allen sechs Zellen dieselben Trades, Abweichung je Trade höchstens 0,001 R. Die Tagesrechnung ist für diese Regel exakt
- Yahoo gegen Kraken an 1.216 gemeinsamen Tagen: mittlere Abweichung 0,05 % bei Open und Close, 0,15 % bei Hoch und Tief. Auf Trade-Ebene reagiert der Ausbruch empfindlich darauf: Long N = 10 hat auf Yahoo 45 statt 40 Trades, 38 davon gemeinsam, netto +0,18 statt +0,30 R. Die Richtung ist in allen Zellen gleich

Haupttest und Beschreibung, Yahoo 2015 bis 2022:

| Seite | N | Trades | Treffer | Tage im Trade | R netto | t-Wert | R ohne Top 3 |
|---|---|---|---|---|---|---|---|
| Long | 10 | 97 | 45,4 % | 10,6 | +0,907 | +3,1 | +0,515 |
| Long | 20 | 45 | 60,0 % | 25,1 | +1,744 | +2,7 | +0,763 |
| Long | 30 | 31 | 54,8 % | 36,9 | +2,153 | +2,5 | +0,807 |
| Short | 10 | 78 | 33,3 % | 9,3 | −0,013 | −0,1 | −0,127 |
| Short | 20 | 38 | 50,0 % | 18,6 | +0,206 | +1,6 | +0,055 |
| Short | 30 | 26 | 42,3 % | 22,9 | +0,050 | +0,3 | −0,141 |

R netto Long N = 10 je Jahr: 2015 +1,52, 2016 +1,58, 2017 +2,09, 2018 −0,09, 2019 +0,55, 2020 +1,56, 2021 +0,02, 2022 −0,36. Über 2015 bis April 2026 zusammen: 142 Trades, +0,74 R, t = 3,3.

Das vorab festgelegte Kriterium ist für Long N = 10 erfüllt: netto +0,91 R, t = 3,1, ohne die drei besten Trades +0,52 R. In den beiden Bärenjahren 2018 und 2022 verliert die Regel nur wenig.

**Kontrollvergleich, nachträglich und nur beschreibend:** Im Testzeitraum stieg BTC rund um das Fünfzigfache. Um zu prüfen, ob der Ausbruch selbst etwas beiträgt, wurde dieselbe Ausstiegsregel (Anfangs-Stop am 5-Tage-Tief, täglich nachgezogen) mit anderen Einstiegen gerechnet:

| Einstieg | Zeitraum | Trades | R netto je Trade |
|---|---|---|---|
| Donchian N = 10 | Yahoo 2015 bis 2022 | 97 | +0,92 |
| jeden Tag, sobald flach | Yahoo 2015 bis 2022 | 517 | +1,02 |
| zufällig (8 % je Tag, 300 Läufe) | Yahoo 2015 bis 2022 | im Mittel 149 | im Mittel +1,34 |
| Donchian N = 10 | Kraken 2023 bis April 2026 | 40 | +0,31 |
| jeden Tag, sobald flach | Kraken 2023 bis April 2026 | 220 | +0,47 |
| zufällig (8 % je Tag, 300 Läufe) | Kraken 2023 bis April 2026 | im Mittel 64 | im Mittel +0,36 |

In 83 % der Zufallsläufe 2015 bis 2022 und in 47 % der Läufe 2023 bis 2026 liegt das Ergebnis je Trade mindestens so hoch wie mit dem Ausbruchssignal.

**Entscheidung H7c:** Das Kriterium ist formal erfüllt, als Timing-Vorteil ist der Ausbruch aber nicht bestätigt. Das positive Ergebnis kommt aus der Kombination von BTCs langfristigem Anstieg mit einem nachgezogenen Stop, nicht aus dem Einstiegssignal. Zufällige Einstiege mit demselben Stop schneiden genauso gut oder besser ab. Kein OOS-Test, weil es kein Signal gibt, das sich zu bestätigen lohnt.

Folgen für Trado:

- Kein eigener Ausführungspfad für Donchian-Ausbrüche, der Einstieg bringt nichts
- Was bleibt, ist eine Aussage über die Marktrichtung: Long BTC mit Trailing-Stop am 5-Tage-Tief hat 2015 bis 2026 positiv abgeschnitten, Short in keiner Form. Das ist eine Wette darauf, dass BTC weiter steigt, keine Handelsregel mit Vorteil gegenüber dem Halten
- Für künftige Hypothesen gehört dieser Kontrollvergleich mit Zufallseinstiegen fest ins Protokoll, sobald eine Regel nur eine Richtung handelt

---

## H9: Intraday-Momentum am Ende der US-Sitzung

**Herkunft (Online-Recherche 24.10.2026, Auftrag Gregor):** Gesucht war die Strategie mit der besten Belegung für BTC allein, die zu den Kosten von Stufe 5 passt und genug Trades für einen Nachweis liefert. Geprüft wurden:

- Intraday-Momentum (Shen, Urquhart, Wang 2022, Financial Review): Bei BTC sagt die Rendite vom Vortagesschluss bis eine halbe Stunde nach der Öffnung die letzte halbe Stunde bis 17 Uhr EST voraus, die vorletzte halbe Stunde sagt sie mit umgekehrtem Vorzeichen voraus. Daten von fünf Börsen inklusive Kraken bis Ende 2020, Out-of-Sample-R² 1,1 bis 1,8 %. Kostendeckung ohne Hebel bei 3, 7 und 10 Basispunkten je Runde für die drei Signale
- Kurzfristige Umkehr über 15 Minuten bis 4 Stunden: in Krypto klar messbar, brutto aber nur rund 1,3 Basispunkte je Trade und damit unter den Kosten (arXiv 2608.21888, 2026)
- Umkehr zwischen Tag- und Nachtsitzung (MDPI 2026, Kraken 2016 bis 2025): nach Korrektur für 300 getestete Varianten nicht signifikant, nach Auswahl auf 2016 bis 2020 in 2021 bis 2025 schlechter als Halten
- Liquidationskaskaden mit anschließender Erholung: keine direkte empirische Studie gefunden, verwandte Arbeiten sehen kurzfristige Umkehr nach Kosten schwach. Liquidationsdaten wären außerdem nicht frei verfügbar
- Viertelstunden-Effekt (arXiv 2607.09426, 2026): Mikrostruktur in den ersten Sekunden, für 1m-Daten nicht handelbar
- Stundeneffekte nach den Spot-ETFs (Schmidt und Kraft 2026): keine robuste Richtung nach Mehrfachtest-Korrektur

Ausgewählt wurde das Intraday-Momentum. Gründe: begutachtet und für BTC inklusive Kraken belegt, die Veröffentlichung endet 2020 und 2023 bis 2026 ist damit echter Nachtest, ein Trade an fast jedem Tag und damit genug Stichprobe, Long und Short gleichermaßen statt nur Marktrichtung, und die Kostenschwelle der Studie (10 Basispunkte) liegt über Gregors Kosten von 6 Basispunkten je Runde. Das Fenster fällt zudem in die Abendstunden, in denen H8 brutto einen Effekt gefunden hat.

**Regeln** (scan/intraday_momentum_scan.py), Zeiten wie in der Studie fest in EST = UTC − 5, ohne Sommerzeit

- Tagesschluss 22:00 UTC (17:00 EST), Öffnung Kraken laut Studie 14:15 UTC (9:15 EST)
- r_ONFH: Rendite vom Schluss 22:00 UTC des Vortags bis 14:45 UTC (eine halbe Stunde nach der Öffnung)
- r_SLH: Rendite von 21:00 bis 21:30 UTC (vorletzte halbe Stunde)
- Einstieg per Market zum Open der Minute 21:30 UTC (Taker), Ausstieg per Market zum Open der Minute 22:00 UTC (Taker), kein Stop
- Signal A: Long wenn r_ONFH > 0, sonst Short
- Signal B: Long wenn r_SLH < 0, sonst Short
- Signal C (kombiniert, Haupttest): Long wenn r_ONFH > 0 und r_SLH < 0, Short wenn r_ONFH ≤ 0 und r_SLH ≥ 0, sonst kein Trade
- Funding über add_funding, bei 30 Minuten vernachlässigbar
- Auswertung in Basispunkten je Trade und in R mit R = ATR14 der abgeschlossenen 1h-Kerzen zum Einstieg (nur Normierung, kein Stop)

**Vorab festgelegt** (In-Sample 2023-01-01 bis 2026-04-30)

- Haupttest genau eine Zelle: Signal C. A und B werden mit ausgewiesen, zählen aber nicht als eigene Bestätigung
- Erfolgskriterium für C: netto über null mit t ≥ 2, ohne die drei besten Trades positiv, in jedem der Jahre 2023, 2024 und 2025 netto positiv
- Kontrolle Zufallsrichtung: an denselben Tagen wie C zufällig Long oder Short, 1.000 Läufe. C muss über dem 95-%-Quantil liegen
- Kontrolle Marktrichtung: an denselben Tagen immer Long. C muss netto darüber liegen, damit das Ergebnis nicht nur den Abend-Effekt aus H8 abbildet
- beschreibend: dieselben Regeln in New Yorker Ortszeit mit Sommerzeit (Schluss 17:00 ET), Aufteilung nach Volumen der ersten halben Stunde in Drittel (laut Studie stärker an aktiven Tagen)

**Folgen:** Besteht C, folgt ein Nautilus-Lauf und danach der OOS-Test ab Mai 2026, bei rund einem Trade an jedem zweiten Tag mit etwa 90 Trades aussagekräftig. Für Trado wäre das ein regelbasierter Zeitplan-Trade ohne LLM.

**Ergebnis Scan** (24.10.2026, In-Sample 2023-01 bis 2026-04, 1.215 Tage, `python -m scan.intraday_momentum_scan`)

Zeiten fest in UTC − 5 (Haupttest):

| Signal | Trades | bps brutto | bps netto | R netto | t-Wert | Treffer | R netto 2023 / 2024 / 2025 |
|---|---|---|---|---|---|---|---|
| A (r_ONFH) | 1.215 | +0,1 | −5,9 | −0,107 | −7,3 | 36,1 % | −0,13 / −0,05 / −0,15 |
| B (r_SLH umgekehrt) | 1.215 | +1,9 | −4,1 | −0,090 | −6,1 | 41,7 % | −0,08 / −0,09 / −0,10 |
| C (kombiniert) | 647 | +1,9 | −4,1 | −0,093 | −4,6 | 38,8 % | −0,09 / −0,06 / −0,14 |

- Kontrolle Marktrichtung: an denselben 647 Tagen immer Long ergibt −5,5 bps netto, C liegt nur 1,4 bps darüber
- Kontrolle Zufallsrichtung: Mittel der 1.000 Läufe −0,107 R, 95-%-Quantil −0,072 R, C mit −0,093 R liegt darunter. 25 % der Zufallsläufe sind mindestens so gut wie C
- Volumen der ersten halben Stunde: in allen Dritteln negativ (−2,3 / −4,4 / −5,5 bps netto), anders als in der Studie nicht stärker an aktiven Tagen
- In New Yorker Ortszeit mit Sommerzeit noch schwächer: alle drei Signale brutto knapp negativ

**Entscheidung H9:** abgelehnt. Der in der Studie bis 2020 belegte Effekt ist auf Kraken 2023 bis 2026 nicht mehr vorhanden. Das Momentum-Signal A hat brutto keinerlei Vorhersagekraft (+0,1 bps), nur die Umkehr der vorletzten halben Stunde (B) zeigt brutto knapp 2 bps, ein Drittel der Kosten. Das passt zu der Studie über kurzfristige Umkehr (rund 1,3 bps brutto, unter den Kosten). Kein Nautilus-Lauf, kein OOS-Test. Varianten: 3 Signale in 2 Zeitzonen, nur C zählte.

---

## H10: Limit-Ausführung statt Market

**Idee (Gregor, 24.10.2026):** H8 (Long 21 bis 23 UTC) und Signal B aus H9 (Umkehr der vorletzten halben Stunde) haben brutto einen kleinen Effekt von +6,8 und +1,9 bps, scheitern aber an zweimal Taker (6 bps). Mit zweimal Maker kostet die Runde 2 bps. Geprüft wird, ob der Effekt die Limit-Ausführung übersteht. Risiken: Orders werden nicht gefüllt, und gefüllt werden bevorzugt die Fälle, in denen der Kurs gegen die Position läuft.

**Füllmodell:** Eine Limit-Order füllt nur, wenn eine spätere 1m-Kerze den Preis echt durchhandelt (Kauf: Tief < Limit, Verkauf: Hoch > Limit). Berührung allein reicht nicht, weil die Warteschlange am Preis unbekannt ist. Beschreibend zusätzlich mit Füllung bei Berührung als optimistische Obergrenze.

**Regeln H10a** (scan/maker_scan.py), Grundlage H8

- 21:00 UTC: Post-Only-Limit Kauf zum Open der Minute 21:00, gültig bis 22:00, sonst kein Trade
- Not-SL per Stop-Market bei Einstieg − 1,5 × ATR14 (1h) wie in H8, gilt ab der Füllminute
- 23:00 UTC: Post-Only-Limit Verkauf zum Open der Minute 23:00, gültig bis 23:30, danach Market zum Open von 23:30 (Taker)
- R = 1,5 × ATR wie in H8

**Regeln H10b** (scan/maker_scan.py), Grundlage H9 Signal B

- Richtung wie B: Long wenn die Rendite 21:00 bis 21:30 UTC negativ ist, sonst Short
- 21:30 UTC: Post-Only-Limit zum Open der Minute 21:30, gültig bis 21:45, sonst kein Trade
- 22:00 UTC: Post-Only-Limit zum Open der Minute 22:00 zum Schließen, gültig bis 22:15, danach Market (Taker)
- kein Stop, R = ATR14 (1h) wie in H9

**Vorab festgelegt** (In-Sample 2023-01-01 bis 2026-04-30, je eine Regel, kein Raster)

- Erfolgskriterium je Regel: netto über null mit t ≥ 2, ohne die drei besten Trades positiv, in jedem der Jahre 2023, 2024 und 2025 netto positiv
- H10b zusätzlich: über dem 95-%-Quantil von 1.000 Läufen mit Zufallsrichtung und identischer Ausführung
- beschreibend: Füllquote, Anteil der Ausstiege per Market, Brutto der gefüllten gegen die nicht gefüllten Tage (gemessen mit der Market-Variante, zeigt die negative Auswahl der Fills)

---

## H11: Umkehr nach sehr starken Bewegungen

**Idee (Gregor, 24.10.2026):** Nach einem sehr starken Fall oder Anstieg kehrt BTC um. Gehandelt wird gegen die Bewegung. Literatur: kurzfristige Überreaktion in Krypto ist dokumentiert, nach Kosten aber schwach (vgl. H9 Recherche). Weil die Frage offen formuliert ist, erst eine Ereignisstudie mit vorab festgelegtem Raster, dann nur bei einem eindeutigen Befund eine Handelsregel.

**Ereignisdefinition** (scan/umkehr_scan.py)

- zu jeder vollen Stunde t die Bewegung r_L über die letzten L Stunden (Open der Minute t gegen Open der Minute t − L)
- Maßstab σ_L = σ_1h × √L, σ_1h = Standardabweichung der 1h-Renditen der letzten 720 Stunden (30 Tage), nur Vergangenheit
- Ereignis, wenn |r_L| ≥ k × σ_L
- Entballung: nach einem Ereignis in einer Zelle zählt das nächste derselben Zelle frühestens 24 h später, damit sich die Folgerenditen nicht überlappen
- Folgerendite über H Stunden ab dem Open der Minute t, mit Vorzeichen gegen die Bewegung (positiv heißt Umkehr)

**Raster:** L 1 / 4 / 24 h, k 2 / 3 / 4, H 1 / 4 / 24 h, getrennt nach Fall und Anstieg. 54 Zellen.

**Vorab festgelegt**

- Wegen 54 Zellen zählt eine Zelle nur bei t ≥ 3,3 brutto (Bonferroni für 5 %) und netto positiv bei zweimal Taker (6 bps)
- erfüllt keine Zelle das Kriterium, ist H11 abgelehnt und es wird keine Regel gebaut
- erfüllt eine Zelle es, wird genau diese als Regel mit Market-Einstieg und Zeitausstieg in Nautilus gerechnet, mit Kontrolle gegen Zufallseinstiege derselben Richtung, danach OOS

**Ergebnis H10** (24.10.2026, In-Sample 2023-01 bis 2026-04, `python -m scan.maker_scan`)

| Regel | Füllung | Trades | Füllquote | Limit-Ausstieg | bps brutto | bps netto | t (bps) | R netto | t (R) |
|---|---|---|---|---|---|---|---|---|---|
| H10a | durchgehandelt (Haupttest) | 1.174 | 96,5 % | 82,9 % | +4,0 | +1,6 | +0,8 | −0,008 | −0,4 |
| H10a | Berührung (Obergrenze) | 1.216 | 100 % | 88,7 % | +6,7 | +4,4 | +2,2 | +0,023 | +1,2 |
| H10b | durchgehandelt (Haupttest) | 1.107 | 91,0 % | 92,1 % | −1,6 | −3,8 | −3,0 | −0,084 | −4,8 |
| H10b | Berührung (Obergrenze) | 1.216 | 100 % | 100 % | +1,9 | −0,1 | −0,1 | −0,019 | −1,3 |

Negative Auswahl der Fills, gemessen mit der Market-Variante an denselben Tagen:

- H10a: an gefüllten Tagen +7,1 bps brutto, an den 3,5 % nicht gefüllten +43,4 bps. Nicht gefüllt wird genau dann, wenn der Kurs sofort steigt, und das sind die besten Tage
- H10b: an gefüllten Tagen +0,6 bps, an den 9 % nicht gefüllten +15,7 bps. Das kleine Brutto von H9 B kehrt sich durch die Auswahl ins Minus
- H10b gegen Zufallsrichtung mit gleicher Ausführung: 18 % der 1.000 Läufe sind mindestens so gut, 95-%-Quantil −0,073 R, H10b −0,084 R

Die Berührungs-Variante ist keine realistische Ausführung: Ein Limit zum aktuellen Open wird damit immer in der ersten Minute gefüllt, das entspricht einem Market-Einstieg zum Maker-Tarif. Sie zeigt nur, was ohne negative Auswahl möglich wäre, und selbst dann erreicht keine Regel das Kriterium.

**Entscheidung H10:** abgelehnt. Mit Limit-Orders sinken die Kosten wie erwartet, aber die Fills sind systematisch schlechter als der Durchschnitt. Bei H10a bleibt netto ein kleiner Rest von +1,6 bps je Trade mit t = 0,8, in R negativ. Kein Nautilus-Lauf, kein OOS-Test.

**Ergebnis H11** (24.10.2026, 29.184 Stunden In-Sample, `python -m scan.umkehr_scan`)

- keine der 54 Zellen erreicht t ≥ 3,3. Ohne Korrektur liegt nur eine Zelle über t = 2 (24-h-Fall um mehr als 4 σ, 24 h danach, 8 Ereignisse) und drei Zellen unter t = −2, zusammen etwa so viele, wie der Zufall bei 54 Zellen erwarten lässt
- Nach Fällen ist die Folgerendite über 24 h in allen neun Zellen positiv (+16 bis +341 bps), nach Anstiegen geht der Kurs über 24 h in acht von neun Zellen weiter nach oben. Beides ist im Wesentlichen der allgemeine Aufwärtstrend: Über alle Stunden steigt BTC im Mittel um +15,6 bps in 24 h. Nach Fällen um 2 σ liegt die Folgerendite mit +16 bis +17 bps genau auf diesem Niveau
- über 1 h und 4 h gibt es keine Umkehr. Nach Fällen über 1 h läuft der Kurs eher leicht weiter (−3 bis −25 bps Umkehr, nicht signifikant)
- Ereignisse über 3 σ und 4 σ sind selten (8 bis 204 je Zelle in 40 Monaten), die großen Mittelwerte der seltenen Zellen hängen an einzelnen Tagen

**Entscheidung H11:** abgelehnt. Eine Umkehr nach starken Bewegungen, die über den allgemeinen Aufwärtstrend hinausgeht, ist auf BTC 2023 bis 2026 nicht messbar. Nach dem vorab festgelegten Protokoll wird keine Handelsregel gebaut. Varianten: 54 Zellen.

---

## Zwischenstand und Abbruchregel (24.10.2026)

Gregors Auftrag: weiter recherchieren, bis eine profitable Strategie gefunden ist. Bisher getestet: H1 bis H11 mit zusammen über 300 Varianten und Zellen. Jede weitere Suche erhöht die Wahrscheinlichkeit eines Zufallstreffers. Deshalb gilt ab hier:

- nur noch Ansätze mit strukturellem Grund (Risikoprämie oder Marktmechanik), nicht nur ein statistisches Muster
- je Hypothese eine vorab festgelegte Hauptregel, Varianten nur beschreibend
- höchstens zwei weitere Hypothesen (H12, H13), danach Zusammenfassung statt weiterer Suche

Recherche-Grundlage:

- Trendfilter auf BTC: Grayscale Research (2012 bis 2023) fand mit 50-Tage-Schnitt und 150-Tage-EMA höhere Sharpe Ratios als Halten (1,9 gegen 1,3), ohne Gebühren. Eine vorab registrierte Open-Source-Studie (crypto-trend-research) halbierte mit Trend und Volatilitätssteuerung den größten Verlust (−77 % auf −34 %), lag aber bei der Rendite unter Halten (28 % gegen 44 % p.a.), und der Sharpe-Vorteil war statistisch nicht gesichert
- Carry: Halten von BTC und gleich großer Short im Perp vereinnahmt das Funding ohne Kursrisiko. Strukturelle Prämie, solange Longs mehr Hebel nachfragen. Die genannte Studie fand mit 25 bps Kosten je Seite einen Verlust, bei Gregors Kosten (3 bps) ist das anders zu bewerten

---

## H12: Trendfilter gegen Halten

**Idee:** Kein Timing-Vorteil beim Einstieg (siehe H7c), sondern Risikosteuerung: BTC nur halten, solange der Trend intakt ist. Die Frage ist nicht, ob die Regel Geld verdient (das tut in einem steigenden Markt fast jede Long-Regel), sondern ob sie risikobereinigt besser ist als einfaches Halten.

**Regeln** (scan/trendfilter_scan.py)

- Tagesschluss UTC. Liegt der Schluss von Tag d über dem einfachen 200-Tage-Schnitt der Schlüsse, ist die Position an Tag d + 1 long mit Faktor 1, sonst flach
- jeder Wechsel kostet einmal Taker (3 bps), solange long fällt Funding mit dem festen Satz an (Perp)
- Vergleich: BTC halten ohne Kosten und ohne Funding (Spot)

**Daten:** Yahoo BTC-USD 2015-01-01 bis 2026-04-30 (Hauptauswertung), Teilzeiträume 2015 bis 2022 und 2023 bis April 2026. Für 2023 bis 2026 zusätzlich mit Kraken-Tageskerzen.

**Vorab festgelegt**

- Hauptregel: 200-Tage-Schnitt. Beschreibend: 50-Tage-Schnitt und 150-Tage-EMA aus der Grayscale-Studie, 125-Tage-Schnitt
- Kennzahlen: Rendite p.a., Volatilität p.a., Sharpe (ohne Zins), größter Verlust, Zeit im Markt, Anzahl Wechsel
- Erfolgskriterium: Sharpe der Regel höher als beim Halten, mit 95-%-Konfidenzintervall der Differenz über null (Block-Bootstrap mit Wochenblöcken, 2.000 Läufe), und größter Verlust kleiner als beim Halten, jeweils im Gesamtzeitraum

---

## H13: Carry mit BTC als Sicherheit

**Idee:** BTC als Sicherheit bei Kraken Futures hinterlegen und dieselbe Menge PF_XBTUSD short halten. Kursrisiko null (bis auf Abwicklungs- und Börsenrisiko), Ertrag ist das Funding, solange es positiv ist.

**Regeln** (scan/carry_scan.py)

- Short dauerhaft, Ertrag je Stunde = relativeFundingRate von Kraken, Kosten einmal Taker beim Öffnen und Schließen
- Daten: echtes Kraken-Funding ab 2025-10-15 (nur so weit zurück verfügbar). Der Zeitraum überschneidet sich mit dem OOS-Zeitraum. Das ist hier vertretbar, weil die Regel keine Parameter hat
- beschreibend zusätzlich: Variante, die nur short ist, wenn das Funding der Vorstunde positiv war

**Kennzahlen:** Ertrag p.a., Anteil Stunden mit negativem Funding, schlechteste 30 Tage, Vergleich mit dem US-Geldmarktzins. Kein Erfolgskriterium im statistischen Sinn, die Frage ist die Größenordnung.

**Ergebnis H12** (24.10.2026, `python -m scan.trendfilter_scan`)

| Regel | Zeitraum | Rendite p.a. | Volatilität | Sharpe | größter Verlust | im Markt | Wechsel |
|---|---|---|---|---|---|---|---|
| SMA200 (Haupttest) | 2015 bis 04/2026 | 58,4 % | 52,9 % | 1,13 | −70,2 % | 62 % | 74 |
| Halten | 2015 bis 04/2026 | 68,3 % | 66,2 % | 1,12 | −83,4 % | 100 % | 0 |
| SMA200 | 2023 bis 04/2026 | 36,1 % | 39,1 % | 0,98 | −32,0 % | 70 % | 32 |
| Halten | 2023 bis 04/2026 | 58,2 % | 47,6 % | 1,20 | −49,7 % | 100 % | 0 |

- Sharpe-Differenz SMA200 minus Halten im Gesamtzeitraum: 95-%-Intervall −0,36 bis +0,40, also kein gesicherter Unterschied
- der größte Verlust ist kleiner (−70 % statt −83 %), die Rendite aber ebenfalls (58 % statt 68 % p.a.). Seit 2023 ist der Filter in allen Kennzahlen außer dem größten Verlust schlechter als Halten
- Kraken-Schlüsse 2023 bis 2026 liefern praktisch dieselben Zahlen wie Yahoo
- beschreibend, nicht als Ergebnis zu werten: SMA125 (Sharpe 1,43) und SMA50 (1,39) schneiden im Gesamtzeitraum besser ab als SMA200. Das ist eine Auswahl im Nachhinein aus vier Längen und passt zur Beobachtung der Quelle, dass der 200-Tage-Schnitt unter den Längen eher schwach ist

**Entscheidung H12:** abgelehnt nach dem Kriterium. Der Trendfilter senkt Volatilität und größten Verlust, ist risikobereinigt aber nicht nachweisbar besser als Halten und bringt weniger Rendite. Er ist eine Frage der Risikoneigung, kein Vorteil.

**Ergebnis H13** (24.10.2026, `python -m scan.carry_scan`, Kraken-Funding 15.10.2025 bis 24.10.2026)

- dauerhaft short gegen BTC als Sicherheit: +3,48 % Funding in 374 Tagen, nach Öffnen und Schließen +3,34 % p.a.
- 30,8 % der Stunden mit negativem Funding, Februar bis April 2026 drei Monate leicht negativ, schlechteste 30 Tage −0,31 %
- Variante nur bei positivem Vorstunden-Funding: −26 % p.a., weil über 1.000 Wechsel die Gebühren verursachen
- Vergleich: US-Leitzins seit 16.09.2026 bei 3,75 bis 4,00 %. Ein US-Geldmarktfonds hätte im selben Zeitraum mehr gebracht, ohne Börsen- und Abwicklungsrisiko

**Entscheidung H13:** abgelehnt. Das Carry ist positiv und fast risikolos gegenüber dem BTC-Kurs, liegt aber unter dem Zins für Bargeld. Interessant würde es erst in Phasen mit hohem Funding (in Bullenmärkten historisch 10 % p.a. und mehr), die mit dem verfügbaren Kraken-Jahr nicht abgebildet sind.

---

## Abschluss der Suche (24.10.2026)

Nach der Abbruchregel endet die Suche hier. Getestet wurden 13 Hypothesen mit zusammen über 330 Varianten und Zellen, alle auf BTC.

- Keine Einstiegsregel schlägt nach Kosten den Zufall: Sweeps (H2 bis H5), Fib-Pullback (H6), Ausbrüche (H7, H7c), Uhrzeit (H8), Intraday-Momentum (H9), Limit-Ausführung (H10), Umkehr nach starken Bewegungen (H11)
- Positiv sind nur Ansätze, die den langfristigen Anstieg von BTC mitnehmen. Sie verdienen Geld, weil BTC gestiegen ist, nicht wegen des Signals. Der Trendfilter (H12) tauscht etwas Rendite gegen kleinere Verluste, ohne risikobereinigt besser zu sein
- Die einzige strukturelle Prämie (Carry, H13) liegt derzeit unter dem Geldmarktzins
- Brutto-Effekte von 1 bis 7 bps existieren, sind aber kleiner als die Kosten. Mit Limit-Orders werden sie von der negativen Auswahl der Fills aufgezehrt

---

## Nachtrag zur Abbruchregel (24.10.2026)

Gregor hat nach dem Abschluss zwei weitere Ideen aus einer externen Übersicht freigegeben, beide zu testen. Damit sind es 15 Hypothesen. Für H14 und H15 gilt je genau eine vorab festgelegte Regel und wegen zwei gleichzeitiger Tests die Schwelle t ≥ 2,24 (Bonferroni, 5 %). Danach keine weiteren Hypothesen ohne neuen Marktgrund.

---

## H14: Liquidationskaskade nach Open-Interest-Aufbau

**Idee (externe Übersicht, Gregor 24.10.2026):** Steigt das Open Interest stark, während der Preis seitwärts läuft, bauen Hebel-Trader Positionen auf. Bricht der Preis dann aus der Range, lösen die Stops und Liquidationen der falschen Seite eine Kaskade in Ausbruchsrichtung aus. Ohne Funding-Historie (nur ein Jahr) lässt sich die überfüllte Seite nicht bestimmen, deshalb wird in die Richtung des ersten Ausbruchs gehandelt.

**Daten:** Kraken Open Interest PF_XBTUSD stündlich ab 2023-03-07 (scripts/fetch_derivatives.py). Nur Kraken, nicht der Gesamtmarkt.

**Regeln** (scan/oi_kaskade_scan.py)

- zu jeder vollen Stunde t: ΔOI = OI-Schluss der Stunde vor t gegen OI-Schluss 24 h davor, z_OI = (ΔOI − Mittel) / Standardabweichung der ΔOI der 720 Stunden davor
- Preis seitwärts: |r_24h| ≤ 1 × σ_24 (Definition wie H11)
- Setup bei z_OI ≥ 2 und Preis seitwärts. Range = Hoch und Tief der 24 h vor t
- Einstieg per Stop-Market (Taker) beim ersten Bruch innerhalb von 24 h: über dem Range-Hoch Long, unter dem Range-Tief Short. Bricht eine Minute beide Seiten, kein Trade
- SL per Stop-Market in der Range-Mitte, TP als Limit eine Range-Höhe jenseits des Ausbruchslevels (Maker), Zeitstopp 24 h. R = Abstand Einstieg zu SL
- ein Setup zur Zeit, ein neues erst nach Ende des Trades oder Verfall
- Funding mit festem Satz

**Vorab festgelegt** (In-Sample 2023-03 bis 2026-04)

- Erfolgskriterium: netto über null mit t ≥ 2,24, ohne die drei besten Trades positiv, 2023, 2024 und 2025 jeweils positiv
- Kontrolle 1, Zufallsrichtung: an denselben Einstiegszeiten mit zufälliger Richtung und gleicher Geometrie, 1.000 Läufe, H14 über dem 95-%-Quantil
- Kontrolle 2, ohne Open Interest: dieselbe Regel für alle Seitwärts-Setups ohne OI-Bedingung. H14 muss netto darüber liegen, sonst trägt das Open Interest nichts bei
- beschreibend: ab 2025-10 Aufteilung nach Vorzeichen des echten Fundings beim Einstieg

---

## H15: SMC-Kette mit Sweep, MSS und FVG

**Idee (externe Übersicht, Gregors Trading-Stil, 24.10.2026):** Sweep eines wichtigen Levels mit Docht, Bestätigung durch einen Market Structure Shift auf kleiner Zeiteinheit, Einstieg im Retest des Fair Value Gaps, Stop knapp hinter dem Docht. Abgrenzung zu H2 bis H5: dort nur Sweep und Wick-Geometrie auf 1h, hier die volle Kette mit Bestätigung auf 5m.

**Regeln** (scan/smc_kette_scan.py), Long beschrieben, Short spiegelbildlich

- Level: 1h-Swing-Tiefs nach Trado-Definition (k = 5, nutzbar ab Bestätigung), solange nicht unterschritten
- Sweep: eine 15m-Kerze handelt unter ein aktives Level und schließt wieder darüber. Sweep-Tief = Tief dieser Kerze. Alle dabei unterschrittenen Level fallen weg
- MSS: das jüngste bestätigte 5m-Swing-Hoch (k = 2) vor dem Schluss der Sweep-Kerze, höchstens 4 h alt. MSS, wenn innerhalb von 12 Kerzen (1 h) nach dem Sweep ein 5m-Schluss darüber liegt. Fällt der Kurs vorher unter das Sweep-Tief, verfällt das Setup
- FVG: jüngste bullische Lücke auf 5m zwischen Sweep und MSS (Tief der Kerze i über dem Hoch der Kerze i − 2). Ohne FVG kein Trade
- Einstieg: Limit (Maker) in der Mitte des FVG, gültig 1 h ab MSS, gelöscht wenn der Kurs vorher unter das Sweep-Tief fällt. Füllung nur bei Durchhandeln (wie H10)
- SL per Stop-Market 0,1 × ATR14 (1h) unter dem Sweep-Tief, TP als Limit bei 2,5 R (CRV aus der Übersicht), Zeitstopp 24 h
- nur eine Position zur Zeit

**Vorab festgelegt** (In-Sample 2023-01 bis 2026-04)

- Erfolgskriterium: netto über null mit t ≥ 2,24, ohne die drei besten Trades positiv, 2023, 2024 und 2025 jeweils positiv
- Kontrolle Zufallsrichtung: an denselben Einstiegszeiten mit zufälliger Richtung, gleichem SL-Abstand und CRV, 1.000 Läufe, H15 über dem 95-%-Quantil
- beschreibend: Füllung bei Berührung, Anzahl Setups je Stufe der Kette

**Ergebnis H14** (24.10.2026, In-Sample 2023-04 bis 2026-04, `python -m scan.oi_kaskade_scan`)

| Regel | Trades | TP-Quote | R brutto | R netto | t-Wert | R ohne Top 3 | Haltedauer h |
|---|---|---|---|---|---|---|---|
| H14 (z_OI ≥ 2, seitwärts) | 75 | 16,0 % | −0,142 | −0,180 | −1,4 | −0,270 | 14,2 |
| Kontrolle ohne OI-Bedingung | 974 | 25,1 % | +0,063 | +0,015 | +0,4 | +0,009 | 12,9 |

- 460 Setup-Stunden mit starkem OI-Aufbau bei Seitwärtskurs, durch Bündelung und die Regel „ein Setup zur Zeit“ 75 Trades
- R netto je Jahr: 2023 −0,52, 2024 −0,13, 2025 −0,07, 2026 +0,01
- Zufallsrichtung an denselben Einstiegen: Mittel −0,108 R, 95-%-Quantil +0,080 R, 75 % der Läufe sind mindestens so gut wie H14
- Funding ab 2025-10 beschreibend: nur 13 Trades, alle Gruppen negativ
- Die Bedingung auf das Open Interest verschlechtert die Ausbruchsregel deutlich. Nach starkem OI-Aufbau setzt sich der Ausbruch seltener fort, nicht häufiger

**Entscheidung H14:** abgelehnt. Kein Hinweis auf Kaskaden in Ausbruchsrichtung, die sich mit Kraken-Open-Interest vorhersagen lassen. Einschränkung: Kraken-OI ist nur ein kleiner Teil des Gesamtmarkts.

**Ergebnis H15** (24.10.2026, In-Sample 2023-01 bis 2026-04, `python -m scan.smc_kette_scan`)

Stufen der Kette: 1.579 Sweeps mit Docht-Rückeroberung, davon 267 mit MSS innerhalb einer Stunde, davon 235 mit FVG. Gefüllt wurden 119 Orders (nur eine Position zur Zeit).

| Füllung | Trades | TP-Quote | R brutto | R netto | t-Wert | R ohne Top 3 | Risiko im Median |
|---|---|---|---|---|---|---|---|
| Durchhandeln (Haupttest) | 119 | 21,8 % | −0,062 | −0,143 | −1,0 | −0,211 | 52 bps |
| Berührung (beschreibend) | 120 | 22,5 % | −0,040 | −0,121 | −0,9 | −0,188 | 52 bps |

- Long 57 Trades −0,07 R, Short 62 Trades −0,21 R
- R netto je Jahr: 2023 −0,37, 2024 +0,02, 2025 −0,17, 2026 +0,06
- Bei CRV 2,5 liegt die Gewinnschwelle ohne Kosten bei 28,6 % Treffern, erreicht werden 21,8 %
- Zufallsrichtung mit gleichem Einstieg, Stop-Abstand und CRV: Mittel −0,128 R, 95-%-Quantil +0,067 R, 53 % der Läufe sind mindestens so gut wie H15
- Gebühren kosten rund 0,08 R je Trade, weil der Stop im Median nur 52 bps entfernt liegt

**Entscheidung H15:** abgelehnt. Die vollständige SMC-Kette ist auf BTC 2023 bis 2026 nicht besser als eine Münze für die Richtung. Kein Nautilus-Lauf, kein OOS-Test.

**Endstand:** 15 Hypothesen, keine mit belegtem Vorteil. Weitere Suche nur mit neuem Marktgrund oder neuen Daten.

---

> Zusammenführung 2026-11-11: H16 bis H26 entstanden parallel zu V1, V2 und H6 bis H15 auf einem eigenen Branch und hießen dort H6 bis H16. Beim Zusammenführen wurde um 10 weitergezählt. Der spike-bot und frühere Notizen verweisen teils noch auf die alten Nummern (H10 dort = H20 hier). Die Läufe von H16 bis H22 sind ohne Funding gerechnet. Für die finale H20-Variante nachgerechnet (add_funding): zusammen −0,02 R über 124 Trades, also vernachlässigbar, weil die meisten Trades nach Minuten bis wenigen Stunden enden. Elf Trades mit Zeitstopp ohne Kursänderung bekommen dabei r_net = NaN, weil die alten Trade-Listen kein risk_px haben. Neue Läufe sind davon nicht betroffen.

## H16: Wick-Füllung ETH mit Stop an der Oberkante

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
- Der OOS-Zeitraum wurde dabei berührt: 10 Trades der Variante ab 60 USD gesehen, überwiegend Verluste. Ein Lauf mit --oos ist für H16 deshalb keine saubere Prüfung mehr. Belastbar wäre nur das Mitprotokollieren neuer Fälle ab 12.11.2026
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

**Entscheidung H16:** abgelehnt. Mit den Labor-Regeln (Setup laufend geprüft, Einstiegsorder verfällt zur vollen Stunde, Fills über Nautilus) verschwindet der Vorteil aus der Chat-Vorarbeit. Dort lag er bei +0,18 bis +0,30 R mit 344 Trades. Er hängt also an Details der Umsetzung, vor allem am Einstieg nach Ablauf der Stunde, und ist kein robuster Effekt. Die TP-Quote liegt zwar über einem Zufallsverlauf, das reicht nach Gebühren aber nicht. Kein OOS-Test, der Zeitraum ist für H16 ohnehin berührt.

Festhalten: Der Hang von ETH-Wicks zur Füllung ist auf 1h messbar (Chat-Vorarbeit), aber klein. Bei kleinen Wicks fressen ihn die Gebühren, bei großen verschwindet er. Ein enger Stop an der Wick-Oberkante verbessert das Chance-Risiko-Verhältnis, macht die Regel aber empfindlich für Ausführungsdetails.

---

## H17: Limit-Short beim Rücklauf zum Open (ETH)

**Idee (Gregor, 11.11.2026):** Der Kurs bewegt sich innerhalb einer Stunde mindestens 30 USD vom Open weg und läuft in derselben Stunde bis auf 10 bis 15 % der Bewegung an den Open zurück. Dort Einstieg gegen den Rücklauf, Ziel 50 % Füllung, Stop leicht über dem Open.

**Regeln** (Skript außerhalb des Repos, Labordaten PF_ETHUSD, In-Sample 2023-01 bis 2026-04)

- Bewegung M = Open − bisheriges Extrem der Stunde, Setup ab M ≥ 30 USD, obere Seite spiegelbildlich mit Long
- Limit-Order bei Open − f × M (Maker), läuft bei neuem Extrem mit, nur innerhalb der Stunde
- Ziel Limit bei Open − 0,5 × M, Stop bei Open + s × M (Taker)
- Raster: f = 0,10 und 0,15, s = 0 / 0,05 / 0,10 / 0,15 / 0,20 / 0,30, Stundenende glattstellen, Stop auf Einstieg oder weiterlaufen lassen (72 Varianten)

**Ergebnis:** Alle Varianten schon brutto negativ (−0,03 bis −0,13 R), netto −0,09 bis −0,40 R bei t-Werten um −3 bis −5. Die Trefferquote liegt in jeder Variante leicht unter der eines Zufallsverlaufs mit gleichem Chance-Risiko-Verhältnis. Fast alle Trades entscheiden sich in 2 bis 11 Minuten.

**Entscheidung H17:** abgelehnt. Ein Rücklauf bis kurz vor den Open hat Schwung und läuft meist durch den Open, statt wieder halb in die Kerze zu fallen. Kein OOS-Test.

---

## H18: Freie Parametersuche über Rücklauf-Setups (ETH)

**Anlass (11.11.2026):** Nach H16 und H17 bewusst breite Suche, um zu sehen, ob irgendeine Variante der Wick- und Rücklauf-Idee trägt. Diese Suche verletzt das Protokoll mit wenigen vorab genannten Varianten absichtlich und ist deshalb nur als Erkundung zu werten.

**Vorgehen** (Skripte außerhalb des Repos, Labordaten PF_ETHUSD)

- Zwei Einstiegsarten: Limit beim Rücklauf (wie H17) oder Stop-Order nach der Umkehr (Rücklaufhoch − p × M)
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

**Entscheidung H18:** abgelehnt. Kein Rücklauf-Setup auf ETH 1h trägt über Zeiträume und realistische Ausführung. Die Lehren daraus fließen in H19 ein: Einstieg erst nach der Umkehr, nur große Bewegungen, bescheidenes Ziel.

---

## H19: Wick nach Spike zur Hälfte füllen (ETH und BTC)

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

**Entscheidung H19:** abgelehnt. Realistisch ausgeführt ist die Regel auf beiden Märkten und beiden Seiten nicht positiv, die einzige knapp positive Zelle (BTC obere Seite) hängt an den drei besten Trades. Kein OOS-Lauf, kein Protokoll-Skript.

Festhalten für künftige Hypothesen: Scans mit sehr engen Einstiegen und Stops (unter etwa 0,3 % vom Kurs) und Einstieg in der Minute der Umkehr überschätzen das Ergebnis deutlich, weil die Reihenfolge innerhalb einer Minute angenommen wird. Das betrifft auch die Chat-Vorarbeit zu H16 bis H18. Solche Regeln nur mit Nautilus bewerten oder mit Trade-Ticks rechnen.

---

## H20: Spike-Füllung mit weiterem Stop und Laufenlassen (ETH und BTC)

**Idee (Gregor, 11.11.2026):** H19 ist in Nautilus vor allem am engen Stop gescheitert, der in Spike-Minuten übersprungen wird. Mit mehr Abstand und der Möglichkeit, Gewinner laufen zu lassen, könnte die Regel tragen.

**Regeln** (strategies/spike_fill.py, erweitert um sl_ref, trail_start, trail_w)

- Spike, Erholung und Einstieg unverändert wie H19 (spike = 0,02, rb_min = 0,3, fill_in = 0,1, window = 180, cooldown = 15)
- Stop wahlweise über dem Erholungshoch (sl_ref = rh: RH + sl_w × W) oder über dem Spike-Start (sl_ref = start: S + sl_w × M)
- Laufenlassen (trail_w > 0): kein festes Ziel. Sobald der Kurs trail_start × W vom Erholungshoch Richtung Tief gelaufen ist, Stop auf den tatsächlichen Einstieg, danach nach jeder Minute auf bestes Niveau + trail_w × W nachziehen, nur in Gewinnrichtung
- Zeitstopp 72 h, Gebühren wie immer, nur Nautilus (der Scan überschätzt solche Regeln, siehe H19)

**Vorab festgelegtes Raster** (9 Kombinationen je Markt und Seite, 36 Läufe, nur In-Sample bis OOS_START)

- Stop: rh mit sl_w = 0,3, rh mit sl_w = 0,5, start mit sl_w = 0,1
- Ausstieg: festes Ziel fill_out = 0,5, festes Ziel fill_out = 1,0, Laufenlassen mit trail_start = 0,5 und trail_w = 0,5

**Nautilus, In-Sample 2023-01 bis 2026-04** (runs/20261111-2100_spike_fill_H20_raster, R netto)

| Markt | Seite | Stop | Ziel 50 % | Ziel 100 % | laufen lassen |
|---|---|---|---|---|---|
| ETH | untere | rh 0,3 / rh 0,5 / start 0,1 | −0,04 / −0,04 / −0,02 | −0,04 / −0,05 / −0,02 | −0,05 / −0,05 / −0,03 |
| ETH | obere | rh 0,3 / rh 0,5 / start 0,1 | −0,06 / +0,01 / +0,02 | −0,08 / +0,02 / +0,04 | −0,16 / −0,05 / −0,01 |
| BTC | untere | rh 0,3 / rh 0,5 / start 0,1 | −0,18 / −0,13 / −0,11 | −0,17 / −0,08 / −0,07 | −0,03 / −0,02 / −0,06 |
| BTC | obere | rh 0,3 / rh 0,5 / start 0,1 | +0,07 / +0,13 / +0,13 | +0,27 / +0,25 / +0,21 | −0,01 / +0,05 / +0,10 |

- Jeder weitere Stop verbessert gegenüber H19 (dort −0,11 bis −0,15 R bei ETH)
- Laufenlassen ist in 10 von 12 Gruppen schlechter als ein festes Ziel, wie schon in H18
- ETH bleibt auf beiden Seiten bei null oder leicht negativ, BTC untere Seite negativ
- BTC obere Seite (Spike nach oben, Long nach dem Ende des Rücksetzers) ist in 8 von 9 Varianten positiv. Bestwerte: start 0,1 mit Ziel 50 % +0,13 R bei t = 4,3, TP-Quote 85 %, alle Jahre positiv (+0,16 / +0,11 / +0,12 / +0,16). Start 0,1 mit Ziel 100 % +0,21 R bei t = 3,3. Nur erster Trade je Tag: +0,13 R (t 3,3) bzw. +0,21 R (t 2,5). Rund 3 Trades pro Monat
- Prüfung auf Fills in der Einstiegsminute (Reihenfolge innerhalb der Minute angenommen): Bei BTC obere Seite tragen die länger laufenden Trades das Ergebnis (+0,11 bis +0,41 R, t bis 3,1). Trades mit Ausstieg in der ersten Minute liegen um null

**Einordnung:** 36 Zellen gerechnet, die positive Gruppe ist eine von vier Markt-Seiten-Kombinationen und hat auf ETH kein Gegenstück. Das spricht gegen einen allgemeinen Effekt. Für BTC ist es dennoch das stärkste Ergebnis im Labor bisher. Nächster Schritt laut Protokoll: eine Variante festlegen und einmal mit --oos rechnen (Zeitraum ab 2026-05 für diese Regel unberührt, in der H19-Vorarbeit aber mit engem Stop bereits gesehen).

**Finale Variante für den OOS-Test (festgelegt 2026-11-11 vor dem Lauf):** PF_XBTUSD, side = upper, sl_ref = start, sl_w = 0,1, fill_out = 0,5, sonst wie H19. Auswahlgrund: in allen vier Jahren positiv, höchster t-Wert. Einmaliger Lauf mit --oos ab 2026-05-01.

**OOS-Lauf** (2026-11-11, runs/20261111-203112_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5_OOS, 2026-05-01 bis 2026-11-11)

| Zeitraum | Trades | TP-Quote | R brutto | R netto | t-Wert | ohne Top 3 |
|---|---|---|---|---|---|---|
| In-Sample 2023-01 bis 2026-04 | 124 | 84,7 % | +0,16 | +0,13 | 4,3 | +0,11 |
| OOS 2026-05 bis 2026-11 | 17 | 88,2 % | +0,14 | +0,11 | 1,0 | +0,04 |

- 15 Gewinner mit +0,08 bis +0,51 R, 2 Verlierer mit je −1,04 R, Summe +1,9 R
- Profil mit hoher Trefferquote und kleinen Gewinnen: typischer Gewinn rund +0,25 R gegen −1 R Verlust. Die Gewinnschwelle liegt bei etwa 80 % Treffern. Sinkt die Trefferquote um wenige Prozentpunkte, wird die Regel negativ
- Trades gehäuft in wenigen Phasen (Juni und August 2026)

**Entscheidung H20:** OOS bestanden für BTC obere Seite mit Stop über dem Spike-Start und Ziel 50 %. Wegen kleiner OOS-Stichprobe, fehlendem Gegenstück auf ETH und dem engen Abstand zur Gewinnschwelle noch kein Einsatz in Trado. Nächster Schritt: neue Fälle ab 2026-11-12 mitprotokollieren (Paper), Entscheidung nach etwa 30 weiteren Trades.

---

## H21: Mehr Trades für die H20-Regel

**Ziel (Gregor, 11.11.2026):** Die H20-Regel (BTC, Spike nach oben, Stop über Spike-Start, Ziel 50 %) handelt nur etwa 3-mal im Monat. Gesucht sind mehr Trades ohne schlechteres Ergebnis pro Trade.

**Basis:** strategies/spike_fill.py mit side = upper, sl_ref = start, sl_w = 0,1, fill_out = 0,5, sonst wie H19. In-Sample BTC: 124 Trades, +0,134 R, t 4,3.

**Vorab festgelegte Läufe** (nur Nautilus, nur In-Sample bis OOS_START, je ein Hebel gegenüber der Basis)

- Kleinere Spikes: spike = 0,015 und 0,0175 (BTC)
- Längere Spikes: Spike-Dauer span = 10 und 15 Minuten statt 5, neuer Parameter span (BTC)
- Weitere Märkte: PF_SOLUSD (Tick 0,01) und PF_XRPUSD (Tick 0,0001) mit der Basisregel, Kontrakte neu in lab/instruments.py

**Übernahmekriterium:** R netto pro Trade nicht unter +0,13 und R pro Monat höher als bei der Basis. Der OOS-Zeitraum ist für die H20-Regel verbraucht, übernommene Hebel gelten nur nach Papier-Beobachtung als bestätigt.

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

**Entscheidung H21:** abgelehnt, die H20-Regel bleibt unverändert. Mit ETH, SOL und XRP gibt es jetzt drei Märkte ohne den Effekt. Das erhöht den Verdacht, dass H20 auf BTC eine Eigenheit oder ein Zufallstreffer ist, und spricht umso mehr für die Papier-Beobachtung vor jedem Einsatz.

---

## H22: Liquidationen als Ursache der H20-Regel

**Idee (Forum-Input, 11.11.2026):** Ein Vorteil entsteht dort, wo jemand zu einem schlechten Preis handeln muss. Bei H20 wäre das ein Short-Squeeze: Liquidierte Shorts kaufen zu jedem Preis, der Spike schießt über, danach läuft ein Teil zurück. Trifft das zu, laufen H20-Trades mit Liquidationen im Spike besser als solche ohne. Ein Unterschied würde H20 erklären, kein Unterschied wäre eine Warnung vor einem Zufallstreffer.

**Daten:** Kraken Futures Analytics, liquidation-volume für PF_XBTUSD als 1-Minuten-Werte ab 2023 (scripts/fetch_analytics.py). Der Wert trennt nicht nach Long und Short. Bei einem Spike nach oben werden aber fast nur Shorts liquidiert.

**Regeln** (festgelegt 2026-11-11 vor dem Rechnen, keine neue Strategie, Auswertung der vorhandenen H20-Trades)

- Trades: finale H20-Variante, In-Sample runs/20261111-204153_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5 (124 Trades), OOS runs/20261111-203112_spike_fill_sideupper_sl_refstart_sl_w0.1_fill_out0.5_OOS (17 Trades)
- Spike-Minuten je Trade: Minuten vor dem Einstieg, deren Hoch das höchste der letzten 5 Minuten ist und mindestens 2 % über dem Tief dieser 5 Minuten liegt. Gesucht wird bis 190 Minuten vor dem Einstieg, verwendet wird die letzte zusammenhängende Gruppe (Abstand höchstens 5 Minuten)
- Liquidationsfenster: 4 Minuten vor der ersten bis 1 Minute nach der letzten Spike-Minute
- Kennzahl L: Summe des Liquidationsvolumens im Fenster
- Aufteilung 1: L = 0 gegen L > 0
- Aufteilung 2: L unter gegen ab dem Median der In-Sample-Trades
- Keine weiteren Schnitte und keine Suche nach Schwellen

**Kriterium:** Der Mechanismus gilt als gestützt, wenn in beiden Aufteilungen die Gruppe mit mehr Liquidationen um mindestens 0,1 R besser ist und in mindestens einer Aufteilung der t-Wert der Differenz (Welch) über 2 liegt. Nur dann werden die OOS-Trades einmal mit derselben Aufteilung (Median aus In-Sample) geprüft, dort zählt nur die Richtung. Ein Filter für den spike-bot folgt daraus erst nach Papier-Beobachtung.

**Ergebnis** (2026-11-11, runs/20261111-2200_h22_liquidationen, R netto aus den Nautilus-Trades)

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

**Entscheidung H22:** Mechanismus mit Kraken-Daten nicht gestützt, aber auch nicht widerlegt, weil Kraken die marktweiten Liquidationen kaum abbildet. H20 bleibt unverändert in der Papier-Beobachtung. H23 baut auf H22 auf und wird zurückgestellt, bis es marktweite Liquidationsdaten gibt oder H24 bzw. H25 etwas Neues zeigen.

---

## H23 bis H26: geplante Hypothesen aus dem Forum-Input

Grundsatz: Jede Regel beginnt bei einem Marktteilnehmer, der zu einem schlechten Preis handeln muss. Die Regeln unten sind Entwürfe und werden vor dem jeweiligen Lauf endgültig festgelegt.

- H23 Positionierung vor dem Spike: H20 nur, wenn vor dem Spike-Start die Shorts überwiegen. Messgrößen Basis bzw. Perp minus Spot im Mittel der 60 Minuten davor und das Kontenverhältnis aus long-short-info. Nur sinnvoll, wenn H22 den Mechanismus stützt
- H24 Long-Liquidationskaskade: Liquidationsvolumen in höchstens 5 Minuten weit über dem Üblichen bei fallendem Kurs, Long auf den Rücklauf nach dem Muster von H20. Auslöser ist hier der Mechanismus, nicht die Kerzenform. Abgrenzung zu H14: dort Ausbruch nach Open-Interest-Aufbau (abgelehnt), hier Umkehr nach der Kaskade
- H25 Premium- bzw. Funding-Extrem: Basis über mehrere Stunden extrem, danach 1 bis 3 Tage gegen die Mehrheit. Funding ist seit V1 im Lab (fester Satz), echte Raten gibt es bei Kraken nur ab 2025-10, die Basis ab 2023. Abgrenzung zu H13: dort Funding vereinnahmen (Carry), hier Umkehr nach Extremen
- H26 Trend auf Tagesbasis: entfällt, in der parallelen Reihe mit H7 (Donchian), H7c (längere Historie) und H12 (Trendfilter) bereits geprüft, jeweils ohne Mehrwert gegenüber Halten

---

## H28: Trendfilter rückwirkend auf alle vorhandenen Trade-Listen

**Idee (Gregor, 13.11.2026):** Viele Setups könnten besser sein, wenn nur in Richtung des übergeordneten Trends gehandelt wird. Ein Filter, der bei den meisten bisherigen Strategien die Trades gegen den Trend aussortiert und damit das Ergebnis hebt, wäre ein allgemeiner Baustein für Trado.

**Regeln** (festgelegt 2026-11-13 vor dem Rechnen, scan/h28_trendfilter.py, keine neuen Backtests)

- Trade-Listen: alle Nautilus-Läufe in runs/ mit mindestens 30 Trades vor OOS_START. Nicht verwendet werden der OOS-Lauf von H20 und die H22-Auswertung (Kopie der H20-Trades). Das H20-Raster zählt je Zelle als eigener Lauf
- Trend zum Einstieg aus den bis dahin abgeschlossenen 4h-Kerzen des gehandelten Markts
- T1 4h-EMA wie Trado: aufwärts bei EMA20 > EMA50 und Schluss > EMA50, abwärts spiegelbildlich, sonst gemischt. EMA als exponentieller Durchschnitt über das ganze Archiv (Trado nutzt die letzten 600 Kerzen, der Unterschied ist bei EMA50 vernachlässigbar)
- T2 4h-Marktstruktur: Swings mit k = 5 (Hoch bzw. Tief über bzw. unter je 5 Kerzen davor und danach, erst 5 Kerzen später bekannt). Aufwärts, wenn die letzten beiden bekannten Swing-Hochs und Swing-Tiefs jeweils steigen, abwärts spiegelbildlich, sonst gemischt
- Gruppen je Lauf: mit dem Trend (Long bei aufwärts, Short bei abwärts), gegen den Trend, gemischt
- R netto wie in den Läufen gespeichert, ohne Neuberechnung

**Kriterium:** Ein Trendfilter gilt als allgemein hilfreich, wenn in mindestens zwei Dritteln der Läufe das R mit dem Trend über dem R aller Trades liegt und der Median der Differenz mit dem Trend gegen gegen den Trend mindestens +0,05 R beträgt. Beide Definitionen werden getrennt bewertet. Für einzelne Strategien ist das Ergebnis nur ein Hinweis, eine gefilterte Strategie braucht einen eigenen Test mit OOS.

**Ergebnis** (2026-11-13, runs/20261113-1312_h28_trendfilter, 49 Läufe aus H1 bis H5, H7 und H16 bis H21, In-Sample)

| Trend | Läufe mit Trend besser als alle | Median Differenz mit gegen gegen | Anteil Trades mit / gegen / gemischt | Läufe mit R > 0 vorher / nachher |
|---|---|---|---|---|
| T1 4h-EMA | 65 % | +0,04 R | 42 / 43 / 15 % | 19 / 26 von 47 |
| T2 4h-Struktur | 76 % | +0,06 R | 26 / 30 / 44 % | 20 / 28 von 49 |

- T1 verfehlt das Kriterium knapp (zwei Drittel und +0,05 R), T2 erfüllt es formal
- Die Läufe sind nicht unabhängig: 18 stammen aus dem H20-Raster, viele weitere sind Varianten derselben Regel. Nach Strategie-Familien zusammengefasst ist der Struktur-Filter nur in 6 von 11 Familien mehrheitlich besser
- Der Filter verschiebt das Ergebnis im Mittel um wenige Hundertstel R. Keine bisher abgelehnte Strategie wird dadurch klar positiv. Die größten Sprünge (ETH-Wick-Füllung, bis +1,0 R) beruhen auf 17 bis 45 Trades
- T2 behält nur ein Viertel der Trades. Die Gruppe ohne klare Struktur (gemischt) ist oft schlechter als die Gruppe gegen den Trend. Das spricht eher für „nur bei klarer Struktur handeln“ als für „nur mit dem Trend“. Das ist nicht vorab festgelegt und nur eine Beobachtung
- H20 (finale Variante): alle +0,13 R (124), mit T2-Trend +0,23 R (31), gegen +0,13 R (50), gemischt +0,07 R (43). Mit T1: mit +0,17 R (54), gegen +0,14 R (48)

**Entscheidung H28:** Ein Trendfilter ist kein Hebel, der schwache Strategien rettet. T2 bleibt als Baustein für H29 und künftige Hypothesen, jeweils vorab festgelegt und mit eigenem OOS-Test. Für H20 ergibt sich kein Grund, die Regel zu ändern.

---

## H29: Zonen-Setups mit dem Trend

**Idee (Gregor, 13.11.2026):** An starken Zonen in Trendrichtung einsteigen: im Aufwärtstrend an einer Unterstützung kaufen, nach einem Ausbruch den Retest des alten Widerstands kaufen, Short spiegelbildlich. Dazu prüfen, ob mehrere Ziele und ein nachgezogener Stop besser sind als ein festes Ziel.

**Vorgehen in Stufen,** jede Stufe dünnt die nächste aus, um bei vielen Varianten Zufallstreffer zu vermeiden.

**Zonen** (nur aus abgeschlossenen Kerzen, ATR = ATR14 der 4h-Kerzen)

- Z1 mehrfach berührt: 4h-Swings mit k = 5 der letzten 100 Tage. Nach Preis sortiert werden Nachbarn mit Abstand höchstens 0,5 ATR zu Gruppen zusammengefasst, Spanne einer Gruppe höchstens 1 ATR, mindestens 3 Swings. Hochs und Tiefs zählen beide (Rollentausch). Zone = Spanne der Gruppe, neu nach jedem 4h-Schluss
- Z2 Tages- und Wochenextreme: Hoch und Tief des Vortags und der Vorwoche (UTC, Woche ab Montag), Zone = Niveau ± 0,1 ATR
- Z3 runde Zahlen: Vielfache von 1.000 USD bei BTC und 50 USD bei ETH, Zone = Niveau ± 0,1 %
- Z4 Volumenknoten: 1m-Volumen der letzten 30 Tage in Preisstufen von 0,25 %, je Minute dem typischen Preis (H + L + C) / 3 zugeordnet. Knoten = Stufe mit Volumen über dem 90-%-Quantil, die zugleich das Maximum ihrer zwei Nachbarn je Seite ist. Zone = Stufe, neu täglich um 00:00 UTC. Nur Kraken-Volumen

**Setups** (Long beschrieben, Short spiegelbildlich bei Abwärtstrend und Widerstand)

- S1 Rücklauf: Trend aufwärts, Zone unter dem Kurs. Auslöser ist die erste Berührung der Oberkante (1m-Tief ≤ Oberkante), nachdem der Kurs seit der letzten Berührung mindestens 1 ATR über der Oberkante lag
- S2 Ausbruch und Retest: Eine 4h-Kerze schließt über der Oberkante einer Zone, die beim Öffnen dieser Kerze über dem Kurs lag. Auslöser ist die erste Berührung der Oberkante innerhalb der folgenden 12 4h-Kerzen, bei Trend aufwärts im Moment der Berührung
- Trend T1 oder T2 wie in H28
- Einstieg als Limit an der Oberkante, Stop bei Unterkante − 0,25 ATR, R = Einstieg − Stop
- Je Zelle höchstens ein Trade gleichzeitig, Zeitstopp 72 h

**Stufe 1, Scan brutto** (scan/h29_zonen_scan.py, In-Sample BTC bis OOS_START, 32 Zellen: 2 Setups × 4 Zonen × 2 Trenddefinitionen × Long/Short)

- Messgröße: Ergebnis eines 1:1-Brackets (+1R oder −1R, sonst Schlusskurs nach 72 h in R), ohne Gebühren
- In der Minute der Berührung zählt ein Erreichen des Stops als Verlust, das Ziel erst ab der Folgeminute
- Kontrolle: je Zone 5 Kontrollzonen gleicher Breite, um zufällig 1 bis 3 ATR nach oben oder unten verschoben (fester Zufallsstartwert), mit denselben Auslöse- und Trendregeln
- Weiter in Stufe 2 nur Zellen, deren mittleres R über dem der Kontrollzonen liegt mit t ≥ 3 (Welch) und selbst über null

**Stufe 2, Ausstiege in Nautilus** (nur für die Zellen aus Stufe 1, netto mit Gebühren und Funding)

- A1 ein Ziel bei 2R
- A2 Teilziele 50/30/20 % bei 1R, 2R und 3R, nach dem ersten Teilziel Stop auf den Einstieg
- A3 50 % bei 1R, danach Stop auf den Einstieg und nach jeder abgeschlossenen 1h-Kerze unter das letzte bekannte 1h-Swing-Tief (k = 2) nachgezogen, nur in Gewinnrichtung
- Kriterium wie bei H6: netto über null, t ≥ 2,5, ohne die drei besten Trades positiv, in mindestens zwei der drei vollen Jahre 2023 bis 2025 positiv, auf ETH mit denselben Parametern dasselbe Vorzeichen

**Stufe 3:** Die beste Variante aus Stufe 2 genau einmal mit --oos. Danach Papier-Beobachtung, erst dann Trado.

**Ergebnis Stufe 1** (2026-11-13, runs/20261113-1315_h29_zonen_scan_PF_XBTUSD, BTC In-Sample 2023-04 bis 2026-04, brutto, 1:1-Bracket)

| Zone | Trades (alle Zellen) | R Zone | R Kontrolle | Zellen besser als Kontrolle |
|---|---|---|---|---|
| Z1 mehrfach berührt | 1.253 | 0,00 | +0,05 | 2 von 8 |
| Z2 Tages- und Wochenextreme | 1.762 | −0,05 | +0,01 | 2 von 8 |
| Z3 runde Zahlen | 3.752 | −0,06 | +0,04 | 0 von 8 |
| Z4 Volumenknoten | 860 | +0,06 | 0,00 | 6 von 8 |

- Keine der 32 Zellen erreicht t ≥ 3 gegenüber den Kontrollzonen, der beste Wert liegt bei 1,3 (S2, Z4, Long, T1, 94 Trades, +0,17 R)
- Die Trefferquote des 1:1-Brackets liegt fast überall zwischen 44 und 59 %, also beim Münzwurf. Mit dem Trend und an einer Zone einzusteigen verschiebt das nicht messbar
- Runde Zahlen und Tagesextreme sind sogar etwas schlechter als beliebige Niveaus daneben (t bis −2,6). Das passt dazu, dass solche Niveaus von vielen gesehen und eher durchlaufen werden, ist aber nicht vorab als Hypothese formuliert
- Volumenknoten sind als einzige Zone im Mittel besser als die Kontrolle (+0,06 R gegen 0,00), aber in keiner Zelle signifikant. Das ist nur Kraken-Volumen
- Gebühren fehlen noch. Bei R-Abständen von meist 0,5 bis 1,5 ATR (4h) kosten sie etwa 0,02 bis 0,05 R je Trade

**Entscheidung H29:** In Stufe 1 abgelehnt. Die Zonen tragen gegenüber zufälligen Niveaus keine Information, die ein 1:1-Bracket ausnutzen könnte. Stufe 2 (Teilziele, nachgezogener Stop) wird für diese Setups nicht gerechnet, weil ein Ausstieg aus einem Einstieg ohne Vorteil keinen Vorteil macht. Getestet: 32 Zellen, dazu je Zelle 5 Kontrollreihen.
