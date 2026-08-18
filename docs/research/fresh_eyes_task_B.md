# A concrete matrix problem for a fresh mind (self-contained)

Let p be an odd prime.  For every pair (s₁, s₂) of positive integers with s₁²+s₂² a quadratic residue mod p, and every e ∈ {±1}, consider the
"quadruple patterns" q, q+s₁D, q+s₂D, q+(s₁+s₂)D  in the integer plane, where D = (u,v) is a primitive integer vector with uv ≡ 2e/(s₁s₂)
(mod p) and q = (x,y) satisfies xy ≡ e (mod p), (x/u)² + (s₁+s₂)(x/u) + s₁s₂/2 ≡ 0 (mod p); the four points then satisfy
(x+t u)(y+t v) ≡ e, −e, −e, e (mod p) for t = 0, s₁, s₂, s₁+s₂.  Restrict to the patterns whose points lie in the box
B = [−(p−1)/2, (3p−1)/2] × [0, 2p−1] and take all sub-triples π with three distinct residue classes.  For each residue a ∈ {1,…,p−1} let ε_a ∈ {±1}
be a free sign; each triple π defines a sign vector s_π ∈ {±1}³ on the three residues (x-coordinates mod p) of its points (rule: a point in the
"left" copy of its class gets +1, in the "right" copy −1, reversed for the second hyperbola).  Define the symmetric (p−1)×(p−1) matrix
   C = (1/16) Σ_π ( s_π s_πᵀ − diag(s_π s_πᵀ) )       (i.e. the off-diagonal part of a Gram matrix of ±1 vectors of support 3).
Numerical facts (all p ≤ 199): C is dense (≈ (p−1)/2 nonzeros per row), entries in (1/8)Z with |c| ≤ 1.75; m₂ := tr C²/(p−1) ≈ 5.4 log p − 11;
the normalised moments tr C⁴/((p−1)m₂²) ∈ [2.0, 2.6] and tr C⁶/((p−1)m₂³) ∈ [5, 10] (semicircle: 2 and 5); λ_min(C) ≈ −2.4√m₂ − 2.1 and
λ_max ≈ +2.4√m₂ (never below −9 for p ≤ 199).
Question.  Prove λ_min(C_p) ≥ −K·√m₂ (or ≥ −K·√(log p)) for an absolute K and all p.  Suggested route: trace method
tr C^{2k} ≤ (p−1)(K′ m₂)^k Cat_k for k ≍ log p, i.e. show that closed walks of length 2k in the weighted "pattern graph" are dominated by
tree-like (backtracking) walks — the arithmetic input being the equidistribution of the directions D on the hyperbolas uv ≡ 2e/(s₁s₂) and of the
base points q (Weil/Kloosterman-type cancellation for the non-backtracking walks).  Any partial result (e.g. λ_min ≥ −K·m₂^{3/4}, or the bound
under a "generic position" hypothesis on the patterns) is useful.  Deliver: statement + proof, or the precise obstruction.
