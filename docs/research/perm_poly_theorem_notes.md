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
