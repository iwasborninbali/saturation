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
```
