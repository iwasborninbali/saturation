# Letter 2 to Achim Flammenkamp — draft (second solver sends after the 39/41 sweeps finish)

```
Subject: no-three-in-line: two more n = 36 configurations (three in total), a second n = 39, and a correction to my wording

Dear Achim,

two follow-ups to my message of 17 August.

1. Two further 2n-point configurations for n = 36 with stabilizer exactly {identity, rot2},
inequivalent to the first one and to each other (checked by canonical forms under D4):
  :JK1J9OCK6AORRVEH56QXLV25MWCIAS0301DS7MYZWZ7PHN3DUX4E29TUIL488BPTFNBQGYFG
  :DK1GGNLRBK7RNPSU35AH6QIV26LZ3D04XYBQ9O12VZMW0ETX4H9TIPUW57AC8SFO8ECJJYFM
They come from the same family (quarter-turn orbits off the long diagonals plus one half-turn
pair on each diagonal, at rows (1,34) and (9,26), resp. (1,34) and (7,28)); an exhaustive
sweep of that family for n = 36 (153 sub-classes up to D4) shows that these three are all its
configurations.  And a second configuration for n = 39, inequivalent to the one I sent, for the
column ':' as well:
  :BI5HCWEQST8J2MSU7X4M47Dc3aKRNZEH69NbDc1b0P1FTWLO3FBI2Z0PVYGY5V8AGaJU9ACO6QLXKR
(quarter-turn orbits plus a 3-cycle of half-turn pairs (1,5),(37,33); (5,19),(33,19); (19,1),(19,37)
— the cycle passes through the central row and column).  As before: every triple checked in
exact integer arithmetic, stabilizer computed explicitly, and each configuration verified by two
independent programs.

2. A correction to the subject line of my previous message ("first configurations with exact
rot2 symmetry for n = 36, 37, 39"): that is right for n = 36 (both cells of your table were
empty), but for n = 37 and 39 your rct4 configurations of course already have stabilizer
exactly rot2 — the correct statement is that ours are the first ones for the column ':' (not
of rct4 type).  I should have said so; the drafts of our note now say exactly this.
Also for the record: the sub-class lists behind my earlier statement "the 3-cycle family
has configurations at n = 13, 17, 33, 37, 39 and none at 15, 19, 21" omitted the 3-cycles
through the central row/column class; after adding them the family also has one further
configuration at n = 13 (dia2 base) and one at n = 21 (rot4 base) — both already in your
database, of course, since the rot2 column is complete there — and still none at 15, 19,
23, 25.  Both 3-cycle sub-families at n = 37 are now completely enumerated (exactly the two
configurations I sent).

May I ask two things?  (a) Whether the ':' cells for n = 36, 37, 39 were still empty in your
files on 2026-08-11 to your knowledge (your history page mentions contributions in
preparation) — we say "first located, as of that date, awaiting the maintainer's
confirmation", and would gladly correct it; (b) whether you would like to be named in the
acknowledgements of the note (drafts are public at
https://github.com/iwasborninbali/saturation, paper/no3inline_defects.pdf).

With best regards,
Alex Komang
```
