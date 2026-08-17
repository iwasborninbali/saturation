# SUBMISSION — candidate entries for Achim Flammenkamp's database

Rule: a line enters this file only after (1) `saturation.certify` (2n tokens, every triple at
full rank), (2) `web/stab.py` says the exact class, (3) the class/size cell is *not already
complete* in his table (https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html), i.e. the
configuration can be new to the database.  Sending is the owner's decision.

Format: his encoding (class char + two column chars per row, alphabet of 90), one per line,
with provenance (who, machine, seed, seconds).

| n | class | encoded configuration | provenance |
|---|-------|-----------------------|------------|
| 33 | rot2 (:) | `:MOAC3H9J6GJOBS9B05PT0VPQHV5UEI2C4SKUEI2R1F671W37RWLN4L8DGQDNFTKM8A` | linux-12c, linux-12c: there_tw sym9 PAIRS=2,3;3,19;19,2 (C4 orbits + 3-cycle of half-turn pairs), exhaustive sub-class, 2026-08-17T00:50Z; note: the ':' cell at 33 shows '..' + n33.gif in the table (not empty); this book is inequivalent to the pictured one |
| 37 | rot2 (:) — cell empty in the table | `:GJ39EP7VENDZJRSX7P6ZCF28IQ4VWYKQFa06COUa0LAG245WAISYLO1UBT389H1NDM5TBMRXHK` | linux-12c, linux-12c: there_tw sym9 PAIRS=1,3;3,31;31,1 (C4 orbits + 3-cycle of half-turn pairs), exhaustive sub-class, 2026-08-17 ~01:2xZ |
| 36 | rot2 (:) — cell empty in the table | `:3NEHFSVZ3FPU6E2BNQ8I5GDS08JOTYVXDP9Y1QAM2416BGRZ7MJUHR9COXLT5AKW047KILCW` (exact class rot2; structure = rct4-type for even n: quarter-turn orbits off the long axes + a half-turn loop on each axis — his 'c' column is blank for all even n, so class char ':' or 'c' as he prefers) | mac-m3 (second solver): `PAIRS="6,6;5,30" ./there 36 2 28761 120` — C4 orbits + main-axis loop (6,6),(29,29) + anti-axis loop (5,30),(30,5); found in 103 s; 2026-08-17 09:50 |
