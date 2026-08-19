# erdosproblems.com scan: computational research targets

Scope: candidates drawn **specifically from the erdosproblems.com database** (Thomas
Bloom's curated, actively-maintained catalogue of 1217 numbered Erdős problems), as
opposed to curated problem *lists* like Ben Green's or Guy's UPINT (`problem_lists_scan.md`)
or raw OEIS/arXiv trawling (`oeis_arxiv_scan.md`). Same C1-C4 rubric as the rest of this
directory: C1 decisive computation nameable in advance (publishable either way), C2 cost
estimable to an order of magnitude quickly, C3 small cases actually informative (not
pre-asymptotic), C4 verification exact and cheap. Each score 0-3, total out of 12.

**Method.** The site tags every problem's *informal status*. Six values exist:
`open`, `proved`, `disproved`, `solved`, and — critically — two we did not expect going
in: **`falsifiable`** ("open, but could be disproved with a finite counterexample") and
**`verifiable`** ("open, but could be proved with a finite example"), plus a ninth-ever
value **`decidable`** ("resolved up to a finite check"). This is *exactly* our C1 filter,
built into the source by a professional number theorist. We fetched all ~41 tag pages
(covers essentially the whole site; rate-limited to 10 req/min, respected) and
cross-checked completeness against the project's own GitHub mirror
([teorth/erdosproblems](https://github.com/teorth/erdosproblems), `data/problems.yaml`,
which we cloned directly). Result: the *entire* universe of site-flagged
finite-computation-resolvable open problems is **9 decidable + 27 falsifiable + 7
verifiable = 43 problems out of 1217**. We then read the full writeup (statement,
references, current frontier) for all 43, individually, off the live site. This report is
a complete census of that 43, not a sample.

**Deconfliction against this directory's existing documents:**
- `problem_lists_scan.md` already claims **Erdős-Straus conjecture (#242 here)** as its
  candidate #2 (score 11), citing the same [arXiv:2509.00128](https://arxiv.org/abs/2509.00128)
  (n<=10^18, Aug 2025) we independently found. Not re-proposed as new; see the rejected
  section below for our own read on it (we lean more skeptical of the "low duplication
  risk" verdict, but do not re-litigate it as a fresh pick).
- `problem_lists_scan.md` independently rejects **projective plane of order 12** on cost
  grounds; we reach the same verdict from erdosproblems.com's own writeup of the same
  problem (#723) — a clean cross-check between two unrelated sources.
- `problem_lists_scan.md`'s candidate #9 (central binomial coefficients, practical
  numbers) uses a **Kummer's-theorem carry-counting sweep** to avoid factoring huge
  binomial coefficients directly. We use the identical technique for a *different* problem
  (#699 below, Erdős-Szekeres binomial gcd) — independent convergence on the same tool,
  which raises our confidence in that technique's cost estimate.
- No other candidate below overlaps in subject with `SELECTION.md` or `oeis_arxiv_scan.md`.

## The trap we nearly walked into: "decidable" does not mean "computable by us"

All 9 `decidable`-tagged problems read, at first glance, like the best possible genre for
this group: a theorem proves the conjecture for "all sufficiently large n," leaving only
finitely many small cases. We chased all 9 down to their source papers. **In every case
we could pin a number on, the remaining gap is either non-explicit or explicitly
astronomical:**

- **#742** (Murty-Simon diameter-2-critical graphs, <=n²/4 edges): Füredi (1992) proves it
  for n > n₀ where **n₀ is a tower of 2's of height ≈ 10¹⁴**. Not a typo. The "finite
  check" is not reachable by any computation that will ever run.
- **#19** (Erdős-Faber-Lovász): proved for "all sufficiently large n" by a five-author,
  80+-page *Annals of Mathematics* absorption-method proof (Kang-Kelly-Kühn-Methuku-Osthus,
  2021/2023); no explicit threshold is stated anywhere we could find. Known explicitly
  resolved only below n=10 (Hindman, 1981) — the entire gap above that is of unknown size.
- **#547, #580, #556**: same disease, same root cause (Szemerédi regularity-lemma-based
  proofs by Zhao 2011 / Ajtai-Komlós-Szemerédi 1995 / Kohayakawa-Simonovits-Skokan 2005),
  which structurally produce tower-type or non-explicit constants.
- **#551** (Ramsey R(C_k,K_n)=(k-1)(n-1)+1): Keevash-Long-Skokan (2021) cover k >= C·log
  n/log log n for an *unspecified absolute constant C*. We cannot even get an
  order-of-magnitude C2 estimate without re-deriving C from their paper ourselves — which
  is new theoretical work, not computation.
- **#506** (min. circles from n points): resolved for n>393 (Elliott/Purdy-Smith), but the
  object being searched over is *continuous point configurations in R²*, not integers —
  exact enumeration (order-type databases) currently tops out near n≈15-16 even for
  specialists, hopelessly short of 393.
- **#475, #848**: technically finite, but the remaining threshold requires deriving an
  explicit constant from very recent (2024-2026), still-moving analytic number theory —
  real research, not verification.

**Conclusion: we are dropping "decidable" as a search filter for this group.** It is a
mathematically honest label, not a computationally actionable one. Our top 10 below comes
almost entirely from the `falsifiable`/`verifiable` buckets instead, where — unlike the
`decidable` cluster — most writeups cite a **concrete existing numerical frontier**
(10^10, 10^18, 10^22, 10^28...) rather than a qualitative "for n large enough."

## Table of the 10 best candidates

| # | Problem | Statement | What we'd compute | Current frontier (who/when) | C1 | C2 | C3 | C4 | Total | Risk (one line) |
|---|---------|-----------|--------------------|------------------------------|----|----|----|----|-------|------------------|
| 1 | [#375](https://www.erdosproblems.com/375) Grimm's conjecture | If n+1,...,n+k are all composite, can each be assigned a *distinct* prime factor? | Segmented factor-sieve + bipartite-matching (Hall's theorem) check over every maximal composite run up to 10^11-10^12 | n<=1.9x10^10, all k (Laishram-Shorey 2006) — 20 years stale | 3 | 3 | 3 | 3 | **12** | A failure would only be a *counterexample to Grimm*, not to Legendre's conjecture (which it implies) — don't oversell a positive result |
| 2 | [#398](https://www.erdosproblems.com/398) Brocard-Ramanujan (n!=x^2-1) | Are n=4,5,7 the only solutions to n!+1=x^2? | Modular quadratic-residue pre-filter over n, then exact big-integer square test on survivors, extending past 10^9 | n<10^9, Berndt-Galway (2000) — 25 years stale, no recent push found | 3 | 2 | 3 | 3 | **11** | Cost grows fast in n (n! has ~n log n digits); a careless implementation burns the budget on bignum arithmetic instead of filtering |
| 3 | [#366](https://www.erdosproblems.com/366) weaker Erdős-Mollin-Walsh (2-full n, n+1 3-full) | Does a 2-full n with (n+1) 3-full exist? (opposite order from the two known examples) | Enumerate consecutive-powerful pairs via the known Pell-recurrence families (Sentance 1981 / OEIS A118894), filter for the 3-full direction | n<10^22, zero examples of this direction (via completeness of OEIS A060355) | 3 | 3 | 2 | 3 | **11** | Depends on the Pell-family parametrization being *provably exhaustive*, not just empirically complete — verify against Sentance's proof before trusting a "no results" run |
| 4 | [#364](https://www.erdosproblems.com/364) Erdős-Mollin-Walsh (3 consecutive powerful numbers) | Do 3 consecutive powerful integers exist? | Same Pell-family machinery as #366, pushed to check the *middle* term too (triple, not pair) | n<7.38x10^28, via OEIS A076445 (no recent large-scale computational push; only 2025-26 theory papers on special subcases) | 3 | 2 | 2 | 3 | **10** | "Hopelessly hard... probably beyond reach" per a domain amateur's own assessment (Wroblewski, primepuzzles.net) — abc-conjecture-flavored; a real result is a range extension, not a proof either way |
| 5 | [#699](https://www.erdosproblems.com/699) Erdős-Szekeres binomial gcd | For 1<=i<j<=n/2, does gcd(C(n,i),C(n,j)) always have a prime factor >= i? | Kummer's-theorem carry-counting (no huge binomial coefficients materialized) sweep over n, i, j | Only one exception known at all (n=28,i=4,j=14); partial proof for j<=1.5i or n=2j (2026, AI-assisted per the site) | 2 | 3 | 2 | 3 | **10** | A fairly narrow, technical statement — a clean negative sweep is real but low-drama unless it finds a second exception |
| 6 | [#647](https://www.erdosproblems.com/647) Erdős-Selfridge tau(n) prize (£25, ~$44) | Is there n>24 with max_{m<n}(m+tau(m)) <= n+2? | Trivial O(N log N) divisor-count sieve + running max, pushed as far as budget allows | True at n=24; Erdős "extremely doubtful" more exist; **no computational search found published at all** | 2 | 3 | 2 | 3 | **10** | Nobody publishing a search may mean it's simply not deemed interesting enough, not that it's unexplored |
| 7 | [#779](https://www.erdosproblems.com/779) primorial + prime is prime | For P = product of first n primes, does a prime p in (p_n, P) with P+p prime always exist? | Certified big-integer primality search (BPSW/ECPP) extending n past 1000, one prime-candidate stream per n | n<=1000 (Deaconescu) | 2 | 2 | 2 | 3 | **9** | Heuristic failure probability is "ridiculously small" (~exp(-n^cn)) — expected outcome is a low-surprise range extension |
| 8 | [#835](https://www.erdosproblems.com/835) Johnson graph J(2k,k) coloring | Does chromatic number of J(2k,k) ever equal k+1 for k>2? | Exact chromatic-number computation (SAT/ILP with symmetry breaking) for the first unresolved case, k=10 | False for 3<=k<=8 (Brouwer's graph database); Ma-Tang prove false for all k not of form p-1 — next case is exactly k=10 (184,756 vertices) | 2 | 1 | 2 | 3 | **8** | Chromatic-number computation cost is genuinely hard to bound in advance; k=10 may be fine, k=12+ may not be |
| 9 | [#458](https://www.erdosproblems.com/458) LCM growth inequality | Is [1,...,p_(k+1)-1] < p_k*[1,...,p_k] for all k? | Direct lcm computation from prime tables, sweep k to the limits of available prime tables | No stated computational record; likely already implicit in existing large prime-gap tables | 1 | 3 | 1 | 3 | **8** | The interesting regime is tied to Legendre's conjecture and known prime gaps are nowhere near it — a sweep mostly reconfirms what's already known from gap tables, low novelty |
| 10 | [#848](https://www.erdosproblems.com/848) Erdős-Sárközy squarefree ab+1 | Is the extremal A subset of {1..N} with ab+1 never squarefree exactly the n=7(mod 25) class? | Constrained combinatorial optimization (residue-class structure per van Doorn's reduction) for small N | Density bound proved exact (1/25) for "sufficiently large N" (Sawhney, note dated 2025/26, AI-assisted); **no explicit N₀** given | 2 | 1 | 2 | 2 | **7** | We would have to derive our own explicit N₀ from Sawhney's sieve estimates before knowing what to check — real analytic-NT work, not pure computation |

## Explicitly rejected (tempting, but no)

- **[#242](https://www.erdosproblems.com/242) Erdős-Straus conjecture** (4/n=1/x+1/y+1/z). Textbook C1-C4 fit — and already claimed in `problem_lists_scan.md` at score 11. We independently found the same fact that makes us more skeptical than that document: the record moved from 10^17 to **10^18 in August 2025**, one year ago. This is not a stale target quietly waiting for anyone with 56 cores; it is a live frontier with visible recent movement by people specifically optimizing the covering-congruence sieve. Extending it further is plausible but is racing, not claiming empty ground.
- **[#7](https://www.erdosproblems.com/7) odd covering systems.** Erdős offered $25 to prove none exists; **Selfridge offered $2000** for a construction — unclaimed for 50+ years despite that bounty. Best partial construction has minimum modulus 40 (Nielsen); any full solution needs >=22 distinct odd prime-power moduli (Simpson-Zeilberger/Guo-Sun) with no known upper bound on their size. The search space is a combinatorial existence problem over unbounded moduli sets, not a "check n<=X" sweep — fails C2 outright. Active 2025 papers exist (arXiv:2507.16135, 2504.09579): specialists are already on it.
- **[#723](https://www.erdosproblems.com/723) projective plane of order 12.** Order 10 was ruled out only by a landmark ~1989 supercomputer search (Lam, Swiercz, Thiel) that was, by reputation, one of the most expensive individual computer proofs of its era. Order 12's search space is understood by the design-theory community to be far beyond that — 35+ years of silence since order 10 is itself the evidence. Independently rejected in `problem_lists_scan.md`.
- **[#107](https://www.erdosproblems.com/107) Erdős-Szekeres "Happy Ending" problem**, f(n)=2^(n-2)+1. f(6)=17 took 1500 CPU-hours in 2006 (Szekeres-Peters) — later re-verified in just 8.53 CPU-seconds by 2024 SAT encodings (Heule-Scheucher). That speedup is real, but it is the signature of a hyper-competitive specialist SAT-solving niche (Heule, Scheucher, Marić) already grinding exactly this problem with best-in-class tooling; f(7) is a combinatorial-explosion step up in order-type count, not "the same search, a bit bigger."
- **[#19](https://www.erdosproblems.com/19) Erdős-Faber-Lovász**, **[#742](https://www.erdosproblems.com/742) Murty-Simon diameter-2-critical**, **[#547/#580/#556](https://www.erdosproblems.com/547) regularity-lemma tree/cycle Ramsey bounds**, **[#551](https://www.erdosproblems.com/551) R(C_k,K_n)**, **[#506](https://www.erdosproblems.com/506) minimum circle count** — the whole non-explicit/tower-threshold "decidable" cluster discussed above.
- **[#672](https://www.erdosproblems.com/672) AP product = perfect power.** k=4..34 already fully resolved unconditionally by an active specialist program (Bennett, Győry, Hajdu, Pintér, Siksek — four papers, 2004-2020, each pushing k up by increments using deep Diophantine/Frey-curve machinery). The next increment is exactly the kind of thing that program is already doing, using tools well outside pure brute-force search.
- **[#475](https://www.erdosproblems.com/475) sequenceable sets in F_p.** Four overlapping asymptotic-regime papers from **2024, 2024, 2025, and 2026** (Kravitz; Bedert-Kravitz; Costa-Della Fiore; Pham-Sauermann; Bedert-Bucić-Kravitz-Montgomery-Müyesser; Müyesser-Pokrovskiy) — about as "actively being ground by a serious group" as a problem can look. Also fails C2: the object being searched over is a subset A of F_p, not a single integer range.
- **[#488](https://www.erdosproblems.com/488) density-doubling for multiples of a finite set.** Quantifies over *all finite sets A* — not a bounded parameter sweep, fails C2.
- **[#307](https://www.erdosproblems.com/307) prime reciprocal sets with product 1.** Only known lower bound is |P union Q|>=60 with no upper bound on prime size; even the easier coprime-relaxation has no known example. No natural cutoff to search to — fails C2.

## Top 3: five-line first-experiment plans

### #1 — Grimm's conjecture (#375)

1. Calibrate: reproduce Laishram-Shorey's n<=1.9x10^10 claim on a small sub-range first (e.g. verify the SDR/Hall's-theorem check against a few published near-tight composite runs) to confirm the pipeline before trusting any "no counterexample" output.
2. Segmented smallest-prime-factor sieve upward from 1.9x10^10, chunked to fit RAM (~10^9-wide segments), identifying every maximal run of consecutive composites per segment.
3. Per run of length k: build the bipartite graph {n+1,...,n+k} x {prime factors used} and test for a perfect matching (Hopcroft-Karp); a Hall-violator subset is the exact, machine-checkable counterexample certificate if one ever appears.
4. Parallelize by segment across the 56 cores; log the longest run and the "tightest" near-miss (smallest slack in Hall's condition) as auxiliary output regardless of outcome.
5. Ship either a counterexample with certificate, or "Grimm verified for all n <= X" (target: one to two orders of magnitude past 1.9x10^10) as a clean citable extension.

### #2 — Erdős-Mollin-Walsh cluster: consecutive powerful numbers (#364 + #366)

1. Read Sentance (1981) and confirm (don't just assume) that the cited Pell-recurrence families provably generate *all* consecutive odd powerful-number pairs — this completeness claim is the whole basis for C3/C2 here and must be checked against the primary source, not just OEIS's comment field.
2. Implement the recurrence generation in exact big-integer arithmetic, reproducing every known term below 10^12 exactly as a calibration step (per this group's own C2 protocol: check against known truth before trusting scale).
3. Push generation far past the current 7.38x10^28 / 10^22 frontiers (cheap: recurrence terms, not sieving) and, for each candidate pair, exactly factor the adjacent third number to test the triple/3-full condition.
4. Cross-verify with a second, independently-coded generator (different recurrence formulation) on an overlapping range before trusting any "no example" claim at record scale.
5. Report new verified bounds for both the #364 triple question and the #366 ordered-pair question — the latter comes almost free once the former's infrastructure exists.

### #3 — Brocard-Ramanujan, n!+1=x^2 (#398)

1. Calibrate against the known record: confirm the pipeline reproduces "no solution for 10^7<n<10^9 besides n=4,5,7" on a fast subrange before trusting anything past 10^9.
2. Build a cheap modular pre-filter: maintain n! mod m incrementally for a battery of small prime-power moduli m, rejecting any n where n!+1 is a non-residue mod any m (eliminates the overwhelming majority of n at near-zero cost).
3. For survivors, apply a second independent filter (different modulus set) before promoting to expensive exact arithmetic — matches this group's cross-verification-by-two-methods discipline.
4. On remaining survivors, compute n!+1 exactly and test for a perfect square via integer Newton's method (exact, no floating point).
5. Partition n-ranges across the 56 cores (factorial-mod state can be checkpointed and resumed per range); report an extended verified bound past 10^9, or — vanishingly unlikely per the heuristics but genuinely decisive if it happens — a fourth solution to a 150-year-old problem.
