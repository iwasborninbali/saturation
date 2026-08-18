# The model theorem, conditionally: what is proved, what is assumed (2026-08-19, second solver; sources in pair_bound_notes.md)

**Setting.**  p odd prime; P₋₁ = (H(1)∪H(−1)) ∩ G(p); vertical-pair model S(r), r ∈ {0,1}^{p−1}; T(r) = # collinear triples of S(r).

**Theorem (conditional on CH).**  There is c > 0 such that for all large p and every orientation r,  T(r) ≥ c·(p−1)·log log p.
Consequently every lawful subset of every S(r) misses at least T(r)/Δ_r points, Δ_r = max triple-degree in S(r).

**Proof structure — every step with its status.**
1. [PROVED, §20 + THREAD 82]  T(ε) = E + εᵀCε with ε_a = (−1)^{r_a}; E = |Π|/8, C = (1/16)(Σ_π s_π s_πᵀ − D).  (R′-symmetry kills odd degrees.)
2. [TRIVIAL]  min_r T(r) ≥ E + (p−1)·λ_min(C).
3. [PROVED modulo Lemma K, B.17 + §22]  E ≥ c₁ (p−1) log log p:  Lemma K (Kloosterman count per coprime present family with all integer steps D,
   box lift, distinct classes, injectivity) + B.17 (square scales are never empty: NR·NR = QR and multiplicative energy of Gaussian integers).
   Lemma K rests on the classical estimate #{(u,v) ∈ [−L,L]²: uv ≡ w} = (2L+1)²/p + O(√p log²p) [Kloosterman; IK / Shparlinski].
4. [PROVED, B.17 remark]  m₂ := tr C²/(p−1) ≤ K₀·E/(p−1) (codegree of a class pair ≤ 384), so √m₂ = O(√(E/(p−1))) = o(E/(p−1)).
5. [ASSUMED — Conjecture B / CH_δ]  λ_min(C_p) ≥ −K·√m₂ for an absolute K.  Numerically K ≈ 2 (edge inside the semicircle): λ_min(C)/√m₂ = −1.94, −1.87, −1.94, −2.01, −2.08 at p = 199, 499, 997, 1999, 4001
   (§23; `slack/vp_lines.c`, `vp_circulant.py`); the spectral bound (E+(p−1)λ_min)/(p−1) = 8.3, 8.5, 10.0, 14.5, 15.3 — positive and growing.  Trace-method reduction (B.16): doubled trees give the main term Cat_k·Σ_a rn_a^{2k}; the needed input is CH_δ = power-saving
   cancellation of the signed sums over closed walk shapes of positive cyclomatic number (4-cycles cancel to Wigner level p^{−0.9} in data);
   with CH_δ, tr C^{2k} ≤ (1+o(1))Cat_k Σ_a rn_a^{2k} for k ≤ p^{δ/3−ε}, whence max|λ| ≤ 2 max_a rn_a (1+o(1)) ≤ 2.6√m₂.
6. [1–5 ⇒ theorem]  T(r) ≥ E − K(p−1)√m₂ ≥ E − K′(p−1)√(E/(p−1)) = E(1 − o(1)) ≥ c(p−1) log log p.

**What the theorem would and would not say.**  It certifies, for every orientation, linearly many (in fact ≫ p log log p) collinear triples —
the first uniform statement about the model that does not go through a union bound.  It does not give T1 (singles/mixed pairs are outside
the model), and the deletion bound T/Δ is weak (Δ ~ log p?); the exact model optimum 3(p−1)+O(1) (data) is far stronger.

**Open input (the whole difficulty):** CH_δ.  Precise formulation and the torus-line description of closed walks: B.16 addendum; the split C = C̄ + C̃
(B.18) and the scale accounting of §23 show that BOTH parts need cancellation of two-dimensional character sums over the family disc at scales
below p^{1/4} — outside the Burgess range; this is why the theorem stays conditional.
**Strong form of A (E ≫ p log p):** Burgess-type QR-density among small sums of two squares (deep-research brief 7); not needed for the theorem.
