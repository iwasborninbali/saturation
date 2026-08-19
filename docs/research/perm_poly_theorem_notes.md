# G3.7 — permutation polynomials of bounded degree: the ±1-line cover in general (first solver, 2026-08-19)
*Tools: `slack/pp_constant.py` (asymptotic constant from root-count laws), `slack/g35_agents/perm_poly_covers.py` (numerics), logs
`slack/verification/perm_poly_covers.txt`.*

## 1. Setting and the general lift accounting (exact, elementary)
f a permutation polynomial of F_p of fixed degree d ≥ 3, box B = [x₀,x₀+2p) × [y₀,y₀+2p), P = box lift (4p points, 2 per row/column ⇒ rows/columns
useless). Slope σ ∈ {+,−}: residue equation f(t) − σt = c; R_σ(c) its root set, k = |R_σ(c)| ∈ {0,…,d}. Classes exactly as for the cubic
(`permutation_cubic_note.md` §1, §3): with u_t = position of t in the x-window and thresholds θ₊(c) = 1 − g(c), g(c) = ((c − y₀ + x₀) mod p)/p,
θ₋(c) = g′(c) = ((c − x₀ − y₀) mod p)/p, class₊(t) = 0 iff u_t ≥ θ₊, class₋(t) = 0 iff u_t ≤ θ₋; for a residue x the two thresholds are tied:
θ₋(c₋(x)) = g(c₊(x)) + 2u_x (mod 1) [i.e. θ₋ = 1 − θ₊ + 2u_x].
For a residue c with k roots, n₀ of class 0 and n₁ = k − n₀ of class 1, the four consecutive ±1‑lines of the residue carry n₀, k+n₀, k+n₁, n₁ points.
**Lemma (lift accounting).** Let x be a residue, k_σ the root count of its residue on slope σ and n_σ = number of roots of that residue in x's own class
(1 ≤ n_σ ≤ k_σ). Then the sizes of the ±1‑lines through the four lifts (δ,ε) of x are
   (0,0): slope+ k₊+n₊ ; slope− {n₋, 2k₋−n₋}   (1,1): slope+ k₊+n₊ ; slope− {2k₋−n₋, n₋}   (the two values in some order),
   (0,1): slope+ {2k₊−n₊, n₊} ; slope− k₋+n₋   (1,0): slope+ {n₊, 2k₊−n₊} ; slope− k₋+n₋.
(Three lifts of a root lie on the two central lines of its residue, sizes k+n and 2k−n; the fourth, outer, lift lies on a line with n points.)
A lift is uncovered by the cover W₄ := "weight 1 on every ±1‑line with ≥ 4 points, weight 1 on every point on none" iff both its lines have ≤ 3 points, so
   U(x) = [k₊+n₊ ≤ 3]·([n₋ ≤ 3] + [2k₋−n₋ ≤ 3]) + [k₋+n₋ ≤ 3]·([n₊ ≤ 3] + [2k₊−n₊ ≤ 3]),
   L = Σ_σ Σ_c ([n₀ ≥ 4] + [k+n₀ ≥ 4] + [k+n₁ ≥ 4] + [n₁ ≥ 4]),      cost(W₄) = 2L + Σ_x U(x) ≥ α.
For d = 3 this reproduces the cubic bookkeeping (k₊+n₊ ≤ 3 ⇔ k₊ = 1, or k₊ = 2 with a split pair; [n₋≤3]+[2k₋−n₋≤3] = 2 for a same triple, 1 for a split one).

## 2. Local law (hypotheses) and the constant
(H1) root-count laws: #{c : |R_σ(c)| = k} = P_k^σ·p + o(p) (Chebotarev for the Galois closure of f(t) − σt − c over F_p(c); for "generic" f, i.e. Galois group
S_d, P_k = rencontres numbers (1/k!)Σ_{j≤d−k}(−1)^j/j!: d=3: (1/3,1/2,0,1/6); d=4: (3/8,1/3,1/4,0,1/24); d=5: (11/30,3/8,1/6,1/12,0,1/120)).
(H2) positions: for k-root residues the vector (u_{t₁},…,u_{t_k}, θ) is equidistributed on T^{k+1} (Bombieri on the variety of ordered k-tuples of distinct
roots — for S_d it is absolutely irreducible; the box conditions cost the usual log-powers). Consequence: n₀ | k = Bin(k, θ) with θ uniform ⇒ uniform on
{0,…,k}; for a *random member* x of a k-root residue, n_σ = 1 + Bin(k−1, q) with q the probability that a partner shares x's class.
(H3) across the two slopes: root counts independent of each other and of the positions; partner positions of the two slopes independent given (u_x, g)
(fibre product of the two root varieties over the x-line; the counts via Kummer twists as in the cubic case). The thresholds remain tied (θ₋ = 1−θ₊+2u_x).
Caveat: when k = d (all roots rational) and f has no x^{d−1} term, the d positions satisfy one linear relation (Σ roots = 0); this affects only the P_d ≈ 1/d!
part and is ignored in the calculator (exact for d = 3 by the pairwise identity).
**Constant.** Under (H1)–(H3), cost(W₄)/p → C(P⁺,P⁻) := 2·Σ_σ Σ_k P_k^σ·E_{n₀∼U{0..k}}[#rich lines] + ∫∫ E[U(x) | u_x, g] du_x dg,
where in the inner expectation k_σ has the size-biased law k·P_k^σ, n_σ = 1 + Bin(k_σ−1, q_σ) with q₊ = 1−θ₊ if u_x ≥ θ₊ else θ₊, q₋ = θ₋ if u_x ≤ θ₋ else 1−θ₋.
`slack/pp_constant.py` evaluates it (grid quadrature): d = 3 (rencontres): 2.7500 = 11/4 exactly ✓ (independent check of Theorem G3.5);
S₄: 2.828 (1.414 N); S₅: 2.796 (1.398 N); S₇: 2.805 (1.402 N). With the empirical root-count histograms of x⁵ at p = 317: 2.746 (1.373 N) vs the observed
W₄ cost 1.369/1.383 N (two boxes); at p = 233: 1.416 N predicted vs 1.429/1.481 observed (√p‑fluctuations of the class patterns; ~20 three-root residues).
So for every "generic" permutation polynomial the ±1‑cover constant is ≈ 1.40 N, comfortably below 3/2 (margin ≈ 0.1 N), and the theorem
   α(f, B) ≤ (C(P⁺,P⁻) + o(1))·p  for every 2p × 2p box
holds as soon as (H1)–(H3) are established for f — for the S_d case this is Chebotarev + Bombieri on the (irreducible) root varieties and their fibre product.

## 3. Towards a universal statement ("no permutation polynomial of bounded degree beats HJSW")
* If f − x is not a permutation polynomial then, by Wan's theorem, |V(f−x)| ≤ p − (p−1)/d, so at least (p−1)/d residues of slope +1 carry ≥ 2 roots; same-class
  pairs (probability ≥ 1/2 in every local law: 2/3 when c is independent of the pair, 1/2 when c = t₁+t₂ as for the hyperbola) give 4‑point lines with
  positive density ⇒ a saving linear in p from slope +1 alone (and likewise for slope −1). Niederreiter–Robinson (1982): for p large in terms of d there
  are no complete mapping polynomials of degree d ≥ 2 (f and f + x both permutations), so at least one slope always saves — but a *quantitative* universal
  constant needs the equidistribution on the (possibly reducible) pair curve {(t₁,t₂): (g(t₁)−g(t₂))/(t₁−t₂) = 0}, g = f ∓ x: for non-exceptional g it has an
  absolutely irreducible component over F_p (this is the exceptional-polynomial dichotomy), which carries ≥ p/d² pairs and on which the positions
  equidistribute. A universal c_d > 0 therefore looks provable, with a worse constant than the generic 1.40; not written.
* Rational bijections (Möbius maps = shifted hyperbolae, Rédei functions, x^k with gcd(k,p−1)=1 …) fit the same framework; the hyperbola is the unique
  case with no residue-collinear triples and P₂ = 1 (every residue has exactly two roots on both slopes), which is why it sits at 3/2.

## 4. What is left for a theorem G3.7 (division of labour)
(a) Galois groups / root laws for the target families (x^k: Gal(t^k − t − c / F_p(c)); Dickson) — second solver's workflow; (b) numerics of C for x⁵,x⁷ at
p ≤ 1000 vs W₄ — second solver's workflow; (c) statement + proof text for the S_d case (positions equidistribution on the k-tuple varieties and the two-slope
fibre product; Kummer twists for the counts) — first solver, after (a),(b).

## 5. Statement and proof outline for the generic (S_d) case — what exactly has to be checked
**Theorem G3.7 (conditional form).** Let d ≥ 3 be fixed and f ∈ F_p[x] a permutation polynomial of degree d such that, for both g = f − x and g = f + x,
(i) the geometric and arithmetic monodromy groups of the cover t ↦ g(t) (i.e. of g(t) − c over F_p(c)) are both S_d, and (ii) the splitting fields of
g₊(t) − g₊(x) and g₋(t) − g₋(x) over F_p(x) are linearly disjoint (equivalently their Galois closures over the x-line have no common subcover; a
sufficient check: the discriminants disc_t(g₊(t) − g₊(x)) and disc_t(g₋(t) − g₋(x)) are coprime polynomials in x, so already the quadratic subfields differ,
and no non-trivial normal subgroup of S_d other than A_d could give a common quotient). Then for every 2p × 2p box, as p → ∞ (p ∤ 6·d·disc),
   α(f, B) ≤ (C_d + o(1))·p,   C_d = C(rencontres_d, rencontres_d) = 2.750 (d=3), 2.828 (d=4), 2.796 (d=5), 2.805 (d=7), … (all ≤ 2.83 < 3),
with the error term O_d(√p log^{d+1} p). In particular α(f,B) ≤ (1.42 + o(1))·N < (3/2)N.
Examples: f = x^k, gcd(k, p−1) = 1, p ∤ k(k−1): (i) holds since t^k ∓ t has k−1 simple critical points with distinct critical values (monodromy S_k, tame);
(ii) holds since disc(t^k − t − c) ∝ k^k c^{k−1} ± (k−1)^{k−1} evaluated at c = x^k ∓ x gives the polynomials D₊(x) = k^k(x^k − x)^{k−1} − (k−1)^{k−1},
D₋(x) = k^k(x^k + x)^{k−1} + (k−1)^{k−1}, whose resultant is a non-zero integer (sympy: k = 3, 5, 7 — with prime factors < 5000 only {2,3,5}, {2,5,7,97,127},
{2,3,5,7,193,1327}), so for p ∤ Res the two extensions have disjoint finite branch loci; a common subextension would then be unramified over the affine line
and tame at ∞ (degree ≤ d! < p), hence trivial — this is the linear disjointness (ii), for all p ∤ k(k−1)·Res(D₊,D₋).
**Proof outline.** (1) Lift accounting: §1 (exact, all p). (2) (H1) with error O_d(√p): Chebotarev for the S_d-cover, P_k = proportion of permutations
with k fixed points. (3) (H2): the variety V_k of ordered k-tuples of distinct roots of g(t) = c is a curve; by k-transitivity of S_d = geometric monodromy it is
absolutely irreducible for every k ≤ d; the functions t₁,…,t_k, c on V_k admit no linear relation for k < d (the fibre of V_k → V_{k−1} has d−k+1 ≥ 2 points, so
t_k is not a rational function of the others; then induct) and exactly the relation Σt_i = −(coefficient of x^{d−1}) for k = d; Bombieri on V_k plus Fourier
expansion of the k+1 interval conditions gives the counts with error O_d(√p log^{k+1}p) — for k < d the positions and θ = 1 − g(c) are jointly uniform, so
n₀ | k ∼ Bin(k, U) is uniform on {0..k} and a random member sees n = 1 + Bin(k−1, q). (4) (H3): the fibre product W of the +/− root varieties over the x-line is
absolutely irreducible by (ii) (linear disjointness); the joint law of (u_x, g(c₊(x)), partner positions of both slopes) is uniform (Bombieri on W; the tie
θ₋ = 1 − θ₊ + 2u_x is an identity, not a hypothesis) and the root counts (k₊,k₋) are jointly Chebotarev-distributed on the disjoint product, i.e. independent,
and independent of the positions (Kummer/Artin–Schreier twists as in the cubic case). (5) The k = d terms: positions constrained by one linear relation — treat
them separately (a (d−1)-dimensional integral depending on κ = (d·x₀ mod p)/p, hence weakly on the box) or bound crudely: the residues x lying in a d-root
residue of a given slope have density d·P_d = 1/(d−1)!; for such x only the factor [n_σ ≤ 3] in the cross term of U(x) (at most 1 lift-pair) and the two
outer-line indicators [n₀ ≥ 4] + [n₁ ≥ 4] of L can deviate from the i.i.d. computation, so C_d changes by at most 2/(d−1)! + 4·P_d = 2/(d−1)! + 4/d!:
for d = 5 this is 0.083 + 0.033 ≈ 0.12, i.e. C₅ ≤ 2.80 + 0.12 = 2.92 < 3 even with the crude bound; for d ≥ 7 the correction is < 0.01.
Monte-Carlo with the relation built in (`slack/pp_constant_mc.py`, 6·10⁵ samples, κ ∈ {0, 0.3, 0.5, 0.8}): C₅ = 2.7952 ± 0.0005 for every κ, versus 2.7950
without the relation — the k = d effect is invisible at this precision, so C₅ = 2.795 (1.398 N) can be taken as the constant (rigorous version: 2.92). For d = 3 the pairwise identity makes everything exact.
Note d = 4 is vacuous: by Dickson's classification there are no permutation polynomials of degree 4 over F_p for p > 7. ∎ (outline)
Open for the theorem text: the k = d bookkeeping (5) done cleanly; the discriminant coprimality (ii) for x^k; the constant's tabulation with rigorous
quadrature error (the integrand is piecewise polynomial in (u_x, g): exact rational values are computable).

## 6. Numerics for (H1) and (H3) on x^k (`slack/pp_joint_counts.py`)
Root-count laws for t^k ∓ t = c at p = 10007 (k = 5): N₀,…,N₅ / p = 0.367, 0.377, 0.167, 0.080, 0, 0.010 vs rencontres 11/30, 3/8, 1/6, 1/12, 0, 1/120 ✓ (S₅).
Independence of (k₊(x), k₋(x)) over residues x: the counts are constant on orbits of the group {μ : μ^{k−1} = 1} (since t^k − t is homogeneous of degree
1 under t ↦ μt) — e.g. x ↦ −x always, and x ↦ ωx (ω³ = 1) when 3 | p−1 — so a χ² test must count one representative per orbit; doing so:
k = 7: p = 10007 (orbits of size 2): χ² = 7.2 on ≈25 df; p = 30011 (size 2): 23.6; p = 10009, 20011 (3 | p−1, size 6): 109/3 ≈ 36, 40.5/3 ≈ 13.5 — all
consistent with independence; k = 5, p = 10007: χ² = 8.0. Also for k odd and ζ^{k−1} = −1 in F_p (2(k−1) | p−1) the two slopes are conjugate: t^k − t at ζt equals
−ζ(t^k + t), so k₊(ζx) = k₋(x); this does not affect independence at the same x (checked at p = 10009 where 12 | p−1).

## 7. Theorem G3.7 for the monomials x^k — hypotheses verified
**Theorem G3.7 (monomial permutation graphs).** Let k ≥ 3 be odd [k = 3: Theorem G3.5], p a prime with gcd(k, p−1) = 1 (so x ↦ x^k is a bijection),
p ∤ k(k−1)·Res(D₊, D₋), and B any 2p × 2p box. Then α(x^k, B) ≤ (C_k + o(1))·p as p → ∞ (k fixed), where C_k = C(rencontres_k, rencontres_k) is the constant of
§2: C₃ = 11/4, C₅ = 2.795, C₇ = 2.805 (rigorous crude version for the k = d terms: C₅ ≤ 2.92); in particular α(x^k, B) ≤ (1.42 + o(1))·2p < (3/2)·2p.
Hypotheses of §5: (i) monodromy of t ↦ t^k ∓ t: the critical points t^{k−1} = 1/k (k−1 of them, simple) have distinct critical values t_i(1−k)/k, so each finite
branch point contributes a transposition; the polynomial t^k ∓ t − c is irreducible over F̄_p(c) (linear in c), so the group is transitive and generated by
transpositions ⇒ S_k, geometric = arithmetic; (ii) linear disjointness of the two slopes: §5 (coprime discriminant polynomials ⇒ disjoint finite branch loci ⇒
no common tame subextension). The proof is the outline of §5 with the general lift lemma of §1; the constant is the integral of §2, evaluated by
`pp_constant.py` / `pp_constant_mc.py`. What remains is only the write-up (positions equidistribution on the k-tuple curves and on the two-slope fibre product,
with Fourier expansions of the box conditions and Chebotarev with box conditions for the counts).
Same statement, same constants, for every permutation polynomial of degree k whose two covers f ∓ x have S_k monodromy and disjoint finite branch loci
(Dickson D₅(x,a) etc. — to be checked family by family).
