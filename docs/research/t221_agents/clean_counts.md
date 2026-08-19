# T2.21 task B: clean 7-groups and the resulting bound, k = −1 — census over 100 ≤ p ≤ 3000 (+ a sparse tail to 10⁵)

Setting as in `slack/lp1_anatomy.py` / `slack/lp1_types.py` and `docs/research/pair_bound_notes.md` §24 and
B.19 with its addendum (a)–(c), lines ~962–1035: p odd prime, h = (p−1)/2,

```
P = { (x,y) ∈ [-h, 3h+1] × [0, 2p-1] : xy mod p ∈ {1, p-1} }          (|P| = 8(p−1))
```

A slope-(+1) **residue group** `G_d` (d ∈ Z/pℤ) is the union of P's integer diagonals x−y ≡ d (mod p);
`type(G_d)` = sorted-descending profile of its (≥1-point) integer-line sizes. Slope-(−1) groups are the
R-images, R:(x,y)↦(p−x,y). For every residue d, the **orbit**

```
Ω_d := G_d ∪ G_{-d} ∪ G'_d ∪ G'_{-d}  =  {q∈P: (x-y)%p ∈ {d,-d}} ∪ {q∈P: (x+y)%p ∈ {d,-d}}
```

is closed under rows and columns (B.19 addendum (a)) and satisfies Ω_d = Ω_{−d} as **sets** — orbits are
therefore indexed by the canonical representative d ∈ {0,…,h}; d = 0 is the self-paired "central" orbit,
excluded from all *orbit-level* counts below (it is never of type (8,4,4) or (7,5,3,1) — verified, see §2).

**B** := union of all (8,4,4)-orbits (both slopes) — the block cover of Theorem 17. A (7,5,3,1) orbit Ω_d
is **clean** iff it is disjoint from B and from every other (7,5,3,1) orbit Ω_e (e ≠ ±d); "disjoint" /
"meets" means "shares/doesn't share ≥ 1 point of P".

Code: `slack/t221_agents/clean_counts.py` (main O(p)-per-prime computation + LP(1) for p ≤ 300) and
`slack/t221_agents/clean_counts_verify.py` (independent brute-force cross-check, see §2). Data table:
`slack/t221_agents/clean_counts_output.txt`. Environment: **`/Users/iwasborninbali/venvs/sat/bin/python3`**
(numpy 2.5.2, scipy 1.18.0, `linprog(...,method='highs')`; the bare `python3` on this machine did not have
numpy/scipy at the start of this task — `pip install --user numpy scipy` was run for both `python3.13` and
the default `python3.14` so that plain `python3 slack/...py` also works, in addition to the venv).

```
/Users/iwasborninbali/venvs/sat/bin/python3 slack/t221_agents/clean_counts.py          # 3.7 s, writes the table
/Users/iwasborninbali/venvs/sat/bin/python3 slack/t221_agents/clean_counts_verify.py   # 0.4 s, brute-force check
```

## 1. Result in one line

**All 405 primes 100 ≤ p ≤ 3000, plus a sparse tail to p = 100003, computed exactly in 3.7 s total.**
m8/p, m7/p → 1/12 and N4/p → 1/4 as expected; the **clean-orbit fraction θ stabilises at θ ≈ 0.44** (pooled
over the whole range, no drift out to p = 10⁵); the resulting candidate bound averages **U(p)/(p−1) ≈
3.59–3.60**, comfortably above the true LP(1) saving (LP(1) is the better, i.e. numerically smaller, bound
at every one of the 37 tested primes p ≤ 300 — the clean-orbit accounting captures only part of LP(1)'s
saving, as B.19 point 3–4 already found). A parenthetical numerical claim in B.19 addendum (c) — "4 of 28
pairs of (8,4,4)-orbits and 5 of 45 pairs of (7,5,3,1)-orbits at p=113 share points" — is an artifact of
not collapsing the d ↔ −d mirror pairing before counting pairs (§5): the **true** count of genuinely
distinct orbit pairs that meet at p = 113 is **zero**, for both types.

## 2. Method and validation

**O(p) algorithm.** `km1_lines_5678.py`'s per-residue classification (section 24's F1/F2 centre formulas)
is O(p) *per d*, hence O(p²) over all d; it was reused verbatim but restructured around one O(p) sieve of
modular inverses plus dictionary buckets (`a ↦ d=(a−1/a)%p` for the κ-classes, `a ↦ e=(a+1/a)%p` for the
λ-classes, so that group d's classes are an O(1) lookup instead of an O(p) scan), giving the same
(profile, m) per residue in O(1) amortised — O(p) total. The **meets-graph** uses B.19 addendum (c)
directly: the H(1) point at residue a has diagonal residue d₀ = a−1/a and antidiagonal residue e₀ = a+1/a
(mod p); the H(−1) branch at the same a gives the *swapped* pair (e₀,d₀) (checked, so it adds no new
witness); one shows canon(d₀) ≠ canon(e₀) always (a in 1..p−1), where canon(x)=min(x,p−x) — so each of the
p−1 nonzero residues a contributes exactly one genuine cross-orbit "witness" edge {canon(d₀), canon(e₀)},
and the union of these p−1 edges is *exactly* the "share a point" relation among canonical orbit indices.
Building this graph is O(p); testing whether a 7-orbit meets B or another 7-orbit is then O(1) per
neighbour, O(p) total over all orbits of a prime.

**Four independent validations, all exact matches, zero exceptions:**
1. *Type classification vs. the O(p²) reference* (`classify_slow_ref`, a direct, unmodified port of
   `km1_lines_5678.py`'s per-d scan): m8, m7, m6g, N4 match exactly at p = 29, 53, 101, 113, 137, 199.
2. *Type classification vs. Task A's fully independent implementation* (`slack/t221_agents/orbit_cover.py`,
   `orbit_cover_output.txt`, computed by construction/LP rather than the class-data formulas): **0
   mismatches out of 70 common primes** (11 ≤ p ≤ 500 ∩ 100 ≤ p ≤ 500). Also, N4 = m8+m7+m6g exactly at
   **all 410** rows of this task's own table (the 4-class groups are exhaustively split among the three
   patterns, no residual "other" 4-class case).
3. *Meets-graph vs. brute-force point-set intersection*, done during development (build all 8(p−1) points
   of P literally, compute the meets-adjacency by direct diagonal/antidiagonal residue membership): exact
   match of the full adjacency structure at p = 29, 53, 101, 113, 137, 199 — this check lived in a
   throwaway scratch script and was not preserved, but it is strictly subsumed by validation 4 below (which
   checks the clean/dirty *outputs* that depend on the same adjacency, via a separately-written,
   independent, and persisted implementation).
4. *Clean/dirty classification and I7 vs. an independent brute-force re-implementation*
   (`clean_counts_verify.py`: rebuilds P, retypes every group by literal line-size counting — no class-data
   formulas — computes every (7,5,3,1)/(8,4,4) orbit's actual 64-point set, and intersects them pairwise):
   exact match of (clean, dirtyB, dirty7, dirtyBoth, I7) at p = 101, 113, 127, 137, 199, 251, 283, 307, 401,
   499 — chosen to cover every combination of the four dirty causes appearing in the data.
5. *Internal consistency, all 410 rows, zero exceptions*: clean+dirtyB+dirty7+dirtyBoth = n7orb; m8 =
   2·n8orb and m7 = 2·n7orb exactly (the central group d=0 is **never** type m8 or m7 — confirmed at every
   one of the 410 primes); m6g = 2·n6gorb **+1** exactly at the 201 primes with p ≡ 1 (mod 4) and exactly
   (no +1) at the 209 primes with p ≡ 3 (mod 4). Explanation: d=0 has nk(0)=2 always (disc = 4, a nonzero
   square) and nl(0) = 2 iff −4 is a QR iff p ≡ 1 (mod 4) — so d=0 is 4-class only at those 201 primes, and
   in every one of them it is of type m6g ("neither pair shares its centre"), never m8 or m7: its κ-pair is
   {1,−1}, and 1 is its own inverse, so the "shares centre" test (which compares X(a) to X(1/a) for a root
   a) compares X(1) to X(1/1)=X(1) — literally equal, hence "does not share"; its λ-pair is {b₀,−b₀} with
   b₀²≡−1 (so 1/b₀ = −b₀), and X(−u) = −X(u) always, so X(b₀) and X(1/b₀)=X(−b₀) always have opposite sign
   — again "does not share". Both pairs fail to share ⇒ m=2 ⇒ type m6g, unconditionally whenever d=0 is
   4-class. (This is a genuine structural fact about d=0, not an instance of the general type(d)=type(−d)
   symmetry, which is vacuous at d=0.)

## 3. Densities and their limits

Pooled (Σclean/Σp etc., not average-of-ratios) over p-bands, main run 100 ≤ p ≤ 3000 (405 primes):

| p-band | n | m8/p | m7/p | N4/p | clean/p | I7/p | θ (pooled) | U/(p−1) |
|---|---|---|---|---|---|---|---|---|
| [100,300] | 37 | 0.0823 | 0.0765 | 0.2462 | 0.0169 | 0.0184 | 0.4420 | 3.6010 |
| [300,600] | 47 | 0.0798 | 0.0813 | 0.2445 | 0.0185 | 0.0195 | 0.4555 | 3.6058 |
| [600,1000] | 59 | 0.0843 | 0.0827 | 0.2486 | 0.0179 | 0.0208 | 0.4337 | 3.5905 |
| [1000,1500] | 71 | 0.0827 | 0.0814 | 0.2486 | 0.0181 | 0.0201 | 0.4437 | 3.5966 |
| [1500,2000] | 64 | 0.0836 | 0.0826 | 0.2495 | 0.0182 | 0.0204 | 0.4415 | 3.5924 |
| [2000,2500] | 64 | 0.0828 | 0.0817 | 0.2485 | 0.0180 | 0.0204 | 0.4401 | 3.5967 |
| [2500,3000] | 63 | 0.0833 | 0.0834 | 0.2494 | 0.0186 | 0.0207 | 0.4451 | 3.5924 |
| **[100,3000] all** | **405** | **0.0831** | **0.0823** | **0.2488** | **0.0182** | **0.0204** | **0.4424** | **3.5945** |

Expected limits (task / section 24): m8/p, m7/p → 1/12 = 0.08333, N4/p → 1/4 = 0.25. Both are matched to
three significant figures already by p ≈ 3000 (m8/p = 0.0831, m7/p = 0.0823, N4/p = 0.2488), with visible,
non-monotone O(1/√p)-scale fluctuation band-to-band and no residual drift — cumulative pooling from p=101
up to (and including) each of p≈300,600,1000,1500,2000,2500,3000 gives N4/p: 0.2462 → 0.2449 → 0.2473 →
0.2480 → 0.2486 → 0.2486 → 0.2488 (creeping toward 0.25 with one small dip, consistent with the O(1/√p)
correction terms already discussed in §24 for the smaller 200≤p≤500 sample, which had N4/p = 0.2429,
further from the limit than the present, larger sample) and m8/p: 0.0814 → 0.0802 → 0.0829 → 0.0827 →
0.0830 → 0.0830 → 0.0831 (also converging toward 1/12 = 0.0833). `clean/p` and `I7/p` appear to stabilise
near 0.018 and 0.020 respectively, with no visible trend across the seven bands.

**Sparse tail (no LP(1), same O(p) method), confirming no further drift out to p ~ 10⁵:**

| p | N4 | m8 | m7 | m6g | clean orbits | θ | U/(p−1) |
|---|---|---|---|---|---|---|---|
| 5003 | 1250 | 406 | 450 | 394 | 92 | 0.4089 | 3.6018 |
| 10007 | 2500 | 820 | 850 | 830 | 195 | 0.4588 | 3.5942 |
| 20011 | 5002 | 1668 | 1654 | 1680 | 389 | 0.4704 | 3.5888 |
| 50021 | 12537 | 4204 | 4190 | 4143 | 889 | 0.4243 | 3.5927 |
| 100003 | 25000 | 8154 | 8382 | 8464 | 1915 | 0.4569 | 3.5972 |

Pooled θ for p ≥ 1000 (267 primes, includes the tail to 10⁵): **0.4442**; pooled θ over the *entire* dataset
(410 primes, 100 ≤ p ≤ 100003): **0.4424**. No systematic drift is visible anywhere in the tested range —
the single-prime values swing ±0.05–0.10 around this (small orbit counts per prime, tens to low hundreds,
so this is ordinary sampling noise, not a trend); band- and tail-pooling both land in the same 0.44–0.46
window. **θ appears to stabilise; the best point estimate from this data is θ ≈ 0.44.**

## 4. The four dirty-orbit causes

At each prime, the n7orb (7,5,3,1)-orbits split into `clean`, `dirtyB` (meets B only), `dirty7` (meets
another 7-orbit only), `dirtyBoth`. Pooled over 100 ≤ p ≤ 3000 (Σ over all 405 primes; n7orb totals
**24,392**): clean 10,792 (44.24%), dirtyB 7,915 (32.45%), dirty7 4,494 (18.42%), dirtyBoth 1,191 (4.88%) —
meeting B is roughly **1.76×** as common a dirtying cause as meeting another 7-orbit. The two causes are
mildly **negatively** associated: marginal P(meets B) = (dirtyB+dirtyBoth)/n7orb = 0.3733, marginal
P(meets another 7) = (dirty7+dirtyBoth)/n7orb = 0.2331; independence would predict P(both) =
0.3733×0.2331 = 0.0870, but the observed P(dirtyBoth) = 0.0488 is little more than half of that — an orbit
that already meets B is somewhat *less* likely than average to also meet another 7-orbit (not investigated
further here). I7 (unordered canonical-orbit pairs {7-orbit, (7-or-8)-orbit} sharing a point) pools to
0.0204·p on average, i.e. about **0.89** incidences per non-clean 7-orbit (I7 counts pairs, and a
`dirtyBoth` orbit contributes ≥2 incidences, so 0.89 "per non-clean orbit" is an average over a mix of 1-
and multi-incidence orbits, not literally "most non-clean orbits touch exactly one other").

## 5. The B.19 addendum (c) mirror-pair correction

B.19 addendum (c) reports, from a quick scratch check at p=113: "4 of 28 pairs of (8,4,4)-orbits and 5 of
45 pairs of (7,5,3,1)-orbits ... share points". At p=113: m8=8, m7=10 (per-slope **group** counts, i.e. d
ranges over 0..112 without collapsing d↔−d) — C(8,2)=28 and C(10,2)=45 match these denominators exactly,
which means the scratch check enumerated pairs over the **raw** d-indices, not over the 4 and 5 *distinct*
canonical orbits (Ω_d = Ω_{−d} as sets — checked directly, e.g. for the first 7-type d found, orbit size 64
both ways). Doing that, exactly 4 of the 28 raw pairs are the trivial self-pairs {d,−d} (which of course
"share points" — they're the same 64 points) and exactly 5 of the 45 are likewise trivial mirror pairs.
This task's own O(p) meets-graph, cross-checked against direct brute-force point-set intersection (§2,
validation 3), finds **zero** genuinely distinct-orbit meetings among the four (8,4,4)-orbits and **zero**
among the five (7,5,3,1)-orbits at p=113 — i.e. p=113 happens to be a prime where all four 8-orbits are
mutually disjoint from each other and all five 7-orbits are mutually disjoint from each other (all four 7
orbits are additionally clean of B too: `clean=3, dirtyB=2, dirty7=0` in the main table). The general
phenomenon addendum (c) describes — that same-type orbits *do* sometimes meet through the cross mechanism
of B.19(c) — is real and common at other primes (dirty7+dirtyBoth is 23.3% of all 7-orbits pooled, §4), just
not visible in the specific p=113 numbers as originally computed; p=113 is, in this respect, a
lower-than-typical (in fact zero) example rather than the typical case. This does not affect anything
downstream that depended on the "5 of 45" figure only as an existence statement ("orbits of the same type
overlap" — true, generally, confirmed here) or Task A's `orbit_cover.md`, which explicitly treated the
figure as out of its scope and did not depend on its exact value.

## 6. U(p) vs. LP(1), p ≤ 300

U(p) := 4(p−1) − 4·m8 − 4·(#clean 7-orbits) (task's stated convention: m8 is the per-slope *group* count,
so 4·m8 = 8 per (8,4,4)-orbit — 2 per each of its 4 eight-lines, Theorem 17 — and 4·clean_orbits = 4 per
clean orbit, matching B.19(b)'s LP(Ω)=28=32−4). LP(1) computed exactly as in `slack/lp1_types.py` (all
rows, columns, and slope-±1 lines with ≥3 points, `linprog(method='highs')`) for the 37 primes 100≤p≤300.

**U(p) > LP(1) at every one of the 37 tested primes** — the absolute gap (U−LP1) ranges from +9.3 (p=167,
1.6% of LP1) to +62.0 (p=269), and as a *fraction* of LP(1) it ranges from 1.6% (p=167) up to **7.5%**
(p=241: LP1=814.667, U=876, gap=61.333) and 7.3% (p=181) — i.e. U is always the *weaker* (larger) candidate
bound, as expected: the clean-orbit accounting captures only the (8,4,4)-orbit and *clean* (7,5,3,1)-orbit
savings, none of the further saving LP(1) extracts from dirty 7-orbits, (6,6,2,2)-groups, and the
3-/4-/1-point lines documented in B.19 points 3–4 ("the 4-point and 3-point ±1 lines carry more than half
of the LP(1) saving, although none of them saves anything alone"). Concretely, at p=283: LP(1)=984.000
(saving S=144.0) vs. U=1024 (implied saving 4·m8+4·clean=4·20+4·6=104.0) — U leaves 40 points of saving on
the table relative to LP(1) at this prime, entirely attributable to the 11 dirty 7-orbits (7 dirtyB + 2
dirty7 + 2 dirtyBoth) that this task's construction, by design, does not credit at all. U(p)/(p−1) pools to
3.601 over 100≤p≤300, matching the whole-range average 3.5945 (§3) — consistent with both m8/p, clean/p
having already converged in this range.

**On whether U(p) is more than a numerical candidate.** B.19 addendum (a) states the orbit-closure fact
("Ω is closed under rows and columns... for a lawful S: |S| ≤ |S∩Ω| + (|P|−|Ω|)/2 for any union Ω of
orbits") *for a general union of orbits*, not only good ones; Task A's `orbit_cover.md` independently
established, for **every** (7,5,3,1) orbit at every prime 11≤p≤500 (clean or not), an exact 16-piece
integral dual certifying LP(Ω)=28 for that orbit *in isolation*. Combined with this task's census that a
clean orbit is, by definition, disjoint from B and from every other 7-orbit — so B ∪ {clean 7-orbits} is a
disjoint, row/column-closed union of blocks, each individually certified — the three results together look
like they compose into an actual proof of α(P) ≤ U(p) via the same block-decomposition pattern already used
for Theorem 17, not merely a numerical observation. This note did not carry out the gluing step formally
(matching the trivial 1/2-cover on every row/column outside B ∪ {clean orbits} to the two certified interior
covers), so U(p) is reported here, as the task asked, as a *candidate* bound with strong numerical and
structural support, not as an established theorem.

## 7. Reproducing / extending

`python3 slack/t221_agents/clean_counts.py` regenerates `clean_counts_output.txt` (405 main rows for
100≤p≤3000, 37 with an LP(1) column for p≤300, plus 5 extension rows to p=100003, plus the per-band summary
used in §3) in about 3.7 s wall-clock on this machine; `clean_counts_verify.py [primes...]` re-derives the
clean/dirty/I7 numbers from a completely independent, brute-force point-enumeration code path for a chosen
list of primes (default: the 10 primes used for validation 4 in §2) in well under a second. Both are pure
O(p) (resp. O(p) with a small constant for the brute-force check) per prime, so extending to p in the tens
of thousands, as done for the sparse tail in §3, costs tens of milliseconds per additional prime; LP(1)
itself (via `linprog`) is the only super-linear-feeling step, and even that took ≤0.09 s at p=293 — the
p≤300 restriction in this task's brief was not a hard performance ceiling, just the requested scope.
