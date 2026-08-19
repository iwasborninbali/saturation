# G3 strong form — anatomy of the 3-point-line family for y = x³ (task `family_anatomy`)

Code: `slack/g_agents/family_anatomy.py` (self-contained; `python3 slack/g_agents/family_anatomy.py 197 401 599 797` reproduces
everything below in ≈4.5 min). p ∈ {197, 401, 599, 797}, all ≡ 2 (mod 3), box [0,2p)², N = 2p, f(x) = x³ (a = b = 0, the
permutation cubic — every row/column has exactly 2 points, so rows/columns never enter the "≥3-point" LP and are handled purely
by the point-weight fallback z_P).

## 0. Method and a data-quality note

Lines are found by a **full O(n²) pairwise scan keyed by the reduced line equation (dx,dy,c)** (n = 4p ≤ 12752 points; 10–155s
per p), not by the per-point direction-bucketing used in `slack/cubic_anatomy.py`. That distinction matters: the bucketing
approach re-emits every ≥4-point line's *suffixes* as spurious extra "lines" (at outer index i it correctly finds the full line
starting at i, but at the next point i′ on the same line it finds the same line **minus** the points before i′, and — since
nothing checks whether a shorter member-tuple is a sub-tuple of an already-seen one, only exact tuple equality — that shorter
tuple gets added too whenever it still has ≥2 members). Running `slack/cubic_anatomy.py 197 0 0` today reproduces this exactly:
it reports sizes `{6:35, 3:3539, 4:97, 5:66}`, where the correct counts (cross-checked below) are pm1 `{3:70,4:31,5:31,6:35}` +
generic `{3:3372}` = `{3:3442, 4:31, 5:31, 6:35}` — its 4- and 5-point counts are ~3× inflated, and its 3-point count absorbs
~100 spurious suffixes of the inflated 4/5-point lines. Its degree loop does not filter by direction, so these contaminate the
"3-line degree" statistics too (§3 explains a genuine, non-buggy reason those degrees are wildly non-uniform, which likely
compounds with this bug in whatever produced the "CV ≈ 0.37–0.40" numbers in `curves_conjecture.md` §7a).

**Cross-check.** My line-finder reproduces `slack/verification/lp_curve.txt` exactly at p = 197: pm1 `167` lines, sizes
`{3:70,4:31,5:31,6:35}`, `LP(pm1)=534.00=1.355N`; all-lines `LP=436.28=1.107N`. ✓.

**Formula check.** Every found 3-point line with distinct residues (necessarily slope ∉ {0,∞} — impossible for a bijection —
but occasionally slope ±1 by coincidence, which I classify with the ±1 group, not as "generic") was checked against the family
formula (leftmost-point base, 0 < i < j, J = max(i,j,j−i) = j): **0 mismatches out of 43,264 lines pooled over all four p.**
(Better than the a=1 case's reported 1416/1417 — plausibly because a = 0 is the clean case the formula was derived for.)

## 1. Line counts and the full LP

| p | pts=4p | pm1 rich lines (sizes 3,4,5,6) | generic 3-lines | J range |
|---|---|---|---|---|
| 197 | 788  | 167 (70,31,31,35)  | 3372  | [2,180] |
| 401 | 1604 | 339 (142,63,63,71) | 8060  | [2,388] |
| 599 | 2396 | 499 (198,102,102,97) | 13098 | [2,573] |
| 797 | 3188 | 655 (246,143,143,123) | 18734 | [2,779] |

Generic-line count grows a bit faster than linearly in p (roughly p^{1.15}–p^{1.2} over this range), consistent with the
predicted ≈8p·log(J_max) once J_max itself grows like p.

| p | LP(pm1 only)/N | LP(J≤4)/N | LP(J≤8)/N | LP(J≤16)/N | LP(full, all J)/N |
|---|---|---|---|---|---|
| 197 | 1.3553 | 1.2893 | 1.2284 | 1.1827 | 1.1073 |
| 401 | 1.3242 | 1.2818 | 1.2309 | 1.1899 | 1.0996 |
| 599 | 1.3422 | 1.2821 | 1.2288 | 1.1865 | 1.0972 |
| 797 | 1.3538 | 1.2961 | 1.2419 | 1.1930 | 1.0945 |

`LP(pm1 only)` matches the previously-recorded 1.317–1.355 N (`curves_conjecture.md` §8); `LP(full)` matches the previously
recorded ≈1.10 N (§7a), both to 3 decimals at the one overlapping p (197 vs the note's own p=101,131,167,197 series). Full LP/N
is *flat to slightly decreasing* in p (1.107 → 1.095), no sign of drifting back up toward 4/3.

## 2. How much of the LP saving comes from small J

"Saving" = LP(pm1 only) − LP(full); I re-solved the LP restricted to {pm1 lines} ∪ {generic 3-lines with J ≤ J0} for
J0 ∈ {4,8,16} (a genuine re-optimization, not a readout of the full LP's one arbitrary optimum) and measured what fraction of
the saving each capture:

| p | J≤4 | J≤8 | J≤16 | (J_max for reference) |
|---|---|---|---|---|
| 197 | 26.6% | 51.2% | 69.6% | 180 |
| 401 | 18.9% | 41.5% | 59.8% | 388 |
| 599 | 24.5% | 46.3% | 63.6% | 573 |
| 797 | 22.3% | 43.2% | 62.0% | 779 |

**Small J is a plurality but not the majority mechanism at J≤4, and captures roughly two-thirds of the saving by J≤16 — the
remaining third needs the long tail up to J ≈ p/2.** The fraction is essentially flat in p (no evidence it → 0 or → 1), i.e.
the saving genuinely spreads across scales rather than concentrating at fixed small J or purely growing with p; a proof of the
full G3-strong constant (≈1.10 N) cannot avoid the tail. **But** a fixed, p-independent cutoff already buys a lot: **LP(J≤16)/N
≈ 1.18–1.19 is comfortably under 4/3 ≈ 1.333** (the constant of Conjecture G3) for every tested p, using only 16·(16−1)/2-ish
families total — i.e. a **finite list of families, not growing with p**, already beats the 4/3 benchmark by a solid margin
(~0.14–0.15 N), even though it falls well short of the empirical ≈1.10 N minimum. That is a much cheaper target than the full
strong form and may be provable by a purely "small-J" argument even though the strong constant is not.

## 3. The box-corner hub: one point on ≈ N lines

The point **(p,p)** — the "far" lift of the curve's unique symmetric fixed point (residue (0,0); f is odd, f(−x) = −f(x)) — has
generic-3-line degree far above everything else (p=197: top-10 degrees are `23,23,23,23,23,24,24,26,26,388` — a sheer cliff, no
secondary hub). This is not noise; it is an exact identity.

**Lemma.** For every residue x0 ∈ (0,p) and either Y-lift Y0 ∈ {y0, y0+p} (y0 = x0³ mod p), the reflection
C = 2·(p,p) − (x0,Y0) = (2p−x0, 2p−Y0) lies in the box and on the curve, and is exactly collinear with (x0,Y0) and (p,p).
*Proof.* Cx ≡ −x0, Cy ≡ −Y0 ≡ −y0 (mod p), and (−x0)³ = −x0³ = −y0 identically — so C is on the curve for free, and
C − (p,p) = −[(x0,Y0) − (p,p)] makes the three points collinear by construction (no residue arithmetic needed, it's exact
integer algebra). This gives 2(p−1) triples through (p,p); subtract the ones that land on slope ±1 (already counted with the
pm1 lines, not "generic"): x0 ∈ {1, p−1} always gives slope +1 (f(±1) = ±1), and — when p ≡ 1 (mod 4), i.e. −1 is a QR — the
two square roots of −1 give slope −1. **Predicted generic degree = 2(p−1) − 2 − 2·[p≡1 mod 4].**

| p | p mod 4 | predicted | observed max (=argmax) | hub / N |
|---|---|---|---|---|
| 197 | 1 | 388  | 388  | 0.985 |
| 401 | 1 | 796  | 796  | 0.993 |
| 599 | 3 | 1194 | 1194 | 0.997 |
| 797 | 1 | 1588 | 1588 | 0.996 |

Exact match at all four p. **One point sits on essentially N generic 3-point lines** — the hub is a genuine, provable,
p-linear outlier, not a heavy-tailed-but-boundable fluctuation; the bulk mean degree grows only like ≈1.7·log₂p (§4), so
hub/mean → ∞ as p → ∞. No "near-regular hypergraph" argument can absorb this point; it must be excised by hand (trivial — it
is exactly 1 point out of 4p, worth O(1) to any bound on α).

Crucially, the hub's lines **all have (i,j) = (1,2), J = 2** — the hub is *entirely* a small-J phenomenon. That is the answer
to the "does small J help" question below.

## 4. Degree regularity: does restricting to small J help?

Mean degree (all points, generic 3-lines with J ≤ J0), hub included and excluded, and the resulting coefficient of variation
CV = std/mean:

| p | mean(all-J, excl.hub) | 1.7·log₂p |
|---|---|---|
| 197 | 12.36 | 12.96 |
| 401 | 14.59 | 14.70 |
| 599 | 15.91 | 15.70 |
| 797 | 17.14 | 16.39 |

**CV by J0, raw (hub included) vs. hub excluded:**

| p | CV(J≤4) raw / excl | CV(J≤8) raw / excl | CV(J≤16) raw / excl | CV(all) raw / excl |
|---|---|---|---|---|
| 197 | 4.357 / 0.532 | 2.864 / 0.484 | 2.111 / 0.473 | 1.103 / 0.378 |
| 401 | 6.615 / 0.559 | 4.052 / 0.509 | 2.936 / 0.502 | 1.351 / 0.402 |
| 599 | 7.469 / 0.537 | 5.051 / 0.477 | 3.659 / 0.467 | 1.519 / 0.406 |
| 797 | 9.081 / 0.551 | 5.870 / 0.462 | 4.125 / 0.458 | 1.626 / 0.406 |

`frac(deg ≤ mean/2)`, raw, by J0 (stable across p, the more robust of the two exclusion variants — at J0=4 the hub-excluded
mean is itself only ≈2, so its own frac≤mean/2 is an integer-rounding artifact, not reported here):

| J0 | 4 | 8 | 16 | all |
|---|---|---|---|---|
| range over p | 33–38% | 26–28% | 19–24% | 9–11% |

**Two different answers depending on whether the hub is in scope:**
* **Including the hub (i.e. the literal statistic the task asks for): restricting to small J makes degrees *dramatically less*
  regular, not more**, and it gets *worse* with p: CV(J≤4) climbs from 4.4 (p=197) to 9.1 (p=797); even CV(all) climbs
  1.10 → 1.63 — the opposite of "stays ≈0.4". This is not a contradiction of the earlier note so much as a sharper
  measurement: the earlier ≈0.4 figure quietly excluded (or never hit, via the cubic_anatomy.py bug's own distortions) this one
  point. Mechanically: the hub connects via J=2 lines specifically, so its degree (≈2p) stays essentially fixed as J0 shrinks
  while every other point's degree (whose lines are spread over the whole J range) shrinks — the hub's share of the total
  degree mass *grows* as J0 shrinks, which is the opposite of "diluting away."
* **Excluding the single hub point: mildly yes**, and the trend is stable across p (four curves are within a hair of each
  other): CV falls from ≈0.53–0.56 (J≤4) to ≈0.46–0.51 (J≤8) to ≈0.46–0.50 (J≤16) to ≈0.38–0.41 (all) — a modest ~30%
  reduction, plateauing near 0.40, matching the earlier ≈0.37–0.40 figure almost exactly once the hub is set aside. So the
  *bulk* of the hypergraph is moderately regular (CV ≈ 0.4–0.55) basically independent of both J0 and p over this range; it is
  not getting worse, but it is not converging to 0 either — a genuine, stable ~40–55% relative spread that any degree-based
  argument has to absorb, not eliminate.

## 5. Summary and what this means for a proof

* The formula in `curves_conjecture.md` §7 is exact for a = 0: 43,264/43,264 lines verified, 0 exceptions.
* **Small J alone is not enough** for the full G3-strong constant: J≤16 lines capture only 60–70% of the (pm1-only → full)
  saving; the rest needs the tail up to J ≈ p/2, and this fraction does not visibly drift with p — the tail is here to stay.
* **But a p-independent cutoff (J≤16) is enough to beat the 4/3 benchmark** (LP/N ≈ 1.18–1.19 < 4/3), with real margin, using
  a fixed, finite list of families — a strictly easier target than reproducing the ≈1.10 N minimum, and worth attempting as a
  standalone theorem if the full strong form stalls.
* **Degree concentration is not the obstruction §7a suggested it might be** — once the single, exactly-characterized
  box-corner hub (degree ≈ 2p, an artifact of this particular box's corner (p,p) plus f's oddness, not of the curve's rich-line
  structure in general) is excised, CV sits in a stable 0.38–0.56 band across every J0 and every tested p, matching the
  originally-reported ≈0.4 almost exactly. **A proof strategy of the form "handle (p,p) by hand (worth O(1)); argue
  near-regularity on the remaining 4p−1 points" looks more promising than the raw (hub-contaminated) numbers implied.**
  Restricting to small J does *not* help that near-regularity argument (CV is flat-to-mildly-improving in J0, not improving
  sharply) — but it does not hurt it either, once the hub is set aside; the difficulty is genuinely about the bulk's ~0.4–0.5
  CV, which is present at every scale, not something concentrated at small or large J that a clever cutoff would dodge.
* Negative/open: I have not attempted to check whether the box-corner hub is the *only* structural exception for other centred
  boxes (e.g. HJSW-style, or shifted so (p,p) is not a lattice point of the box), nor whether an analogous but weaker hub
  exists for f = x³ + ax with a ≠ 0 (odd symmetry is broken there, so the exact identity in §3 does not directly transfer —
  plausibly there is no single hub, or a different, milder one; untested here).
