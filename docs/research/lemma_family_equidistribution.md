# Lemma FE (family equidistribution) — the counting input for the W₄ + matching certificate (second solver, 19.08 09:40 WITA)
Context: `cubic_matching_note.md` §3 (first solver). Setting: p ≡ 2 (mod 3) large, f(x) = a x³ (a ≠ 0), box B; a family (i,j) of three-point lines
(0 < i < j, gcd(i,j) = 1, span J ≥ 3) with base residue x₁ ≡ −(i+j)u/3 and residues α_m u (m = 1,2,3), α_m ∈ {−(i+j)/3, (2i−j)/3, (2j−i)/3} ⊂ Q, pairwise
distinct squares α_m² (true for J ≥ 3, i.e. for every family except the centre family (1,2)); direction (u*, v*) with v ≡ c₁u³ + a·u, c₁ = (i²−ij+j²)/3.
For each residue x and each slope σ = ± the partner conic is Q_σ(x): t² + x t + x² − σ/a = 0, discriminant Δ_σ(x) = 4σ/a − 3x²; the two roots (partners) t, t′
satisfy t + t′ = −x.  The "good" status of the three lifted points of a line (all three W₄-uncovered) is a Boolean combination of:
 (i) interval conditions on the least residues of the linear forms α_m u (positions of the residues in the x-window) and of the thresholds
     g_σ(α_m u) = α_m³u³ ∓ α_m u (mod p) (each threshold is an interval condition on the least residue of a POLYNOMIAL in u — g_σ(α_m u) = α_m³ c₀ u³ … but note
     that these polynomials in u are of degree 3 with distinct leading coefficients α_m³ ≠ 0 across m for fixed σ; across σ they differ by the linear term);
 (ii) the memberships [Δ_σ(α_m u) is a nonzero square] (six Legendre symbols χ(Δ_{σ,m}(u)), Δ_{σ,m}(u) = 4σ/a − 3α_m²u²);
 (iii) interval conditions on the least residues of the partner roots t_{σ,m} (and t′_{σ,m} = −α_m u − t_{σ,m}: a linear form in (u, t_{σ,m}));
 (iv) the lift labels (δ_m, ε_m) of the three points, which are determined by the small representatives (u*, v*) and the lifts of the base point — i.e. by
     interval conditions on u* ∈ [−2p/J, 2p/J], on v* (the least residue of v(u) = c₁u³ + au shifted into the box range), and on the residues α_m u.
STATEMENT.  Fix (i,j) with J ≥ 3, and let F be a finite Boolean combination of the conditions (i)–(iv) (a fixed finite union of "boxes" in the variables
u* ∈ I_u (an interval of length ≤ p), the least residue of v(u), the least residues of the linear forms α_m u and of the six roots t_{σ,m} (one per conic, the
other root being −α_m u − t), and the six membership bits).  Then
    #{u ∈ F_p^* : F holds}  =  p·μ(F) + O_{i,j}(√p · log^{c} p),
where μ(F) is the "local law" measure: u* uniform on I_u/p (so the residues α_m u are the DETERMINISTIC functions α_m u* mod p of u*), v* independent uniform,
each membership bit an independent fair coin, and, conditionally on membership, each root t_{σ,m} independent uniform (so the pair (t, −α_m u − t) is a
"line" law given u); c ≤ 16 (the number of interval conditions).  All implied constants depend only on (i,j) (and are uniform in a and in the box).
PROOF.  (1) Algebra.  The six discriminants Δ_{σ,m}(u) = 4σ/a − 3α_m²u² are quadratics in u with root sets {±2/(α_m)·√(σ/(3a))}; for J ≥ 3 the α_m² are pairwise
distinct, so for fixed σ the three root sets are pairwise disjoint; between σ = + and σ = − the root sets could coincide only if α_m² ≡ −α_{m′}² (mod p) — a
congruence on the fixed rationals α_m, α_{m′}, excluded for p large (p ∤ the numerator of α_m² + α_{m′}²).  Hence the six Δ's are pairwise coprime squarefree
polynomials, so their classes in F̄_p(u)^*/(F̄_p(u)^*)² are multiplicatively independent (Kummer): every product of a non-empty subset is a non-square.
Consequently, for every S ⊂ {(σ,m)} the fibre product X_S over the u-line of the conics Q_{σ,m} (σ,m ∈ S) — the curve with function field F̄_p(u, √Δ_s : s ∈ S) —
is absolutely irreducible (degree 2^{|S|} over the u-line), of genus bounded in terms of |S| (Riemann–Hurwitz: ≤ 12 branch points), and its rational points
over a given u ∈ F_p exist iff all Δ_s(u), s ∈ S, are squares (2^{|S|} points, or fewer if some Δ_s(u) = 0 — O(1) values of u).
(2) Reduction to character sums.  Write each membership bit as [χ(Δ_s(u)) = 1] = (1 + χ(Δ_s(u)))/2 (for Δ_s(u) ≠ 0), each non-membership as (1 − χ)/2, and each
interval condition on a least residue as its Fourier series on Z/p (ℓ¹-norm ≤ log p + 3; or Selberg's polynomials).  For a fixed membership pattern with
member set S, the count of u with the pattern and the box conditions equals 2^{−|S|} Σ_{P ∈ X_S(F_p)} Π_{s ∉ S} (1 − χ(Δ_s(u(P))))/2 · Π (interval indicators),
where the roots t_s (s ∈ S) are the coordinates of P and the interval indicators are functions of the least residues of u, v(u), α_m u, t_s, −α_m u − t_s.
Expanding everything, we get sums of the shape
      T(h, S′) = Σ_{P ∈ X_S(F_p)} χ(Π_{s ∈ S′} Δ_s(u)) · e( (h_u u + h_v v(u) + Σ_m h_m α_m u + Σ_{s∈S} (h_s t_s + h′_s(−α_m u − t_s)) ) / p ),
S′ ⊂ complement of S, |h| ≤ H := p^{1/2}, with coefficient masses O(log^{c} p) in total.
(3) The main term.  If S′ = ∅ and the additive linear form is IDENTICALLY zero as a function on X_S, T = |X_S(F_p)| = 2^{|S|}p + O(√p) and the term contributes to
the main term.  The additive form h_u u + h_v v(u) + Σ_m h_m α_m u + Σ_s (h_s − h′_s) t_s − Σ_s h′_s α_{m(s)} u vanishes identically iff h_v = 0 (v(u) = c₁u³ + au
has a genuine cubic term, c₁ ≠ 0 mod p for p large), h_s = h′_s for all s (the square roots √Δ_s, s ∈ S, are linearly independent over F̄_p(u) by (1), so a
non-trivial combination Σ (h_s − h′_s) t_s = ½Σ(h_s−h′_s)√Δ_s + (polynomial in u) is not a polynomial in u), and then the remaining polynomial in u,
(h_u + Σ_m h_m α_m − Σ_s h′_s α_{m(s)})·u, vanishes iff its coefficient is ≡ 0 (mod p).  These are exactly the frequency vectors dual to the LINEAR RELATIONS
of the local law μ(F): the positions of α_m u are the fixed multiples of u, and t′_s = −α_m u − t_s.  Summing the corresponding Fourier coefficients reproduces
p·μ(F) + O(p·H^{−1}·log^c p) (the truncation of the Fourier series at |h| ≤ H costs O(1/H) per interval — with H = √p this is O(√p log^c p)); the independence
of the memberships and of the roots in μ(F) is precisely the statement that no other frequency vector gives a main term.
(4) The error terms.  If S′ ≠ ∅, the multiplicative character χ(Π_{S′}Δ_s) pulled back to X_S is geometrically non-trivial (Π_{S′}Δ_s is not a square in
F̄_p(X_S): its class is independent of those of Δ_s, s ∈ S, by (1)); tensoring with any Artin–Schreier sheaf keeps it non-trivial (coprime orders), so by the
Bombieri–Perel'muter bound (Castro–Moreno explicit form) |T| ≤ C(i,j)√p uniformly in h.  If S′ = ∅ and the additive form is not identically zero on X_S, it is
a non-constant function of bounded degree on the absolutely irreducible curve X_S, and Bombieri's bound gives |T| ≤ C(i,j)√p (the function is not of the
form g^p − g + const for p large, by degree).  Multiplying by the ℓ¹-masses of the Fourier coefficients (O(log p) per interval condition, ≤ 16 conditions) gives
the total error O_{i,j}(√p log^{16} p). ∎
REMARKS.  (a) The lemma is uniform in the box and in a; the constants γ₁(J₀), γ₂(J₀) of `cubic_matching_note.md` are finite sums over families and roles of
integrals of the measure μ(F) of explicit good/pair conditions — piecewise polynomial in u* — computable exactly.  (b) For pairs of good lines sharing a point
(the second moment) the same proof applies to the configuration (family, role, family′, role′): the second line's parameter is u′ = (α_m/α′_{m′})u, its residues
are again fixed multiples of u, and the ten conics (five residues × two slopes; coincidences α = ±α′′ between residues of the two lines are the degenerate
sub-cases with fewer, still coprime, discriminants) give a fibre product X_S of degree 2^{|S|} over the u-line — the same three steps.  (c) The exceptional
primes (p dividing a numerator of α_m² ± α_{m′}², or c₁, or a resultant of two discriminants) are finitely many for each family; the o(1) absorbs them.
