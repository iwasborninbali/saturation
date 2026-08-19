# group_types — residue-class root patterns for the ±1-line groups of the permutation cubic

Agent: `group_types`. Code: `slack/g_agents/group_types.py` (self-contained, no numpy/scipy needed;
run with `/Users/iwasborninbali/venvs/sat/bin/python3 slack/g_agents/group_types.py [p1 p2 ...]` from
the repo root). Raw stdout for the full run below (12 primes, both slopes) is saved verbatim at
`slack/g_agents/group_types_output.txt`. Total wall time for all 12 primes: **0.87s** (pure `O(p)`
bucketing per prime per slope — no `O(p^2)` pair search, no LP).

## Task recap

For `p ≡ 2 (mod 3)`, classify every residue class `c` of the two depressed cubics
`x^3+x≡c` (mod p) (antidiagonal groups, slope −1 lines `X+Y=const`) and `x^3−x≡c` (mod p) (diagonal
groups, slope +1 lines `X−Y=const`) by the point-count pattern on the 4 consecutive integer lines of
its "group" in the box lift, tabulate proportions, check convergence as `p→∞`, and check whether the
antidiagonal-group-type and diagonal-group-type through the same residue point are correlated.

Required primes `{101,197,401,599,797,1097}` all ran in milliseconds, so I added a second, larger batch
`{2003, 5003, 10007, 20021, 50021, 100019}` (also all `≡2 mod 3`, mix of `p mod 12 ∈ {5,11}`) to pin
down the limiting proportions properly — this is the "extended set" referenced throughout.

## Setup

For a class `c` with 3 roots `x_1<x_2<x_3` (sorted ascending, residues in `[0,p)`), each root's actual
curve point is `(x_i, y_i)`, `y_i = x_i^3 mod p` (always — this is just the fixed curve `Y≡X^3`). Define
the **shift bit**:

```
antidiagonal (x^3+x):  b_i = 1  iff  x_i + y_i ≥ p      (the integer sum wraps)
diagonal     (x^3−x):  b_i = 1  iff  x_i ≥ y_i           (the integer difference doesn't go negative)
```

`b_i=0` contributes point-counts `(1,2,1,0)` to the group's 4 consecutive lines (spaced by `p`);
`b_i=1` contributes `(0,1,2,1)`. With `k = #{i : b_i=0} ∈{0,1,2,3}`, the group pattern is exactly
`(k, k+3, 6−k, 3−k)`, giving 3 **shapes**: `k∈{0,3}` → `(3,6,3)` (one line empty — "all three roots
share a bit"), `k=1` → `(1,4,5,2)`, `k=2` → `(2,5,4,1)`. A 1-root class is always `(1,2,1)`, unambiguously.

## 1. Root-count distribution (0/1/2/3 roots per class)

| p | n0/p | n1/p | n3/p (both slopes identical except ramified p) |
|---|---|---|---|
| 101 | 0.3366 | 0.4950 | 0.1683 |
| 599 | 0.3339 | 0.4992 | 0.1669 |
| 1097 | 0.3336 | 0.4995 | 0.1668 |
| 10007 | 0.3334 | 0.4999–0.5000 | 0.1666–0.1667 |
| 100019 | 0.3333 | 0.5000 | 0.1667 |

**Converges cleanly to (1/3, 1/2, 1/6)** — matches to 4 decimals by `p≈50000`. Plausible explanation:
if the Frobenius-type "splitting behaviour" of the family `x^3±x−c` as `c` ranges over `F_p` is
equidistributed over the conjugacy classes of `S_3` (sizes 1, 3, 2 for identity/transposition/3-cycle,
total 6), the heuristic predicts exactly `1/6` (3 roots), `1/2` (1 root), `1/3` (0 roots) — matching the
data. **This is a heuristic, not a proof** — no character-sum argument was attempted here.

`n1 + 2·n2 + 3·n3 = p` exactly, checked (assert) for every run.

**Double-root (ramification) classes** (`n2`): elementary calculus over `F_p`. Antidiagonal
`g(x)=x^3+x`, `g'(x)=3x^2+1=0 ⟺ x^2=−1/3`. Since `p≡2 mod 3`, quadratic reciprocity gives
`L(−3|p)=−1` unconditionally (that's exactly what "`p≡2 mod 3`" *means* number-theoretically — verified
directly for all 12 primes), and `L(−1/3|p)=L(−1|p)L(3|p)=L(−3|p)=−1` always — so `g` has **no**
critical points and **`n2=0` for the antidiagonal slope for every single p tested (12/12, no
exceptions)**. Diagonal `h(x)=x^3−x`, `h'(x)=3x^2−1=0 ⟺ x^2=1/3`, QR-ness of `1/3` = QR-ness of `3`,
which by reciprocity depends on `p mod 12`: `L(3|p)=+1` iff `p≡±1 (mod 12)`. Our `p≡2 mod3` primes only
land on `p mod 12 ∈{5,11}`, and `11≡−1 (mod 12)` while `5≢±1 (mod 12)`, so `L(3|p)=+1` exactly for the
`p≡11` primes and `−1` for the `p≡5` primes — verified directly by Euler's criterion `3^((p−1)/2) mod p`
for all 12 primes. Result: **`n2=0` when `p≡5(mod12)`
(101,197,401,797,1097,20021,50021 — 7/7 exact), and `n2=2` when `p≡11(mod12)`
(599,2003,5003,10007,100019 — 5/5 exact, always exactly 2, never more)**. Fully explained, zero
surprises; these classes are dropped from the 3-root tabulation below (footnoted in the raw output).

## 2. Shape proportions among 3-root classes — the main question

Full table (`slack/g_agents/group_types_output.txt` has all 12×2 rows; representative rows below):

| p | slope | n3 | (3,6,3) | (1,4,5,2) | (2,5,4,1) |
|---|---|---|---|---|---|
| 101 | antidiag | 17 | 0.3529 | 0.3529 | 0.2941 |
| 197 | antidiag | 33 | 0.4848 | 0.2727 | 0.2424 |
| 1097 | antidiag | 183 | 0.4918 | 0.2568 | 0.2514 |
| 1097 | diag | 183 | 0.4973 | 0.2514 | 0.2514 |
| 10007 | antidiag | 1668 | 0.5168 | 0.2416 | 0.2416 |
| 20021 | diag | 3337 | 0.5037 | 0.2481 | 0.2481 |
| 100019 | antidiag | 16670 | 0.5113 | 0.2443 | 0.2443 |
| 100019 | diag | 16669 | 0.5016 | 0.2492 | 0.2492 |

**Two competing null models, tested against the task's own "1/4, 1/2, 1/4" guess:**

- *(a) "3 independent fair coins"* (each root's bit an independent 50/50 flip): predicts
  `P(k=0..3)=1/8,3/8,3/8,1/8`, i.e. shapes `(3,6,3):0.25, (1,4,5,2):0.375, (2,5,4,1):0.375`. **Ruled
  out** — data never gets close to `3/8` for the asymmetric shapes at any tested p.
- *(b) "c's rank among {c, x_1, x_2, x_3} is uniform over the 4 possible ranks"* (`k` = how many roots
  are `≤ c0`, treating the class label as exchangeable with its own roots): predicts `1/4` each for
  `k=0,1,2,3`, i.e. shapes **`(3,6,3): 1/2, (1,4,5,2): 1/4, (2,5,4,1): 1/4`.**

**(b) matches the data well and improves steadily with p.** Mean absolute deviation from
`(0.5, 0.25, 0.25)`, averaged over all 12 rows (both slopes) in each batch:

| batch | mean abs dev, shape (3,6,3) | mean abs dev, shape (1,4,5,2) | mean abs dev, shape (2,5,4,1) |
|---|---|---|---|
| required set (p=101..1097) | 0.0795 | 0.0446 | 0.0361 |
| extended set (p=2003..100019) | **0.0093** | **0.0047** | **0.0047** |

Deviation shrinks by **~8–9×** going from the required batch (mean `n3≈94`) to the extended batch
(mean `n3≈5500`, ratio `≈60`, `√60≈7.7`) — consistent with `O(1/√n3)` sampling noise around an **exact**
limit of `(1/2, 1/4, 1/4)`, not a slower or non-existent convergence. So: **the proportions do
stabilise, to values matching the task's guessed multiset `{1/4, 1/2, 1/4}` — but the "1/2" lands on
the *symmetric* shape `(3,6,3)`, not on one of the asymmetric ones**, and the mechanism is rank
exchangeability, not independent coin flips. Both facts are worth flagging since the task phrased the
guess ambiguously about which category gets which value and by what mechanism — I did not find a proof
of the rank-uniformity heuristic itself (would need an equidistribution / character-sum argument for
the joint position of `c` and its roots; out of scope here), so **item (b)'s numeric target is
empirical, backed by the convergence-rate check above, not proven**.

## 3. Exact theorem: the `c ↔ −c` involution (fully explains every deviation from a clean 50/50 pairing)

If `x` is a root of class `c` (either slope: `(−x)^3±(−x) = −(x^3±x)`), then `p−x` is a root of class
`(−c) mod p`. This is an exact bijection between the roots of class `c` and class `p−c`, for **both
slopes**, reversing root order (so `k ↦ 3−k` exactly: `b_i` complements and reverses).

**Verified computationally with zero exceptions**: for every one of the 12 primes × 2 slopes = 24 runs,
every 3-root class `c≠0` pairs with a 3-root class `p−c` whose root set is *exactly*
`sorted((p−x)%p for x in roots(c))` (`verify_involution()` in the code; 0 mismatches, e.g. 16670+16668
= 33338 paired classes checked without incident at p=100019 alone).

The **unique fixed class is `c=0`** (self-paired, since `−0≡0`), and it is the *entire* source of every
off-by-one in the k-histograms:

- **Diagonal**: `x(x−1)(x+1)≡0` always has roots `{0,1,p−1}` — for **every** odd prime `p>3`, no
  exceptions (confirmed 12/12). These give bits `(1,1,1)`, i.e. `k=0`. So `n(k=0) = n(k=3) + 1` exactly,
  always, for the diagonal slope.
- **Antidiagonal**: `x(x^2+1)≡0` has roots `{0,±i}` (`i=√−1`) **iff `−1` is a QR mod p, i.e. `p≡1(mod4)`**
  — confirmed exactly 7/7 primes with `p≡1(mod4)` in the test set (101,197,401,797,1097,20021,50021)
  show this extra class (bits `(0,1,1)`, `k=1`, so `n(k=1)=n(k=2)+1`), and exactly 5/5 primes with
  `p≡3(mod4)` (599,2003,5003,10007,100019) show **no** defect at all (`c=0` has only 1 root there, since
  `−1` is a non-residue) — `k=0,1,2,3` counts pair up perfectly with **zero** off-by-one (e.g. p=599
  antidiagonal: `k=25,25,25,25` exactly; p=100019: `k=4262,4073,4073,4262` exactly).

So the fine structure of every table above is now **100% accounted for**, not just approximately
explained — a genuinely nice, fully verified piece of structure.

## 4. Shift-bit tuples: only 4 of 8 possible ever occur (exact, not approximate)

Recording `(b_1,b_2,b_3)` (roots sorted ascending by `x`) across **all 12 primes × 2 slopes**, the
tuples `(0,1,0), (1,0,0), (1,0,1), (1,1,0)` have count **0 in every single run** — only
`(0,0,0),(0,0,1),(0,1,1),(1,1,1)` ever appear (full table in the raw output). This is not a numerical
curiosity: `b_i = 1[x_i > c0]` (antidiagonal, `c0=c mod p`) or `b_i=1[x_i ≥ p−c0]` (diagonal) is a
**threshold function of `x_i` against a class-fixed constant** — so sorting roots by `x_i` ascending
*forces* the bit sequence to be non-decreasing. The `bits_counter` breakdown therefore carries **no
information beyond `k`** — my original plan to look for "positional bias" (is the odd-one-out root
preferentially the smallest/largest?) was moot: there is only one possible bit arrangement per `k`,
not several to be biased among. Worth recording as a negative result in its own right.

## 5. Cross-slope correlation

For each residue `x∈[0,p)` (full population, not a Monte Carlo subsample — exact for these p), let
`A(x)=1` if `x`'s antidiagonal class has 3 roots, `B(x)=1` if its diagonal class has 3 roots.

| p | P(A) | P(B) | P(A∧B) | P(A)·P(B) | ratio |
|---|---|---|---|---|---|
| 101 | 0.5050 | 0.5050 | 0.2475 | 0.2550 | 0.9708 |
| 1097 | 0.5005 | 0.5005 | 0.2634 | 0.2505 | **1.0519** |
| 2003 | 0.5002 | 0.4988 | 0.2486 | 0.2495 | 0.9965 |
| 10007 | 0.5000 | 0.4998 | 0.2498 | 0.2499 | 0.9997 |
| 100019 | 0.5000 | 0.5000 | 0.2500 | 0.2500 | **1.0000** |

Mean `|ratio−1|`: **0.0222** over the required set (101..1097) vs **0.0028** over the extended set
(2003..100019) — an ~8× shrink, same `√n` pattern as above. **The required-primes batch alone looks
like it might show a growing positive correlation (ratio creeping from 0.97 to 1.05 as p goes
101→1097)** — but the extended batch kills that reading: ratios there sit tightly around 1.00 with no
trend, so the base-6 wobble is finite-size noise, not a real effect. Honest conclusion: **antidiagonal-
3-root-ness and diagonal-3-root-ness at the same residue point are asymptotically independent** (ratio
→ 1); I would flag it as a false positive if someone only ran the required 6 primes and stopped there.
Full `(size_antidiag, size_diag)` contingency tables (including where the 2 ramified-diagonal residues
land, always in a `(1,2)` or `(3,2)` cell) are in the raw output.

## Summary

- Root-count proportions → **(1/3, 1/2, 1/6)**, matching an `S_3`-conjugacy-class heuristic (unproven).
- Shape proportions among 3-root classes → **(1/2, 1/4, 1/4)** for `((3,6,3), (1,4,5,2), (2,5,4,1))`,
  matching a "rank of `c` among its own roots is uniform" heuristic (unproven), *not* the naive
  independent-coin-flip heuristic. This validates the task's numeric guess as a multiset of values,
  while correcting which category it attaches to.
- The `c↔−c` involution is an **exact, fully verified** theorem explaining every single deviation from
  clean pairing via one boundary class `c=0`, whose behaviour itself is exactly characterised by
  `p mod 4` (antidiagonal) / unconditionally (diagonal).
- Only 4 of 8 bit-tuples ever occur, exactly, by an elementary monotonicity argument.
- Ramification (`n2>0`, diagonal only) occurs exactly for `p≡11(mod12)`, always exactly 2 classes.
- Cross-slope 3-root-ness is asymptotically independent; the required-primes-only data would have
  suggested otherwise (documented as a caution against under-sampling this kind of statistic).

**Relevance to G3'**: this is a structural/enumerative pass, not an LP bound — no cover weights were
computed here. The natural next step (not attempted, out of scope for this task) would be to feed the
`(3,6,3)/(1,4,5,2)/(2,5,4,1)`-shape classification into a type-indexed marginal-saving LP in the style
of `slack/lp1_types.py` (built for the hyperbola's `(4,8,4)`-groups) via the exact rectangle-reduction
cost formula in the task background, to see whether the LP's saving per group differs systematically by
shape-type for the cubic — the classification and the exact `c↔−c` pairing established here would be
the inputs to that.

## Files

- `slack/g_agents/group_types.py` — the analysis (classification, involution/monotonicity
  verification, all summary tables); run with no arguments for the required 6 primes, or pass any list
  of `p≡2(mod3)` primes.
- `slack/g_agents/group_types_output.txt` — full raw output for all 12 primes (required 6 + extended 6
  `{2003,5003,10007,20021,50021,100019}`), both slopes, including the per-class illustrative dump for
  p=101 (every one of its 17+17 three-root classes listed with roots/bits/k/shape) and the involution
  verification lines.
