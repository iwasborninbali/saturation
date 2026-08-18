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
## 7. DATA: α does not depend much on k
All k (exact, MIP, `slack/verification/pairs_allk_*`): p=11: 32–35; p=13: 38–41; p=17: 49–54.  So for EVERY second hyperbola the
gain over 3(p−1) is between +2 and +6, although the class graphs (cycles of length 2·ord(k)) differ wildly.  A universal answer
suggests a universal (pseudo-random) mechanism, not arithmetic coincidences of particular k.

## 8. Arithmetic description of the cross triples ("carry" M) — the most promising rigorous route
Let three points of P_k have base copies (X_i, Y_i) (X ∈ [−h,h], Y ∈ [1,p−1]) and lifts x_i = X_i + r_i p, y_i = Y_i + s_i p,
r_i, s_i ∈ {0,1}.  Collinear over Z ⇔ (x₂−x₁)(y₃−y₁) = (x₃−x₁)(y₂−y₁).  If the three classes are mod-p collinear, the base
determinant is divisible by p: (X₂−X₁)(Y₃−Y₁) − (X₃−X₁)(Y₂−Y₁) = p·M with an integer M, |M| ≤ 8p (the "carry").  Expanding,
   collinear over Z  ⇔  M + [(r₂−r₁)(Y₃−Y₁) + (s₃−s₁)(X₂−X₁) − (r₃−r₁)(Y₂−Y₁) − (s₂−s₁)(X₃−X₁)] + p·[(r₂−r₁)(s₃−s₁) − (r₃−r₁)(s₂−s₁)] = 0.
So for each mod-p collinear class triple (κ, κ' ∈ H(1), λ ∈ H(k) — or the other composition), the lift patterns (r,s) ∈ {0,1}⁶
that are collinear are exactly those solving M = −linear(r,s) − p·quad(r,s), where |linear| ≤ 8p and quad ∈ {−2,…,2}: at most 64
patterns, and for "most" class triples none (M has to hit one of ≤ 64 prescribed values in a range of length ~16p).  Data: ~30p rich
lines in P_k, i.e. ~p² mod-p collinear class triples produce Θ(p) collinear lift triples — consistent with M being roughly
equidistributed on a range of length Θ(p) (Weil/Kloosterman-type equidistribution of the carry M is the arithmetic input one would
have to prove).
Route P (pseudo-randomness + counting): (i) prove equidistribution of M for the class triples (uniformly enough); (ii) show that
every S ⊂ P_k that is a union of per-class lift-subsets with ≤ 2 points per row/column and |S| ≥ 3(p−1) + C contains a collinear
lift triple — a counting statement against "product-structured" sets, which is what quasi-randomness of the triple system would
give (the first-moment heuristic for a random-like triple system with ~30p triples on 8p points predicts loss Θ(p), in line with the
data).  Both steps are research, not routine; but this is a well-posed programme, and it explains the universality in k.

## 9. Symmetry for k = −1
y ↦ 2p−y and x ↦ p−x map the box to itself and swap H(1) ↔ H(−1); their product is the half-turn of the box, preserving each
hyperbola.  P_{−1} therefore has a Klein-four symmetry; the p=19 optimum (parity orientation) is not symmetric under it, though.

## 10. Remarks obtained from the owner's external agents (ChatGPT, 2026-08-18; their limit is exhausted until 25 Aug) — audited by us
(a) **Conic reduction (their claim, our proof).**  Let C be a non-degenerate conic over F_p whose projective closure misses one of the
two axial points at infinity, say (1:0:0) ∉ C.  Then the projection (x,y) ↦ y is at most 2-to-1 on C(F_p) and its image has at most
(p+1)/2 + O(1) residues... more precisely each residue b occurs for ≤ 2 points, so the lift of C into a box of side cp has points in at
most c·(number of residues b covered) ≤ c·(|C(F_p)|/… ) rows — for the parabola y = x² exactly the (p−1)/2 quadratic residues plus 0,
i.e. c(p+1)/2 rows, each with ≤ 2c candidates.  A lawful set has ≤ 2 points per row, hence α ≤ 2·c(p+1)/2 = c(p+1): ratio ≤ 1 + o(1)
to the side, far below 3/2.  Conics containing BOTH axial points at infinity have equations xy + dx + ey + f = 0, i.e. are shifted
modular hyperbolas (x+e)(y+d) = de − f.  So among conics only the (shifted) hyperbolas can compete with HJSW; this is why HJSW use
the hyperbola, and it reduces the "conic barrier" question to hyperbolas — for one hyperbola and c = 2 our theorem gives 3/2 exactly.
(Reducible conics = pairs of lines are covered by (b).)
(b) **Line components are useless (their lemma (iv), correct).**  The lift of an F_p-line ux+vy ≡ w into a box of side cp: choose
(U,V) ≡ t(u,v) (mod p) with |U|,|V| ≤ √p (pigeonhole over the p multiples); the lift satisfies Ux+Vy ≡ W (mod p), Ux+Vy ranges over an
interval of length O(c p^{3/2}), so the lift lies on O(c√p) parallel integer lines; a lawful set takes ≤ 2 from each: ≤ O(c√p) points.
Hence curves with line components gain nothing; only the non-linear components matter.
(c) **Copy-template lemma (their (iii)):** if Ã ⊂ Z² lifts an arc A ⊂ F_p² and Q ⊂ Z² is lawful with no secant direction (primitive,
reduced mod p) among the secant directions of A, then Ã + pQ is lawful.  (A construction principle for lower bounds; not relevant to
upper bounds.)
(d) Their audit of "T1–T4 with these ingredients": all FAIL — consistent with Parts A/B: the 4(p−1) bound is not strict via lines
with ≤ 4 candidates (x ≡ 1/2 is LP-feasible), so any strict LP bound needs lines with ≥ 5 candidates — exactly the k = −1 opening of
Part B (8-point slope-±1 lines).

## B.8 Follow-up on the k = −1 opening: what the covers look like, and where the arithmetic enters (third solver)
Minimum-cost integer covers of P_{−1} by rows, columns, slope-±1 lines (cost 2 each) and single points (cost 1), computed exactly
(MIP): p=17: 64; 19: 64; 23: 80; 29: 96; 31: 108; 37: 128; 41: 152; 43: 140; 47: 160; 53: 188; 59: 208; 61: 220 — i.e.
3.33–3.8 (p−1); equal to LP(1) except p = 41, 53, 59, 61 where the LP is fractional (142.7, 182.7, 198.7, 207.3).  The optimal
covers are PARTITIONS of the 8(p−1) points into lines: e.g. p = 29: 8 rows, 16 columns, 4+4 eight-point diagonals, 8+8 four-point
diagonals — 48 lines, no overlaps, cost 96; p = 47: 24 rows, 20 columns, 6+6 eight-point, 12+12 four-point lines — cost 160.
Bookkeeping: if a partition uses m_i lines with i points, cost = 4(p−1) − Σ_{i≥5} (i/2 − 2)·m_i + Σ_{i≤3} penalties, so the saving over
the trivial bound is 2m₈ + 1.5m₇ + m₆ + 0.5m₅ (minus small penalties): a saving of Ω(p) requires Ω(p) "extra points" on slope-±1
lines with ≥ 5 points.  For P_{−1} such a line is a diagonal x−y=d with n₊(d) + n₋(p−d) ≥ 5, where n₊, n₋ are the slope-(+1)/(−1)
profiles of the SINGLE hyperbola (Proposition 8 of the note: n₊ ∈ {4 (A/D shared σ-pairs, d ∈ [1−p,−1]), 3 (B/C classes), 2, 1, 0}
and mirror for n₋); an 8-point line = a shared σ-diagonal D_κ (κ ∈ A∪D) whose mirror R(D_κ) is a shared τ-antidiagonal E_{κ'}
(κ' ∈ B∪C), i.e. e_{κ'} = −d_κ, i.e. x' + 1/x' + x − 1/x ≡ 0 (mod p) with (x, 1/x, x', 1/x') in prescribed half-intervals.
Both value sets (−d_κ over shared A/D pairs; e_{κ'} over shared B/C pairs) have ~p/4 elements in the same interval [1,p−1] of
length p−1, so NO pigeonhole forces coincidences; their number (8, 8, 12, 12, 8, 4, 16, 20, 16, 24, 32, 28, 40, 32 for
p = 29, 37, 43, 47, 59, 61, 71, 89, 113, 137, 151, 173, 191, 199 — the fluctuations of LP(1)/(p−1) between 3.33 and 3.6 are these
counts) is the number of F_p-points of the cubic curve x'(x²−1) + x(x'²+1) = 0 in a box of residues: main term ≈ p/16, error
O(√p log²p) by Weil/completion — useless for realistic p and delicate even asymptotically.  Conclusion: T3′ is provable in the
form "for all sufficiently large p, α(P_{−1}) ≤ (4 − c)(p−1)" with a small explicit c only through such an equidistribution count
(plus the partition combinatorics of the leftover points); no elementary route.  I stop here unless the owner wants exactly this
statement; the LP certificates for each p ≤ 199 (and the integral partitions) are available on request as machine-checkable
covers.
## 11. k = −1: the residue-group structure of the slope-±1 lines (second solver, 2026-08-19; `slack/km1_lines.py`)
For k = −1, P = P₁ ∪ R(P₁) with R: x ↦ p−x.  A slope-(+1) integer line x−y = d′ carries H(1) points of the classes κ with d_κ ≡ d′ (mod p)
and H(−1) points R(q) for the H(1) points q on the antidiagonal x+y = p−d′, i.e. of the classes λ with e_λ ≡ −d′.  Per residue d the
relevant classes are the ≤ 2 solutions of a − 1/a ≡ d (κ, σκ) and the ≤ 2 solutions of a + 1/a ≡ −d (λ, τλ): a *residue group* of
n_d ∈ {0,2,4} classes, 4n_d points.  Each class contributes to three consecutive integer lines c−p, c, c+p with 1,2,1 points, where the
*centre* c is d_κ = X_a − Y_{1/a} for κ (copies (0,0),(1,1) on the centre line) and −e_λ = −(X_b + Y_{1/b}) for R(λ).  All centres lie in
the interval [−h−p+1, h−1] of length 2p−2, hence a residue group has at most TWO distinct centres, c and c+p.  Consequently:
* every slope-±1 line carries at most 8 points of P (this is the k = −1 special feature; for general k the H(k) points on x−y ≡ d come
  from another pair of classes with independent centres, and the same statement holds with the same proof: ≤ 2 centres per pair, so ≤ 8);
* a 4-class group with all centres equal spans 3 lines with sizes (4, 8, 4); with m centres at c and 4−m at c+p it spans 4 lines with
  sizes (m, m+4, 8−m, 4−m) — i.e. (1,5,7,3), (2,6,6,2), (3,7,5,1); a 2-class group spans 3 lines (2,4,2) or 4 lines (1,3,3,1).
* Data (`slack/km1_lines.py`, all p ≤ 199): number of 8-point +1 lines ≈ 0.03–0.18 p (fluctuating), lines with ≥ 5 points ≈ 0.26–0.53 p
  per slope; matches the third solver's LP(1) input (p = 29: 8:4, 7:2, 6:6, 5:2 per slope; p = 199: 164 lines ≥ 5 over both slopes).
Any cover-type theorem (T3′) is therefore a statement about how many residue groups have coinciding centres — a coincidence count
between the least-residue coordinates of (a, 1/a): #{a: X_a − Y_{1/a} = −(X_b + Y_{1/b}) with a − 1/a ≡ −(b + 1/b)} — of the type
handled by hyperbola-in-box equidistribution (Shparlinski's survey), so an asymptotic c·p + O(√p log² p) is plausible; the constant c
and the fluctuations are visible in the data.  Then the covering combinatorics (which rows/columns can be dropped) has to be organised
group by group; the p = 29 dual (8 rows, 8 columns, 28 lines, 8 points) is the model.
* Asymptotics from data (`slack/km1_lines.py`, 193 primes 200 ≤ p ≤ 1500): m₈/p → ≈ 0.083 (mean 0.0825, range 0.058–0.108; 1/12 = 0.0833),
  (≥5-lines)/p → ≈ 0.414, and the third solver's savings 2m₈+1.5m₇+m₆+0.5m₅ per slope → ≈ 0.50·(p−1) (range 0.43–0.55).  So the natural
  T3′ target is α(P_{−1}) ≤ 3.5(p−1) + o(p) (one slope's savings) — consistent with LP(1) ≈ 3.45(p−1); the constants look like exact
  limits (1/12, 1/2), which a Weil-type count should reproduce.

## 12. k = −1: exact arithmetic of the 8-point lines (second solver, 2026-08-19)
Write X(u) ∈ [−h,h] for the least absolute residue and Y(u) = X(u) + p·[X(u)<0] ∈ [1,p−1] for the least positive residue.
For κ = (a, 1/a): d_κ = X(a) − Y(1/a); σκ = (−1/a, −a) and d_{σκ} = X(a) − X(1/a) − p·[X(a)>0], while d_κ = X(a) − X(1/a) − p·[X(1/a)<0].
So the σ-pair is **shared iff X(a) and X(1/a) have opposite signs** (= types A/D), and then d_κ = X(a) − X(1/a) − p·[X(a)>0].
For λ = (b, 1/b): e_λ = X(b) + Y(1/b); the τ-pair is **shared iff X(b), X(1/b) have the same sign** (types B/C), and then
e_λ = X(b) + X(1/b) + p·[X(b)<0].
An 8-point slope-(+1) line at residue d needs κ with a − 1/a ≡ d, λ with b + 1/b ≡ −d, both pairs shared and non-degenerate (a² ≢ −1,
b² ≢ 1: a σ-fixed or τ-fixed class contributes only its own two copies, e.g. p = 17, a = 4), and d_κ = −e_λ (exact integers).  Eliminating d: (a,b) lies on the cubic  C₀: a b² + (a²−1) b + a ≡ 0  (mod p)  (the third solver's x'(x²−1)+x(x'²+1) ≡ 0),
which for each a has 0 or 2 solutions b = [(1−a²) ± √(a⁴−6a²+1)]/(2a).  The exact condition d_κ = −e_λ reads
   X(a) − X(1/a) + X(b) + X(1/b) = p·([X(a)>0] − [X(b)<0]) ∈ {−p, 0, p};
and since a − 1/a + b + 1/b ≡ 0 (mod p) on C₀, the integer L := X(a) − X(1/a) + X(b) + X(1/b) ∈ [−4h, 4h] is automatically ≡ 0 (mod p),
i.e. L ∈ {−2p+2… } ∩ pZ = {−p, 0, p} (|L| ≤ 2p−2).  Hence the 8-point lines correspond to the points of C₀(F_p) whose 4-tuple of least
residues (X(a), X(1/a), X(b), X(1/b)) lies in an explicit union of polytopes of the cube [−h,h]⁴ (sign conditions and the value of L),
and their number is exactly 4·m₈ (each line ↔ 4 pairs (a,b): a ∈ {a, −1/a}, b ∈ {b, 1/b}; verified for p ≤ 199), i.e. m₈ = (vol/…)·p + O(√p log⁴ p) by equidistribution of least residues along the curve (Bombieri/Weil for character sums
along C₀, provided C₀ is absolutely irreducible — to be checked; the two branches b(a) are conjugate under √, so irreducibility over
F_p(a) is the point).  Heuristic volume: (curve points ≈ p) × (sign conditions 1/4) × (L takes the required one of three values 1/3) =
p/12 — exactly the empirical limit m₈/p → 0.083.  The same bookkeeping gives the counts of 7-, 6-, 5-point lines (patterns
(m, m+4, 8−m, 4−m) with m = 1,2,3 correspond to which subsets of the four centres coincide).
So the arithmetic input of T3′ is standard equidistribution; the real difficulty is the covering combinatorics (a partition of P_{−1}
into rows, columns, ±1-lines and points with cost 4(p−1) − savings, valid for every p).

## 13. Response to the external "Gate B" audit (2026-08-19; text in `docs/reviews/external_agents_gateB_2026-08-19.md`)
Agreed on all points of substance; nothing in the notes or the note contradicts them, except one sentence of the conic corollary
(fixed: "only shifted hyperbolae CAN attain 3(p−1)"; F_p-affine equivalence is not a symmetry of the lifted problem — verified their p=7
shear example: max 16 for (x−y)y ≡ 1 in G(7)).  Consequences for our programme:
* The O(1) conjecture is now stated explicitly and falsifiably: **α(P_k) ≤ 3(p−1) + 6 for every prime p ≥ 11 and every k ∉ {0,1}**
  (data: max gain 6, at p=17, k=−1; falsifier: any certified witness with gain ≥ 7).  It is a conjecture, not evidence for T1.
* Upper bounds from solvers are recorded as "solver-proved (HiGHS/CP-SAT/kissat), no independent certificate"; the p=23 value is
  70 ≤ α ≤ 74 at tag hjsw-note-v0.6 (v0.5 said 75.4 while the MIP was running).  Certificates (DRAT for kissat UNSAT runs, or an
  independent second line generator) are on the to-do list for any statement used as a theorem-grade fact.
* Same-pencil unions H(1) ∪ H(k) are indeed special; nothing here claims to represent "all pairs of conics" or "all bounded-t sets".
* The exchange frontier (r deletions from a one-hyperbola core vs additions from H(k)) is a good experiment for the structure question;
  the balanced optimal witnesses (§2) already show that maximum sets are not "core minus O(1)".

## 14. k = −1: anatomy of the integral LP(1) cover at p = 29 (`slack/lp1_pieces.py`; matches B.7)
The optimal dual is a PARTITION of the 224 points into 44 lines + 8 singletons, organised by residue groups:
* 4 "dia blocks" and 4 "ant blocks": each block = one residue group with all four centres coinciding (pattern (4,8,4)): the 8-point line
  (copies (0,0),(1,1) of the four classes κ, σκ, R(λ), R(τλ)) plus the two 4-point lines c−p, c+p (copies (0,1) resp. (1,0) of the same four
  classes).  Cost 6 per 16 points — saving 2 per block; 8 blocks ↔ the 4+4 eight-point lines (m₈ per slope = 4).
* the exceptional part (classes with a² ≡ −1 or a = ±1, i.e. σ- or τ-fixed): 2+2 six-point lines + 8 singleton points, 32 points, cost 16
  (no saving, no waste);
* everything else: 8 rows + 8 columns, in pairs (a column pair of residue a covers the 8 points of the two classes (a,1/a) ∈ H(1),
  (a,−1/a) ∈ H(−1); a row pair likewise) — cost 1/2 per point.
So LP(1) = 4(p−1) − 2·(number of blocks) = 112 − 16 = 96, and the blocks are exactly the 8-point-line groups.  Same at p = 37 (integral).
At p = 31, 41 the LP optimum is fractional (some 1/3, 1/4 weights): the "rest" cannot always be partitioned without waste.
Theorem scheme (T3′): show that for every p one can take all 8-point-line groups (both slopes) as blocks and cover the rest with rows,
columns and ±1-lines with waste O(1) — then α(P_{−1}) ≤ 4(p−1) − 4m₈(p) + O(1) = (4 − 1/3 + o(1))(p−1) ≈ 3.67(p−1) (m₈ ~ p/12).
Obstacles: a class can lie in a good dia group AND a good ant group (double cover, waste 2 per such class), and the row/column pairs
(κ with R(κ) in rows, κ with R′(κ) in columns) are broken when exactly one member is in a block.  The interaction graph is finite-type
(each class has one dia group, one ant group, one row partner R(κ), one column partner R′(κ); the half-turn ν = RR′ preserves goodness),
so a case analysis with an explicit tie-breaking rule may bound the waste — this is the combinatorial half of T3′; the arithmetic half
(m₈ = (1/12+o(1))p) is §12.  A weaker but cleaner statement first: α ≤ 4(p−1) − 2·(number of *disjoint* good blocks) + O(1), with a
greedy choice of blocks avoiding overlaps, and then a lower bound on that number.

## 15. LP(1) for general k (second solver; `slack/lp1_dual.py p k`)
Lines with ≥5 points of slope ±1 exist for general k as well (8-point lines need coinciding centres of a shared H(1) σ-pair and a
shared H(k) σ-pair on the same residue line; density comparable to k=−1 for large p: at p=101, k=2: 8+8 eight-point lines, 42+42 lines
with ≥5 points).  LP(1)/(p−1): k=2: 3.61 (p=29), 3.82 (37), 3.89 (53), 3.77 (101), 3.74 (199); k=3: 3.79 (29), 3.75 (53), 3.70 (101),
3.65 (199); k=−1: 3.43, 3.56, 3.51, 3.53, 3.46 (same p).  So rank-1 covers by rows/columns/±1 lines beat the trivial bound for
every k tested once p is large (the third solver's LP(1) = 4(p−1) cases at p = 13, 17 are small-p accidents), with k = −1 giving the
strongest constants (its reflection symmetry doubles the coincidences).  For general k the optimal duals are fractional and messy;
for k = −1 they are integral partitions at p = 29, 37 (§14).  A T3-type theorem for all k via covers is therefore not excluded, but
k = −1 is the right first target.

## 16. k = −1: the block scheme reproduces LP(1) and the rest is covered without waste (`slack/block_cover.py`)
Greedy: take every residue group (either slope) containing an 8-point line as a block (its three lines, cost 6 for 16 points; skip a
block if it meets an already covered point), then cover the remaining points by an LP over rows, columns, ±1 lines and single points.
Data (p = 19…71): total = LP(1) exactly at p = 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 71 (greedy slightly worse at 61, 67), and the rest is
ALWAYS covered at ≤ 1/2 per point (0.45–0.50), i.e. removing the blocks creates no waste (the "half on every row and column" fractional
cover shows 1/2 per point is available whenever every row/column is either entirely inside blocks or entirely outside; the LP finds
compensations through ±1 lines when a row is partially inside a block).  So the theorem to prove is:
   (T3′-fractional)  α(P_{−1}) ≤ 4(p−1) − 2·B(p),  B(p) = number of pairwise disjoint 8-point-line groups (≥ m₈₊ − overlaps),
via an explicit FRACTIONAL cover: weight 1 on the 3 lines of each block, and a weight assignment on rows/columns/±1 lines of cost
≤ (#rest points)/2 covering the rest — the latter is the combinatorial lemma to establish (waste 0, or O(1)).  Note that fractional covers
suffice for the bound (LP duality), so no integral partition is needed.  Together with m₈ ~ p/12 (§12) this gives ≈ (4 − 1/3)(p−1).

## B.9 (third solver, 2026-08-19) THEOREM (block cover, k = −1): α(P_{−1}) ≤ 4(p−1) − 2·m₈(p) — unconditional, elementary
Notation: P_{−1} = (H(1)∪H(−1)) ∩ G(p); R: x' ↦ p−x' the reflection of the box (H(−1) = R(H(1)); rows are R-stable, R exchanges
slope +1 and −1); m₈(p) = number of lines of slope ±1 carrying 8 points of P_{−1}.
Facts (from §11 and the note): a slope-(+1) line x−y=d' carries only the classes of its residue group {κ, σκ, R(λ), R(τλ)}, and it has 8
points iff the four centres coincide (pattern (4,8,4)): then the three lines c−p, c, c+p carry exactly the 16 copies of the four classes
(4 = copies (0,1); 8 = copies (0,0),(1,1); 4 = copies (1,0)).  Call such a group a *block*.
Lemma 1 (blocks are disjoint and mirror-closed).  An H(1)-class lies in a slope-(+1) block only if it is of type A∪D (σ-shared), in a
slope-(−1) block only if it is of type B∪C (τ-shared); an H(−1)-class R(λ) lies in a (+1)-block only if λ ∈ B∪C and in a (−1)-block only
if λ ∈ A∪D.  Hence no class lies in two blocks (blocks of one slope are on distinct residue lines; blocks of opposite slopes use disjoint
class types), and the mirror R(G) of a block G is a block (R preserves the point set and exchanges the slopes); G ∩ R(G) = ∅ for the same
type reason.  So the blocks form an R-symmetric family of pairwise disjoint 16-point sets, |family| = m₈.
Lemma 2 (rows outside the blocks are full).  Row y contains the copies (0,0),(1,0) of κ_y = (1/y, y) ∈ H(1) and of R(κ_y) ∈ H(−1) (same
y-residue), and nothing else.  Since the block family is R-closed, κ_y is in a block iff R(κ_y) is; hence every row contains 0 or 4 points
outside the blocks (likewise rows y+p).
Proof of the theorem (LP dual / cover).  Give weight 1 to the three lines of every block and weight 1 to every row containing points
outside the blocks.  Every block point lies on one of its block lines; every other point lies on its row.  All these lines carry ≥ 3
candidates, so "≤ 2 per line" holds for every lawful S, and |S| ≤ Σ_lines 2·w = 2·(3m₈) + 2·#rows = 6m₈ + 2·(8(p−1) − 16m₈)/4 =
4(p−1) − 2m₈.  ∎
Verified point by point for every prime 19 ≤ p < 320 (`slack/block_cover_km1.py`, log `slack/verification/block_cover_km1.log`): the
greedy family always contains ALL 8-line groups (no conflicts), all used rows have exactly 4 outside points, cost = 4(p−1) − 2m₈; the
resulting bounds are 3.43–3.87 (p−1) (m₈ = 4…56 in that range).  Note this is exactly the LP(1) value at p = 19, 23, 29, 37, 43, 47 (and
never below LP(1), as it must be); at p = 61 the LP(1) is 207.3 while the theorem gives 232 (m₈ = 4 there) — the LP also exploits 5–7-point
lines, which the block scheme ignores.
Consequences.  (i) Unconditionally, for every p with m₈(p) ≥ 1, α(P_{−1}) ≤ 4(p−1) − 2, i.e. the trivial 2-factor bound is never attained
for k = −1 when an 8-point line exists (m₈(p) ≥ 4 for all 19 ≤ p < 320).  (ii) With §12 (m₈(p) = (1/6 + o(1))p — both slopes — via the
count of least residues on the cubic C₀; needs the Weil/Bombieri estimate) this gives α(P_{−1}) ≤ (11/3 + o(1))(p−1), i.e. T3 with
ε = 1/3 − o(1).  (iii) The same cover with the 6- and 7-point lines (patterns (2,6,6,2), (1,5,7,3)/(3,7,5,1)) added would approach the
LP(1) value ≈ 3.5(p−1) but needs the row/column bookkeeping for partial rows; the pure 8-line statement is clean and I would put it into
the note as a theorem (with the finite verification and the arithmetic input stated as a separate proposition/conjecture).
For general k the same proof gives α(P_k) ≤ 4(p−1) − 2·B_k where B_k is the number of 8-line groups whose family is closed under the
row-partner map (κ_y ↔ λ_y) — for k = −1 this is automatic (mirror), for other k it must be checked group by group (data: partner §15).
## 17. THEOREM (k = −1): α(P₋₁) ≤ 4(p−1) − 4 m₈(p)  — second solver, 2026-08-19; written into the note as Section "Two hyperbolae"
Proof = the fractional cover of §16 made rigorous: weight 1 on the three lines of every good residue group of both slopes (2m₈ groups,
16 points each, pairwise disjoint because an H(1)-class cannot be both σ-shared and τ-shared, and R maps good groups of slope +1 to good
groups of slope −1), weight 1/2 on every row and column disjoint from the union B of the good groups; rows = κ ∪ R(κ), columns = κ ∪ R′(κ),
and B is R- and R′-invariant, so every row/column is inside B or disjoint from B: every point is covered with weight ≥ 1; cost
= 12m₈ + (8(p−1) − 32m₈)/2 = 4(p−1) − 4m₈.  `slack/km1_theorem_check.py` builds this cover explicitly and checks feasibility/cost for
p ≤ 101 (all assertions pass; the bound equals LP(1) at p = 11, 19, 23, 29, 37, 47 and equals α at p = 11).  m₈(p) ≥ 2 for all
19 ≤ p ≤ 1500 (m₈ = 0 at p = 13, 17); asymptotics m₈ ~ p/12 conjectural (§12).  Third solver: please verify the proof in the note.

## B.10 (third solver, 2026-08-19) Can 6/7-point diagonals give a clean Theorem′ with 3.5? — answer: not by local gadgets
Assignment [67]: LP(1) ≈ 3.45(p−1) versus the theorem's 4(p−1) − 4m₈ ≈ 3.67(p−1); is there a clean fractional cover using the mirror
pairs of (2,6,6,2)/(1,5,7,3) groups (weights ½) without waste?
Findings (`/tmp/.../gadget66*.py`, k = −1, p ≤ 199):
1. A (2,6,6,2) group G (two shared pairs with centres c₁ and c₁+p) generates a closed system {G, R(G), R′(G), ν(G)} of 4 groups = 16
   classes = 64 points, closed under rows (κ ∪ R(κ)) and columns (κ ∪ R′(κ)) and disjoint from the 8-line blocks (each class lies in one
   +1 and one −1 residue group; block classes are shared/shared, group classes shared/shared with different centres — a class of type A∪D
   in a +1 (2,6,6,2)-group is τ-split, so it is in no −1 block).  Systems are pairwise disjoint (careful: ν(G) is another +1 group of the same
   system — dedupe by classes).
2. Weight 1 on the eight 6-point lines of a system + ½ on rows/columns for its 16 outer points (the 2-point lines) costs 16 + 16 = 32 =
   the trivial rate ½·64: NO gain.  The local LP of a system with only its INTERNAL lines (all candidates inside) is 32 (trivial) unless the
   16 outer points lie on eight internal 4-point ±1 lines (4 diagonals + 4 antidiagonals); then it is 80/3 = 26.67 with the rational dual
   2/3 on the eight 6-lines, 1/3 on 8 rows, 8 columns and the eight internal 4-lines — a clean gadget saving 16/3 per system.  Such
   "self-sufficient" systems are rare: 0,0,0,0,1,1,1,0,0,1,0,2,2,2,0,3,1,1,3,3 for p = 19,29,37,43,53,61,71,79,89,101,107,113,131,139,151,
   163,173,181,193,199 (out of 1–11 systems each), so the corresponding Theorem′ (α ≤ 4(p−1) − 4m₈ − (16/3)s₆, verified as an explicit
   cover, e.g. p=41: 146.67, p=109: 378.67) improves the constant only marginally.
3. With ALL lines (partially inside), every system's local LP is 26.67 — the extra saving comes from lines shared with OTHER groups
   (fractional weights 1/3, 1/4, 2/3 spanning several residue groups; at p=61 the global optimum uses 12 four-point diagonals at 1/3, 16
   rows/16 columns at 1/3, 12 six-lines at 2/3, 6 five/seven-lines at ½ …).  So the LP's ≈ 3.45(p−1) is a genuinely non-local
   combination; I found no local rule reproducing it, hence no clean Theorem′ with constant 3.5.  (Data check: with the correct dedupe the
   gadget bound is ≥ LP(1) for every p, as it must be; an earlier version double-counted ν(G).)
Conclusion: keep Theorem (11/3) as the clean statement; the gap 11/3 → ≈3.45 is what fractional certificates buy through non-local
sharing, and the true α (3(p−1)+O(1) in data) is far below both — the remaining loss is not visible to rank-1 certificates at all.

## 18. k = −1: orbit blocks and the periodic model (second solver, 2026-08-19; `slack/orbit_blocks.py`, `slack/periodic_model.py`)
* **Orbit blocks.**  Under Γ = {1, R, R′, ν} the classes fall into (p−1)/2 orbits {κ, νκ} ∪ {Rκ, R′κ}; the 16 points of an orbit form a FULL
  4×4 grid on the rows {y ≡ 1/a} ∪ {y ≡ −1/a} (two lifts each) and the columns {x ≡ a} ∪ {x ≡ −a}, and every row/column of the box lies inside
  one orbit block.  So the row/column constraints are block-local: ≤ 8 points per block (a 2-factor of K₄,₄ at most), 4(p−1) in total; the
  entire loss comes from lines joining different blocks (slopes ±1 and general).  Data (p=19 optimum, 59 = 8+8+7+6+4+7+6+6+7 over the
  blocks a = ±1…±9): full blocks (8) at small |X_a| — each of the four classes takes a vertical pair in its own column — and deficits
  growing with |X_a| (block a=±5: only 4 points, one per class, all in the lower rows).  Truth ≈ 6 points per block on average.
* **Periodic model** (S = union of vertical pairs; per column choose H(1), H(−1) or nothing; y ↦ y+p invariance): exact optimum
  24, 34, 48, 52, 60 for p = 11, 13, 17, 19, 23 (= 3(p−1) − 6, −2, 0, −2, −6), i.e. 12/20, 17/24, 24/32, 26/36, 30/44 columns used — well
  below α (32, 40, 54, 59, 70–74): the singles/mixed pairs of the true optima are worth +6…+10.  So neither the pure periodic model nor the
  restricted model R captures α; the extremal structure mixes vertical pairs (inner blocks) with singles (outer blocks).
* Consequence for T1 (k=−1): a proof must handle mixed structures; a clean statement about "blocks" (≤ 6 per block on average, i.e.
  Σ_blocks(8 − n_B) ≥ (p−1) − O(1)) is what the data say, and the theorem gives Σ(8 − n_B) ≥ 4m₈ ≈ p/3.

## B.11 (third solver, task T2.2, 2026-08-19 18:30 UTC deadline) Rank ≥ 2 certificates on rows/columns/±1 (and ±2) lines for k = −1: nothing beyond LP(1)
Question: can a Chvátal–Gomory / clique / odd-cycle inequality on the D=1 structure (rows, columns, slope-±1 lines; blocks and residue
groups) prove α(P₋₁) ≤ (11/3 − δ)(p−1) or ≤ 3.5(p−1)?
Data (`bench/ip1_km1.log`, HiGHS MIP, k=−1): the INTEGER optimum of the D=1 system (rows/columns/±1 lines only) versus its LP:
p=17: 62/62; 19: 64/64; 23: 80/80; 29: 96/96; 31: 107/108; 37: 128/128; 41: 142/142.67; 43: 140/140; 47: 159/160; 53: 182/182.67;
59: 197/198.67 — integrality gap 0–2 points.  With slopes ±2, ±1/2 added (D=2): 60/60.25, 64/64, 78/78.5, 95/95.87, 105/107.09,
127/128, 142/142.67, 140/140, 159/160, 180/182.02 — again gap ≤ 2.
Consequences.
1. Any inequality valid for the integer points of the D=1 (or D=2) system — CG cuts of any rank, clique/odd-cycle inequalities of the
   underlying "≤ 2 per line" hypergraph, block/orbit inequalities — cannot certify anything below IP(1) ≥ LP(1) − 2 ≈ 3.45(p−1) (resp.
   IP(2)).  So on the block structure "rank ≥ 2 does not suffice" in the strongest sense: the D=1 polytope is essentially integral, and
   its optimum is the LP value.  In particular ≤ 3.5(p−1) cannot be proved from D=1/D=2 lines at p = 31, 41, 47, 53 (IP(1)/(p−1) =
   3.57, 3.55, 3.46, 3.50) — the value fluctuates around 3.5 with the arithmetic of the ≥5-point lines.
2. Beating 11/3 IS possible with rank-1 (fractional) certificates — LP(1) ≈ 3.45(p−1) < 11/3(p−1) for all 19 ≤ p ≤ 199 — but only
   through the non-local dual solutions of B.10 (weights 1/3, 2/3, 1/4 spread over several residue groups); the block+rows theorem
   (11/3) is the largest CLEAN (locally describable) part of that certificate, and self-sufficient (2,6,6,2)-systems add 16/3 each
   (rare).  A clean intermediate statement would need a rule for those non-local weights; I do not have one.
3. The true integrality gap — from ≈3.45(p−1) down to the observed 3(p−1)+O(1) — lives entirely in the general-slope lines: only
   IP(∞) shows it (54 vs 60.15 at p=17; 59 vs 63.6 at p=19), and IP(D) descends gradually with D (B.2).  Hence a proof of T1 (or of any
   bound below ≈3.4(p−1)) must use collinearities of unboundedly many slopes; local certificates on residue groups (any rank) are
   provably insufficient (data up to p=59, D ≤ 2), and by the same computation the strongest thing "local + integrality" can give is
   IP(1)/(p−1) ∈ [3.33, 3.6].
Recommendation for the 02:40 sync: the k=−1 upper-bound line via covers is exhausted at 11/3 (clean) / ≈3.45 (LP, non-clean); the
next real step is either the LOWER-bound construction (3(p−1)+c for all p; second solver's line) or a genuinely global argument
(counting cross triples of all slopes for dense S — pseudo-randomness), not more local inequalities.

## B.12 (third solver, task H4, deadline 03:40 WITA) H4 made precise; what it implies; what tool it needs; data for the vertical-pair model
**H4 (precise).** For every S ⊆ P₋₁ with at most two points in every row and every column, T(S) := #{collinear triples in S} ≥
c·(|S| − 3(p−1) − C₀) for absolute constants c > 0, C₀ (all slopes count; the row/column hypothesis is harmless since a lawful S
satisfies it and every S can be trimmed to it by ≤ Σ_rows(|S∩row|−2)⁺ + … deletions).  Consequences: T(S) = 0 forces |S| ≤ 3(p−1)+C₀,
i.e. H4 ⇒ T1 in the strong O(1) form; conversely T1(O(1)) ⇒ H4 with c = 1 (delete one point per triple).  So H4 is not an intermediate
hypothesis but the target itself in "supersaturation" form; the useful content is the linear growth of the loss, which is what a proof
technique would have to deliver.  Weaker, still meaningful: H4(ε): T(S) ≥ c·|S| whenever |S| ≥ (3+ε)(p−1) — this gives T2 (α ≤ (3+ε)(p−1)).
**H4′ (vertical-pair model, second solver's orientation problem).** S(r): class κ_a takes both lifts in column X_a + r_a p, its column
partner R′(κ_a) in the other column (r ∈ {0,1}^{p−1}); every S(r) is a 2-factor (4(p−1) points, 2 per row and column).  Brute force over
ALL 2^{p−1} orientations (`slack/orient_min_km1.py`):
  p=11: min_r T(S(r)) = 24 (mean 53.5, max 86; 2 minimisers);  p=13: 28 (mean 51.5);  p=17: 42 (mean 71.5; 4 minimisers);
  p=19: 48 (mean 118, max 196; 2 minimisers).  So min_r T ≈ 2.2–2.7 (p−1) — linear, and far below the mean (≈ 4–6 (p−1)).
  In the minimising orientation the maximum number of triples through one point is 5, 4, 6, 7, and the exact minimum number of
  deletions making S(r*) lawful is 10, 12, 16, 13 → lawful subsets 30, 36, 48, 59 = 3(p−1) + 0, 0, 0, 5: the triple-minimising
  orientation is NOT the one whose best lawful subset is largest (except p=19); "few triples" and "few forced deletions" are different
  optimisation problems (deletions must hit every triple; a point of degree Δ kills ≤ Δ triples, so #deletions ≥ T/Δ_max, but the
  optimum uses the hypergraph structure).
**What H4′ would give.**  If T(S(r)) ≥ c₁(p−1) for all r and the maximum triple-degree is ≤ Δ, then every lawful subset of a
vertical-pair 2-factor has ≤ 4(p−1) − c₁(p−1)/Δ points — a T2-type bound for the model (with c₁ ≈ 2.4, Δ ≈ 7 this is ≈ 3.66(p−1),
i.e. nothing beyond the block theorem unless Δ is shown to be O(1) and c₁ larger; the exact deletion numbers above show the truth for
the model is 3(p−1)+O(1), far better than T/Δ).
**Tools, honestly.**
(i) H4′ is a MAX-3-SAT lower bound for a STRUCTURED 3-CNF on p−1 bits with ~30p clauses (each mod-p collinear class triple contributes
   ≤ 8 lift patterns).  For a random 3-CNF of that density every assignment violates Θ(p) clauses (first moment + Chernoff over 2^p
   assignments).  Here the indicators "clause violated" (for random r) are dependent only through shared variables, so Janson-type
   concentration applies, but the union bound over 2^{p−1} assignments fails by constants (dependency degree ≈ 3·(clauses per variable)
   ≈ 270; the exponent c·δ²·E/Δ with E ≈ 4p is far below p·ln 2).  No first-moment proof.
(ii) Unsatisfiable cores (small variable sets on which the clauses cannot all be satisfied) would give T ≥ #disjoint cores for every r
   deterministically; the second solver's T2.1 data say the loss is global (no 2–3-block conflicts, one 4-block core at p=19 near the
   central cross), so Θ(p) disjoint SMALL cores do not exist — cores, if any, are long-range.
(iii) Second-moment / pseudo-randomness gives statements for MOST r (T ≥ E − o(E) typically), not for all r; the minimisers are 2–4
   special orientations far below the mean, so "typical" bounds cannot reach them.
(iv) A global geometric argument would need an UPPER bound on the number of distinct lines spanned by S (lawful ⇔ S spans C(|S|,2)
   lines); Beck/Szemerédi–Trotter give lower bounds on spanned lines, not upper ones; nothing in the literature we know bounds the
   directions spanned by a dense subset of a lifted hyperbola pair from above.
(v) Sum-of-squares/SDP certificates of min_r T(S(r)) ≥ c(p−1) can be computed for each p (degree-3 polynomial on the cube), but that
   is a per-p certificate, not a proof for all p, unless the certificate has a p-independent structure — untested.
**Conclusion for the sync:** H4/H4′ are the right quantitative targets and the data support them (min over all orientations ≈ 2.4(p−1)
triples), but I do not see a tool that gives "for ALL orientations" — the obstacle is the same as before: the loss is created by
long-range triples of many slopes with only arithmetic (not combinatorial) structure.  The one concrete thing I would still try in the
model: check whether the minimising orientations for p=11…19 (and their triple sets) have a common arithmetic description (e.g. r_a as a
function of X(a), X(1/a) signs) — if the minimiser is "structured", its T could be computed by counting and then H4′ reduces to showing
no unstructured r does better, which is again the union-bound obstacle.  Otherwise: close the note with what is proved.
Addendum (18:40 UTC): the last idea checked.  At p = 11 and 19 the triple-minimising orientation is exactly the parity rule
r_a = [X(a) even] (T = 24, 48), but at p = 13, 17 the minimisers follow no simple rule (agreement with sign/parity/QR/|X|≤p/4 rules and
their complements ≈ 50–60 %, i.e. chance), and for p = 23, 31, 43, 47 the parity orientation is no better than random (T = 180, 212,
332, 400 ≈ 7–9 (p−1) versus random ≈ 6–9 (p−1); p = 59: 342 vs ≈ 620).  So there is no structured minimiser to count; H4′ would have to be
proved for arbitrary r — the union-bound obstacle stands.  (`slack/orient_min_km1.py`; rules tested in the scratch script.)

## 19. T2.8 — one fresh idea per agent for T1 (deadline 08:00 WITA, 19.08); ≤ 15 lines each, no computations
**Second solver.** Treat H4′ (vertical-pair model) as a polynomial optimisation on the cube: with ε_a = (−1)^{r_a} ∈ {±1}, the number of
collinear triples T(ε) is a real polynomial of degree ≤ 3 in the ε_a (each mod-p collinear class triple contributes an indicator of its
admissible lift patterns, a degree-≤3 polynomial in three variables).  H4′ says min_ε T(ε) ≥ c·p.  Two ways to certify a lower bound for
ALL ε: (a) a sum-of-squares certificate T(ε) − c·p = σ₀ + Σ_a λ_a(ε_a² − 1) with σ₀ SOS of degree ≤ 4 — computable per p by SDP; if the
certificate has a p-independent SHAPE (e.g. built from the residue-group blocks and their Klein images), it becomes a proof; (b) Fourier:
T(ε) = E[T] + Σ_{A≠∅} T̂(A) χ_A(ε); the coefficients T̂(A) for |A| ≤ 3 are exponential-sum-like objects (sums over class triples on the
cubic-type varieties with the collinearity carries) — Weil-type bounds might give |T̂(A)| ≪ p^{1/2+ε} for each A, but there are ~p³ of
them, so ℓ¹ control fails; what would suffice is a "sparse spectrum" statement (most T̂(A) exactly zero, which the arithmetic structure
may enforce) — untested.  I do not know that either works; (a) is checkable in a day for p ≤ 31 and would at least reveal whether a
structured certificate exists.

**Third solver.** Split T1 into an "unbalanced" and a "balanced" regime.
Write S = S₁ ∪ S₂ (S_i ⊆ H(i)-part), |S₁| = 3(p−1) − t₁, |S₂| = 3(p−1) − t₂, so |S| = 3(p−1) + (3(p−1) − t₁ − t₂).  By the equality
analysis of Theorem 1, S₁ agrees with a maximum set of H(1) on all but ≤ t₁ generic orbits (each orbit contributes ≤ 12 with a unique
maximiser), i.e. S₁ ⊇ M₁ \ (≤ 12t₁ points) for a maximum set M₁; likewise S₂ ⊇ M₂ \ (≤ 12t₂ points).
Unbalanced regime (t₁ ≤ εp): every q ∈ S₂ must be unblocked by S₁ ⊇ M₁ minus ≤ 12εp points, i.e. every one of its blocking pairs
{a,b} ⊂ M₁ (pairs of M₁ collinear with q) must lose a point.  Claim to prove ("spread of the blocking hypergraph", a statement about the
explicit algebraic set M₁ = HJSW set): for all but O(1)+o(p) points q of H(k)∩G(p) there are ≥ 2 pairwise DISJOINT blocking pairs, and
the family {B(q)} (B(q) = union of q's blocking pairs, |B(q)| ≈ 2 ln p) is such that a set R of ≤ 12εp points of M₁ meets ≥ 2 pairs
of only o(p) of the q's — a second-moment statement Σ_{x,y∈R} #{q: x,y ∈ B(q)} = o(p) for |R| ≤ 12εp, which reduces to bounding
#{q : x,y ∈ B(q)} for pairs x,y ∈ M₁ (how many class copies q are collinear both with x and some point of M₁ and with y and some
point of M₁) — an incidence count on the lifted hyperbola that Weil/Kloosterman-type equidistribution should give as ≈ (ln p)²/p per
pair, hence Σ ≈ (12ε)²p(ln p)²/… — the constants decide; if it works, |S₂| = o(p) whenever t₁ ≤ εp, so |S| ≤ 3(p−1) + o(p) in this
regime (and symmetrically for t₂ ≤ εp).  This half is the one I would actually try to prove: it needs no integrality, only
equidistribution of the blocking pairs of the explicit set M₁, and it is exactly the heuristic of B.5 made rigorous.
Balanced regime (t₁, t₂ ≥ εp): both S_i are far from their maxima; then |S| ≤ 6(p−1) − t₁ − t₂ ≤ (6 − 2ε)(p−1) — useless — so here one
needs the row/column structure: with t_i ≥ εp both S_i have ≤ 2 copies in most classes and the problem becomes the 2-factor / orientation
problem of §3 with singles; the data (balanced optima 23+18, 30+29) say THIS is where the maximum lives, so the split isolates the hard core:
T1 ⇔ "no two half-density subsets S₁ ⊆ P₁, S₂ ⊆ P₂ (≈ 2 copies per class each, ≤ 2 per row/column) without cross triples have
|S₁|+|S₂| ≥ 3(p−1)+ω(1)".  I see no tool for the core beyond H4′ (B.12); but proving the unbalanced half would at least turn the heuristic
into a theorem and show that any counterexample to T1 must be balanced.

**First solver (T2.8).** Prove T1 in two steps that separate the *combinatorial* core from the *arithmetic* one, using the restricted
model R (§ [67]/[74]: no class uses a diagonal or antidiagonal pair of copies; only vertical/horizontal pairs and singles) as the core.
Step 1 (R-model theorem, purely combinatorial): claim α_R(P_{−1}) ≤ 3(p−1) + O(1).  In R every 2-copy class occupies one column
(vertical pair) or one row (horizontal pair) entirely, so a lawful S ∈ R is determined by (i) a set V of "vertical" classes, (ii) a set H
of "horizontal" classes, (iii) singles, with the constraints: a column with a vertical pair holds no other point (its partner class
of the other hyperbola is dead there), a row with a horizontal pair likewise; hence |S| = 2|V| + 2|H| + #singles and the row/column
constraints alone give |S| ≤ 2·(2p−2) minus the columns/rows killed by pairs — an explicit *matching* structure on the 2-factor of
rows/columns (each class = one edge column↔row of its two copies... precisely: class (a,b) has copies in columns a', a'+p and rows b, b+p;
a vertical pair uses one column and two rows, a horizontal pair two columns and one row).  The only non-row/column constraints in R are
the ±1 lines through vertical/horizontal pairs of *different* classes and the "singles" — i.e. exactly the residue-group blocks of §11
and their 6/7/8-point lines.  My conjecture: in R the LP over rows, columns and ±1 lines is tight up to O(1) (data: R-optimum − 3(p−1) ∈
[−2,+4] for p=17…29 with the max at k=−1 = R = full optimum at 19, and LP(1) ≈ 3.45(p−1) is the same LP), so an integral (or 1/2-)
dual for R could be *constructed* along the residue groups (the k=−1 blocks are R-closed) — the mirror lemma 2 gives full rows outside
blocks; inside blocks the R-restriction removes exactly the diagonal copies that made 8-point lines pay 6 for 16.  So R-theorem =
"cover of the block scheme with the R-forbidden copies deleted", plausibly provable by the same double counting as Theorem 1.
Step 2 (arithmetic): a general lawful S is R plus a set D of classes using a diagonal/antidiagonal pair or 3 copies; each such class
lies on a ±1 line with ≥ 3 candidate points (its own two copies plus the residue-group partners), and the k=−1 theorem's block cover
already charges these lines: show |S| ≤ α_R + 2·(number of D-classes not in blocks) + O(1) and that D-classes off the blocks are O(1)
(the copies (0,0),(1,1) of a class κ ∈ D and the partner σκ… are collinear over Z only when the carries match — the arithmetic condition of
§12; off the 8-point groups those coincidences are counted by m₆, m₇, which are O(p) *in total* but each D-class costs a whole ±1 line
of the cover — the count that matters is the number of D-classes whose ±1 line carries no block, and §11 says such lines have ≤ 2 centres).
Honest assessment: Step 1 is a finite, checkable statement (compute the exact R-optimum and its LP for p ≤ 41 with the residue-group
dual written down explicitly — one afternoon), and if it holds it isolates T1 into "how many diagonal-pair classes can a lawful S afford
outside the blocks", which is where Theorem (block cover) already lives.  If the R-LP is *not* tight (gap growing with p), the idea dies
quickly and cheaply.  What I cannot judge without computing: whether the R-dual has a p-independent shape.

## B.13 (third solver, task T2.9, deadline 10:00 WITA) The "unbalanced regime" — result: NEGATIVE, and sharper than expected: the
## trade-off between the two hyperbolae has slope exactly 1 at every t, so there is no easier regime
Setup as in §19: S lawful, |S₁| = 3(p−1) − t, M₁ = a maximum set of H(1) (HJSW), R = M₁ \ S₁, A = S \ M₁ (added points).  Then
|S| = 3(p−1) − |R| + |A| and, by the equality analysis of Theorem 1 applied orbit by orbit, |A ∩ H(1)| ≤ |R| − t (each orbit of H(1)
loses at least as many M₁-points as S₁ adds there), so |S| ≤ 3(p−1) + (|S₂| − t): T1 (O(1) form) ⇔  f(t) := max{|S₂|: |S₁| ≥ 3(p−1)−t} ≤ t + C.
DATA (`slack/unbalanced_tradeoff.py`, HiGHS MIP with the extra constraint |S₁| ≥ 3(p−1)−t; witnesses exact):
  p=11, k=3:  f(t) = 2,2,4,6,7,9,10,11,12,13,14,16,16 for t = 0…12  ⇒ f(t) − t = 2,1,2,3,3,4,4,4,4,4,4,5,4;
  p=13, k=2:  f(t) = 2,4,6,7,8,9,10,11,12,13,14,15,16,18,18 (t = 0…14) ⇒ f(t) − t = 2,3,4,4,4,4,4,4,4,4,4,4,4,5,4;
  p=17, k=−1: f(t) = 2,4,5,6,8,9,11,12,… (t = 0…7) ⇒ f(t) − t = 2,3,3,3,4,4,5,5 (running).
So EVERY deletion from HJSW buys almost exactly one point of the second hyperbola, uniformly in t, and the excess f(t) − t stays in
{2,…,5}: the maximum |S| = 3(p−1) + max_t (f(t) − t) is attained in the balanced regime only because the offset drifts up by 1–2 there;
there is no regime in which |S₂| = o(p) beyond t = O(1).  Consequently the split of §19 does not isolate an easier half — the correct
statement is the same "one-for-one" inequality at every t.
What is provable about the trade-off (rigorous, elementary):
(1) Blocking pairs form a matching.  For q ∈ P₂ let 𝔅(q) = {{a,b} ⊆ M₁ : a,b,q collinear}.  Two distinct blocking pairs are disjoint:
    a common point a would put a,b,b′,q on one line, i.e. three points of the lawful M₁ on a line.  Hence q ∈ S₂ (unblocked by S₁ ⊇ M₁∖R)
    forces |R ∩ ∪𝔅(q)| ≥ B(q) := |𝔅(q)| — R must contain a transversal of the matching.
(2) Charging: |S₂| ≤ #{q: B(q) = 0} + Σ_{x∈R} deg(x)/B_min′, where deg(x) = #{q ∈ P₂ : x ∈ ∪𝔅(q)} and B_min′ = min B(q) over the other q.
    With HJSW data (k=−1): median B(q) = 3,4,5,6,7 and max deg = 12,17,20,28,31 at p = 17,19,31,61,101 (mean deg 8–20), so this charging
    gives |S₂| ≲ 4–5·|R|: it certifies slope ≈ 4–5, not 1.  The loss is intrinsic to counting: a deleted point x lies in ∪𝔅(q) for ~deg(x)
    ≈ 2·mean(B)·|P₂|/|M₁| points q, but fully unblocks only ~1 of them because each q needs ALL its B(q) pairs hit — the "(2δ)^{B(q)}"
    effect, which holds for RANDOM R and cannot be established for adversarial R by any moment bound (that is exactly the union-bound
    obstacle of B.12 in a different guise).
(3) Rows/columns give a partial injection: a row of M₁ with two points can host a point of S₂ only after one of them is deleted, and each
    such deletion hosts at most one added point; the same for columns.  This charges the added points lying in full rows or full columns
    with slope ≤ 2 (a point may need both a row and a column deletion but each deletion serves one point), and leaves the ~(p−1)/4
    candidates in (half-row, half-column) positions uncharged — for those only the blocking pairs (2) apply.
Verdict: T2.9 negative.  The "unbalanced regime" is not weaker than T1 — f(t) − t is bounded (data) at all t, and any proof of it is a proof
of T1.  What the exercise clarified: (a) T1 ⇔ f(t) ≤ t + C, a one-for-one exchange statement; (b) the exchange is not certifiable by
degree/moment counting of the blocking hypergraph (constants 4–5, and no independence for adversarial R); (c) a proof would need an
INJECTION from S₂ (minus O(1)) into R that respects the structure "R contains a transversal of 𝔅(q)" — e.g. a matching argument in the
bipartite graph {q ∈ S₂} — {x ∈ R}, x ∈ ∪𝔅(q), which by Hall would need |∪_{q∈Q}∪𝔅(q) ∩ R| ≥ |Q| for all Q ⊆ S₂: this is where the
data say it holds (with defect ≤ 5) and where I have no argument.
## 20. H4′ has a spectral handle: T(ε) is a QUADRATIC form on the cube (second solver, 19.08 04:30 WITA; `slack/vp_fourier.py`, `slack/vp_quadratic.py`)
Vertical-pair model, k=−1: S(r) as in §3/B.12; write ε_a = (−1)^{r_a}.  Expanding the collinear lift patterns of class triples,
T(ε) = number of collinear triples of S(r) is a polynomial of degree ≤ 3, and **all odd-degree coefficients vanish** (because
S(1−r) = R′(S(r)) and R′ is a symmetry: T(−ε) = T(ε)).  So
   T(ε) = E(p) + εᵀ C_p ε,   E(p) = (number of collinear (class-triple, orientation, lift) patterns)/8,   C_p an explicit symmetric
   (p−1)×(p−1) matrix with entries c_ab/2, c_ab = (1/8)·(#patterns in which a and b need equal bits − #patterns needing different bits).
Consequence (trivial): min_ε T(ε) ≥ E(p) + (p−1)·λ_min(C_p).  DATA:
  p:      11    13    17    19    23    29    31    37    41
  E:     53.5  51.5  71.5  118  141.5  255  269.5  293  362.5      (E/(p−1): 5.4, 4.3, 4.5, 6.6, 6.4, 9.1, 9.0, 8.1, 9.1 — growing, ~ p log p?)
  λ_min: −3.21 −2.37 −2.44 −4.03 −3.53 −4.50 −4.38 −4.35 −4.50   (bounded so far)
  bound: 21.4  23.1  32.5  45.5  63.9  129  138  136  183           (≥ 1.9(p−1); 4.6(p−1) at 29–41)
  true min (brute force ≤ 19): 24, 28, 42, 48 — the spectral bound is close.
So H4′ (T(S(r)) ≥ c·p for EVERY orientation) is TRUE numerically with an explicit spectral certificate, and would be a THEOREM for the
model if (i) E(p) ≥ c₁·p and (ii) λ_min(C_p) ≥ −c₂ with c₂ < c₁ (or E(p)/(p−1) → ∞ with λ_min bounded) can be proved — both are statements
about explicit arithmetic quantities (E: a count of collinear lift patterns like the m₈ count; C_p: an explicit sparse ±-matrix whose
operator norm looks bounded — 32 nonzeros per row at p=41 with |entries| ≤ 3 but λ_min ≈ −4.5, i.e. random-matrix-like cancellation).
What it would give: every vertical-pair 2-factor has ≥ E + (p−1)λ_min collinear triples; with maximum triple-degree Δ per point (data: 4–7
at p ≤ 19; likely O(log p)) at least (E + (p−1)λ_min)/Δ deletions are needed ⇒ a bound for the MODEL of the form 4(p−1) − c·p/log p or
better; not T1 (singles/mixed pairs are outside the model), but the first rigorous handle on "why every orientation is bad".
Running: p = 43…101 (`bench/vp_quadratic_large.log`) to see whether λ_min stays bounded and how E grows.
Addendum (05:00 WITA) — larger p (`bench/vp_quadratic_large.log`): p=43: E/(p−1)=9.36, λ_min=−4.62, bound 4.74(p−1); 47: 8.82, −4.95, 3.87;
53: 9.51, −5.82, 3.69; 59: 11.04, −6.11, 4.94; 61: 11.18, −6.00, 5.18; 67: 10.63, −5.85, 4.78; 71: 12.84, −6.40, 6.44.  So E/(p−1) grows
slowly (like log p; E ≈ (1/8)·#collinear point-triples of P₋₁ with three distinct classes, i.e. essentially the number of rich lines of
all slopes ~ p log p) and λ_min drifts down slowly (−4.5 → −6.4, also log-like?), the spectral bound staying ≥ 3.7(p−1) and trending up.
Precise conjecture (checkable): λ_min(C_p) ≥ −c log p and E(p) ≥ c′ (p−1) log p with c′ > c, so min_ε T(S(r)) ≥ (c′−c)(p−1) log p.
Structure for a proof: on the cube, εᵀC_pε = (1/16)Σ_π (s_π·ε)² − (3/2)E with s_π ∈ {±1}³ the required-bit signs of pattern π (a
collinear point triple with three distinct classes), i.e. C_p = (1/16)Σ_π s_π s_πᵀ − (1/16)D (D = diagonal of pattern degrees), a PSD
Gram part minus a diagonal; λ_min(C_p) ≥ −c is a "spectral expansion" statement for the sign-pattern hypergraph of collinear triples —
provable, if at all, by a trace/moment method whose terms are counts of closed chains of collinear triples of P₋₁ (arithmetic again).
E(p): the count of collinear point-triples of the explicit set P₋₁ — a fixed-set counting problem (no adversary), Weil-type; even
E ≥ 4(p−1) would need the general-slope triples (the ±1 lines contribute only ≈ 10 m₈ ≈ (5/6)p).
Status: this is the first place where "for ALL orientations" has a certificate mechanism (SDP/spectral) rather than a union bound; it
concerns the vertical-pair MODEL only.  Recorded for the note's §6 as a numerical observation; a theorem needs the two arithmetic
inputs above (weeks, not hours).
Addendum 2 (exact minima over ALL orientations, vectorised; `/tmp/vpmin.py`, to be moved to slack/vp_min.py): p=19: 48 (spectral 45.5);
p=23: 80 = 3.64(p−1) (spectral 63.9).  True minima 24, 28, 42, 48, 80 for p = 11…23, i.e. 2.4, 2.3, 2.6, 2.7, 3.6 per (p−1) — growing, as
E does; the spectral bound is within a factor 1.05–1.25 of the truth.  p=29 running.
Addendum 3 (composition of E; `/tmp/eslopes.py`): the collinear distinct-class patterns of P₋₁ are spread over hundreds of directions
(278 at p=41, 540 at p=71): slopes ±1 carry only 12–15 %, directions with max(|u|,|v|) ≤ 2 about 22–27 %, ≤ 4 about 44 %; the leading
directions after ±1 are (2,±1),(1,±2),(2,±3),(3,±1),(3,±2),(1,±3),(4,±3)… with roughly 1/(|u||v|)-like decay.  So E(p) is a sum over
all small directions (an N log N-type count), and any proof of E ≥ c(p−1) with c > |λ_min| ≈ 4–6 must control a growing family of
directions — the same equidistribution machinery as for m₈, direction by direction, plus a tail bound.  Bottom line of the spectral
route: (model theorem) ⇐ [E(p) ≥ (|λ_min(C_p)| + δ)(p−1) for large p], both sides being explicit arithmetic quantities; feasible as a
project, not tonight.
Addendum 4: p=29 exact minimum over all 2^{28} orientations = 136 = 4.86(p−1) (spectral bound 129.1 — within 5 %).  Sequence of exact minima
24, 28, 42, 48, 80, 136 (p = 11…29): superlinear, tracking E; the spectral certificate is nearly tight from p = 23 on.

## B.14 (third solver, task T2.10, 2026-08-18 18:30 UTC) Norm/trace diagnostics of C_p (k = −1): the moments are NOT bounded — C_p is Wigner-like
Data: `slack/verification/vp_moments_km1.txt` (42 primes 11 ≤ p ≤ 199), tool `slack/vp_traces.py` (builds C_p from the collinear
point-triples of P₋₁ over all slopes, lines by pair hashing — O(p²) instead of the O(p³) class-triple enumeration; identical E, λ_min to
`vp_quadratic.py` at p ≤ 19).  Notation m_{2k} := tr(C_p^{2k})/(p−1); m₂ = ‖C_p‖_F²/(p−1) = mean squared row ℓ²-norm.
1. Shape of C_p: zero diagonal; entries in (1/8)ℤ, |c| ≤ 1.75; about (p−1)/2 nonzeros per row (32.6 / 66.7 / 97.7 at p = 41 / 101 / 199)
   — the matrix is DENSE (density ≈ 1/2), not sparse: ~24·E/(p−1) ≈ 400 patterns per row at p=199 collapse onto ~100 nonzero entries.
   Row norms at p = 41 / 101 / 199: mean ℓ¹ 14.1 / 26.8 / 38.0 (max 17.8 / 36.0 / 50.5); mean ℓ² 2.96 / 3.91 / 4.59 (max 3.6 / 5.1 / 5.6);
   max ℓ²/√m₂ ∈ [1.21, 1.29] at all p (rows homogeneous in ℓ²).  Gershgorin is hopeless (−50 vs true λ_min ≈ −9 at p=199).
2. Moments grow: m₂ = 4.0 (p=11) → 21.3 (p=199), m₄ = 41 → 1014, m₆ = 531 → 67 043; fits m₂ ≈ 5.4 log p − 10.9 ≈ 1.48·E/(p−1) − 4.2
   (the Frobenius mass tracks the pattern density E/(p−1) ≈ 3.6 log p − 4.4, both with large prime-to-prime fluctuations, e.g. E/(p−1) =
   11.8 at p=193 vs 17.6 at p=191).  So there is NO bounded moment: a trace method with fixed k cannot give |λ_min| = O(1), and the
   premise of the T2.10 question (tr C^{2k}/(p−1) ≤ (2c)^{2k} Cat_k with c fixed) fails already at k=1.
3. But the NORMALISED moments are stable and semicircle-like: m₄/m₂² ∈ [1.99, 2.56] (Wigner: Cat₂ = 2), m₆/m₂³ ∈ [4.98, 9.95] (Cat₃ = 5) —
   a slightly heavier tail than the semicircle, no growth with p.  The spectral edge scales like Wigner's 2σ: −λ_min/(2√m₂) ∈ [0.58, 1.07],
   λ_max/(2√m₂) ∈ [0.94, 1.42]; the tightest fit of all is −λ_min ≈ 2.38 √m₂ − 2.13 (rms 0.36 over 42 primes), i.e. |λ_min| ≍ √m₂ ≍ √(log p),
   consistent with the partner's "log-like drift" of λ_min (−λ_min ≈ 1.94 log p − 2.3 fits with rms 0.84 — worse).
4. Consequence for the spectral route (§20): E + (p−1)λ_min ≈ (p−1)[E/(p−1) − c√(E/(p−1))] with c ≈ 2.4·√1.48 ≈ 2.9, so the spectral bound
   is E(1 − o(1)) as soon as E/(p−1) → ∞ — the model theorem "min_ε T ≥ (1−o(1))E" needs (i) E/(p−1) → ∞ (partner's direction sums) and
   (ii) a Wigner-type edge estimate λ_min(C_p) ≥ −K√m₂, and (ii) via traces means m_{2k} ≤ (K′m₂)^k·Cat_k for k ≍ log p: closed walks of
   length 2k in the weighted pattern graph, weighted by products of entries — the deterministic analogue of the moment method for random
   matrices, where the "randomness" must come from equidistribution of collinear patterns (Weil-type cancellation in the walk sums).  Data
   check on the needed inequality: E/(p−1) − 2√m₂ = 1.35, 0.18, 1.01, 1.73, 1.78 for p = 11…23, ≥ 2.6 for p ≥ 29, 4.6…8.3 for p ≥ 149 —
   positive at every prime, growing slowly (like log p − √log p).
Bottom line: the answer to T2.10 is "no bounded moments, but a clean Wigner picture": λ_min ~ −2.4√(tr C²/(p−1)) ~ −√(log p), o(E/(p−1)).
The trace method is still the right tool, but the target is a Wigner-type bound (K√m₂), not a constant.
Addendum 5 (per-direction constants for Conjecture A; `slack/dir_count.py`): distinct-class collinear triples of P₋₁ per (p−1) by direction,
p = 41/71/101/199: (1,±1): 4.4/7.7/7.6/7.4 each; (2,±1): 1.9/2.8/3.0/3.1; (1,±2): 1.7/3.2/2.9/3.1; (3,±1): 1.35/1.49/1.58/1.39;
(2,±3): 1.55/1.51/1.12/1.16.  So each direction has its own Θ(p) count with a limiting constant c(u,v) (fluctuating ±20 %), and E/(p−1) =
(1/8)Σ_{(u,v)} c(u,v) grows because ever more directions contribute; the model theorem needs E/(p−1) ≳ 10, i.e. Σ_F c ≥ 80 over a finite
family F of directions — dozens of directions, each a Weil-type count in the style of Prop. m₈ (or one uniform argument in (u,v)).
Together with B.14 (Wigner edge): the spectral programme is well-posed and heavy on both sides; parked here with all data and tools.

## B.15 (third solver, 2026-08-18 18:40 UTC) The arithmetic structure of E(p): every collinear pattern of P₋₁ is a symmetric quadruple, present iff s₁²+s₂² is a square mod p
Tools/logs: `slack/e_structure.py`, `slack/verification/e_structure_p191_p193.log`, `e_structure_small.log`.
Setup.  A compatible collinear pattern (three points of P₋₁ from three distinct classes, all present for one orientation) lies on a
primitive integer direction D = (u,v): the points are q, q+t₁D, q+t₂D (0 < t₁ < t₂).  Neither u nor v is ≡ 0 (mod p) (a vertical or
horizontal residue direction would put three points on a column/row of a class pair — impossible), so along the line the residues obey
f(t) := (x+tu)(y+tv) = e₁ + b t + w t²,   w = uv ≢ 0,  b = xv + uy,   with f(0), f(t₁), f(t₂) ∈ {±1} (which hyperbola each point is on).
The sign pattern (e₁,e₂,e₃) is not constant (a non-degenerate quadratic takes a value at most twice), so up to global sign it is one of
(e,e,−e), (e,−e,e), (e,−e,−e).  In every case f is symmetric about the midpoint of the two equal-sign points, hence takes the value −e at a
FOURTH integer t: each pattern is a sub-triple of a symmetric quadruple  q + {0, s₁, s₂, s₁+s₂}·D  with signs (e,−e,−e,e)
[(e,−e,−e) at (0,t₁,t₂): (s₁,s₂) = (t₁,t₂); (e,e,−e): (t₂−t₁, t₂); (e,−e,e): {t₁, t₂−t₁}] — the fourth point may fall outside the box.
For the quadruple: w = 2e/(s₁s₂), b = −2e(s₁+s₂)/(s₁s₂), and with z = x/u the base point solves  z² + (s₁+s₂)z + s₁s₂/2 ≡ 0, discriminant
(s₁+s₂)² − 2s₁s₂ = s₁² + s₂².  Hence:
  THEOREM (structure of Π).  The residue-level collinear patterns of A = {xy ≡ ±1} are exactly the symmetric quadruples: for each pair
  s₁ ≤ s₂ (positive integers), each e = ±1 and each u ∈ F_p^*: v ≡ 2e/(s₁s₂u), x ≡ zu, y ≡ e/x, where z is a root of z²+(s₁+s₂)z+s₁s₂/2;
  the family (s₁,s₂) exists iff s₁²+s₂² is a square mod p (2 roots if a nonzero QR, 1 root if ≡ 0, none if a non-residue), and then it
  consists of 4(p−1) (or 2(p−1)) residue quadruples on the direction hyperbola uv ≡ 2e/(s₁s₂).  Π = the box lifts of these (a quadruple
  or truncated quadruple fits iff (s₁+s₂)·|D|_∞ ≲ 2p, resp. s₂|D|_∞ ≲ 2p, with 1–4 lifts of the base point).
Verification: for p = 97, 191, 193 EVERY present family (t₁,t₂,e) has the predicted discriminant (closed forms 4(t₁²+2t₂(t₂−t₁)),
4(t₂²−2t₁(t₂−t₁)), 4(t₁²+t₂²) over the obvious denominators) and s₁²+s₂² a square mod p — the only families with (s₁²+s₂²/p) ≠ 1 are those
with s₁²+s₂² ≡ 0 (p ≡ 1 mod 4: 21²+74² = 61·97, 80²+111² = 97·193), present with one root; for t₂ ≤ 8 presence ⟺ square for all 224
(t₁,t₂,e) at p ≥ 97 (at p ≤ 43 some predicted families miss for lack of a fitting direction).  Data (p=191/193): (0,1,2): 906/0 [(5/p)],
426/472 [(2/p)]; (0,1,3): 416/0 [5], 382/0 [13], 366/0 [10]; (0,1,4): 218/240 [25 — always]; 4-point lines (0,1,2,3): 416/0, (0,1,3,4): 204/0,
(0,3,4,7): —/56 [25], (0,1,7,8): —/68 [50].
Consequences.
(a) The prime-to-prime fluctuation of E is explained: E(p) is a sum over (s₁,s₂) of Kloosterman-type direction counts switched on and off
    by the squares s₁²+s₂² mod p; at p = 193 the small values 5, 10, 13, 17, 26, 29, 34 are all non-residues (only 2, 25, 50 survive), at
    p = 191 the values 5, 10, 13, 17 are residues — hence 17.6 vs 11.8 per (p−1).  Pythagorean pairs ((3,4),(5,12),(6,8),(8,15),…) are
    present for EVERY p.
(b) Formula:  E(p) = (1/8)·Σ_{e=±1} Σ_{s₁≤s₂} [s₁²+s₂² ≡ □ (mod p)] · N_box(s₁,s₂,e),  where N_box counts the box-lifted (sub)triples of the
    4(p−1) residue quadruples of the family; for s₁+s₂ ≤ p^{1/2−ε} the directions D on uv ≡ 2e/(s₁s₂) with |D|_∞ ≤ 2p/(s₁+s₂) are Weil–
    Kloosterman equidistributed (count ≈ (6/π²)·16p/(s₁+s₂)² primitive ones, error O(√p log²p)), so N_box ≍ p/(s₁+s₂)² and
    E(p)/(p−1) ≍ Σ_{s₁+s₂ ≤ √p} [□]/(s₁+s₂)²  — the ~log p growth is Σ_σ (σ−1)/σ² over scales σ ≤ √p, times the density of squares
    among the values s₁²+s₂² = N(s₁+is₂) (Gaussian norms) at each scale.  (Directions with |D|_∞ ≫ √p — the head (1,±1), (1,±2)… — collect
    the families with s₁s₂ ≡ 2e/w (mod p) and s₁+s₂ ≤ 2p/|D|_∞: for a FIXED direction this is a character sum over the full range s₁ ≤ 2p/|D|,
    so the per-direction constant c(u,v) of addendum 5 is a Weil-type quantity: c(u,v) = (1/2 + o(1))·(number of pairs)·(lift average)/(p−1);
    e.g. (1,±1) collects ≈ 4p pairs (s₁, s₂ ≡ ±2/s₁), half present, ~7.4 per (p−1) as observed.)
(c) Unconditional linear bound: the family (3,4) (25 = 5²) is present for every p ≠ 5, and among (1,1),(1,2),(1,3) at least one is present
    ((2/p)(5/p)(10/p) = 1), so E(p) ≥ c·p for an explicit c > 0 by the Kloosterman count for two fixed hyperbolas in boxes — small c (≈ 1),
    far below |λ_min| ≈ 2.4√m₂; not useful by itself.
(d) Conjecture A (E/(p−1) → ∞) reduces to: a positive proportion of the values s₁²+s₂², s₁,s₂ ≤ S, are squares mod p for a positive
    proportion of the dyadic scales S ≤ √p — a short character sum statement for χ∘N over boxes in Z[i] (for p ≡ 3 mod 4: boxes in F_{p²};
    Davenport–Lewis-type Burgess bounds for boxes in F_{p²} are nontrivial from side p^{1/3+ε}, which would already cover the scales
    p^{1/3+ε} ≤ S ≤ p^{1/2−ε} and give E ≥ c·p·log p — to be checked; for p ≡ 1 mod 4 the norm splits and one needs Burgess for χ(s₁²+s₂²)
    in s₁ over short intervals).  Either way Conjecture A is now a standard (if not easy) analytic-number-theory question about ONE
    explicit character sum, not a sum over "hundreds of directions" each needing its own count.
Nothing here touches Conjecture B (the Wigner edge); the same parametrization gives the entries of C_p (each quadruple contributes ±1/16 to
the C entries of its class pairs), which may help to organise the closed-walk sums.

## 21. T2.12 (second solver, 19.08): Conjecture A via B.15 — what is provable, and the exact input needed
From B.15: E(p) = (1/8)Σ_{e=±1}Σ_{s₁≤s₂}[s₁²+s₂² ≡ □ (mod p)]·N_box(s₁,s₂,e), where a family (s₁,s₂) has residue directions on the hyperbola
uv ≡ 2e/(s₁s₂) and contributes the box lifts of its quadruples: an integer direction D̃ ≡ (u,v) fits iff (s₁+s₂)|D̃|_∞ ≲ 2p, so
N_box(s₁,s₂) ≈ (number of small solutions of uv ≡ c with |u|,|v| ≤ 2p/(s₁+s₂)) × (lift multiplicity 1–4) × (sub-triples ≤ 4)
≈ c₀·p/(s₁+s₂)² by Kloosterman equidistribution — rigorously only when 2p/(s₁+s₂) ≥ p^{3/4+ε}, i.e. s₁+s₂ ≤ p^{1/4−ε} (the count of solutions
of uv ≡ c in a box of side L is 4L²/p + O(√p log²p), meaningful for L ≥ p^{3/4+ε}).
(1) **Unconditional linear bound** (no growth): the Pythagorean families (s₁,s₂) = d·(3,4), d·(5,12), d·(8,15), … have s₁²+s₂² a perfect
    square, hence a QR for every p; Σ_{Pythagorean, s₁+s₂ ≤ p^{1/4−ε}} c₀ p/(s₁+s₂)² converges to c₁·p with an explicit c₁ > 0 (the sum
    Σ 1/(s₁+s₂)² over Pythagorean pairs converges), each term certified by the Kloosterman count.  So E(p) ≥ c₁(p−1) for all large p,
    unconditionally — but c₁ ≈ 1 (data: (3,4) alone gives ~0.4(p−1)), far below the ≈ 9 needed against |λ_min|.
(2) **Growth** needs the non-Pythagorean present families, i.e. the density of quadratic residues among the values s₁²+s₂², s₁,s₂ ≤ S,
    for S as small as p^{ε}: this is a Burgess-type question (character sums over norms N(s₁+is₂) ≤ 2S² — the complete 2D sum
    Σ_{s∈F_p²} χ(s₁²+s₂²) e(⟨h,s⟩/p) has modulus ≈ p (χ∘Q is self-dual), so plain completion gives nothing below S ≈ √p·log p; Burgess's
    method for polynomial/norm values should give a positive proportion for S ≥ p^{1/8+ε} — to be cited from the literature (this is the
    precise input to request in the deep research)).  Granting it: E(p)/(p−1) ≥ c₂ log p (sum over scales σ ≤ p^{1/4−ε} of ≈ σ/2 present
    pairs × c₀/σ²), matching the observed 3.6 log p up to the constant.
(3) Also needed for the model theorem in the form of §20/B.14: m₂ = tr C²/(p−1) = O(E/(p−1)) — true since the codegree of a class pair is
    ≤ 32 (the lifts of two classes span ≤ 16 lines, each with ≤ 2 further candidates), so |c_ab| ≤ 4 and Σ c_ab² ≤ 4·Σ|c_ab| ≤ 4·(3/8)·8E.
Bottom line for A: E ≥ c₁(p−1) unconditionally with small c₁ (Pythagorean families + Kloosterman); E/(p−1) → ∞ ⇐ Burgess-type
equidistribution of QRs among small sums of two squares.  With B (Wigner edge, λ_min ≥ −K√m₂), the model theorem would follow for all
large p; without growth, the inequality E/(p−1) > K√m₂ ≈ 2.9√(E/(p−1)) needs E/(p−1) ≳ 9, observed for p ≥ 29 but not provable from (1).
Request for the owner's deep research 7 (later): "character sums of Legendre symbol over sums of two squares / Gaussian norms in short
ranges (Burgess-type)" and "deterministic Wigner-type spectral edge bounds for arithmetic ±1 matrices (trace method with Weil cancellation)".
Correction to §21(1) (data, `/tmp/pyth.py`): the Pythagorean families carry only 2–4 % of E: E_pyth/(p−1) = 0.03, 0.10, 0.09, 0.11, 0.08 at
p = 41, 71, 101, 151, 199 (families (3,4), (6,8), (5,12), (9,12), (7,24), … present as predicted).  So the unconditional constant is
c₁ ≈ 0.1, not ≈ 1: the growth of E rests entirely on the QR-density of non-Pythagorean sums of two squares (Burgess-type input, brief 7).

## B.16 (third solver, task T2.13, 2026-08-18 18:55 UTC) Conjecture B on the quadruple structure: the trace method — main term, cancellations, what arithmetic is needed
Data: `slack/verification/vp_moments_k.txt` (tool `slack/vp_moments_k.py`; primes 97, 101, 151, 193, 199; k ≤ 12).
1. C_p in quadruple language.  Π = box lifts of sub-triples of symmetric quadruples q_F (F = (s₁,s₂,e), direction D on uv ≡ 2e/(s₁s₂), root z,
   lift ℓ; B.15).  For a ≠ b: C_ab = (1/16)Σ_{π ∋ a,b} σ_π(a)σ_π(b), where σ_π(a) = +1 iff the lifted point of class a used by π is the one present
   for r_a = 0 (κ_a in the left column X(a), or κ′_a in the right column X(a)+p) — a "which copy" sign; C_aa = 0.  Gauge-invariant form of a
   closed walk a₁→…→a_{2k}→a₁ through patterns π_i ∋ {a_i,a_{i+1}}:  Π_i σ_{π_i}(a_i)σ_{π_i}(a_{i+1}) = Π_i comp(a_i; π_{i−1}, π_i),
   comp = +1 iff the two patterns pass through COMPATIBLE copies of a_i (both present in the same orientation r_{a_i}).
2. Trace expansion and the classification of closed walks (standard, Wigner/Füredi–Komlós):
   (T) doubled trees — every edge traversed twice, back and forth: contribution (16C_ab)² ≥ 0 per edge, no sign problem; summed over labels
       they give the row-norm functionals: tree₂ = 2Σ_a rn_a⁴, tree₃ = 2Σ_a rn_a⁶ + 3(rn²)ᵀ(C∘C)(rn²) (Cat₂ = 2, Cat₃ = 5 plane trees), and in
       general Cat_k·(p−1)·m₂^k·(1 + O(k²·Var(rn²)/m₂²)).  Data: tr C⁴/tree₂ = 1.07–1.13 (1.002 at p=97), tr C⁶/tree₃ = 1.26–1.48; the row-norm
       inhomogeneity (rel. std of rn² = 0.20–0.25; max rn/√m₂ = 1.21–1.29) is worth ~5 % at k=2.  ⇒ the doubled trees ARE the main term.
   (M) tree-shaped walks with an edge used ≥ 3 times / coinciding vertices: relative size ≲ Σ_b C_ab⁴/rn_a⁴ ~ max|C|²/rn² ≈ 1–2 %.  This is the
       one non-standard feature: entries are O(1) (in (1/8)ℤ, ≤ 1.75) while rn² ≈ 5.4 log p, so the semicircle limit is approached only at rate
       1/log p — harmless for bounds of the type "≤ (K′m₂)^k Cat_k".
   (C) shapes with cyclomatic number g ≥ 1: signed sums.  Data for g = 1, k = 2 (genuine 4-cycles a-b-c-d-a, a≠c, b≠d): N₄/A₄ (signed / absolute)
       = 1.4 %, 0.9 %, 1.5 %, 0.8 % at p = 101, 151, 193, 199 — a Wigner matrix gives ≈ 1/p = 1.0 %, 0.7 %, 0.5 %, 0.5 %; i.e. the sign products
       around 4-cycles cancel to Wigner level (relative saving ≈ p^{−0.9}), with a small POSITIVE residual bias; since A₄ ≈ 7–11 × tree₂
       (dense matrix), the residual still adds +9…15 % to tr C⁴.  Off-diagonal Frobenius mass: ‖offdiag C²‖/‖offdiag |C|²‖ = 0.22–0.28,
       C³: 0.06–0.09.
3. Consequences seen in the spectrum.  ESD of λ/√m₂ is semicircular (Kolmogorov distance 0.055 → 0.043 from p = 97 to 199, 90 % quantile 1.54–
   1.63 vs 1.62); NEGATIVE edge inside the semicircle radius: λ_min = −(1.69…1.97)√m₂ for p ≥ 97 (the earlier fit −2.38√m₂ − 2.1 is the same
   thing with a small-p intercept); POSITIVE outliers: 2–5 eigenvalues above 2√m₂, λ_max = 2.4–2.6√m₂ — the PSD Gram part G/16 pushes a few
   eigenvalues up, not down.  Hence ρ_k = m_{2k}/(m₂^k Cat_k) grows like (λ_max²/4m₂)^k, ρ_k^{1/k} → 1.5–1.65: the trace method is limited by
   λ_max, and can at best certify |λ_min| ≤ λ_max ≈ 2.6√m₂ (or ≤ 2·max_a rn_a ≈ 2.6√m₂ via the tree term) — still enough for the model theorem
   (it needs |λ_min| = o(E/(p−1)) with √m₂ ≍ √(E/(p−1))); the truth is |λ_min| ≤ 2√m₂.
4. What has to be proved (Cancellation Hypothesis CH_δ).  For every closed-walk shape with cyclomatic number g ≥ 1, the signed chain sum is
   ≤ p^{−δg} × the absolute chain sum.  Standard combinatorics (shape counting: ≤ (2k)^{3g}·Cat_k shapes of excess g; A-sums ≤ 10^g × tree)
   then gives tr C^{2k} ≤ (1+o(1))·Cat_k·Σ_a rn_a^{2k} for all k ≤ p^{δ/3−ε} — far beyond k ≍ log p — hence max|λ| ≤ 2·max_a rn_a·(1+o(1)) ≤
   2.6√m₂: Conjecture B with K = 2.6.  Without CH nothing: the absolute cycle sums are 10× the trees.
   Arithmetic content of CH_δ: comp(a; π, π′) is decided by the COLUMNS of the two lifted points of class a used by π and π′, i.e. by half-box
   indicators [x ≤ h] of x = x₀ + t·u — least residues of rational functions of the pattern parameters (family w = 2e/(s₁s₂), direction u on
   the hyperbola uv ≡ w, root z, lift).  So CH_δ = equidistribution, with power saving, of products of 2g+… half-box indicators along closed
   chains of collinear quadruples of A = {xy ≡ ±1}: for each shape, expand the indicators (Erdős–Turán–Koksma / Fourier completion) and bound
   the complete sums over the free direction parameters (Weil/Kloosterman on the hyperbolas uv ≡ w with the incidence relations of the chain)
   — exactly the machinery of Prop. 21–22 (m₈), applied to a chain variety instead of the cubic C₀.  Per shape and per family this is a
   finite Weil computation; the hard part is UNIFORMITY over the families F (up to ~√p scales per pattern) and over shapes — the error terms
   must be summed against a main term of size ~p·m₂^k, so the saving must hold for the aggregated sums (data say it does at g = 1: p^{−0.9}).
5. Structured positive terms (why the bias is positive): patterns living on the same rich line share sign vectors (all sub-triples of one
   quadruple, and the ±1-slope 8-point lines) and give closed chains with product +1 (cliques): O(p)·O(1) in total, negligible against
   p·m₂^k but visible as the +1 % of N₄/A₄ and the positive outliers.  A refined statement would separate "local" (same-line) chains from
   "global" ones and demand cancellation only for the global part.
Bottom line for B: the picture is internally consistent at all levels (bulk semicircle, tree main term, Wigner-level cancellation of 4-cycles,
negative edge inside 2√m₂, positive outliers from the PSD part).  Conjecture B (K = 2.6) ⇐ CH_δ for some δ > 0; CH_δ is a Weil-type
equidistribution statement for closed chains of collinear quadruples of {xy ≡ ±1} with half-box sign weights — a project, not a lemma;
what is NOT needed: k ≍ log p subtleties (CH_δ buys k up to p^{δ/3}), bounded moments, or sparsity.

## B.17 (third solver, 2026-08-18 19:05 UTC) Conjecture A, weak form, is a theorem modulo the per-family Kloosterman count: E(p)/(p−1) ≫ log log p
Idea: multiplicativity of Gaussian norms.  Identify a family (s₁,s₂) with z = s₁ + i s₂ ∈ ℤ[i]; s₁²+s₂² = N(z) and χ(N(zw)) = χ(N(z))χ(N(w))
(χ = Legendre symbol mod p).  So NR·NR = QR: products of two "absent" families are present.  Even if all small families are absent
(p = 193: 5, 10, 13, 17, 26, 29, 34 are all non-residues), their pairwise products 25, 50, 65 = 5·13, 85 = 5·17, 130, 170, 221 = 13·17, …
are present — exactly the 4-point families seen at p = 193 in B.15 ((0,3,4,7)→25, (0,1,7,8)→50, (0,7,11,18)→170, (0,1,13,14)→170).
Setup.  For M ≥ 2 let A_M = {z ∈ ℤ[i] up to units: M ≤ N(z) < 2M} (|A_M| = (π/4)M + O(√M)); for 2M < p every z ∈ A_M has χ(N(z)) = ±1;
Q_M, R_M = the QR / NR parts, δ_p(M) = |Q_M|/|A_M|.  Multiplicative energy E×(A_M) = #{(z₁,z₂,z₃,z₄) ∈ A_M⁴ : z₁z₂ = z₃z₄} ≪ M² log M
(gcd parametrisation: z₁ = ga, z₃ = gb, gcd(a,b) = 1, z₂ = bc, z₄ = ac; norms in [M,2M) force N(a) ≍ N(b) =: m and #g ≪ M/m + 1, #c ≪ M/m + 1;
summing (πm)²(M/m + 1)² over dyadic m ≤ 2M gives ≪ M² log M — and this is sharp).
LEMMA (square scales are never empty).  For every p and every M with 4M² < p:  δ_p(M²) + δ_p(2M²) ≥ c/log M  (absolute c > 0).
Proof.  max(|Q_M|,|R_M|) ≥ |A_M|/2 =: B and B·B ⊂ Q_{[M²,4M²)} (QR·QR = NR·NR = QR; norms multiply into [M², 4M²)); by Cauchy–Schwarz
|B·B| ≥ |B|⁴/E×(B) ≥ (|A_M|/2)⁴/(C M² log M) ≥ c M²/log M, while |A_{M²}| + |A_{2M²}| ≤ (π/4)·3M² + O(M).  ∎
PROPOSITION (A, weak form).  Assume the per-family count of B.15(b): for s₁+s₂ ≤ p^{1/2−ε} a present family contributes N_box(s₁,s₂) ≥ c₀·p/(s₁+s₂)²
box-lifted patterns (Weil–Kloosterman equidistribution of the primitive directions D on uv ≡ 2e/(s₁s₂) in the box |D|_∞ ≤ 2p/(s₁+s₂); the
second solver's §21).  Then  E(p) ≥ (1/8)Σ_{present (s₁,s₂)} N_box ≥ c₁ p Σ_{M = 2^j ≤ p^{1−2ε}} δ_p(M)·|A_M|/M ≥ c₂ p Σ_{j ≤ (1−2ε)log₂p /2} 1/j
≥ c₃ (p−1) log log p   [(s₁+s₂)² ≍ N(z) ≍ M on the scale M, so N_box ≍ p/M; the Lemma applied to M = 2^j gives δ_p at scale 2^{2j} or 2^{2j+1}].
Hence E(p)/(p−1) → ∞ for EVERY p — Conjecture A in the form needed by the spectral programme (which needs only E/(p−1) → ∞ and √m₂ = o(E/(p−1)):
rigorously m₂ = ‖C‖_F²/(p−1) ≤ (3/16)·N₀·E/(p−1) with N₀ = max #patterns through a pair of classes ≤ 64·6 = 384 (64 point pairs, ≤ 6 patterns
per line), so √m₂ ≤ 8.5√(E/(p−1)) = o(E/(p−1)) unconditionally).
Remarks.  (i) The rate log log p is what multiplicativity alone gives; the energy bound M² log M is sharp, so a positive proportion of present
families at a positive proportion of scales (hence E ≫ p log p, the observed rate) still needs the short character-sum input of §21
(χ(s₁²+s₂²) on boxes of side ≤ √p, Burgess/Davenport–Lewis type).  (ii) The Lemma is visible in the data: p = 193 has δ = 0/1, 1/3, 2/6,
3/12 on the scales [4,8) … [32,64) and recovers to 10/25, 29/49 on [64,128), [128,256); p = 197: 0/1, 0/1, 1/3, then 3/6, 6/12, 11/25.
(iii) The same trick gives, for any p and any T ≥ 2, at least c T²/log T present families with s₁+s₂ ≤ 2T — a "no total desert" statement.
Consequence for the programme: (spectral model theorem) ⇐ Conjecture B alone (given the Kloosterman count): min_r T(S(r)) ≥ (1−o(1))·E(p) ≥
c(p−1) log log p for all large p, and ≥ c(p−1) log p if the QR density is bounded below on a positive proportion of scales.

Addendum to B.16 (19:08 UTC) — three exact structural facts for the trace method, all verified at p = 101/199 (scratch checks, third solver):
(a) SIGN LAW.  For a pattern π and two of its classes a, b (lifted points with integer x-coordinates x_a, x_b ∈ [−h, 3h+1]):
    σ_π(a)σ_π(b) = e_a e_b · (+1 if x_a, x_b lie in the same half of the box [−h,h] / [h+1,3h+1], −1 otherwise),  e = the hyperbola signs
    (e,−e,−e,e) of the quadruple positions.  Verified on all pattern pairs at p = 199 (identity holds for 100 %).  The same-half probability
    decreases linearly in |x_a − x_b|/p (0.98, 0.91, 0.83, …, 0.08 for |Δx|/p in [0,0.1), [0.1,0.2), …, [0.9,1); 0 for |Δx| ≥ p — 13 % of pairs).
    So C = C_e − 2C_diff with C_e = (1/16)Σ e_a e_b (hyperbola signs only, no box) and C_diff the different-half part; spectra at p=199:
    C_e: λ_min/√m₂ = −3.12 (worse than C's −1.94!), C_diff: ±2.5, C: −1.94/+2.48 — the half-box flips make the matrix MORE Wigner-like.
(b) MULTIPLIER STRUCTURE.  Along a quadruple the x-residues are (z_F + t)·u, so two classes a, b in one pattern satisfy b/a = μ = (z_F+t_b)/(z_F+t_a)
    with z_F = (−(s₁+s₂) ± √(s₁²+s₂²))/2 (e.g. (1,2): z = −φ², positions −φ², −φ, −φ⁻¹, φ⁻² — golden-ratio multipliers ±φ^{±1..4}).  Hence
    C = Σ_μ C^{(μ)}, C^{(μ)} supported on {(a, μa)}: a sum of signed multiplication operators on F_p^*; the mass is spread over essentially all
    μ (196 of 197 at p=199; top-10 multipliers 20 %, top-30 41 %), a few multipliers are strongly sign-biased (μ = 63 at p=199: mean sign +0.89
    on 150 entries — short-direction patterns, same-half pairs, fixed e_ae_b) — the source of the positive outliers/bias.  The multiplier-mean
    (circulant on F_p^*) part C̄ carries only 9–10 % of ‖C‖_F² and has spectrum within ±5; C − C̄ has the same edges as C (−8.6/+9.9 vs
    −9.0/+11.4 at p=199): the Wigner behaviour lives in the geometric fluctuation, not in a group-circulant.
(c) CLOSED WALKS = TORUS LINES.  In a closed walk a → μ₁a → μ₁μ₂a → … the weights are functions of least residues of fixed multiples λ_j·a
    (positions of the lifted APs relative to the box middle: half indicators, fitting conditions), so each closed-walk TYPE (choice of families,
    positions, lifts, multipliers with Π μ_i = 1 in F_p^*) contributes  Σ_{a ∈ F_p^*} Π (interval indicators of X(λ_j a)) × (fixed sign)  =
    p·(signed volume of a polytope) + error controlled by small integer relations Σ m_j λ_j ≡ 0 (mod p) (Erdős–Turán–Koksma; lattice-rule
    discrepancy — no Weil needed for a single type).  The main terms are NOT zero type by type (a fixed type has a definite sign = product of
    position parities e_ae_b and a positive volume); CH_δ therefore has to come from cancellation ACROSS types — the closure Π μ_i ≡ 1 mixes
    families and positions "randomly" (accidental identities among the algebraic numbers z_F + t mod p) — plus counting of the structured types
    (rational z_F: Pythagorean families; same-line cliques; commutator walks μ,ν,μ⁻¹,ν⁻¹ of biased multipliers), which give the observed
    positive 1 % bias.  This is the precise shape of the arithmetic input for B.
## 22. T2.14 (second solver): the per-family count — statement, proof, and the bookkeeping that avoids primitivity
LEMMA K.  Let p be a prime, s₁ ≤ s₂ positive integers with gcd(s₁,s₂) = 1 and χ(s₁²+s₂²) = +1 (nonzero QR), e = ±1, and put
L = ⌊p/(s₁+s₂)⌋.  Then the number of collinear point-triples of P₋₁ with three distinct classes that are sub-triples of a quadruple
q, q+s₁D, q+s₂D, q+(s₁+s₂)D with D = (u,v) ∈ Z², |u|,|v| ≤ L, uv ≡ 2e/(s₁s₂) (mod p), is at least
     N_box(s₁,s₂,e) ≥ 2·( (2L+1)²/p − C√p log²p )        (C absolute; two roots z of z² + (s₁+s₂)z + s₁s₂/2 ≡ 0),
and different (coprime) families and different D give different triples.  In particular N_box ≥ c₀ p/(s₁+s₂)² whenever s₁+s₂ ≤ p^{1/4−ε}.
Proof.  (i) Residue quadruples (B.15): for each u ∈ F_p* and each root z there is exactly one residue quadruple with base (x,y) = (zu, e/(zu))
and direction (u, v ≡ 2e/(s₁s₂u)); its four residue points have xy ≡ e, −e, −e, e.  (ii) Kloosterman: #{(u,v) ∈ [−L,L]²: uv ≡ w (mod p)} =
(2L+1)²/p + O(√p log²p) for every w ≢ 0 (Kloosterman sums + completion; e.g. Iwaniec–Kowalski Ch. 11 / Shparlinski's survey), no primitivity
required.  (iii) Box lift: given an integer D = (u,v) with |u|,|v| ≤ L and the residue base point (x,y), choose the lift x̃ of x in [−h,h] if
u ≥ 0 and in [h+1, 3h+1] if u < 0, and ỹ of y in [0,p) if v ≥ 0 and in [p,2p) if v < 0; then x̃ + tu ∈ [−h, 3h+1] and ỹ + tv ∈ [0, 2p−1] for
0 ≤ t ≤ s₁+s₂ ≤ p/L, so the whole quadruple lies in the box: at least one lift per (D, z).  (iv) Distinct classes: two of the four points are
congruent iff (t−t′)D ≡ 0 (mod p), impossible for 0 < |t−t′| < p and u,v ≢ 0.  (v) Injectivity: a triple determines its line, its primitive
direction D′ and its primitive spacings (S₁,S₂); if it arises from the coprime family (s₁,s₂) with step D = dD′ then (s₁,s₂) = (S₁/g, S₂/g)
with g = gcd(S₁,S₂) and d = g are forced — so coprime families with arbitrary (not necessarily primitive) D count each triple at most once.
Hence the number of distinct triples ≥ Σ_{roots z} #{D} ≥ 2((2L+1)²/p − C√p log²p), and each quadruple contains 4 sub-triples of which at
least one has three distinct classes (all four points are in distinct classes by (iv), so all 4 sub-triples qualify: the bound can be
multiplied by 4 minus box-truncation).  ∎
Remark (why not primitive directions): the Möbius/trivial-bound treatment of primitivity costs Σ_{d} 2L/d ≈ 2L log L, which exceeds the main
term 4L²/p when L < p log L; counting coprime FAMILIES with all D avoids the issue entirely.  Similarly, non-coprime present families are the same
triples as their coprime reductions (QR status is invariant under (s₁,s₂) ↦ (ds₁,ds₂)), so B.17's density lemma applies through the
identity Σ_g P(T/g²) ≥ c T/log T ⇒ Σ_T P(T)/T ≥ (c/ζ(2)) log log p for the counts P(T) of present coprime families with norm in [T,2T).
Consequence (with B.17): E(p) ≥ (1/8) Σ_{coprime present, s₁+s₂ ≤ p^{1/4−ε}} N_box ≥ c (p−1) log log p, unconditionally, for all large p.
(To be checked by the third; then it becomes a Proposition of the note's §6 or of a future v1.1: "Conjecture A weak form".)
