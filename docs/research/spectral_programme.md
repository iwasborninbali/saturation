# The spectral programme for the vertical-pair model (k = −1) — a self-contained problem statement (2026-08-19)

Setting.  p odd prime, h = (p−1)/2, box G(p) = [−h, 3h+1] × [0, 2p−1], P₋₁ = {(x,y) ∈ G(p): xy ≡ ±1 (mod p)} (8(p−1) points).
Classes: for a ∈ F_p* the H(1)-class κ_a = (a, 1/a) and the H(−1)-class κ′_a = (a, −1/a); each has four lifts (X(a) + r p, Y + s p),
r,s ∈ {0,1}, X(a) ∈ [−h,h] the least absolute residue, Y ∈ [1,p−1] the least positive residue of ±1/a.
Vertical-pair model.  An orientation r ∈ {0,1}^{p−1} chooses for every a: κ_a takes both lifts in column X(a) + r_a p and κ′_a both lifts in
column X(a) + (1−r_a) p.  S(r) has 4(p−1) points, exactly two in every row and column (a 2-factor of the row/column structure).
T(r) := number of collinear triples of S(r).  A lawful subset of S(r) must delete a hitting set of these triples.

Fact 1 (proved; second solver, verified by the third): with ε_a = (−1)^{r_a},  T(ε) = E + εᵀ C ε  exactly — a quadratic form:
the odd-degree Walsh coefficients vanish because S(1−r) = R′(S(r)) for the reflection R′: (x,y) ↦ (x, 2p−y), a symmetry of P₋₁.
Here E = (1/8)·#Π, Π = the set of collinear point-triples of P₋₁ with three distinct classes (each such triple is present in S(r) for
exactly one of the 8 orientation patterns of its three residues), and C = (1/16)·(Σ_{π∈Π} s_π s_πᵀ − D), s_π ∈ {±1}³ the required-bit signs
of π (H(1)-copies in column r=0 → +1, r=1 → −1; H(−1) reversed), D = diag(pattern degrees).  Hence, trivially,
      min_r T(r) ≥ E + (p−1)·λ_min(C).                                                                     (★)

Fact 2 (data).  Exact minima (all 2^{p−1} orientations): 24, 28, 42, 48, 80, 136 for p = 11, 13, 17, 19, 23, 29 (`slack/vp_min.py`).
E/(p−1) ≈ 3.6 log p − 4.4 (11 ≤ p ≤ 199; e.g. 5.4, 6.6, 9.1, 12.8 at 11, 19, 29, 71).  λ_min(C) ≈ −2.4·√(tr C²/(p−1)) − 2.1 with
tr C²/(p−1) ≈ 5.4 log p − 10.9; normalised moments semicircle-like (m₄/m₂² ≈ 2–2.6, m₆/m₂³ ≈ 5–10); C is dense (≈ (p−1)/2 nonzeros per
row, entries in (1/8)Z, |c| ≤ 1.75).  Consequently the bound (★) is E·(1 − o(1)) numerically: 21, 23, 33, 46, 64, 129 at p = 11…29 against
the true minima above; ≥ 3.6(p−1) for 41 ≤ p ≤ 71 (`slack/vp_quadratic.py`, `slack/vp_traces.py`, `slack/verification/vp_moments_km1.txt`).

Conjecture A (growth of E).  E(p)/(p−1) → ∞ (data: ~ log p).  E is a fixed-set count: the number of collinear triples of the explicit set
P₋₁ with three distinct classes, summed over all directions (±1 carry 12–15 %, |u|,|v| ≤ 4 about 44 %, hundreds of directions contribute).
Conjecture B (Wigner edge).  λ_min(C_p) ≥ −K·√(tr C_p²/(p−1)) for an absolute K (data: K ≈ 2.4).  Equivalently a trace estimate
tr C^{2k}/(p−1) ≤ (K′ m₂)^k Cat_k for k ≍ log p, i.e. control of closed walks of length 2k in the weighted pattern graph — the deterministic
analogue of the moment method for random matrices, where cancellation must come from equidistribution of collinear patterns.
Theorem (conditional on A and B).  Every vertical-pair 2-factor of P₋₁ contains ≥ (1−o(1))·E(p) ≥ c(p−1) log p collinear triples.
What it would NOT give: T1 (the true optima use singles and mixed pairs, outside the model); a bound on lawful subsets of the model needs
in addition a hitting-set argument (min hitting set ≥ T/Δ with Δ the maximum triple-degree; the exact model optimum is 3(p−1)+O(1) by
data — much better than T/Δ).
Why it matters.  It is the first mechanism that certifies a property "for ALL orientations" without a union bound (which fails, B.12);
the two conjectures are explicit arithmetic statements about one explicit set, checkable numerically to large p.
Tools: `slack/vp_fourier.py` (Walsh structure), `slack/vp_quadratic.py` (E, C, λ_min, spectral bound), `slack/vp_min.py` (exact minima),
`slack/vp_traces.py` (O(p²) construction, moments), notes `docs/research/pair_bound_notes.md` §20, B.14.
