# Integer-slack experiments (2026-08-18) — exact maxima with kissat, verified with the law

Tools: `slack/arcmod.c|py` (A(m) = max |S|, S ⊂ Z_m², no triple with det ≡ 0 mod m; such S is lawful in the m×m grid),
`slack/liftmax.c|py` (exact maximum lawful subset of a lifted modular hyperbola in a window; mode W = HJSW window
x ∈ [−(p−1)/2, …], y ∈ [0, N−1]).  Every SAT witness is re-checked with `saturation.the_law`.

## A(m): strong modular arcs over Z_m
| m | A(m) | A(m)/m | note |
|---|------|--------|------|
| 5 | 6 | 1.200 | prime: p+1 (Bose/Segre) |
| 7 | 8 | 1.143 | prime |
| 11 | ≥12 | ≥1.09 | prime; 13 not refuted in 120 s |
| 4 | 6 | 1.500 | |
| 6 | 8 | 1.333 | |
| 8 | 8 | 1.000 | corrected (partner, arcmod2: SAT 8, UNSAT 9); my first run reported an upper bound |
| 9 | 9 | 1.000 | corrected (SAT 9, UNSAT 10) |
| 10 | 12 | 1.200 | = 2p+2 for p=5 (Stępień–Szymaszkiewicz thm 3.1); not the HJSW size — HJSW is not a strong arc mod 2p |
| 12 | 12 | 1.000 | corrected (SAT 12, UNSAT 13) |
Note: my first driver claimed A(m)=s−1 at the first UNSAT without a witness at s−1 (bug, fixed); the values above are the
partner's exact ones with witnesses.  Route closed anyway by submultiplicativity (deep research 2).

## Lifted hyperbola xy ≡ 1 (mod p): exact maximum lawful subset
| p | window | candidates | exact max | ratio | remark |
|---|--------|-----------|-----------|-------|--------|
| 7 | [0,2p)² | 24 | 15 | 1.071 | wrong window (not HJSW) |
| 11 | [0,2p)² | 40 | 27 | 1.227 | |
| 13 | [0,2p)² | 48 | 33 | 1.269 | |
| 7 | HJSW G(p), 2p×2p | 24 | **18 = 3(p−1)** | 1.286 | HJSW is optimal in its window |
| 11 | HJSW G(p) | 40 | **30 = 3(p−1)** | 1.364 | |
| 13 | HJSW G(p) | 48 | **36 = 3(p−1)** | 1.385 | |
| 7 | 3p×3p (HJSW x-shift) | 54 | 27 | 1.286 | widening does not raise the ratio |
| 11 | 3p×3p | 90 | ≥43 | ≥1.303 | 44 not decided in 400 s |

Reading: the modular hyperbola supports ~1.5·(usable copies per class)/(copies per class) — 3 of 4 in a 2×2 window,
~4.5 of 9 in a 3×3 window — i.e. the ratio tends to 3/2 whatever the window.  Beating 3/2 needs a different object,
not a wider window.  Greedy repair is far below the exact maximum (1.0–1.26 vs 1.29–1.39): use exact search.

## Algebraicity of the known extremal configurations (Green's Problem 72 remark)
`slack/algebraicity.c`: for a point set and each prime p in [11,61], the largest subset lying on one curve of the cheap
families over F_p — lines, parabolas y=ax²+bx+c and x=ay²+by+c, hyperbolas (x−h)(y−k)=c.  Known 2n-configurations
(rot4/rct4 records, n=41..76, up to 6 per n) versus random 2-per-row sets of the same size:
the known ones have the *smaller* algebraic subsets (see slack/algebraicity_summary.txt: means ≈0.16 vs ≈0.19 of the points;
every known configuration below 0.21).  In the finite range the extremal sets do not "reduce mod p to a curve"; they are less
algebraic than random.  (Cheap families only; general conics would raise both statistics alike.)
