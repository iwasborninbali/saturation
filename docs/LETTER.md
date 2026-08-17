# Draft letter to Achim Flammenkamp (owner decides whether/when to send)

Subject: new no-three-in-line configurations with exact rot2 symmetry at n = 36 and 37 (first known), and n = 33

Dear Achim,

we are two AI solvers (Claude, Anthropic) run by <owner name>, working on the no-three-in-line problem
with an exact bit-parallel branch-and-bound search and its symmetry classes.  Following your table
(2026-08-11), the ':' cells (exact rot2 symmetry) at n = 36 and n = 37 were empty.  We found:

- n = 37, exact rot2 (stabilizer {e, rot180}), not rct4:
  :GJ39EP7VENDZJRSX7P6ZCF28IQ4VWYKQFa06COUa0LAG245WAISYLO1UBT389H1NDM5TBMRXHK
  structure: quarter-turn (C4) orbits plus a directed 3-cycle of half-turn pairs (1,3),(3,31),(31,1)
  [second configuration of the same family: see docs/SUBMISSION.md]
- n = 36, exact rot2, structure "rot4 except on the long diagonals" (rct4-type for even n):
  :3NEHFSVZ3FPU6E2BNQ8I5GDS08JOTYVXDP9Y1QAM2416BGRZ7MJUHR9COXLT5AKW047KILCW
  quarter-turn orbits plus a half-turn loop on each long diagonal: (6,6),(29,29) and (5,30),(30,5)
- n = 33, exact rot2 (a new configuration; the cell was not empty):
  :MOAC3H9J6GJOBS9B05PT0VPQHV5UEI2C4SKUEI2R1F671W37RWLN4L8DGQDNFTKM8A

All three were verified by two independent implementations of the collinearity check (every triple
in exact integer arithmetic) and classified by explicit stabilizer computation.  Encoding follows your
90-character alphabet, class char + two column chars per row.

The families come from a small "balance lemma": if H ≤ D4 contains a motion mapping column a to row a
(any quarter turn or diagonal reflection), every H-orbit puts equally many markers into row a and
column a; hence a rot2 configuration that is H-symmetric except for a set of half-turn pairs must have
those pairs forming an Eulerian digraph on the row classes {i, n-1-i}: single pairs must be diagonal
loops (this is exactly your rct4), and the next possibilities are directed 3-cycles of pairs (odd n) or
two loops, one per diagonal (even n).  We enumerated these families exhaustively for small n
(e.g. even two-loop family: empty for n = 14..22, 8/4/4 configurations at n = 24/26/28) and searched
them at 36 and 37.  Code and logs: https://github.com/iwasborninbali/saturation (we can make it public).

Best regards,
<owner name>
