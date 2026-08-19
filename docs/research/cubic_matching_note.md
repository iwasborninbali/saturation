# G3 (4/3) for cubic graphs via W₄ + a matching of "good" three-point lines — the certificate, the numbers, and what remains to prove
*(first solver, 2026-08-19; tools `slack/cube_3line_probe.py`, `slack/cube_3line_families.py`, `slack/cube_matching_fast.py`; log
`slack/verification/cube_matching_fast.txt`)*

## 1. The certificate
For the box lift of y = a·x³ (p ≡ 2 mod 3; every permutation cubic up to a box shift), let W₄ = weight 1 on every ±1-line with ≥ 4 points, S₀ = the points
on none of them (|S₀| = (7/4 + o(1))p, `permutation_cubic_note.md`), and call a three-point line (of a slope ≠ 0, ∞, ±1) **good** if its three points lie in
S₀.  If M is a set of pairwise disjoint good lines, then "W₄ + weight 1 on the lines of M + singletons on the rest of S₀" is a fractional cover of cost
   cost = 2L₄ + |S₀| − |M| = (11/4 + o(1))·p − |M|          (each matched line replaces three singletons, cost 3, by one line, cost 2),
so α ≤ (11/4 + o(1))p − |M|.  Conjecture G3 (α ≤ (4/3 + o(1))·2p = (8/3 + o(1))p) for permutation cubics therefore follows from a matching of size
|M| ≥ (1/12 + ε)p = (0.0833… + ε)p; non-permutation cubics already satisfy G3 by the row bound (`curves_conjecture.md` §8), with the constant 4/3 exactly in the S₃ case.
Elementary matching bounds: for the intersection graph of the good lines (edges = pairs sharing a point), |M| ≥ #good − #pairs, and (Caro–Wei/Turán)
|M| ≥ Σ_{good e} 1/(1 + n_e), n_e = number of good lines meeting e.

## 2. Family structure and the numbers (box (0,0), y = x³)
Three-point lines come in families (i,j) (second solver, `curves_conjecture.md` §7): steps 0 < i < j, gcd(i,j) = 1, base residue x₁ ≡ −(i+j)u/3, points
x₁, x₁+iu, x₁+ju, integer direction (u*, v*) ≡ (u, c₁u³) with |iu*|, |ju*|, |iv*|, |jv*| inside the box; span J := number of primitive steps between the extreme
points.  `cube_matching_fast.py` enumerates all lines of span ≤ J₀ in O(p) (validated against the O(p²) brute force at p = 401: identical counts).
Span 2 = the lines through the four lifts of the centre (0,0): ~1.2p lines, NEVER good.  Span 3: ~1.0p lines, 7–9 % good; span 4: 0.85p, 3.5–7 %; …
Matching bounds (per p; "needs" = (cost(W₄) − 8p/3)/p, the finite-p threshold for 4/3):
```
   p     needs   span≤4: good  pairs  good−pairs  CW     greedy | span≤5: good  pairs good−pairs  CW    greedy | span≤6: good  pairs good−pairs  CW    greedy | greedy(all spans)
  401    0.0865        0.100  0.015   0.085     0.087  0.090  |        0.155  0.045   0.110    0.118  0.125  |        0.209  0.070   0.140    0.151  0.165  |  0.384  (cost 1.185 N)
  797    0.101         0.133  0.035   0.098     —      0.105  |        0.178  0.068   0.110    —      —      |        0.221  0.100   0.120    —      0.158  |  0.408  (1.180 N)
 1601    0.0654        0.122  0.031   0.091     0.096  0.098  |        0.156  0.068   0.089    0.103  0.113  |        0.200  0.096   0.104    0.127  0.141  |  —
 3203    0.0895        0.129  0.028   0.101     0.103  0.107  |        0.179  0.062   0.116    0.128  0.136  |        0.231  0.109   0.122    0.148  0.161  |  —
 6449    0.0817        0.122  0.028   0.094     0.097  0.101  |        0.171  0.068   0.104    0.117  0.127  |        0.211  0.112   0.099    0.129  0.147  |  —
12809    0.0847        0.137  0.038   0.100     0.105  0.109  |        0.186  0.080   0.106    0.124  0.135  |        0.229  0.125   0.104    0.139  0.157  |  —
```
(all entries in units of p; "CW" = Caro–Wei sum).  Asymptotically the threshold is 1/12 = 0.0833; the rigorous second-moment bound at span ≤ 5 is
0.104–0.116 (margin ≈ 0.02–0.03), Caro–Wei at span ≤ 6 is 0.13–0.15 (margin ≈ 0.05); the actual greedy matching gives cost ≈ 1.30 N (span ≤ 6), 1.28 N
(span ≤ 8), 1.18 N (all spans; the LP over all lines is 1.10 N).

## 3. What has to be proved (two counting lemmas), and why it is within the existing machinery
(A) #good lines of span ≤ J₀ = γ₁(J₀)·p + O(√p log^c p); (B) #pairs of good lines of span ≤ J₀ sharing a point = γ₂(J₀)·p + O(√p log^c p) (or the
Caro–Wei sum = γ_CW·p + o(p)); then |M| ≥ (γ₁ − γ₂ − o(1))p and α ≤ (11/4 − γ₁ + γ₂ + o(1))p.  Numerically γ₁ − γ₂ ≈ 0.105 for J₀ = 5 (⇒ α ≤ 2.645p = 1.32 N < 4/3 N).
Proof structure for (A): a line of family (i,j) is a residue u together with a lift of x₁ and small representatives (u*, v*); its three residues are the fixed
multiples α_m u, α_m ∈ {−(i+j)/3, (2i−j)/3, (2j−i)/3}; the good status of the lift of α_m u is a box condition on (position of α_m u, the ±1 thresholds
g_±(α_m u) built from α_m³u³ ∓ α_m u, the partner positions on the two conics t² + α_m u t + α_m²u² ∓ 1/a = 0, and the lift (δ_m, ε_m), itself determined by
u*, v*).  For J ≥ 3 the three squares α_m² are pairwise distinct (checked for all (i,j) with j ≤ 6; for the centre family (1,2) they are not — α = (−1,0,1) — which
is why it never gives good lines), so the six discriminants ±4/a − 3α_m²u² are distinct squarefree quadratics in u and the fibre product of the six partner
conics over the u-line is absolutely irreducible of bounded genus.  Hence the joint law of (u, u³, six Legendre symbols, twelve partner roots) is the
product law (Weil for χ(Π quadratics), Bombieri for the additive characters on the fibre product), and the count is Σ over lifts/representatives of a
Weil-in-boxes sum in (u*, v* ≡ c₁u³) (the second solver's G3.3, with the box conditions of the partner data attached — more log factors, same √p).  The
constant γ₁ is a one-dimensional integral over u* (the positions of α_m u* enter through the class thresholds; u* ranges over an interval of length ≍ p/J,
so the positions of the three residues are NOT uniform — the law is explicit but family-dependent, e.g. for 3 | i+j the residues are integer multiples of u*).
For (B): a pair of lines sharing a point is a configuration (family, role, family′, role′) with the second parameter determined by the first
(u′ = (α_m/α′_{m′})u), five residues (multiples of u), ten conics; the same argument, finitely many configurations for J₀ ≤ 6 (≈ 11 families × 11 × 9 roles);
degenerate coincidences (α = ±α′′ between the two lines' residues, e.g. the mirror residue −αu) give dependent but still explicit laws.  For the Caro–Wei
sum one needs the neighbour-count distribution — the same finite configuration analysis.

## 4. Status and plan
* The certificate and the two elementary matching bounds are rigorous for every p; the numbers above are exact computations (not simulations).
* A theorem "α(permutation cubic) ≤ (4/3 − c)·2p" needs (A)–(B) with proven values γ₁ − γ₂ > 1/12 (or the Caro–Wei constant): the equidistribution part is
  the same as Lemmas positions/twoslopes of Section 9 (more components, bounded genus); the constants are explicit one-dimensional integrals of piecewise
  polynomial functions (positions of α_m u* and the box constraints on (u*, v*)), evaluable numerically with rigorous error, or bounded from below crudely.
  Estimated effort: 1–2 days (bookkeeping of lifts/representatives is the tedious part).
* This bypasses the degree-concentration obstacle of `curves_conjecture.md` §7a: only first and second moments of good lines are used.
* Corollary once done: Conjecture G3 holds for EVERY cubic graph (rows for non-permutation cubics; W₄ + matching for permutation cubics), strictly for the latter.
