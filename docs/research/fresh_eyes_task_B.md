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

## Refinement (third solver, 2026-08-18 21:20 UTC): the two sub-problems that together give λ_min(C) ≥ −(1−c)·E/(p−1)

Write b/a = μ ∈ F_p^* for a pair of residues; every entry of C lives on such a "multiplier": C_{a,μa} = w_μ(a).  Split
   C = C̄ + C̃,   C̄_{a,μa} := w̄_μ = (1/(p−1)) Σ_a w_μ(a)  (a circulant on the cyclic group F_p^*),   C̃ := C − C̄  (mean zero along every μ).
Facts (numerical, p ≤ 199): C̄ carries ~10 % of ‖C‖_F², its operator norm max_ψ|Σ_μ w̄_μ ψ(μ)| (ψ = multiplicative characters) is
(0.20–0.35)·E/(p−1), and behaves like a random circulant (max ≈ √(2 log p) × rms); C̃ is Wigner-like: λ_min(C̃) ≈ −2.1·√(tr C̃²/(p−1)),
its 4-cycle sums cancel to level ~1/p.  Since εᵀCε ≥ −(p−1)(‖C̄‖ + ‖C̃‖), it suffices to prove:
 (β′)  ‖C̄‖_op ≤ (1−c)·E/(p−1)  — a character-sum statement: the weights w̄_μ are explicit sums over "slots" (F = (s₁,s₂), e, root z, positions t,t′)
       with μ = (z_F+t)/(z_F+t′), z_F a root of z² + (s₁+s₂)z + s₁s₂/2 (mod p), weight ≍ (s₁+s₂)⁻², sign = hyperbola-position parity times the
       mean of a half-box indicator; needed: |Σ_slots (±w) ψ(μ_slot)| ≤ K √(log p) · (Σ_slots w²)^{1/2} for every ψ ≠ 1 (numerically true; the
       trivial triangle bound gives a per-family ratio (2s₁+s₂)/(s₁+s₂) ≥ 1, i.e. is NOT enough — cancellation across slots is essential);
 (α′)  ‖C̃‖_op = o(E/(p−1))  — the Wigner statement for a zero-mean geometric matrix: in the trace expansion, closed walks are lattice-rule sums
       Σ_{u ∈ F_p^*} Π_j f_j(X(λ_j u)) (X = least residue, f_j = interval indicators / their centred versions); for closed-walk types without small
       integer relations among the λ_j the main term vanishes (product of independent centred functions), the remainder is discrepancy
       (Erdős–Turán–Koksma); the work is counting the types WITH small relations (structured: same line, rational z_F, commutator walks) uniformly.
Either statement alone would be a real result; both together give the model theorem  min_r T(r) ≥ c·E(p) ≥ c′(p−1) log log p.
