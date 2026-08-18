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
