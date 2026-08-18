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
| 36 | rot2 (:) — second configuration, inequivalent to the first (different loop rows) | `:JK1J9OCK6AORRVEH56QXLV25MWCIAS0301DS7MYZWZ7PHN3DUX4E29TUIL488BPTFNBQGYFG` (exact class rot2; rct4-type structure: quarter-turn orbits off the long axes + a half-turn loop on each axis; loops (1,1),(34,34) and (9,26),(26,9)) | mac-m3 (second solver): `PAIRS="1,1;9,26" ./there 36 2 1280 120` — found in 26 s in the finding sweep of the two-loop family; certified 2026-08-18 |
| 36 | rot2 (:) — third configuration, inequivalent to the first two | `:DK1GGNLRBK7RNPSU35AH6QIV26LZ3D04XYBQ9O12VZMW0ETX4H9TIPUW57AC8SFO8ECJJYFM` (exact class rot2; rct4-type structure; loops (1,1),(34,34) and (7,28),(28,7)) | mac-m3 (second solver): exhaustive sweep of the two-loop family, sub-class x=1,y=7 (`ALL=1 PAIRS="1,1;7,28" ./there 36 2`, 2 labelled solutions = 1 configuration up to the diagonal reflections); certified 2026-08-18 |
| 37 | rot2 | `:FJ7E4PBGKO6U5VDZDH9RCF2X4QSTIZQa2X0SEM8a3Y0A1I78AW3YLO9RJN1N5V6UCGKPBWMTHL` | linux-12c, there_tw sym9 PAIRS=2,4;4,20;20,34 (odd-cycle defect family), exhaustive sub-class |
| 39 | rot2 | `:CGAWLU7M8CAN1FPZ2K9TXbOPYc7BBL5W3c2E4JIKJYOa0Z6XHRRV04DE159TIa3DNbFSQUGV8H6SMQ` | mac-m3, there_tw sym9 PAIRS=4,8;8,20;20,34 (odd-cycle defect family), exhaustive sub-class |
| 39 | rot2 (:) — second configuration, inequivalent to the first | `:BI5HCWEQST8J2MSU7X4M47Dc3aKRNZEH69NbDc1b0P1FTWLO3FBI2Z0PVYGY5V8AGaJU9ACO6QLXKR` (exact class rot2; C4 base + directed 3-cycle of half-turn pairs through the central class: (1,5),(37,33); (5,19),(33,19); (19,1),(19,37)) | VM2 (second solver): `ALL=1 PAIRS="1,5;5,19;19,1" ./there_tw 39 9` (central-class sweep of the 3-cycle family, `logs/sweeps/central3_sym9_n39.txt`); certified 2026-08-18 |
| 39 | rot2 (:) — third configuration, inequivalent to the first two | `:AEIUHR9P678GRYJP1XHZNc26CQ37NcAEIXTaMb4Y1G295KOS0FVZCQWa0F3L5bDJ4BMUVWDTBL8KOS` (exact class rot2; C4 base + 3-cycle through the central class: (4,7),(34,31); (7,19),(31,19); (19,4),(19,34)) | VM2 (second solver): `ALL=1 PAIRS="4,7;7,19;19,4" ./there_tw 39 9` (central-class sweep, `logs/sweeps/central3_sym9_n39.txt`); certified 2026-08-18 |
