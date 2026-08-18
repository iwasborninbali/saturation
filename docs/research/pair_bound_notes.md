# Notes towards a theorem for two hyperbolae in the HJSW box (working file; second solver, 2026-08-18/19)

Goal (owner): α(P_k) = 3(p−1) + O(1) for P_k = (H(1)∪H(k)) ∩ G(p), or any provable bound < 4(p−1) − Ω(p).
Everything below is either computed (marked DATA, with the script) or a reformulation; no theorem yet.

## 1. The trivial bound is 4(p−1) and it is a 2-factor bound
Columns x ≢ 0 (2p−2 of them) each contain 4 points of P_k: the two lifts of the H(1) class with x-residue a and the two lifts of the
H(k) class with x-residue a.  Rows likewise.  So the column/row incidence graph B (columns and rows as vertices, points as edges)
is 4-regular bipartite; a lawful S has max degree ≤ 2 in B; hence |S| ≤ 4(p−1), with equality iff S is a 2-factor of B.
Structure of B: every class is a K_{2,2} (its 2 columns × 2 rows); K_{2,2}'s of H(1)-class (a,1/a) and H(k)-class (a,k/a) share the
column pair of residue a; the row pair of residue b is shared by H(1)-class (1/b,b) and H(k)-class (k/b,b).  The "class graph"
(classes as vertices, shared column/row pairs as edges) is 2-regular bipartite: cycles H1(a) –col– Hk(a) –row– H1(a/k) –col– … of
length 2·ord(k).
Loss := 4(p−1) − |S| = #columns with 1 point + 2·#empty columns = same for rows.

## 2. DATA: the exact maxima and their structure (`slack/pair_structure.py` on `slack/witnesses/pair_*`)
| p | k | α | 3(p−1) | loss from 4(p−1) | split H(1)+H(k) | copies per class | pairs |
|---|---|---|---|---|---|---|---|
| 11 | 2 | 33 | 30 | 7 | 15+18 | 1:9, 2:9, 3:2 | mixed |
| 11 | 3 | 35 | 30 | 5 | | | |
| 13 | 2 | 41 | 36 | 7 | 23+18 | 1:8, 2:15, 3:1 | horizontal {(0,0),(1,0)}, {(0,1),(1,1)} |
| 17 | −1 | 54 | 48 | 10 | 19+35 | 1:8, 2:17, 3:4 | vertical/horizontal, some 3-copy |
| 19 | −1 | 59 | 54 | 13 | 30+29 | 1:13, 2:23 | ALL vertical {(r,0),(r,1)}; loss = #singles |
| 23 | −1 | 70–74 | 66 | 14–18 | | | |
So the maxima are BALANCED between the hyperbolae, use 1–2 copies per class (never 4, rarely 3), and the two copies of a class are
in one column or one row (not on a diagonal).  Loss = p−6 for p = 11, 13, 19 (p−7 at 17).  Note |S₁| + |S₂| ≈ 3(p−1)+5 while each
S_i alone could be 3(p−1): the second hyperbola is "almost useless" although it carries half of the points.

## 3. Reformulation for vertical-pair sets: an orientation problem
Take S(r) = for every H(1) class a: both lifts in column X_a + r_a·p; for every H(k) class a: both lifts in column X_a + (1−r_a)·p
(r ∈ {0,1}^{p−1}).  Every S(r) is a 2-factor of B (4(p−1) points, 2 per row and column) — the row/column constraints are
automatically satisfied.  All its collinear triples are CROSS triples of general slope (`slack/vertical_model.py`, DATA: r ≡ 0 gives
~4p rich lines and a maximum lawful subset of 3(p−1) − 2…−7 for p = 11…23; the "parity" rule r_a = [|X_a| even] gives exactly the
optimum 59 at p=19, k=−1 but is bad for other (p,k)).  For mod-p collinear class triples (a₁,a₂ ∈ H(1), a₃ ∈ H(k)) the triple of
lifts is collinear over Z only for specific patterns (r_{a₁}, r_{a₂}, r_{a₃}) (and specific lifts s), so the orientation problem is a
3-CNF-like system on p−1 boolean variables with ~30p clauses (each mod-p collinear class triple contributes ≤ 8 patterns; each pattern
kills 1/8 of the assignments).  A random r violates ~4p clauses; the best r (data) still needs ~p−6 "singles" (delete one lift of a
class, which removes it from half of its clauses) to become lawful.  So the theorem for vertical-pair sets is a statement about this
structured 3-CNF: every assignment plus every set of ≤ (1−ε)p singles leaves a violated clause.  (This is not yet a statement about
general S — mixed pairs, singles, 3-copy classes — but the R-model below suggests general S gains only O(1) over vertical/horizontal
pair sets.)

## 4. DATA: restricted model R (no class uses both copies of a diagonal or antidiagonal pair; `slack/cpsat_max.py R …`)
p=11: k=2 → 31, k=3 → 34, k=−1 → 31 (true α: 33, 35, 32?); p=13: k=2 → 41 (=α), k=3 → 38, k=−1 → 38.  Solves in seconds; results
for p = 17…37 in `bench/restricted_R_vm2.log` (VM2, running).

## 5. Why linear certificates cannot work
LP with all rich lines (≤ 2 per line, incl. rows/columns) = 47.5 at p=13 (α = 41), i.e. ≈ 4(p−1) − ε: the fractional 2-factor
(x ≡ 1/2) is nearly feasible.  Any proof of loss Ω(p) must use rank ≥ 2 inequalities (integrality), i.e. genuinely combinatorial
arguments about how cross triples interact with the 2-factor structure.  Local analysis (one column-class and its four neighbouring
classes) contains no cross triple: the losses come from long-range triples (small primitive directions (u,v) with many lattice
points in the box: the rich cross lines have directions like (1,±1), (2,±1), (3,±2), (5,±4), …).

## 6. Candidate statements, honest status
- (T1) α(P_k) ≤ 3(p−1) + o(p): open; no route.
- (T2) α(P_k) ≤ (4−c)(p−1) for an explicit c>0: open; would need Ω(p) forced deficient columns; no local gadget exists (see §5).
- (T3) k = −1 special structure (classes come in 4-cycles (a,1/a),(a,−1/a),(−a,−1/a),(−a,1/a)): the parity orientation is optimal at
  p=19; maybe a formula for α(P_{−1})?  DATA needed: α for p = 23 (70–74), 29, 31.
- (T4) construction with gain ω(1): the R-model data up to p=37 will show whether the restricted optimum's gain grows.


---
# Part B — third solver (2026-08-18/19): LP/IP by direction class; the k = −1 opening

Complements Part A. Main new point (B.7): for k = −1 a RANK-1 certificate using only rows, columns and slope ±1 lines is
already ≈ 3.45(p−1) for every prime 19 ≤ p ≤ 199 (data), with an integral dual (a line cover) at p = 29 — so §5 of Part A ("linear
certificates cannot work") is true for the full LP at small p and for general k, but NOT for k = −1: there a covering argument in
the style of the one-hyperbola note could plausibly give T3 with ε ≈ 0.4–0.5 for all p.

## B.2 What linear certificates can and cannot do (all k)
Let LP(D) be the LP "Σx_q ≤ 2 on every line with ≥3 candidates whose primitive direction (u,v) has max(|u|,|v|) ≤ D",
0 ≤ x ≤ 1, and IP(D) its integer optimum (α = IP(∞)). Computed values (`slack/lp_bound.py`, `slack/milp_max.py`):

| p,k | IP(1) | IP(2) | IP(3) | α | LP(1)/LP(2)/LP(∞) |
|---|---|---|---|---|---|
| 11,3 | 36 | 36 | 36 | 35 | 36.0/36.0/36.0 |
| 11,2 | 38 | 36 | 34 | 33 | 38.9/38.1/37.6 |
| 13,2 | 48 | 45 | 43 | 41 | 48.0/48.0/47.5 |
| 13,12 | 48 | 44 | 42 | 40 | 48.0/45.2/44.8 |
| 17,16 | 62 | 60 | 58 | 54 | 62.0/60.2/60.2 |
| 17,2 | 62 | 61 | 57 | 53 | 63.5/62.5/61.6 |
| 19,18 | 64 | 64 | 62 | 59 | 64.0/64.0/63.6 |
IP(2) for k=−1: 36, 45, 60, 64, 78, 95, 105 at p=11,13,17,19,23,29,31 (≈ 3.4–3.75 (p−1)).
LP(1) maximised over k: 39.25 (p=11), **48 = 4(p−1)** (p=13, k=2,8,12), **64 = 4(p−1)** (p=17, k=13), 68.9 (19), 85.0 (23).

Consequences.
* Rank-1 (LP) certificates cannot give T2 uniformly in k even with all rich lines (LP(∞) ≈ 3.65–3.9 (p−1)); with rows,
  columns and slopes ±1 only, the LP is exactly 4(p−1) for some k at p=13,17, so no dual weighting of those lines proves anything
  below the trivial bound. Any proof of T1/T2 must use integrality (rank ≥ 2 inequalities), and must use lines of slopes other
  than 0,∞,±1: IP(1) ≈ 4(p−1) (48 at p=13, k=2), i.e. rows+columns+diagonals alone allow the trivial bound to be attained.
* The loss accumulates over many directions: at p=13,k=2 the excess over 3(p−1) drops 12 → 9 → 7 → 5 as D goes 1 → 2 → 3 → ∞;
  in the optimal witnesses the lines that block the non-chosen candidates have directions of size ≤ 2 in 58–70 % of the
  incidences (rows/columns/±1: 40–45 %), the rest spread over many directions (`pair_bound_notes` §4). So there is no small
  family of directions that carries the whole loss, but slopes ±2, ±1/2 already carry a constant fraction of it: IP(2) ≈ 3.5(p−1)
  for k=−1 up to p=31 (data, not a theorem). **A proof that IP(2) ≤ (4−ε)(p−1) would prove T2**; the D=2 problem is of "finite
  type" (rows, columns, and the six slopes m ∈ {±1,±2,±1/2}, each with its class involution σ_m(a,b) = (−b/m, −ma) on each
  hyperbola and with ≤2 partner classes of the other hyperbola per line), but its integrality gap is exactly what has to be
  understood.

## B.4 Blocking structure of the optimal witnesses
For the exact witnesses at p=13 (41), 17 (54), 19 (59): every non-chosen candidate is blocked (lies on a line through two
chosen points) — mostly by 2–7 lines; blocking incidences by direction: axis (1,0),(0,1): 27–30 %; slopes ±1: 15–21 %;
max(|u|,|v|)=2: 15–25 %; the remaining 30–40 % spread over ≥ 20 directions. Unblocked candidates: 0 (the sets are maximal, as
they must be).

## B.5 Heuristic for O(1) (not a proof)
Fix S₂ = HJSW set of H(1) (3(p−1) points). For q ∈ P₂ the number B(q) of pairs of S₂ collinear with q averages 3.1 (p=11) →
7.4 (p=101) — growth like log p — and #{q : B(q)=0} ∈ {0,1,2} for every p ≤ 101, k ∈ {2,3,−1} (`bench`, THREAD [36]). A
random-like model (pairs of S₂ have ~1.8 ln p extra lattice points on their line, each hits a given class of H(k) with
probability ~1/p) reproduces these numbers. Adding a point of H(k) therefore costs deletions in S₂ that free it, and the exact
optima trade ~ (p−1)−5 deletions for the same number +5 of additions. Turning this into a theorem needs a LOWER bound on the
number of collinear triples with points on both hyperbolae for EVERY pair of dense subsets S₁ ⊆ P₁, S₂ ⊆ P₂ (|S₁|,|S₂| ≥ (2−ε)(p−1)),
i.e. a pseudo-randomness statement for lifts of hyperbolae in a box; incidence bounds of Szemerédi–Trotter type are too weak
by a log factor, and no equidistribution result of the needed strength (collinearity over Z, not mod p) is known to us.

## B.6 Routes not yet tried / for the external agents
(a) T2 via IP(2): rows, columns and slopes ±1, ±2, ±1/2 only. Data suggest IP(2) ≤ 3.75(p−1) for k=−1 (p ≤ 31). The
    structure is explicit: a slope-m line through a copy of κ ∈ H(1) contains at most one copy of κ, at most one of σ_m κ,
    and at most one copy of each of the ≤ 2 classes λ of H(k) with λ on the same line mod p (a quadratic in the class
    coordinate); which copies are on the same Euclidean line is decided by ±p shifts as in the orbit lemma. A Chvátal–Gomory
    (rank-2) argument or a matching-type argument on the row/column 2-factor could conceivably show that Ω(p) row-pairs
    cannot be full.
(b) T3 (k=−1): the union H(1)∪H(−1) = {(xy)²≡1} is symmetric under x' ↦ p−x' (reflection of the box); a line meets it in ≤4
    classes. IP(1) is already < 4(p−1) for k=−1 at p ≥ 17 (62/64/80/96/108 vs 64/72/88/112/120), LP(1) = 62, 64, 80, 96, 108,
    128, 142.7 for p=17…41 (≈ 3.4–3.6 (p−1)) — so for k=−1 a rank-1 certificate with rows/columns/±1 gives T3 with ε ≈ 0.4
    numerically for p ≥ 17 (but LP(1) = 48 = 4(p−1) at p=13); proving the pattern of the dual solution for all p would be a
    T3-type theorem. This is the most concrete opening I see.
(c) T4: no growth in the exact data (+5,+5,+6,+5 for p=11…19, ≤ +8 at 23); a construction with unbounded gain would have to
    beat all exact optima found so far, and none of the structured families tried (pairs of copies, HJSW minus orbits + points of
    the second hyperbola) does.


## B.7 The k = −1 opening: LP(1) ≈ 3.45 (p−1) for all p ≤ 199 (DATA)
LP(1) = LP with rows, columns and slope-±1 lines only (all lines with ≥3 candidates of P_{−1}); values (p: LP(1), LP(1)/(p−1)):
17: 62 (3.88); 19: 64 (3.56); 23: 80 (3.64); 29: 96 (3.43); 31: 108 (3.60); 37: 128 (3.56); 41: 142.7 (3.57); 43: 140 (3.33);
47: 160 (3.48); 53: 182.7 (3.51); 59: 198.7 (3.43); 61: 207.3 (3.46); 67: 228 (3.45); 71: 238.7 (3.41); 73: 250.7 (3.48);
79: 272 (3.49); 83: 286.7 (3.50); 89: 306 (3.48); 97: 346.7 (3.61); 101: 353.3 (3.53); 103: 353.3 (3.46); 107: 368 (3.47);
109: 370.7 (3.43); 113: 384 (3.43); 127: 438 (3.48); 131: 453.3 (3.49); 137: 460.7 (3.39); 139: 485.3 (3.52); 149: 509.3 (3.44);
151: 517.3 (3.45); 157: 553.3 (3.55); 163: 555.3 (3.43); 167: 570.7 (3.44); 173: 589.3 (3.43); 179: 614.7 (3.45); 181: 618.7 (3.44);
191: 645.3 (3.40); 193: 667.3 (3.48); 197: 679.3 (3.47); 199: 684 (3.45).  (Exception: p = 13: LP(1) = 48 = 4(p−1).)
So α(P_{−1}) ≤ LP(1) ≤ 3.65 (p−1) for 19 ≤ p ≤ 199 (certified per p by the LP dual), i.e. T3 with ε ≈ 0.35 holds numerically
in this range.  At p = 29 the optimal dual is INTEGRAL: weight 1 on 8 rows, 8 columns, 14 diagonals and 14 antidiagonals (exactly the
slope-±1 lines with ≥ 5 points: sizes 8:4, 7:2, 6:6, 5:2 per slope) and weight 1 on 8 points: value 2·44 + 8 = 96.  So the bound is a
COVER: every candidate lies on one of 44 lines (rows, columns, diagonals) or is one of 8 exceptional points, hence |S| ≤ 2·44 + 8.
Structure behind it: for k = −1, H(−1) = R(H(1)) with R: x' ↦ p − x' the reflection of the box; rows/columns are R-stable and R
exchanges diagonals and antidiagonals; a diagonal D_κ (κ ∈ H(1)) carries the H(−1)-points R(H(1) ∩ R(D_κ)), i.e. an 8-point line is a
shared σ-diagonal (A/D pair) whose mirror is a shared τ-antidiagonal (B/C pair).  The number of ≥5-point slope-±1 lines grows
roughly linearly (12, 12, 16, 28, 24, 28, … 164 at p = 199; 8-point ones 0, 4, 4, 8, … 32).
Concrete theorem candidate (T3′): for k = −1 and all p ≥ 19, α(P_{−1}) ≤ (3.6 + o(1))(p−1), proved by exhibiting a line cover:
all slope-±1 lines with ≥ 5 points, plus rows/columns/points covering the rest, and showing 2·#lines + #points ≤ 3.6(p−1) + O(1).
Needs: (i) the exact combinatorics of which diagonals of P_{−1} carry ≥ 5 points (an equality of base coordinates as in the orbit
lemma, plus a quadratic-residue condition), (ii) a lower bound ≥ c·p on their number for every p — a Weil-type equidistribution
count (the fluctuations of LP(1)/(p−1) between 3.33 and 3.6 are the fluctuations of these counts).  This is the most concrete
opening I see; it does not reach T1, but it would be the first rigorous bound below 4(p−1) for a union of two hyperbolae.
Scripts: `slack/lp_bound.py` (LP by direction class: add a max-direction filter), the LP(1) run in `bench/` (third solver).
