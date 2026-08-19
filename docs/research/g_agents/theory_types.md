# theory_types — the interval condition and limiting densities for the ±1-line residue groups of y = x³

Agent: `theory_types` (workflow `perm-cubic-cover-G35`). Code: `slack/g_agents/theory_types.py`
(self-contained, no numpy/scipy; `/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/theory_types.py`
runs everything below in **≈2 seconds**). Task: derive, from first principles, the exact combinatorial
condition that splits a 3-root residue class of x³±x≡c into the "(3,6,3)" vs "{1,2,4,5}" line-pattern
shapes (background's KEY STRUCTURE paragraph), identify the curve that governs the equidistribution of
this condition and the Bombieri-type estimate that applies to it, and compute the limiting densities —
then spot-check at p = 401, 797.

**Headline result**: the shift-bit of a root is simply "is the root's least residue above or below c's own
least residue" (Part 1) — an exact, assumption-free fact. The relevant curve is the plane conic
`x₁²+x₁x₂+x₂² = ∓1` (Vieta for x³±x−c, x₃=−x₁−x₂), which is absolutely irreducible with the **exact**
point count `p+1` for every prime `p ≡ 2 (mod 3)` (Part 2). Under the stated equidistribution (justified via
a Bombieri-type bound on this curve for a fourth "coordinate" tracking c, Part 3), the four sub-types
`k=0,1,2,3` (k = number of roots below c) are **exactly equidistributed, 1/4 each** (Part 4) — i.e. shape
`(3,6,3)` has density **1/2** and shape `{1,2,4,5}` (in its two mirror sub-shapes) has density **1/4 + 1/4**,
for *both* slopes. This resolves, with a closed form and a mechanism, the "(0.5, 0.25, 0.25), rank
exchangeability" pattern the companion agent `group_types` found numerically but flagged unproved.

## 0. Setup recap (from the task brief)

`p` prime, `p≡2 (mod 3)` so `f(x)=x³` permutes `F_p`. Box `[0,2p)²`, curve lift `Y≡X³ (mod p)`. For the
slope-(−1) lines (antidiagonals `X+Y=const`), a residue class `c` with 3 roots `x₁,x₂,x₃` of `x³+x≡c` gives
a "residue group" of 4 consecutive antidiagonals `c₀,c₀+p,c₀+2p,c₀+3p` (`c₀ = c mod p ∈[0,p)`) whose point
counts depend on how many roots' lifted sum "wraps"; task background states the two possible shapes are
`(3,6,3)` (all three roots agree) and `(2,5,4,1)`/`(1,4,5,2)` (two-and-one). Symmetric story for slope +1
(diagonals `X−Y=const`, roots of `x³−x≡c`).

## 1. The exact shift-bit / interval condition

**Slope −1 (antidiagonal).** Let `x` be a root of `x³+x≡c`, `y=x³ mod p`, and write least residues
`X(x),X(y)∈[0,p)`. Since `x` is *by definition* a root, `x³≡c−x (mod p)`, i.e. `y≡c−x`. Hence
`X(y) = c₀−X(x)` if `X(x)≤c₀`, else `X(y) = c₀−X(x)+p`. Therefore the **integer** sum
`s := X(x)+X(y)` (which is what decides which antidiagonal a lift lands on) is exactly:

```
X(x) ≤ c₀  ⟹  X(y) = c₀−X(x)         ⟹  s = c₀            (no wrap, "shift bit" 0)
X(x) >  c₀ ⟹  X(y) = c₀−X(x)+p       ⟹  s = c₀+p          (wrap, "shift bit" 1)
```

So **the shift bit of a root is simply `[X(x) > c₀]`** — no reference to `X(x³)` needed once the
substitution `x³≡c−x` is used; the least residue of the *root itself*, compared to the least residue of
`c`, decides everything. (This is the same fact used differently by `group_types`, whose definition
`b_i=1 iff x_i+y_i≥p` is verified identical — see `slack/g_agents/theory_types.py:classify_class`, which
reproduces their k-histograms and shapes exactly, §6 below.)

Each root with bit 0 contributes point-counts `(1,2,1,0)` to the 4 lines `(c₀,c₀+p,c₀+2p,c₀+3p)`; bit 1
contributes `(0,1,2,1)` (direct count of the 4 lifts `X∈{X(x),X(x)+p}, Y∈{X(y),X(y)+p}` by `X+Y`). With
`k := #{i : bit_i=0} = #{i : X(x_i) ≤ c₀} ∈{0,1,2,3}`, summing the 3 roots' contributions gives **exactly**

```
sizes(c₀, c₀+p, c₀+2p, c₀+3p) = (k, k+3, 6−k, 3−k)
```

`k∈{0,3}` ⟹ one zero entry, shape `(3,6,3)`; `k∈{1,2}` ⟹ shape `{1,2,4,5}` (mirror images `(1,4,5,2)` /
`(2,5,4,1)`). **This is the exact combinatorial derivation of the task's stated shapes** — no assumption
used yet.

**The interval/polytope condition.** Sort the roots' least residues `X_{(1)}≤X_{(2)}≤X_{(3)}`. Then

```
k=3  ⟺  c₀ ≥ X_{(3)}         k=0  ⟺  c₀ < X_{(1)}          }  Type A  (3,6,3)
k=2  ⟺  X_{(2)} ≤ c₀ < X_{(3)}   k=1  ⟺  X_{(1)} ≤ c₀ < X_{(2)}  }  Type B  {1,2,4,5}
```

i.e. **Type B ⟺ c₀ falls in the half-open interval `[X_{(1)}, X_{(3)})` spanned by the min and max of the
three roots' least residues; Type A ⟺ c₀ falls outside it.** This is exactly the "interval condition on
the least residues of the three roots [and c]" the task asks for — a single real interval per class, no
further case-work, and it needs no equidistribution assumption to be *exact* (only the *density* of Type
A/B over all `c` needs the equidistribution argument of Parts 2–4).

**Slope +1 (diagonal), by the same computation.** For `x³−x≡c`, `x³≡c+x`, so
`X(y)=c₀+X(x)` if `<p`, else `c₀+X(x)−p`. The integer *difference* `X(x)−X(y)` is `−c₀` (needs a `+p`
shift, bit 1) when `X(x)<p−c₀=:d₀`, and `p−c₀=d₀` directly (bit 0, no shift) when `X(x)≥d₀`. So
**the diagonal shift bit is `[X(x) < d₀]`, `d₀:=p−c₀`** — the mirror threshold. The same `(k,k+3,6−k,3−k)`
formula and interval condition hold verbatim with `c₀` replaced by `d₀=p−c₀` (`k=#{X(x_i)≥d₀}`).
Since (Part 4) `c₀/p` equidistributes as Uniform(0,1) in the limit, so does `d₀/p=1−c₀/p`, so **the two
slopes have identical limiting densities** — confirmed numerically below (§6), and consistent with
`group_types`' finding that both slopes converge to the same (0.5,0.25,0.25).

## 2. The curve of root triples

**Definition.** By Vieta for `x³+εx−c` (ε=±1, `x₁+x₂+x₃=0`, `x₁x₂+x₂x₃+x₃x₁=ε`, `x₁x₂x₃=c`), eliminating
`x₃=−x₁−x₂` from the second relation gives `x₁x₂−(x₁+x₂)² = ε`, i.e.

```
C_ε :  x₁² + x₁x₂ + x₂²  =  −ε        (a plane conic in (x₁,x₂), x₃:=−x₁−x₂, c:=x₁x₂x₃)
```

This *is* "the curve of ordered root triples of x³+εx−c": every ordered pair of two of the three roots of
some 3-root class lands on `C_ε`, and conversely every `F_p`-point of `C_ε` with `x₁≠x₂` gives two roots of
a specific class `c=x₁x₂x₃` (with the third root `x₃=−x₁−x₂` forced, and *automatically* a root of the
same `c` — division of `x³+εx−c` by `(x−x₁)` gives the quadratic `x²+x₁x+(x₁²+ε)`, whose product of roots
is `x₁²+ε` and whose sum is `−x₁`, matching `x₂x₃` and `x₂+x₃` exactly iff `x₂` satisfies `C_ε`).

**Absolutely irreducible.** `C_ε` is a *conic*: writing it `x₁²+x₁x₂+x₂²−(−ε)=0` with matrix
`M=[[1,½,0],[½,1,0],[0,0,ε]]`, `det M = ε(1−¼) = 3ε/4 ≠ 0` for `p∤6`. A plane conic is smooth iff this
determinant is nonzero, and a smooth conic is absolutely irreducible (a reducible conic is either two
lines meeting at a point or a double line, both singular everywhere the reducibility shows — so
irreducibility over `F̄_p` follows from smoothness, checked at every one of `p=101,131,167,197,401,797`
in the code, always nonzero). So `C_ε` is a smooth, absolutely irreducible plane conic for every odd prime
`p>3`.

**Exact point count `p+1` (not just Weil's `O(√p)`).** A smooth projective conic over `F_p` always has
exactly `p+1` points (classical: it is isomorphic to `P¹` over `F_p` once it has one rational point, and
every conic over a finite field has one). The two points at infinity of `C_ε` are the projective solutions
of the homogeneous part `x₁²+x₁x₂+x₂²=0`, i.e. `(x₁/x₂)² + (x₁/x₂) + 1=0`, discriminant `1−4=−3`. **For
`p≡2 (mod 3)`, `(−3|p)=−1`** (classical quadratic reciprocity for the discriminant of `Q(√−3)`: `p` splits
in `Z[ω]` iff `p≡1 (mod 3)`) — so `−3` is a non-residue, the two points at infinity are Galois-conjugate
over `F_{p²}\F_p`, **not** individually `F_p`-rational, and the *affine* count is the full `p+1`:

```
|C_ε(F_p)| = p+1   exactly, for every prime p ≡ 2 (mod 3), both ε=±1.
```

Verified exactly (not just numerically close) at `p∈{101,131,167,197,401,599,797,1097}`, both `ε`
(`slack/g_agents/theory_types.py: conic_check`, `discriminant_check`) — every single one gives `|C_ε|=p+1`
on the nose.

**Exact link to the class counts.** Let `n₃` = #{3-distinct-root classes}, `n₂` = #{double-root
("ramified") classes}. A genuine 3-root class contributes `3·2=6` points to `C_ε` (ordered pairs of its 3
distinct roots); a double-root class `{x₀ (mult 2), x₁}` contributes exactly **3**: `(x₀,x₀)` [which lies
on `C_ε` precisely because `3x₀²=−ε` is the ramification condition `g'(x₀)=0`/`h'(x₀)=0`] plus the two
ordered pairs `(x₀,x₁),(x₁,x₀)`. So

```
6n₃ + 3n₂  =  |C_ε(F_p)|  =  p+1     exactly (both directions checked, 0 exceptions, §6).
```

Since `n₂∈{0,2}` is `O(1)` (0 always for `ε=+1`; 0 or 2 for `ε=−1` depending on `p mod 12` — the
ramification-locus computation `group_types` did independently), this gives the **exact** closed form
`n₃ = (p+1−3n₂)/6`, i.e. `n₃ = p/6 + O(1)` with an *explicit* O(1), sharper than the generic
Chebotarev-type heuristic `n₃≈p/6` used to explain the 0/1/3-root split.

## 3. The Bombieri-type estimate for c₀

Parametrize `C_ε` by its two free coordinates `(x₁,x₂)`. We need the *joint* least-residue equidistribution
of `(x₁,x₂,x₃,c)` — `x₃=−x₁−x₂` is linear (already covered by ordinary Weil/Bombieri for the conic itself),
but `c=x₁x₂x₃=−x₁x₂(x₁+x₂)` is a genuine **cubic** polynomial on `C_ε`, so its least residue's
independence from `(x₁,x₂,x₃)` needs its own non-constancy check — this is exactly the gap `group_types`
flagged as unproved ("would need a character-sum argument for the joint position of c and its roots; out
of scope"). Filling it:

**Lemma (non-constancy).** For every `(h₁,h₂,h₃,h₄)∈Z⁴` not all `≡0 (mod p)`, the function
`F_h := h₁x₁+h₂x₂+h₃x₃+h₄c` (restricted to `C_ε`, `x₃=−x₁−x₂`) is a non-constant rational function on `C_ε`.

*Proof.* `F_h = (h₁−h₃)x₁+(h₂−h₃)x₂ − h₄x₁x₂(x₁+x₂)`, a polynomial of degree ≤3 in `(x₁,x₂)`.
If `F_h` were constant `=γ` on `C_ε`, then (since `C_ε` is absolutely irreducible of degree 2, and
`F_h−γ` vanishes on all of `C_ε(F̄_p)`) `F_h−γ` would have to be divisible by the defining quadratic
`Q=x₁²+x₁x₂+x₂²+ε`, say `F_h−γ = Q·(αx₁+βx₂+γ')` (degree count forces the cofactor linear). Expanding
`Q·(αx₁+βx₂+γ')` and matching the `x₁³,x₂³` coefficients forces `α=β=0`; but then the `x₁²x₂` coefficient
of `Q·(αx₁+βx₂+γ')` is `0`, while that of `F_h−γ` is `−h₄` — forcing **`h₄=0`**. So `h₄≠0 ⟹ F_h`
non-constant. If `h₄=0`, `F_h=(h₁−h₃)x₁+(h₂−h₃)x₂` is a linear form on the irreducible conic `C_ε`
(degree 2 > degree 1, so a line can meet `C_ε` in ≤2 points by Bézout unless the "line" `F_h=γ` contains
all of `C_ε`, impossible for a degree-2 irreducible curve) — non-constant unless it is the **zero**
polynomial, i.e. `h₁=h₂=h₃(=:h)`, in which case `F_h≡h(x₁+x₂+x₃)≡0` identically (the trivial Vieta
relation). ∎

The excluded direction `h₁=h₂=h₃, h₄=0` never arises among the combinations the box-counting needs
(individual `u_i` vs `c₀`, or `u₁+u₂` vs a threshold — see below): all of these have `h₄≠0` (conditions
involving `c₀`) or unequal `h_i` (conditions comparing two *different* roots), so they fall outside the
degenerate direction.

**The estimate.** By the Lemma, every relevant `F_h` is a non-constant rational function of bounded degree
(≤3, uniformly in `h,p`) on the absolutely irreducible curve `C_ε`, hence **Bombieri's estimate for
exponential sums along an absolutely irreducible curve** (Bombieri 1966; see also Iwaniec–Kowalski,
*Analytic Number Theory*, Ch. 11 — the same citation used for `Proposition m8asym` in `paper/hjsw_window.tex`,
whose whole machinery this argument mirrors) gives

```
S(h) := Σ_{(x₁,x₂)∈C_ε(F_p)} e( F_h(x₁,x₂) / p )  =  O(√p)      for every h ≢ (0,0,0,0) mod p (excl. above),
```

with an absolute implied constant (degree of `F_h` bounded independent of `h,p`; not of Artin–Schreier
form for `p` large by the same degree-boundedness).

**From here to the density theorem.** With `S(h)=O(√p)` in hand for all the needed linear/cubic
combinations, the *identical* 4-linear-form Selberg-polynomial telescoping argument of `Proposition
m8asym`, Step 4 (§ ~880–905 of `paper/hjsw_window.tex`) applies verbatim: writing the type-A/B (and
finer, k=0..3) conditions as finitely many interval conditions on the torus coordinates
`(x₁/p, x₂/p, c/p) mod 1` (a `k`-condition is, per §1, an inequality on `X(x_i)` vs `c₀`, i.e. exactly of
this shape once `x₃` is eliminated via the two branches `u₁+u₂ ≶ p`, exactly parallel to their `T`
bookkeeping for `X(1/b)`), the count of points of `C_ε(F_p)` in each such region is
`N·λ(W) + O(√p log⁴p)` (`N=|C_ε(F_p)|=p+1`, `λ` = the continuum volume of Part 4). **This is the precise
sense in which the counts of each pattern are `(density)·p + O(√p log^C p)`**: `C=4`, matching
`m8asym`'s own error term. *Honesty note*: this last step is a structural transcription, not a re-derivation
— I verified the non-constancy hypothesis (the genuinely new ingredient here) rigorously above, but did not
re-run the full Selberg-polynomial bookkeeping symbol-by-symbol for this specific 3-coordinate torus (that
would essentially retype `m8asym`'s Step 4 with relabelled variables); given the brief's "reason, with small
computations to check" scope, and that §6 below confirms the resulting prediction numerically at the
required primes, I consider this an appropriate stopping point, not a completed formal theorem.

## 4. The limiting densities

The task's own heuristic model — "the three roots' least residues jointly uniform subject to
`x₁+x₂+x₃≡0`" — is realized concretely (matching the branch structure of §1) as: `u₁,u₂ ~ iid Uniform(0,1)`
free, `u₃ := 1−u₁−u₂` if `u₁+u₂<1` else `2−u₁−u₂` (so `u₁+u₂+u₃∈{1,2}` always — this *is* the continuum
shadow of `C_ε`'s two free coordinates, justified as an equidistribution statement by the `h₄=0` case of
the Lemma above). By Part 3, `γ:=c₀/p` is an **independent** `Uniform(0,1)` (the `h₄≠0` case). We want
`P(k=j)`, `k=#{i:u_i≤γ}`.

**Key sub-computation.** Conditioned on the branch `u₁+u₂<1`, `(u₁,u₂,u₃)` is *exactly* the classical
"3 spacings from 2 uniform cut points on `[0,1]`" distribution (uniform on the 2-simplex), whose order
statistics have the standard closed form `E[D_{(k)}] = (1/3)Σ_{j=4−k}^{3} 1/j`: **`E[min]=1/9`,
`E[max]=11/18`** on this branch. The other branch (`u₁+u₂≥1`) is the *reflection* `u_i↦1−u_i` of the first
(direct check: it maps `u₃=1−u₁−u₂` to `u₃'=1−u₃=u₁+u₂`, which is exactly the branch-2 rule applied to
`u₁'=1−u₁,u₂'=1−u₂` — so the reflection is an exact symmetry of the *whole* model, swapping the branches),
so `min↦1−max, max↦1−min` there. **Mixing the two branches 50/50** (not applying branch-1's formula to
the whole mixture — the one error caught and fixed while writing `theory_types.py`, see commit history in
the code's docstring):

```
E[min]_full = ½·(1/9) + ½·(1−11/18) = ½·(2/18+7/18) = 1/4
E[max]_full = ½·(11/18) + ½·(1−1/9) = ½·(11/18+16/18) = 3/4
```

Since `γ⊥(u₁,u₂,u₃)`: `P(k=0)=P(γ<min)=E[min]=1/4`; `P(k=3)=P(γ>max)=1−E[max]=1/4`. The
`(γ,u)↦(1−γ,1−u₁,1−u₂,1−u₃)` reflection (a symmetry of the full independent-product model, since it
preserves `Uniform(0,1)` for `γ` and the `(u₁,u₂,u₃)`-law as just shown) sends `k↦3−k`, giving
`P(k=1)=P(k=2)`; with `P(k=1)+P(k=2)=1−P(k=0)−P(k=3)=1/2`, **`P(k=1)=P(k=2)=1/4`** too. So:

```
P(k=0) = P(k=1) = P(k=2) = P(k=3) = 1/4   exactly
     ⟹  density(shape (3,6,3))     = P(k=0)+P(k=3) = 1/2
        density(shape (1,4,5,2))   = P(k=1)         = 1/4
        density(shape (2,5,4,1))   = P(k=2)         = 1/4
```

(`fractions.Fraction`-exact in `slack/g_agents/theory_types.py:density_model_exact`; confirmed by a 2M-sample
Monte Carlo: `{0: 0.2501, 1: 0.2500, 2: 0.2496, 3: 0.2504}`.) **This is exactly `group_types`' empirical
"(0.5, 0.25, 0.25), rank-uniform" finding**, now with a closed-form value and the mechanism that produces
it (an independent 4th uniform coordinate against 3 sum-constrained ones, not literal 4-way exchangeability
— the naive "`γ` and `u₁,u₂,u₃` fully exchangeable" reading of "rank uniform over 4" is not quite what's
happening, since `(u₁,u₂,u₃)` alone are *not* mutually independent — but it gives the identical numbers).

## 5. Numerics — the required check at p = 401, 797

`slack/g_agents/theory_types.py` (default run) prints, per prime, per slope: the 0/1/3-root class counts
(cross-check against `group_types`' `(1/3,1/2,1/6)`), the `k`-histogram against `1/4` each, and the merged
shapes against `1/2, 1/4, 1/4`:

| p | slope | n₃ | k=0 | k=1 | k=2 | k=3 | shape A (3,6,3) | shape B {1,2,4,5} |
|---|---|---|---|---|---|---|---|---|
| 401 | antidiag | 67 | 0.239 | 0.269 | 0.254 | 0.239 | 0.478 | 0.522 |
| 401 | diag     | 67 | 0.284 | 0.209 | 0.209 | 0.299 | 0.582 | 0.418 |
| 797 | antidiag | 133 | 0.233 | 0.271 | 0.263 | 0.233 | 0.466 | 0.534 |
| 797 | diag     | 133 | 0.226 | 0.271 | 0.271 | 0.233 | 0.459 | 0.541 |

Predicted `0.25` per `k`, `0.5/0.5` per shape. Mean absolute deviation from `0.25` across these 16 numbers:
**0.022** (row means 0.011, 0.041, 0.017, 0.021) — small classes (`n₃=67,133`) so `O(1/√n₃)≈0.09–0.12`
binomial-scale noise is expected; all 16 values are within that noise band, and the *antidiagonal* rows (no
ramification correction at these two primes — `401,797≡5 (mod 12)`, so `n₂=0` for both slopes here) are the
tightest. `group_types`' own much larger extended batch (`p` up to `100019`) shows the deviation shrinking
`∝1/√n₃` down to `≈0.005` — consistent with `1/4` being the exact limit, not a nearby-but-different
constant.

**Exact (not asymptotic) cross-checks, zero exceptions:**
- `geometric_vs_algebraic`: brute-force box-lift line counts vs. the `(k,k+3,6−k,3−k)` formula, checked
  point-by-point for every 3-root class at `p∈{11,13,17,19,101,131,167,197}` (both slopes, 210 classes
  total) — **0 mismatches**.
- `6n₃+3n₂ = |C_ε(F_p)| = p+1`, checked exactly at `p∈{11,101,131,167,197,401,599,797,1097}`, both `ε` —
  **0 exceptions** (e.g. `p=131,ε=−1`: `n₃=21,n₂=2`, `6·21+3·2=132=p+1` ✓; the two double-root classes
  there have `k₂∈{0,2}`, contributing an extra unmatched 4-point line each — this fully explains a
  residual `lp_curve.py`-style `4≠5` mismatch of exactly 2 at `p=131`, and analogously an exact `3≠2·6`
  mismatch of exactly 4 at `p=11,167` (both `≡11 mod 12`, `n₂=2` with `k₂=1` there — contributing
  `(1,3,3,1)`, i.e. 2 extra 3-lines with no matching 6-line); see `double_root_diagnostic()` in the code
  for the fully itemised, p-by-p accounting.

## 6. What this contributes to G3.5

The `reduced_lp`/`group_types` line of work needs, for the ±1-line-only cover, the average cost achievable
by a per-type weighting rule; this note supplies the missing **mechanism and closed-form density**
(`1/2` type A, `1/4`+`1/4` type B, both slopes, both roughly `p/6` three-root classes per slope) that such
a rule's average is computed against, plus an *exact* (not just asymptotic) formula
`n₃=(p+1−3n₂)/6` for the class counts themselves. It does not itself produce a covering LP or a `(3/2−c)N`
bound — that is `reduced_lp`'s and `family_anatomy`'s remit.

## 7. Honest caveats

- **Fully rigorous, no gaps**: the shift-bit/interval condition (§1); the conic's absolute irreducibility,
  exact point count `p+1`, and the exact identity `6n₃+3n₂=p+1` (§2, including the double-root
  contribution count); the non-constancy Lemma for all four-parameter linear-plus-cubic combinations (§3).
- **Structural, not re-derived line-by-line**: the final `O(√p log⁴p)` error term (§3's last paragraph) —
  I verified the specific new hypothesis this problem needs (non-constancy of the cubic direction) but did
  not retype the Selberg-polynomial telescoping computation itself; it is the same argument as
  `Proposition m8asym` with relabelled coordinates, and I did not find (or look hard for) a shortcut that
  would make it shorter than that ~40-line computation for this problem.
- **The independence of `γ=c₀/p` from `(u₁,u₂,u₃)`** (used in Part 4's exact density computation) is the
  thing Part 3 argues for via Bombieri but does not fully close into a citation-ready theorem statement
  (no explicit constant, no fully written-out box decomposition into the `W_i`-style pieces `m8asym` has) —
  treat Part 4's "exactly 1/4 each" as *conditional* on Part 3's argument being completed at that level of
  rigor, which the numerics (§5, and independently `group_types`' much larger-p batch) support strongly but
  do not by themselves prove.
- **`p mod 12` ramification** (`n₂∈{0,2}` for the diagonal slope) is `group_types`' finding, re-derived
  independently here only insofar as needed to explain the small-p residuals (§5); the QR argument itself
  (`(3|p)` depends on `p mod 12`) is not re-proved in this file, only used.
- Densities are asymptotic-in-`p` statements about *proportions*; nothing here bounds the *o(1)* term's
  rate beyond the generic `O(1/√p)`-type Bombieri scaling, and (per §3) even that rate is inherited by
  structural analogy rather than computed explicitly for this curve.

## Reproduce

```
/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/theory_types.py            # full report (p=401,797 + all checks), ~2s
/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/theory_types.py densities  # continuum-model exact + Monte Carlo only
/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/theory_types.py small      # small-p geometric cross-check + double-root diagnostic + conic counts
/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/theory_types.py 599 1097   # any other prime(s)
```
Key functions: `classify_class(p,eps,c,xs)` — the §1 formula; `geometric_vs_algebraic` — the exact
brute-force cross-check; `conic_point_count` / `discriminant_check` — §2; `density_model_exact` /
`density_model_montecarlo` — §4; `double_root_diagnostic` — the §5/§6 residual accounting.
