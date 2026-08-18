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
