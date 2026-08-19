# Local law of the family-(1,3) three-point lines and the constants γ₁, γ₂ (specification for the computation)
*(first solver, 2026-08-19; companion of `cubic_matching_note.md`; ground truth from `slack/cube_matching_fast.py`)*

Setting: f(x) = a·x³ (a ∈ F_p^*, p ≡ 2 mod 3 large), box B = [x₀,x₀+2p)×[y₀,y₀+2p), lifted points (X,Y): X ∈ {r_x, r_x+p}, Y ∈ {s_x, s_x+p},
r_x = x₀ + ((x−x₀) mod p), s_x = y₀ + ((f(x)−y₀) mod p).  Positions: pos(x) = ((x−x₀) mod p)/p ∈ [0,1).  All "mod 1" arithmetic below is on positions.

## 1. The lines of family (1,3)
A line is (u ∈ F_p^*, lift (δ₁,ε₁) of x₁, integer representatives u*, v*) with points P₁ = (X₁,Y₁), P₂ = P₁ + (u*,v*), P₃ = P₁ + 3(u*,v*), where
   z := 3⁻¹u (mod p),  x₁ = −4z,  x₂ = −z,  x₃ = 5z  (mod p)   [a_m = (−4, −1, 5)],   v ≡ f(x₂) − f(x₁) (mod p),
X₁ = r_{x₁} + δ₁p, Y₁ = s_{x₁} + ε₁p, u* ≡ u, v* ≡ v (mod p), and P₂, P₃ ∈ B (this forces |u*|, |v*| < 2p/3 and determines the lifts
δ₂ = (X₁+u*−r_{x₂})/p, ε₂ = (Y₁+v*−s_{x₂})/p, δ₃ = (X₁+3u*−r_{x₃})/p, ε₃ = (Y₁+3v*−s_{x₃})/p ∈ {0,1}).  Each geometric line arises from exactly one such
datum (u is the direction residue; the base point is the end of the line whose next point is at distance one step).  Excluded: directions of slope
0, ∞, ±1 (u* = 0, v* = 0, |u*| = |v*|) — measure zero asymptotically.
Parametrisation of the local law: s := u*/p ∈ (−2/3, 2/3) (continuous), and w′ := (a·z³ mod p)/p ∈ [0,1) (uniform, asymptotically independent of s and of
everything else — Weil in boxes for (u*, a u*³/27); this is the second solver's Lemma G3.3).  Given (s, w′) and the residue class ρ := u* mod 3
(uniform on {0,1,2}, independent): z = (u* + r p)/3 with r ≡ ρ (mod 3) [p ≡ 2 mod 3 ⇒ 3 | u* + rp iff r ≡ u* mod 3], i.e. z/p = (s + r)/3 as a real number,
   pos(x_m) = frac(a_m (s+r)/3 − x₀/p),      F_m := (f(x_m) mod p)/p = frac(a_m³ w′)      (a_m³ = −64, −1, 125),
   thresholds: θ₊(x_m) = 1 − frac(F_m − pos(x_m) − (y₀−x₀)/p),   θ₋(x_m) = frac(F_m + pos(x_m) − (x₀+y₀)/p),
   v/p = frac(F₂ − F₁) = frac(63 w′);  Y₁/p = y₀/p + frac(F₁ − y₀/p) + ε₁;  X₁/p = x₀/p + pos(x₁) + δ₁;
   admissible v*: v*/p ∈ frac(63w′) + Z with (Y₁+v*)/p, (Y₁+3v*)/p ∈ [y₀/p, y₀/p+2);  admissible u*: (X₁+u*)/p, (X₁+3u*)/p ∈ [x₀/p, x₀/p+2);
   ε₂ = ⌊(Y₁+v*)/p − y₀/p − frac(F₂−y₀/p)⌋, ε₃ likewise with 3v* and F₃; δ₂, δ₃ likewise with pos.
Density: the number of lines with (s, w′) in a small rectangle ds·dw′ and given (δ₁,ε₁,ρ, representative choices) is p·(ds·dw′/3)·[admissible] (1+o(1)):
   γ₁ = Σ_{δ₁,ε₁∈{0,1}} Σ_{ρ∈{0,1,2}} ∫ ds ∫ dw′ (1/3) Σ_{admissible v*} Π_{m=1}^{3} U(pos(x_m), θ₊(x_m), θ₋(x_m), δ_m, ε_m).
(Check: dropping the good condition should reproduce #lines(1,3)/p ≈ 1.73–1.81 (box-dependent).)

## 2. The per-residue uncovered probability U(π, θ₊, θ₋, δ, ε)
Independent data of a residue x (position π): slope +: coin E₊ (partners exist iff Δ₊ = 4/a − 3x² is a non-zero square: probability ½), partner positions
τ (uniform) and frac(−π − τ − 3x₀/p) [t₂ + t₃ = −x]; slope −: coin E₋ (Δ₋ = −4/a − 3x²: ½), τ′ uniform and frac(−π − τ′ − 3x₀/p).  Classes: on slope +,
class(t) = 1 iff pos(t) < θ₊ (class 0 iff ≥ θ₊); on slope −, class(t) = 0 iff pos(t) ≤ θ₋.  k₊ = 3 if E₊ else 1; n₊ = 1 + #{partners with the class of x}
(n₊ = 1 if k₊ = 1); a := class₊(x); similarly k₋, n₋, b := class₋(x).  Line sizes through the lift (δ,ε):
   slope +: δ=ε: k₊+n₊;  (0,1): a=0 → 2k₊−n₊, a=1 → n₊;  (1,0): a=0 → n₊, a=1 → 2k₊−n₊.
   slope −: (0,0): b=0 → n₋, b=1 → 2k₋−n₋;  (1,1): b=0 → 2k₋−n₋, b=1 → n₋;  (0,1),(1,0): k₋+n₋.
Uncovered iff both sizes ≤ 3.  U is the probability over (E₊, τ, E₋, τ′): a piecewise polynomial (degree ≤ 2 in each threshold) — derive it in closed
form (cases by π vs θ₊, θ₋ and by the two thresholds' positions relative to π and to each other), or evaluate by exact 1‑D integration in τ, τ′.
Validation: at p ≈ 10⁴ tabulate, for residues x binned by (π, θ₊, θ₋) and by (δ,ε), the empirical uncovered frequency, and compare with U.

## 3. Pairs (γ₂): configurations of two family-(1,3) lines sharing a point
Roles m (of the shared point on line 1) and m′ (on line 2), m ≠ m′: u′ = (a_m/a_{m′})·u, i.e. z′ = (a_m/a_{m′}) z; the six configurations
(m,m′) ∈ {(1,2): z′=4z, (1,3): z′=−4z/5, (2,1): z′=z/4, (2,3): z′=−z/5, (3,1): z′=−5z/4, (3,2): z′=−5z}; line 2 has residues a_n z′ (n = 1,2,3), the same
lift of the shared point, its own (u′*, v′*) with the box constraints, and w″ = (a z′³ mod p)/p = frac((a_m/a_{m′})³ w′) — for the fractional ratios the
division by 4 or 5 mod p introduces the fine residue of z modulo 4 or 5 (uniform, independent), exactly as ρ above.  The five residues (shared one and two
others per line) have pairwise distinct |a| (checked in `cubic_matching_note.md`), so their partner data are independent: P(both lines good) =
Π over the five residues of U(·) with the shared residue's lift counted once.  γ₂ = Σ_{configurations} ∫∫ (density) Π U.  Validation: empirical pair counts
0.021–0.035 p (boxes at p = 3203), 0.028 p (p = 12809, box (0,0)).

## 4. Target
γ₁ ≈ 0.128–0.144 (boxes), γ₂ ≈ 0.02–0.035, γ₁ − γ₂ ≈ 0.107–0.110 > 1/12 = 0.0833 for every box tested; the theorem needs a rigorous
γ₁ − γ₂ > 1/12 uniformly in (x₀/p, y₀/p) — evaluate on a grid of box positions with error control (the integrands are piecewise polynomial in (s, w′)).
