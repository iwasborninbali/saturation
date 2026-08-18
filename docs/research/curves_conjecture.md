# G — "Algebraic curves modulo p cannot beat 3/2 in the natural box": a precise conjecture, what is proved, what the data say
(second solver, 19.08.2026; follows Ben Green's comment to Problem 72 of his list, version 01.2026: "It is possible that any no-three-in-a-line
subset of [N]² is either small, or has a large subset which reduces (mod p) to a set of points on a curve in F_p². It might be interesting to
formulate a precise conjecture of this type and see whether it can be used to show that the construction of [HJSW] is optimal.")

## 1. Setting
p prime, box B = [x₀, x₀+2p) × [y₀, y₀+2p) (side N = 2p; the HJSW box is x₀ = −(p−1)/2, y₀ = 0).  For an affine curve C ⊂ A² over F_p let
L_B(C) = {(x,y) ∈ B : (x mod p, y mod p) ∈ C(F_p)} — the box lift (each residue point has ≤ 4 lifts; exactly 4 when the box is 2p × 2p),
and α(C, B) = the largest no-three-in-line subset of L_B(C).  HJSW/KNS: for the hyperbola xy = c, α = 3(p−1) in the HJSW box (Theorem 1 of the note),
i.e. (3/2)·N − 3.

## 2. Conjecture G (curves)
For every d there is c_d such that for every absolutely irreducible curve C of degree ≤ d over F_p and every 2p × 2p box B,
       α(C, B) ≤ (3/2 + o_d(1))·N   ( = 3p + o(p) ),
with equality (up to O(1)) only for the shifted hyperbolae (x − x₁)(y − y₁) = c in a box that "centres" the residue window as HJSW do.
Stronger form (unions): for a union of ≤ m curves of degree ≤ d, α ≤ (3/2 + o(1))N as well.

## 3. What is proved (this repository)
* Conics: Corollary "all conics" of the note — among all conics only the shifted hyperbolae reach 3(p−1) in a 2p × 2p box; other conics are ≤ c(p+3)
  (row counting), and the hyperbola's maximum is exactly 3(p−1) in the HJSW box and known exactly in every 2p × 2p box (box formula).
* Unions of two hyperbolae: H(1) ∪ H(−1) ≤ (11/3 + o(1))(p−1) (Theorem two); every H(1) ∪ H(k) with ord(k) ≥ C√p log⁵p: ≤ 4(p−1) − c√p/log⁵p
  (Theorem/Corollary of Section "Every second hyperbola", v1.4); numerically ≈ 3(p−1) + O(1) for all k (Section 7).  So for unions of two hyperbolae
  the conjecture's bound (3/2)N + O(1) is what the data show, and 11/3 (resp. 4 − ε) is what is proved.
* Trivial general bound: rows and columns give α ≤ 4p for any curve of degree ≤ 4 in a 2p × 2p box... hmm — in general ≤ 2·(number of non-empty rows) ≤ 4p;
  the conjecture asks for the factor 3/4 of the trivial bound.

## 4. Data (this session; `scratch curvescan.py`, `tricount.py`, `winscan.py`; exact CP-SAT maxima with window scans over all shifts (s,t) for p ≤ 13,
   sparse t for p ≤ 19)
Cubics y = x³, y = x³ + x, y = x³ + 2x + 1, xy² = 1, elliptic y² = x³ + ax + b, quartic y = x⁴ + x, circle x² + y² = 1: see the table appended below
(ratio α/N).  Earlier: p = 11: cubics ≤ 28 (hyperbola 30); p = 13: ≤ 31 (36); p = 17: ≤ 40 (48); p = 19: ≤ 38 (54).  Collinear-triple counts of the
full lifts (p ≤ 101): cubics carry 5–7.6 collinear triples per point (the hyperbola: 0.7), with lines of up to 6 points — the residue-collinear
triples of a curve of degree ≥ 3 lift to many integer collinear triples, which is the mechanism behind the conjecture for d ≥ 3.

## 5. Why it might be provable for d ≥ 3, and why it is hard
* Mechanism: a line meets a curve of degree d in ≤ d residue points; for d ≥ 3 the residue-collinear triples number ≍ p² and a positive proportion of
  their 64 lift-triples are integer-collinear (the determinant, ≡ 0 mod p, is a multiple of p in a range of size ≍ p² → probability ≍ 1/p) — so
  Θ(p) collinear triples per Θ(p) points, i.e. bounded average degree in the "collinearity 3-graph"; the maximum independent set of such a 3-graph
  is a positive fraction of the vertices, and the question is whether that fraction is < 3/4 uniformly.  For the hyperbola (d = 2) there are NO
  residue-collinear triples and all collinear triples come from wrap-around (slopes ±1 in the HJSW box) — that is why the hyperbola is best.
* Upper-bound tools that could work: fractional covers by rich lines (LP), as in the note (the LP with all lines with ≥ 3 points is exact for the
  hyperbola); for cubics the rich lines are the lifted residue-collinear triples — their structure is arithmetic (which residue triples lift with which
  slopes) and needs a classification like the "rich lines" lemma; a general theorem for all cubics is a genuine research problem.
* A weaker but clean first target: graphs y ≡ f(x) of polynomials of degree 3 (columns have exactly 2 points, rows ≤ 6): show α ≤ (3 − c)p for an explicit
  c > 0 by an LP certificate valid for all p (rows at weight ... + the arithmetic of the residue-collinear triples).

## 6. Recommendation
Formulate Conjecture G in the note's Section 7 as the "precise conjecture" Green asks for, with the proven cases and the data; then decide whether to
invest in the cubic case (LP anatomy first, as for the pair of hyperbolae).  Value: a direct answer to a listed problem's comment; risk: the cubic
case may need new ideas.

### Table (exact CP-SAT maxima; window scans over shifts (s,t): all (s,t) for p ≤ 13, t on a grid for p ≥ 17); ratio = α/(2p)
```
p=11 hyp: best alpha=30 at shift (0, 6); ratio to N=2p: 1.364; 3(p-1)=30
p=11 cub: best alpha=28 at shift (4, 3); ratio to N=2p: 1.273; 3(p-1)=30
p=11 cubx: best alpha=23 at shift (0, 0); ratio to N=2p: 1.045; 3(p-1)=30
p=11 cub2: best alpha=24 at shift (2, 2); ratio to N=2p: 1.091; 3(p-1)=30
p=11 ell1: best alpha=24 at shift (0, 0); ratio to N=2p: 1.091; 3(p-1)=30
p=11 ell2: best alpha=20 at shift (0, 0); ratio to N=2p: 0.909; 3(p-1)=30
p=11 quart: best alpha=25 at shift (0, 2); ratio to N=2p: 1.136; 3(p-1)=30
p=11 circ: best alpha=24 at shift (0, 0); ratio to N=2p: 1.091; 3(p-1)=30
p=11 xy2: best alpha=20 at shift (0, 0); ratio to N=2p: 0.909; 3(p-1)=30
p=13 hyp: best alpha=36 at shift (0, 7); ratio to N=2p: 1.385; 3(p-1)=36
p=13 cub: best alpha=20 at shift (0, 0); ratio to N=2p: 0.769; 3(p-1)=36
p=13 cubx: best alpha=27 at shift (4, 11); ratio to N=2p: 1.038; 3(p-1)=36
p=13 cub2: best alpha=31 at shift (7, 1); ratio to N=2p: 1.192; 3(p-1)=36
p=13 ell1: best alpha=31 at shift (0, 0); ratio to N=2p: 1.192; 3(p-1)=36
p=13 ell2: best alpha=28 at shift (0, 0); ratio to N=2p: 1.077; 3(p-1)=36
p=13 quart: best alpha=24 at shift (7, 2); ratio to N=2p: 0.923; 3(p-1)=36
p=13 circ: best alpha=24 at shift (0, 0); ratio to N=2p: 0.923; 3(p-1)=36
p=13 xy2: best alpha=24 at shift (0, 2); ratio to N=2p: 0.923; 3(p-1)=36
p=17 hyp: best alpha=48 at shift (3, 8); ratio to N=2p: 1.412; 3(p-1)=48
p=17 cub: best alpha=41 at shift (0, 8); ratio to N=2p: 1.206; 3(p-1)=48
p=17 cubx: best alpha=38 at shift (0, 0); ratio to N=2p: 1.118; 3(p-1)=48
p=17 cub2: best alpha=36 at shift (0, 0); ratio to N=2p: 1.059; 3(p-1)=48
p=17 ell1: best alpha=28 at shift (0, 0); ratio to N=2p: 0.824; 3(p-1)=48
p=17 ell2: best alpha=36 at shift (0, 8); ratio to N=2p: 1.059; 3(p-1)=48
p=17 quart: best alpha=33 at shift (2, 8); ratio to N=2p: 0.971; 3(p-1)=48
p=17 circ: best alpha=32 at shift (0, 0); ratio to N=2p: 0.941; 3(p-1)=48
p=17 xy2: best alpha=32 at shift (0, 0); ratio to N=2p: 0.941; 3(p-1)=48
p=19 hyp: best alpha=54 at shift (0, 10); ratio to N=2p: 1.421; 3(p-1)=54
p=19 cub: best alpha=28 at shift (0, 0); ratio to N=2p: 0.737; 3(p-1)=54
p=19 cubx: best alpha=39 at shift (0, 8); ratio to N=2p: 1.026; 3(p-1)=54
p=19 cub2: best alpha=40 at shift (0, 4); ratio to N=2p: 1.053; 3(p-1)=54
p=19 ell1: best alpha=36 at shift (0, 0); ratio to N=2p: 0.947; 3(p-1)=54
p=19 ell2: best alpha=36 at shift (0, 0); ratio to N=2p: 0.947; 3(p-1)=54
p=19 quart: best alpha=43 at shift (4, 16); ratio to N=2p: 1.132; 3(p-1)=54
p=19 circ: best alpha=40 at shift (0, 0); ratio to N=2p: 1.053; 3(p-1)=54
p=19 xy2: best alpha=36 at shift (0, 4); ratio to N=2p: 0.947; 3(p-1)=54
```

### LP upper bounds (fractional cover by all lines with ≥ 3 points; `scratch lpcurves.py`), ratio LP/(2p) — the hyperbola is at 1.43–1.47 (→ 3/2):
```
p=43 : hyp 1.430  cub 0.698  cubx 0.976  ell 0.744      (lines>=3: hyp 59, cub 465, cubx 540, ell 303)
p=61 : hyp 1.451  cub 0.689  cubx 0.978  ell 0.742      (85, 766, 799, 554)
p=101: hyp 1.470  cub 1.098  cubx 1.059  ell 0.851      (145, 1517, 1417, 1734)
```
So for these cubics the LP certifies α ≤ 0.7–1.1 N per p — far below 3/2 N: Conjecture G holds for them with a large margin, and the question is a
UNIFORM fractional-cover construction (the rich lines of a lifted cubic are the lifts of the ≍ p² residue-collinear triples that happen to be
integer-collinear; their arithmetic is the analogue of the ±1 residue-group structure of the hyperbola).  Suggested first target: graphs y ≡ f(x),
deg f = 3 — a theorem α ≤ (3 − c)p for an explicit c would be the first "curves cannot beat HJSW" statement beyond conics.

## 7. G3 — cubic graphs y = f(x): the structure of the collinear triples (second solver, 19.08 07:40 WITA; `scratch cubic_lines.py`, `cubic_fam.py`)
Take f(x) = x³ + ax + b (every cubic is a translate of a depressed one; translations move the box, which is allowed).  Three residue points
(x_i, f(x_i)) are collinear mod p iff x₁+x₂+x₃ ≡ 0 (they are then the roots of f(x) − mx − c); this is the "sum0" signature of every rich line of the
lift with three distinct residues (verified: 1415/1417 three-point lines at p = 101, all four-to-six-point lines).
FAMILY STRUCTURE (proved, one line of algebra; verified for 797/799 lines at p = 61 and 1416/1417 at p = 101 for f = x³ + x): a three-point line with
integer direction (u,v) (u ≠ 0) and integer steps i, j (the other two points at q + i(u,v), q + j(u,v)) has base residue x ≡ −(i+j)u/3, and then
v ≡ c₁u³ + a·u (mod p) with c₁ = (i² − ij + j²)/3 — for EVERY u ∈ F_p^* and every pair of steps (i ≠ j) there is exactly one residue triple
(x, x+iu, x+ju), and the line exists in the box iff (u,v) has an integer representative with |iu|,|ju|,|iv|,|jv| inside the box.  So the three-point
lines are organised in families (i,j) (the analogue of the (s₁,s₂) families of the pair of hyperbolae), each family living on the "direction curve"
v = c₁u³ + au — a cubic GRAPH mod p (Weil-type counts of its small solutions, no genus-1 curve needed): family (i,j) has ≈ 4p/J² lines,
J = max(|i|,|j|,|i−j|), and the number of families at scale J is ≈ 2J, whence ≈ 8p·log(J_max) three-point lines in total (data: 14p at p = 101).
Lines with 4–6 points can only have slopes 0, ±1 (two lifts of one residue on a line) — the "wrap-around" lines of the hyperbola story: rows with three
preimages (a 1/6 fraction of the values for a generic cubic), diagonals f(x) − x ≡ c and antidiagonals f(x) + x ≡ c with three roots (1/6 each);
their count is ≈ 2p/3, they cover ≈ 3p of the 4p points at cost 1/3 per point.  A special role is played by the centre of symmetry (0, f(0)) of the
depressed cubic: ~p/2 three-point lines pass through its lifts (pairs of symmetric residues).
LP values (fractional cover by rows, columns and all rich lines): f = x³ (p ≡ 2 mod 3, bijective): 1.10 N at p = 101; f = x³ + x: 0.98–1.06 N (p = 61, 101);
elliptic curves: 0.74–0.85 N (columns half empty).  Expected asymptotics: 6-lines cover 3p points at cost p, the remaining points by three-point lines
at 2/3 per point ⇒ LP → (5/3)p = 0.83 N for cubics with three-preimage rows; ≤ (4/3 + o(1)) N for any cubic graph if the three-point-line hypergraph is
near-regular on the leftover points (uniform weight 1/d on a d-regular 3-graph costs 2n/3).
CONJECTURE G3 (cubic graphs): for every cubic f over F_p and every 2p×2p box, α ≤ (4/3 + o(1))·2p — strictly below the hyperbola's 3/2.
Proof programme: (i) family structure (done); (ii) equidistribution of the small solutions of v ≡ c₁u³ + au (Weil for polynomial exponential sums, boxes
of side ≥ p^{3/4+ε} ⇒ families with J ≤ p^{1/4−ε} — still ≍ log p lines per point); (iii) the degrees d_q of points in the restricted family and their
concentration — the delicate step: the events "u = −3x/(i+j) has a small representative" for different (i,j) are correlated (APs with different
differences), so a second-moment argument must be done carefully, or the cover must be organised by families rather than by uniform weights (as the
block cover was for the pair of hyperbolae); (iv) the fractional cover.  Honest estimate: several days; the payoff is the first "curves of degree three
cannot beat HJSW" theorem, in the direction Green suggests.

### 7a. First obstacle for a proof of G3 (07:45 WITA; `slack/cubic_anatomy.py`, scratch `cubic_deg.py`, `cubic_degpos.py`)
LP values are stable: f = x³ (bijective, p ≡ 2 mod 3): 1.098 N (p=101), 1.100 N (p=401); f = x³+x: 0.98 (61), 1.06 (101), 0.95 (307).  Anatomy at p=401 (x³):
mass on generic 3-lines 570 of 882, on ±1 lines (6,5,4,3 points) 300; degrees of points in the generic 3-line hypergraph: mean 14.6 (≈ 1.7·log₂p),
std 5.9, coefficient of variation 0.37 (p=101), 0.40 (401), 0.40 (809) — NOT decreasing; 9–10 % of points have degree ≤ mean/2; position in the box
(distance to the edges) explains only 29 % of the variance (mean degree 9.8 near the edge, 20–23 in the centre), residual CV 0.34.
Consequence: the "uniform weight on 3-lines ⇒ (4/3)N" argument needs degree concentration, which the data refute at these p (and the correlations
between families — arithmetic progressions with different differences through the same residue — suggest CV stays ≍ 1).  So a proof of G3 must be
organised by families/positions with adaptive weights (as the LP does), or find another mechanism; the LP itself certifies ≈ 1.1 N for each p.
Status: G3 = well-supported conjecture + explicit structure + per-p certificates; a general proof needs a new idea (estimated days–weeks, uncertain).

## 8. CORRECTION and reduction (first solver, THREAD[125]; second solver, 07:55 WITA): the projection bound
For ANY function f: F_p → F_p and any 2p × 2p box, the lifted graph has exactly 2|f⁻¹(c)| points in each of the two rows with residue c, and
2|f(F_p)| non-empty rows; a lawful set has ≤ 2 points per row, hence   α(graph f) ≤ 4·|f(F_p)|.   More generally, for any curve C,
α(C, box) ≤ 4·min(|π_x(C(F_p))|, |π_y(C(F_p))|).
Consequences.  (a) A generic cubic (Galois group S₃ of f(x) − c over F_p(c)) has |Im f| = (2/3)p + O(√p) ⇒ α ≤ (8/3)p + O(√p) = (4/3 + o(1))·N — the
constant of Conjecture G3 for free; the A₃ case (f = a(x+b)³ + c, p ≡ 1 mod 3): |Im| = (p+2)/3 ⇒ α ≤ (2/3)N + O(1) (LP = 4|Im| exactly at p = 103).
(b) The only cubic graphs for which the bound is trivial (4p = 2N) are the PERMUTATION cubics f = a(x+b)³ + c with p ≡ 2 (mod 3) (Dickson).
(c) For elliptic curves and all curves with a projection of degree ≥ 3 the projection misses ≈ 1/3 of the residues ⇒ α ≤ (4/3 + o(1))N trivially;
Conjecture G is non-trivial only for BI-SURJECTIVE curves (graphs of algebraic bijections: x ↦ 1/x — the hyperbola, x ↦ x^k with gcd(k,p−1)=1, Dickson,
Rédei, …), and among those the hyperbola is special: no three of its residue points are collinear, so only the ±1 "wrap-around" lines carry three points.
REFINED CONJECTURE G′.  For every bi-surjective curve of degree ≥ 3 (permutation polynomial graphs in particular): α ≤ (3/2 − c_d)·N.
Data (first solver, `slack/lp_curve.py`, `slack/verification/lp_curve.txt`): y = x³, p ≡ 2 mod 3, p = 101…197: LP with rows/columns/±1 lines only =
1.317–1.355 N (≈ 4/3, slightly increasing), full LP (all rich lines) = 1.098–1.108 N; y = x⁵ (p=197, permutation): 1.355 / 1.072 N; hyperbola in the HJSW
box: 3(p−1) exactly (calibration).  So for permutation cubics the ±1 lines ALONE give ≈ (4/3)N — a "block-cover" theorem of the type of Theorem two
(residue groups of ax³ + b ∓ x ≡ c with three roots; Bombieri for the counts) should give α ≤ (3/2 − c)N (weak form G3′) — assigned to the first solver
(G3.5); the strong form (4/3 or ≈ 1.1) needs the 3-line families (§7) and adaptive covers (§7a).  Together with the projection bound this would give:
"NO CUBIC GRAPH BEATS HJSW in the natural box" — a clean statement in the direction of Green's remark.
