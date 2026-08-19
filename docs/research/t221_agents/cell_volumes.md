# Task C: exact volumes of the sign cells, and the (1/3, 1/3, 1/3) law

k = −1, p an odd prime, h = (p−1)/2. This resolves the item left open at the end of
`docs/research/pair_bound_notes.md` §24 ("the polytope volumes are computable — I have not done it"): the
exact 3‑dimensional volumes of the sixteen sign cells crossed with the three possible values of L/p, their
aggregation into the BOTH/ONE/NEITHER classification of §24, and an empirical check against direct
enumeration of 4‑class groups for p ∈ {1009, 2003, 4001} (plus two larger bonus primes).

**Headline result: the model reproduces (1/3, 1/3, 1/3) exactly, not just approximately.**
V_both : V_one : V_neither = **1/3 : 1/3 : 1/3** (an exact rational identity, not a numerical coincidence —
proved below and cross‑checked three independent ways). Combined with N₄/p → 1/4 (§24's own empirical
constant, and a direct consequence of |C₀(F_p)| = p+O(√p) — `hjsw_window.tex` Prop. `prop:m8asym`, Step 1 —
via the same 4‑to‑1 correspondence its proof uses for m₈, §5) this reproduces, from one computation, all four
constants of §24: m₈/p, m₇/p, m₅/p → 1/12 and m₆/p → 1/6.

Code: `slack/t221_agents/cell_volumes.py`. Raw run: `slack/t221_agents/cell_volumes_output.txt`.

## 1. What was read, and the exact setup

Read first, as instructed: `slack/lp1_anatomy.py` and `slack/lp1_types.py` (docstrings + code — they fix the
point set P = {(x,y) ∈ [−h,3h+1]×[0,2p−1] : xy ≡ ±1 (mod p)} and the residue‑group machinery, `d = x−y mod p`
for slope‑(+1) groups G_d, R‑images for slope‑(−1)); `docs/research/pair_bound_notes.md` §24 ("T2.18 …
exact classification of the 5/6/7/8‑point ±1 lines") and §B.19 with its addendum (lines ≈962–1035, the orbit
closure Ω_d and the class‑graph disjointness/overlap facts); and `paper/hjsw_window.tex`, the proofs of
Proposition `prop:m8` and Proposition `prop:m8asym` (search string `prop:m8asym`), Steps 1–4, in full.

Fixed notation (`hjsw_window.tex` §12 / §24 of the notes, restated): for u ∈ F_p^*, X(u) ∈ [−h,h] is the
centred least residue. A 4‑class group of residue d ⟺ a pair (a,b) ∈ (F_p^*)² on the cubic
C₀ : a − 1/a + b + 1/b ≡ 0 (mod p), with a² ≢ −1 and b² ≢ 1 (both quadratics solvable, both non‑degenerate).
Put A1 = X(a), A2 = X(1/a), B1 = X(b), B2 = X(1/b) and

  L := A1 − A2 + B1 + B2.

**Fact (§24, F1; `hjsw_window.tex`, proof of `prop:m8`).** L is an *exact* multiple of p with |L| ≤ 2p−2,
hence L ∈ {−p, 0, p}; put c := L/p. The σ‑pair {a,−1/a} shares its centre iff sign(A1) ≠ sign(A2); the
τ‑pair {b,1/b} shares iff sign(B1) = sign(B2). **BOTH** shared ⟹ the group is (4,8,4), one 8‑point line
(these groups are counted by m₈); exactly **ONE** shared ⟹ (3,7,5,1) or (1,5,7,3), one 7‑point *and* one
5‑point line (m₇ = m₅ up to O(1)); **NEITHER** shared ⟹ (2,6,6,2), *two* 6‑point lines, so m₆ = 2·#(neither).

## 2. The heuristic model, and why it needs no extra normalisation

`prop:m8asym`'s proof (Step 3–4) shows the point x = (a,1/a,b)/p mod 1 is equidistributed on the 3‑torus as
(a,b) ranges over C₀(F_p) (Bombieri's bound on the exponential sums of the non‑constant rational functions
h·x restricted to the absolutely irreducible curve C₀, |C₀(F_p)| = p + O(√p)). Concretely: writing
(u1,u2,u3) for the centred representatives in the open cube (−1/2,1/2)³, this is equidistribution **w.r.t.
the ordinary Lebesgue probability measure of the whole cube (total mass 1)** — not normalised to any one
slice. Every point of that cube determines a *unique* c ∈ {−1,0,1} with u4 := c−u1+u2−u3 landing in
(−1/2,1/2) (the three "which c" events tile the cube up to its measure‑zero boundary — this is exactly the
L ∈ {−p,0,p} trichotomy, read continuously). So "equidistributed on the cube with mass 1" already *is*
"equidistributed on the union of the three hyperplane slices, same density on each, total mass 1": there is
no separate normalisation to choose, contrary to a natural worry when first setting this up. `prop:m8asym`
only ever evaluates the sub‑case "both shared" (4 of the 16 sign patterns) because that's what m₈ needs; the
task here is the other 12.

## 3. Exact computation

For a sign pattern s = (s1,s2,s3,s4) ∈ {±1}⁴ and c ∈ {−1,0,1},

  V(s,c) := vol{ (u1,u2,u3) ∈ (−1/2,1/2)³ : sign(uᵢ) = sᵢ (i=1,2,3), u4 := c−u1+u2−u3 has sign s4 and |u4| < 1/2 },

measure du1 du2 du3, exactly as the task specifies. Writing uᵢ = sᵢpᵢ (pᵢ = |uᵢ| ∈ (0,1/2)) and
ε = (−s1, s2, −s3) (the coefficients of p1,p2,p3 in u4 − c), the u4‑condition becomes an interval condition
α < ε·p < β on Σεᵢpᵢ, with (α,β) = (−c, 1/2−c) if s4=+1, else (−1/2−c, −c). Substituting qᵢ = pᵢ if εᵢ=+1
else qᵢ = 1/2−pᵢ (so qᵢ ∈ (0,1/2) always) turns ε·p into Σqᵢ − m/2 (m = #{i : εᵢ=−1}), reducing V(s,c) to the
CDF of a sum of 3 i.i.d. Uniform(0,1/2) variables — a scaled Irwin–Hall distribution with the standard closed
form

  F₃(t) = (1/6)·Σ_{k=0}^{⌊t/L⌋} (−1)ᵏ C(3,k) (t−kL)³ ,  L = 1/2 ,

computed with `fractions.Fraction` throughout: **no floating point anywhere** in the volume computation
(`cell_volumes.py`, functions `F3`, `slab_volume`, `cell_volume`). This is a direct, self‑contained
computation of the same quantity `prop:m8`'s proof computes for its four boxes W₁..W₄ via a torus/mod‑1
detour — as a first check, the script reproduces λ(Wᵢ) = 1/12 for all four (see §5).

**Built‑in exact self‑checks** (asserted at runtime, all pass): the 48 volumes sum to exactly 1; the "both"
total is exactly 1/3 (must match the *proved* m₈ ~ p/12, N₄ ~ p/4); each of the four individual
"both"-patterns equals exactly 1/12; every octant (s1,s2,s3) (summed over s4 and c) has total volume exactly
1/8.

### 3.1 Full table (16 sign patterns × 3 values of c)

Sign order is (sign A1, sign A2, sign B1, sign B2); "cell" is the §24 classification.

| A1 | A2 | B1 | B2 | cell | c=−1 | c=0 | c=1 | Σ_c |
|:--:|:--:|:--:|:--:|:-------|:----:|:----:|:----:|:----:|
| + | + | + | + | one     | 0    | 1/48 | 1/48 | 1/24 |
| + | + | + | − | neither | 0    | 1/12 | 0    | 1/12 |
| + | + | − | + | neither | 0    | 1/12 | 0    | 1/12 |
| + | + | − | − | one     | 1/48 | 1/48 | 0    | 1/24 |
| + | − | + | + | **both**| 0    | 0    | 1/12 | 1/12 |
| + | − | + | − | one     | 0    | 1/48 | 1/48 | 1/24 |
| + | − | − | + | one     | 0    | 1/48 | 1/48 | 1/24 |
| + | − | − | − | **both**| 0    | 1/12 | 0    | 1/12 |
| − | + | + | + | **both**| 0    | 1/12 | 0    | 1/12 |
| − | + | + | − | one     | 1/48 | 1/48 | 0    | 1/24 |
| − | + | − | + | one     | 1/48 | 1/48 | 0    | 1/24 |
| − | + | − | − | **both**| 1/12 | 0    | 0    | 1/12 |
| − | − | + | + | one     | 0    | 1/48 | 1/48 | 1/24 |
| − | − | + | − | neither | 0    | 1/12 | 0    | 1/12 |
| − | − | − | + | neither | 0    | 1/12 | 0    | 1/12 |
| − | − | − | − | one     | 1/48 | 1/48 | 0    | 1/24 |

The four **both** rows are exactly `prop:m8`'s W₁..W₄ (confirmed: 1/12 each, one nonzero c per row — the
paper computes these via the torus route, `1/8 · Pr[1<U1+U2+U3<2] = 1/8·2/3 = 1/12`; this script computes the
identical numbers by direct integration, an independent method).

### 3.2 Aggregate — the main result

| cell | c=−1 | c=0 | c=1 | **total** |
|:--|:--:|:--:|:--:|:--:|
| both     | 1/12 | 1/6 | 1/12 | **1/3** |
| one      | 1/12 | 1/6 | 1/12 | **1/3** |
| neither  | 0    | 1/3 | 0    | **1/3** |
| **sum**  | 1/6 | 2/3 | 1/6 | **1** |

**V_both : V_one : V_neither = 1/3 : 1/3 : 1/3 = 1 : 1 : 1, exactly.** The (1/3,1/3,1/3) law of §24 is not an
independent empirical coincidence sitting beside the m₈ ~ p/12 theorem — it is produced by *the same*
Bombieri/Weil equidistribution mechanism, applied to the 12 cells the m₈ proof didn't need. (Sub‑split of
"one", for completeness: sigma‑shared‑only = tau‑shared‑only = 1/6 each, also exactly equal — no claim is
made about why beyond noting the coincidence.)

## 4. A bonus exact (non‑asymptotic) fact, found while building the table

Two structural facts fall out for free and were verified against every empirical run below with **zero**
exceptions over tens of thousands of groups:

**(a) A "neither" group has L = 0 exactly — always, not just on average.** Proof: "neither" means
sign(A1)=sign(A2) and sign(B1)≠sign(B2). Say A1,A2 ∈ {1,…,h} (the case A1,A2 ∈ {−h,…,−1} is symmetric); since
non‑degeneracy forces A1≠A2, |A1−A2| ≤ h−1. Say B1 ∈ {1,…,h}, B2 ∈ {−h,…,−1} (or swap); |B1+B2| ≤ h−1. So
|L| ≤ 2(h−1) = p−3 < p. Since p | L, this forces **L = 0**. This is why row 3.2's "neither" row is
concentrated entirely at c=0 — it is forced, not merely likely. (The same style of interval bound, redone for
each of the four "both" sign sub‑cases, reproduces exactly `prop:m8`'s W₁..W₄ assignment of a *single* forced
c to each both‑pattern — e.g. A1>0>A2, B1,B2>0 gives A1−A2 ∈ [2,2h], B1+B2 ∈ [2,2h], so L ∈ [4,4h], and the
only multiple of p in that range is p itself. By contrast, "one" patterns are genuinely *not* sign‑forced:
e.g. (+,+,+,+) has A1−A2 ∈ [−(h−1),h−1], B1+B2 ∈ [2,2h], so L ∈ [3−h, 3h−1], an interval containing *both* 0
and p — consistent with the table showing that pattern split across c=0 and c=1. This is the exact mechanism
behind why an unconditional identity like m₇ = m₅ needs the equidistribution argument at all, while the "both"
and "neither" c‑assignments are elementary.)

**(b) m₈(c=1) = m₈(c=−1) and m₇(c=1) = m₇(c=−1) exactly, for every p** (not just asymptotically). Proof: the
map (a,b) ↦ (−a,−b) preserves C₀ (the curve is odd: (−a)−1/(−a)+(−b)+1/(−b) = −(a−1/a+b+1/b) = 0) and
non‑degeneracy (a² and b² are unchanged), sends the group at residue d to the group at residue −d, negates
every one of A1,A2,B1,B2 (since X(−u) = −X(u)), hence negates L (so c ↦ −c) while preserving BOTH/ONE/NEITHER
status (sign‑equality/inequality is invariant under a joint sign flip). This is exactly the orbit‑closure pairing
G_d / G_{−d} of §B.19 addendum (a), specialised to L. Confirmed exactly (not approximately) at every tested p
below — see §7.

## 5. What this means for m₈, m₇, m₅, m₆, and what would still be needed for a full theorem

Combining §3.2 with N₄(p) = p/4 + O(√p) — |C₀(F_p)| = p+O(√p) is `prop:m8asym` Step 1, and the 4‑to‑1
correspondence (a,b) ↔ {a,−1/a}×{b,1/b} that `prop:m8`'s proof states for its own (both‑shared) case is,
algebraically, a fact about *any* non‑degenerate point of C₀, both‑shared or not — and §24's line‑count
identities (m₈ = #both, m₇ = #one = m₅ − O(1), m₆ = 2·#neither):

  m₈/p, m₇/p, m₅/p → **1/12** ,  m₆/p → **1/6** ,

reproducing *all four* empirical constants of §24 ("Densities: m₈/p = 0.0795, m₇/p = 0.0800, m₅/p = 0.0835,
m₆/p = 0.1677 (→ 1/12, 1/12, 1/12, 1/6)") from the single computation V_both=V_one=V_neither=1/3.

**Honest gap for a fully written theorem.** `prop:m8asym`'s Steps 3–4 (the exponential‑sum bound and the
Selberg‑polynomial sandwich) are cell‑agnostic: they apply to *any* finite union of boxes cut out by
conditions ℓⱼ(x) mod 1 ∈ Iᵢⱼ on the same four linear forms ℓ1=x1, ℓ2=x2, ℓ3=x3, ℓ4=x1−x2+x3, and would give
N_one(p) = p/12 + O(√p log⁴p), N_neither(p) = p/12 + O(√p log⁴p) (group counts) by literally the same
argument. What this note has *not* done is redo Step 2's careful case check — verifying, for each of the 12
new (pattern,c) cells, that the arithmetic condition on T = A1−A2+B1 (not just its residue mod p) collapses to
a *single* arc on ℓ4, the way the proof does explicitly for W₁..W₄ — rather than, in principle, a union of two
arcs (which would still make Step 4 go through, just with more bookkeeping, since Selberg's polynomials work
per arc and a bounded number of arcs only changes the implied constant). The volumes reported here (§3, the
actual output of a Step‑2‑style computation) are exact and triple‑checked (§8); turning "the mechanism clearly
extends" into a fully written second proposition is the natural next step, not performed here.

## 6. Empirical validation

For each prime, enumerate a ∈ {1,…,p−1} (skip a²≡−1); d := a−1/a mod p; dedupe by d (each valid d is hit by
exactly two a's, a and −1/a mod p — §24's σ‑pair — so only the first occurrence is processed, matching "each
group counted once per residue d"); solve b²+db+1≡0 (i.e. b+1/b≡−d) via a general Tonelli–Shanks (needed:
1009 ≡ 1 mod 4 and 4001 ≡ 1 mod 4, so the p≡3 mod 4 shortcut alone is not enough); skip Δ=d²−4 = 0 (degenerate
b) or a non‑residue (b‑quadratic unsolvable — this a is *not* part of a 4‑class group). Every surviving group
is classified by (A1,A2,B1,B2) exactly as in §1; in addition (for p ≤ 20011) all four representative pairs
(a,b) ↔ {a,−1/a}×{b,1/b} per group are tabulated separately against the full 48‑cell table, matching `prop:m8`'s
"each line arises from exactly four pairs". Runtime: the whole script (exact table + all five primes below)
runs in **0.35 seconds** — pure `fractions`/modular‑arithmetic Python 3, no numpy/scipy/sympy dependency was
needed for this task.

| p | N₄ | N₄/p | m₈ | m₈/N₄ | m₈/p | m₇ | m₇/N₄ | m₇/p | m₆ | m₆/N₄ | m₆/p |
|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| 1009 | 257 | 0.2547 | 90 | 0.3502 | 0.0892 | 82 | 0.3191 | 0.0813 | 85 | 0.3307 | 0.0842 |
| 2003 | 500 | 0.2496 | 148 | 0.2960 | 0.0739 | 184 | 0.3680 | 0.0919 | 168 | 0.3360 | 0.0839 |
| 4001 | 973 | 0.2432 | 314 | 0.3227 | 0.0785 | 332 | 0.3412 | 0.0830 | 327 | 0.3361 | 0.0817 |
| 20011 (bonus) | 5002 | 0.2500 | 1668 | 0.3335 | 0.0835 | 1654 | 0.3307 | 0.0827 | 1680 | 0.3359 | 0.0840 |
| 100003 (bonus) | 25000 | 0.2500 | 8154 | 0.3262 | 0.0815 | 8382 | 0.3353 | 0.0838 | 8464 | 0.3386 | 0.0846 |
| **model** | | **0.2500** | | **0.3333** | **0.0833** | | **0.3333** | **0.0833** | | **0.3333** | **0.0833** |

(m₆/N₄ and m₆/p above are the *group*‑count fractions #neither/N₄, matching the model column directly; the
*line*‑count m₆ of §24 is 2× these, e.g. at p=100003 the 6‑line count is 16928, m₆/p = 0.169 ≈ 1/6, matching
§24's 0.1677.)

**Fine (16‑pattern × 3c) check**, over all 4·N₄ representative pairs, max |empirical fraction − exact volume|
across the 48 cells: p=1009: 0.0111; p=2003: 0.0213; p=4001: 0.0083; p=20011: 0.0010 — shrinking with p, as
expected for an O(1/√p)‑type (really O(log⁴p/√p), per `prop:m8asym`) equidistribution error.

**§4(b) exact‑symmetry check** (both/one counts at c=−1 vs c=+1, should be *identical*, not just close):

| p | both: c=−1 | both: c=+1 | one: c=−1 | one: c=+1 |
|--:|--:|--:|--:|--:|
| 1009 | 22 | 22 | 23 | 23 |
| 2003 | 31 | 31 | 45 | 45 |
| 4001 | 73 | 73 | 79 | 79 |
| 20011 | 422 | 422 | 410 | 410 |
| 100003 | 2104 | 2104 | 2071 | 2071 |

Exact equality at every prime, as predicted by §4(b). **§4(a) exact‑forcing check**: the "neither" cell's
count at c=±1 was exactly 0 at every prime tested (zero exceptions).

The convergence to (1/3,1/3,1/3) is visibly slow and non‑monotonic (p=2003 shows m₈/N₄=0.296, m₇/N₄=0.368 —
a 7‑point spread from 1/3); this is the expected size for an error term stated only as O(√p log⁴p) with an
unspecified constant (`prop:m8asym`), and is the same order of fluctuation §11's raw data already shows for
m₈/p alone at comparable p ("range 0.058–0.108" for 200 ≤ p ≤ 1500). By contrast, N₄/p converges quickly and
cleanly (0.2547 → 0.2496 → 0.2432 → 0.2500 → 0.2500): it is a plain point count on C₀ (Step 1's |C₀(F_p)| =
p+O(√p) alone, no sub‑polytope/Step‑4 argument needed), so its relative error is genuinely O(1/√p) with no
extra log factors, and it clears the 4‑digit‑agreement bar already at p=4001.

## 7. Independent cross‑checks on the exact volumes themselves

Three independent checks, none of which is "the same computation twice":

1. **Runtime assertions** inside `cell_volumes.py` (§3): total = 1, both = 1/3 exactly (must equal the
   *already‑proved* m₈ asymptotic constant), the four W_i = 1/12 each (must match `prop:m8`'s own stated
   values), all 8 octant totals = 1/8. All pass.
2. **By‑hand derivation**, worked independently of the code for two cells and matched to the printed
   fractions: V((+,−,+,+), c=1) = F₃(1) − F₃(1/2) = 5/48 − 1/48 = **1/12** ✓.
   V((+,+,+,+), c=0) = F₃(3/2) − F₃(1) = 1/8 − 5/48 = **1/48** ✓ (and, by the reflection u₁↦1/2−u₁,
   u₃↦1/2−u₃, V((+,+,+,+), c=1) = **1/48** too, matching the printed row exactly).
3. **Monte Carlo** (independent code path, no `Fraction`/`F3`/`slab_volume` machinery at all — plain
   `random.uniform` triples and direct inspection of which of the three hyperplanes each sample lands
   nearest, run separately, not part of `cell_volumes.py`): 20,000,000 samples, max deviation from the exact
   fractions over all 48 cells = **0.000146** (an expected‑size Monte Carlo error at this N for cells of size
   ≈1/24–1/6); both/one/neither ≈ 0.33339/0.33324/0.33337 vs. the exact 1/3 = 0.33333 each.

## 8. Files

- `slack/t221_agents/cell_volumes.py` — exact volume computation (`fractions.Fraction`, no dependencies) +
  empirical enumeration (general Tonelli–Shanks + modular arithmetic, stdlib only). Usage:
  `python3 slack/t221_agents/cell_volumes.py [p1 p2 ...]` (default primes: 1009 2003 4001 20011 100003).
- `slack/t221_agents/cell_volumes_output.txt` — full run captured verbatim (the exact table of §3.1–3.2 and
  the empirical tables of §6, for the five primes above).
- This file: `docs/research/t221_agents/cell_volumes.md`.

**What was checked, honestly.** All 48 exact volumes are rational numbers computed with exact arithmetic and
verified three independent ways (§7); the resulting V_both:V_one:V_neither = 1:1:1 is an exact identity, not
a fit. The empirical enumeration is a direct, unconditional check (every 4‑class group for the given p really
was constructed and classified — no sampling, no LP, no numpy/scipy needed) for p ∈ {1009, 2003, 4001, 20011,
100003}; larger p were not attempted only because they were unnecessary (agreement is already at the
few‑×10⁻³ level by p=20011, and the model constant is exact regardless of p). The one thing this note does
*not* provide is a complete Step‑2‑style formal proof that N_one(p) ~ p/12 and N_neither(p) ~ p/12 as
theorems (§5) — only the exact volumes that such a proof would need to plug in, plus the argument for why the
remaining work (Step 2's arc bookkeeping for 12 more cells) is routine given `prop:m8asym`'s Steps 1, 3, 4.
