# G3.5 — Permutation cubics do not reach HJSW: α ≤ (11/4 + o(1))·p in every 2p × 2p box
*(first solver, 2026-08-19 ~02:30 UTC; tools `slack/lp_curve.py`, `slack/cube_cover4.py`, `slack/cube_local_law.py`; data `slack/verification/lp_curve.txt`)*

## 0. Statement

Let p ≡ 2 (mod 3) be prime, a ∈ F_p^*, β, γ ∈ F_p, f(x) = a(x+β)³ + γ (by Dickson these are exactly the permutation polynomials of degree 3 over F_p, and for
p ≡ 1 (mod 3) there are none), and let B = [x₀, x₀+2p) × [y₀, y₀+2p) be any 2p × 2p box of integers.  Put
   P = P(f, B) = {(X, Y) ∈ B : Y ≡ f(X) (mod p)},   |P| = 4p,
and α(f, B) = the largest subset of P with no three collinear points.

**Theorem G3.5.**  α(f, B) ≤ 4p − (15/2)·N₃ + O(√p log³ p) = (11/4)·p + O(√p log³ p), where N₃ = #{c ∈ F_p : a t³ − t = c has three distinct roots}
= (p+1)/6 + O(1).  The implied constants are absolute (independent of a, β, γ, x₀, y₀).

**Corollary (no cubic graph beats HJSW).**  For every polynomial f of degree 3 over F_p and every 2p × 2p box, α(f, B) ≤ (11/8 + o(1))·N, N = 2p.
Indeed, if f is not a permutation polynomial, the rows give α ≤ 4·|f(F_p)| ≤ (8/3 + o(1))·p (§8 of `curves_conjecture.md`; |f(F_p)| = (2/3)p + O(√p) in the
S₃ case, (p+2)/3 in the A₃ case), and 8/3 < 11/4; if f is a permutation polynomial, Theorem G3.5 applies.  Since 11/8 < 3/2, no cubic graph reaches the
HJSW value 3(p−1) = (3/2)N − 3 of the hyperbola.

The certificate is explicit and needs only the lines of slopes ±1: weight 1 on every such line with ≥ 4 points of P, weight 1 on every point of P lying on
none of them (singletons).  Its cost is 4p − (15/2)N₃ + O(√p log³ p) — the theorem is the cost computation.  Numerically the LP over all ±1-lines is a little
better (1.32–1.36 N) and the LP over all lines with ≥ 3 points is ≈ 1.10 N (three-point lines, the "families" of §7 of `curves_conjecture.md`); this note proves
only the clean 11/8.

## 1. Reduction and the ±1-line structure (elementary, exact)

Translations x ↦ x + β, y ↦ y + γ move the box, so we may take f(x) = a x³.  Every residue x ∈ F_p has exactly two lifts X ∈ {r_x, r_x + p} in the x-window
(r_x ∈ [x₀, x₀+p)), and y ≡ a x³ has two lifts Y ∈ {s_x, s_x + p} (s_x ∈ [y₀, y₀+p)); the four points of residue x are (r_x + δp, s_x + εp), δ, ε ∈ {0,1}.
Rows and columns carry exactly two points each (f is a bijection), so they never help a cover; a lawful set can contain both.

*Slope +1.*  For the four lifts of x, Y − X ∈ {s_x − r_x (twice: δ = ε), s_x − r_x + p (δ=0, ε=1), s_x − r_x − p (δ=1, ε=0)}, and Y − X ≡ a x³ − x =: c₊(x)
(mod p).  Fix c and let R(c) = {t : a t³ − t = c}, |R(c)| ∈ {0, 1, 3} except for the ≤ 2 values of c with a double root.  The integers s_t − r_t (t ∈ R(c))
lie in the interval (y₀ − x₀ − p, y₀ − x₀ + p) of length 2p, which contains exactly two integers ≡ c: c′ < c′ + p.  Say t has **class 0** if s_t − r_t = c′
and **class 1** if s_t − r_t = c′ + p.  With n₀ roots of class 0 and n₁ of class 1, the four lines Y − X ∈ {c′ − p, c′, c′ + p, c′ + 2p} carry
n₀, 2n₀ + n₁, n₀ + 2n₁, n₁ points.  For |R(c)| = 3 the profiles are (3,6,3,0) or (0,3,6,3) if all roots have the same class (**same**) and (2,5,4,1) or (1,4,5,2)
if they split 2:1 (**split**); for |R(c)| = 1 all lines have ≤ 2 points.  Hence the slope-(+1) lines with ≥ 4 points are exactly: one 6-line per same
3-root residue, one 5-line and one 4-line per split 3-root residue (plus O(1) lines from the ≤ 2 double-root residues).  Which lifts of a root t lie on a
≥4-line: in a same group the two lifts with δ = ε; in a split group all lifts except one — the lift (δ,ε) = (1,0) if t has class 0, the lift (0,1) if t has
class 1 (check: a class-0 root's lifts lie on the lines c′ (2n₀+n₁ ≥ 4), c′+p (n₀+2n₁ ≥ 4), c′−p (n₀ ≤ 2)).

*Slope −1.*  X + Y ∈ {r_x + s_x (δ=ε=0), r_x + s_x + p (twice, mixed), r_x + s_x + 2p} and X + Y ≡ a x³ + x =: c₋(x); the class of a root t of a t³ + t = c
is 0 or 1 according as r_t + s_t = c″ or c″ + p (the two integers ≡ c in [x₀+y₀, x₀+y₀+2p)); the four lines c″, c″+p, c″+2p, c″+3p carry n₀, 2n₀+n₁, n₀+2n₁,
n₁ points — the same profiles.  Lifts of t on ≥4-lines: in a same group the two mixed lifts; in a split group all but (0,0) if t has class 0, all but (1,1) if
class 1.

*Root conics.*  a t³ − t − c has no t²-term, so its three roots satisfy t₁ + t₂ + t₃ = 0 and t₁t₂ + t₁t₃ + t₂t₃ = −1/a; eliminating t₃: (t₁, t₂) lies on the
conic Q₊ : t₁² + t₁t₂ + t₂² = 1/a.  Likewise for a t³ + t − c: Q₋ : t₁² + t₁t₂ + t₂² = −1/a.  The form t₁² + t₁t₂ + t₂² is the norm form of F_{p²}/F_p when
p ≡ 2 (mod 3) (its discriminant −3 is a non-residue), so |Q_±(F_p)| = p + 1, and every 3-root residue c corresponds to exactly six ordered pairs of distinct
roots; the ≤ 6 conic points with a repeated coordinate come from double roots.  Hence N₃^± = (p + 1 − r_±)/6 with r_± ∈ {0, 6}, and the number of residues x
that are roots of some 3-root c is 3N₃^± = (p+1)/2 + O(1) — for each slope, "half" of the residues.  Membership: x is such a root for slope + iff the
partner quadratic t² + x t + x² − 1/a = 0 has two distinct roots iff Δ₊(x) = 4/a − 3x² is a non-zero square; for slope − iff Δ₋(x) = −4/a − 3x² is.

## 2. The cover and its exact cost

Weight 1 on every ±1-line with ≥ 4 points, weight 1 on every point on none of them.  If S is lawful, |S| ≤ Σ_ℓ w_ℓ |S ∩ ℓ| + Σ_P z_P ≤ 2L₄ + U, where L₄ is
the number of weighted lines and U the number of singleton points.  By §1:
   L₄ = Σ_σ (A^σ + 2S^σ),   A^σ + S^σ = N₃^σ   (A = same, S = split groups of slope σ),
and, per residue x with membership indicators m₊(x), m₋(x): the lifts (0,0), (1,1) are covered by slope + whenever m₊(x) (they are never the exceptional lift),
and by slope − iff m₋(x) ∧ split₋(x) ∧ [class₋(x) = 1 resp. 0]; the mixed lifts are covered by slope − whenever m₋(x), and by slope + iff m₊ ∧ split₊ ∧
[class₊(x) = 0 resp. 1].  Summing over the two lifts of each kind (exactly one of the two is rescued when the other slope is split):
   U = Σ_x { [¬m₊(x)]·(2 − [m₋ ∧ split₋](x)) + [¬m₋(x)]·(2 − [m₊ ∧ split₊](x)) }.
Everything is now a matter of counting: N₃^σ, S^σ, and the two cross sums Σ_x [¬m₊][m₋ ∧ split₋], Σ_x [¬m₋][m₊ ∧ split₊].

## 3. The local law and the counts

*Classes as box conditions.*  Let u_t = (r_t − x₀)/p ∈ [0,1) be the position of the residue t in the x-window and g = ((c − y₀ + x₀) mod p)/p the position of
c.  For a root t of a t³ − t = c: s_t − r_t = (y₀ − x₀) + p·(v_t − u_t) with v_t = (s_t − y₀)/p, and v_t − u_t ≡ g (mod 1); so s_t − r_t = c′ iff v_t < u_t iff
u_t + g ≥ 1.  Thus  **class₊(t) = [u_t ≥ 1 − g]** — all roots of the same c are compared with the same threshold θ = 1 − g.  For slope −1 the same computation gives
class₋(t) = [u_t > g′] with g′ = ((c − x₀ − y₀) mod p)/p.  For a residue x the two thresholds are tied: g′(c₋(x)) − g(c₊(x)) ≡ (c₋ − c₊ − 2x₀)/p = 2u_x (mod 1).

*Equidistribution on the conic (Weil, genus 0).*  Over the six-fold cover "ordered root pairs" (t₁, t₂) ∈ Q₊(F_p), the vector (u_{t₁}, u_{t₂}, g) ∈ T³ is
equidistributed with error O(√p) per Fourier coefficient: for (h₁, h₂, h₃) ≠ 0 the function h₁t₁ + h₂t₂ + h₃(a t₁³ − t₁) is non-constant on Q₊ (if h₃ ≠ 0 it has
a cubic term in t₁ and t₂ is not a polynomial in t₁ on a conic; if h₃ = 0 a line meets a conic in ≤ 2 points), so Σ_{Q₊(F_p)} e(F/p) = O(√p) by Weil's bound
for rational functions of bounded degree on P¹.  Box indicators are expanded in Fourier series with ℓ¹-norm O(log p) each (or Selberg polynomials), giving
error O(√p log³ p) for the count of any box condition in (u_{t₁}, u_{t₂}, θ).  The third root has u_{t₃} = −u_{t₁} − u_{t₂} − κ (mod 1), κ = (3x₀ mod p)/p — a
deterministic function; only the pairs (u_{t_i}, u_{t_j}, θ) matter below, and any two of the three roots are two coordinates of a point of Q₊ (up to
reordering), hence equidistributed with θ.

*The split count.*  With A_i = [u_{t_i} < θ], the indicator of "same" is [all ≥ θ] + [all < θ] = (1 − ΣA_i + Σ_{i<j}A_iA_j − A₁A₂A₃) + A₁A₂A₃ =
1 − Σ_i A_i + Σ_{i<j} A_iA_j: **the triple term cancels**, so only pairwise data enter.  Summing over the 3-root residues c and using the equidistribution of
(u_{t_i}, θ) and (u_{t_i}, u_{t_j}, θ): #same = N₃·(1 − 3·E[θ] + 3·E[θ²]) + O(√p log³ p) = N₃·(1 − 3/2 + 1) = N₃/2 + O(√p log³ p).  Hence
   A^σ = S^σ = N₃^σ/2 + O(√p log³ p)   for both slopes, for every box (no dependence on κ, x₀, y₀).

*The cross sums.*  Σ_x [¬m₊(x)][m₋ ∧ split₋](x): write [¬m₊] = (1 − χ(Δ₊(x)))/2 for Δ₊(x) ≠ 0 (χ = Legendre symbol) and [split₋] = Σ_i A_i − Σ_{i<j} A_iA_j (from
the identity above), where the A's are box conditions on the roots of a t³ + t = c₋(x), i.e. on points of Q₋; the term with χ is a sum over Q₋(F_p) of a
multiplicative character of Δ₊(t₁) = 4/a − 3t₁² times additive characters of (t₁, t₂, c₋).  The Kummer sheaf of χ(Δ₊) on Q₋ is geometrically non-trivial
(Δ₊ has simple zeros at the four points of Q₋ over t₁ = ±√(4/(3a)), which are unramified for the projection to t₁ since Q₋ ramifies over t₁² = −4/(3a) ≠ 4/(3a)),
so by Bombieri–Perel'muter (as in the arc lemma, `arc_imbalance_lemma.md`) every such mixed sum is O(√p) irrespective of the additive part; therefore
   Σ_x [¬m₊][m₋ ∧ split₋] = ½ · Σ_x [m₋ ∧ split₋] + O(√p log³ p) = ½ · 3S⁻ + O(√p log³ p),
and symmetrically for the other cross sum.  (Alternatively: the same identity holds on the genus-1 fibre product Q₊ ×_x Q₋ used to describe both memberships.)

*Assembly.*  Σ_x [¬m_σ] = p − 3N₃^σ + O(1).  So
   U = Σ_σ [ 2(p − 3N₃^σ) − (3/2)·S^{σ̄} ] + O(√p log³ p) = 4p − 6(N₃⁺ + N₃⁻) − (3/4)(N₃⁺ + N₃⁻) + O(√p log³ p),
   2L₄ = 2Σ_σ (N₃^σ + S^σ) = 3(N₃⁺ + N₃⁻) + O(√p log³ p),
   cost = 2L₄ + U = 4p − (15/4)(N₃⁺ + N₃⁻) + O(√p log³ p) = 4p − (15/2)·N₃ + O(√p log³ p) = (11/4)·p + O(√p log³ p),
using N₃⁺, N₃⁻ = (p+1)/6 + O(1).  ∎

## 4. Numerics (`slack/cube_cover4.py`; cost of the explicit cover; prediction 4p − 7.5·N₃ with N₃ = (p+1)/6)

p = 197 (N₃ = 33, prediction 540.5): boxes (0,0), (−98,0), (−98,−98), (79,−190), (−130,−114): cost 544, 540, 532, 539, 534  (1.35–1.38 N).
p = 293 (N₃ = 49, prediction 804.5): a = 1: 798, 796, 798, 797, 799; a = 7: 804, 820, 810  (1.36–1.40 N).
p = 401 (N₃ = 67, prediction 1101.5): 1104, 1112, 1100, 1108, 1105  (1.37–1.39 N).
Fluctuations are O(√p) as they should be.  Same/split proportions: #6-lines ≈ #5-lines = #4-lines per slope (e.g. p = 401, box (0,0): 71 six-lines vs 63+63)
— the exact ½ of §3.  The LP over all ±1-lines (fractional weights, also on 3-lines): 1.317, 1.313, 1.323, 1.355 N at p = 101, 131, 167, 197 (box (0,0));
over all lines with ≥ 3 points: 1.098, 1.108, 1.098, 1.107 N.  Monte-Carlo of the local law (`cube_local_law.py`, all κ): P_same = 0.500 ± 0.001, doubly
covered lifts per member residue = 1.000 ± 0.001, in agreement with the exact identities of §3.

## 5. Remarks

1. The constant 11/8 is what THIS cover gives; the LP over ±1-lines suggests ≈ 1.33–1.36 (weights on 3-lines and fractional sharing) and the LP with all
   lines ≈ 1.10 (the three-point lines of §7 of `curves_conjecture.md`).  The strong form of G3 (4/3, or ≈ 1.1) needs the 3-line families.
2. The same method applies verbatim to any fixed permutation polynomial f (or algebraic bijection): rows/columns are useless, the ±1-lines are organised by
   the residues of f(x) ∓ x, the profiles are determined by the class pattern of the roots, and the local law lives on the (bounded-genus) root varieties of
   f(t) ∓ t = c — the constant is an explicit function of the root-count distribution (Chebotarev) and comes out with the same pairwise-only computation.
   For the hyperbola x ↦ 1/x the analogous count gives 3(p−1) exactly (two roots per residue, profiles (4,2,2)/(1,3,3,1)); for x³ the third root is what
   pushes the constant below 3/2.
3. Only pairwise equidistribution enters (the triple term cancels in "same", and the double-coverage sums are complementary), which is why the answer is
   box-independent and needs no fibre products beyond a Kummer twist; the O(√p log³ p) is the usual Fourier/Selberg loss and could be reduced to O(√p log p).
