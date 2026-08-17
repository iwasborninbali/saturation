# Letter to Achim Flammenkamp — final text (owner sends)

```
Subject: no-three-in-line: first configurations with exact rot2 symmetry for n = 36, 37, 39 (2n points; empty ':' cells of your table)

Dear Achim,

thank you for your reply on the n = 71 partial — understood: only complete 2n-point
configurations are of interest.  This time these are complete ones.

Your table (state 2026-08-11) lists no configuration with exact half-turn symmetry
(column ':') for n = 36, 37 and 39.  Below are 2n-point no-three-in-line configurations
for these sizes, all with stabilizer exactly {identity, rot2} in D4, in your 90-character
encoding (class character + two column characters per row, rows top to bottom):

n = 36 (72 points):
  :3NEHFSVZ3FPU6E2BNQ8I5GDS08JOTYVXDP9Y1QAM2416BGRZ7MJUHR9COXLT5AKW047KILCW
n = 37 (74 points), two inequivalent configurations:
  :GJ39EP7VENDZJRSX7P6ZCF28IQ4VWYKQFa06COUa0LAG245WAISYLO1UBT389H1NDM5TBMRXHK
  :FJ7E4PBGKO6U5VDZDH9RCF2X4QSTIZQa2X0SEM8a3Y0A1I78AW3YLO9RJN1N5V6UCGKPBWMTHL
n = 39 (78 points):
  :CGAWLU7M8CAN1FPZ2K9TXbOPYc7BBL5W3c2E4JIKJYOa0Z6XHRRV04DE159TIa3DNbFSQUGV8H6SMQ
and one further exact-rot2 configuration for n = 33 (that cell was not empty):
  :MOAC3H9J6GJOBS9B05PT0VPQHV5UEI2C4SKUEI2R1F671W37RWLN4L8DGQDNFTKM8A

Every configuration was checked twice by independent programs (all C(2n,3) triples in
exact integer arithmetic) and the stabilizer was computed explicitly.

How they were found.  A small "balance lemma": if a subgroup H of D4 contains a motion
that maps column a to row a (any quarter turn or any diagonal reflection), then every
H-orbit puts equally many points into row a and column a.  Hence, in a rot2-symmetric
configuration that is H-symmetric except for a set of half-turn pairs, those pairs must
form an Eulerian digraph on the row classes {i, n-1-i}.  A single pair must be a
diagonal loop — this is exactly your rct4 — and the next admissible defects are a directed
3-cycle of pairs (odd n) or one loop on each long diagonal (even n).  The configurations
above are: n = 36 — quarter-turn orbits plus a loop on each diagonal, (6,6),(29,29) and
(5,30),(30,5); n = 37 and 39 — quarter-turn orbits plus a 3-cycle of half-turn pairs
((1,3),(3,31),(31,1); (2,4),(4,20),(20,34); (4,8),(8,20),(20,34)); n = 33 — 3-cycle
(2,3),(3,19),(19,2).  Each sub-class (fixed defect) was searched exhaustively by an
exact bit-parallel branch-and-bound program; the same program reproduces the counts of
your table for the classes we checked (dia1, dia2, rct4, rot2 for small n) and A000769.
For the record: the two-loop family is empty for even n = 14..22 and non-empty for
24, 26, 28; the 3-cycle family (both bases, all canonical sub-classes) has books at
n = 13, 17, 33, 37, 39 and none at 15, 19, 21, and its "both diagonals" base is empty at
37, 39, 41 (41 with quarter-turn base still running).

Code, logs and the sub-class lists are in a repository we can open on request; we are
also writing a short note.  I would be glad if you could add the configurations to
your database; corrections to our reading of the table are welcome.

With best regards,

Alex Komang, Bali
(the search was carried out by two autonomous Claude agents (Anthropic) that I run and
direct; the results were re-verified independently)
```
