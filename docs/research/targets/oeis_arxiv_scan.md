# OEIS / arXiv scan: computational research targets

Scope: OEIS sequences and arXiv (math.CO, math.NT, 2024-2026) papers that hand over an
explicit, finite computational frontier — a conjecture plus a stated verified range, or
"the smallest open case is X" — suitable for a ~56-core group whose edge is large-scale
exact computation, exhaustive enumeration, cross-verification, and negative results, not
new theory. Target compute envelope: ~10^4 core-hours per candidate.

**Sourcing caveat, read before spending any compute budget on any of this:** oeis.org
blocks direct fetches from this session's tooling (HTTP 403 on both `/search` and plain
`/Annnnnn` URLs), so most OEIS content below was pulled either through search-engine
snippets or through a text-proxy re-fetch. In the course of this scan the two different
maximal-determinant sequences (A013588 and A003432) briefly got their frontier numbers
cross-contaminated by a search-engine summary and had to be re-pulled and disentangled
by hand (see entry 9). Treat every number in this report as a lead to re-confirm from a
primary source (the OEIS entry itself, the paper PDF, or the maintainer's own page)
before committing cores — not as pre-verified ground truth.

Scoring: each candidate rated 0-3 on C1 (decisive, publishable-either-way computation
stated in advance), C2 (cost estimable within an order of magnitude quickly), C3 (small
cases are actually informative, i.e. not a pre-asymptotic trap), C4 (verification is
exact, cheap, integer arithmetic). Total out of 12.

## Scoring table

| # | Candidate | C1 | C2 | C3 | C4 | Total | One-line risk |
|---|-----------|----|----|----|----|-------|----------------|
| 1 | Ramanujan tau: perfect-power / distinctness / growth conjectures (OEIS A000594) | 3 | 3 | 3 | 3 | **12** | Needs a correct fast big-integer tau(n) implementation (eta^24 series or Niebur convolution) — engineering, not brute force. |
| 2 | Odd untouchable numbers, is 5 the only one? (OEIS A005114) | 3 | 3 | 2 | 3 | **11** | Strengthened-Goldbach heuristic makes a hit unlikely, so extension is mostly confirmatory rather than high-suspense. |
| 3 | Ideal Prouhet-Tarry-Escott solutions, size 11 (arXiv 2304.11254, 2506.11429) | 3 | 2 | 3 | 3 | **11** | Must confirm the existing search is genuinely exhaustive (not a restricted parametric family) before trusting a "still none found" result. |
| 4 | Zarankiewicz numbers z(m,n;3,3), small open cells (arXiv 2203.02283, 2605.01120) | 3 | 2 | 3 | 3 | **11** | Frontier is scattered across two papers' appendices — first task is pure bookkeeping to find an actually-open cell; at least 2 groups active here. |
| 5 | "Neither square nor square+prime" finiteness (OEIS A020495 / Conjecture H) | 3 | 3 | 2 | 3 | **11** | Li's O(n^0.982) density bound means new terms should get rarer, not a dead end but a softening lead. |
| 6 | Norin's conjecture on antipodal hypercube 2-colorings, n=9 (arXiv 2511.08386) | 3 | 1 | 3 | 3 | **10** | Cost trend from n=7->8 does not extrapolate safely; the paper's own authors are the obvious next people to try n=9. |
| 7 | Greedy B_5-set growth constant gamma_5(h) (arXiv 2312.10910) | 1 | 3 | 2 | 3 | **9** | Not a binary conjecture — it's asymptotic-constant estimation, weak fit for "publishable either way." |
| 8 | Unsolved octal games — extend Sprague-Grundy nim-sequences (Flammenkamp database) | 3 | 1 | 1 | 3 | **8** | Textbook pre-asymptotic trap: what's left already resisted 30 years of dedicated single-researcher computation to huge n. |
| 9 | Maximal-determinant problem, orders 11 and 22 (OEIS A013588, A003432) | 2 | 1 | 2 | 3 | **8** | Raw search space (2^121 at order 11) is astronomical; only tractable via imported design theory, and a failed structured search does not prove non-existence. |
| 10 | Sum-representations by 2^a*5^b+1 (Zhi-Wei Sun, OEIS A003592) | 2 | 1 | 2 | 2 | **7** | Verified range (n<=3700) is suspiciously small for how cheap the statement looks — per-term cost needs scoping before this is trustworthy. |

---

## Candidate detail

### 1. Ramanujan tau function: five sibling conjectures (score 12)
- **Source:** [OEIS A000594](https://oeis.org/A000594) — comments added by Zhi-Wei Sun, Dec 18-29 2024.
- **Statement:** Let a(n) = tau(n), the Ramanujan tau function. Sun conjectures, in a cluster:
  (i) |a(n)| (n>1) is never a perfect power; (ii) the |a(n)| are pairwise distinct;
  (iii) |a(n)| > 2n^4 for n>2; (iv) a(m)^2+a(n)^2 is never a perfect power; (v) |a(m)a(n)|
  is never a perfect power (m<n).
- **What we'd compute:** Exact tau(n) for n up to 10^9-10^10 via the eta(q)^24 power-series
  expansion (Euler's pentagonal-number sparse product, repeated squaring, exact big-integer
  coefficients) or the classical Niebur sigma-convolution formula, cross-checked against
  each other and against published small-n tables. Then run tests (i)-(iii) on every n up
  to that bound, and tests (iv)-(v) on all pairs up to whatever m,n range is affordable
  (O(N^2), likely 10^5-10^6).
- **Current frontier / who set it:** n up to 10^6 for the single-variable conjectures;
  m,n <= 1000 (sum of squares) and m<n<=5000 (product) for the pair conjectures. Set by
  Zhi-Wei Sun himself, by hand, three weeks before this scan (Dec 2024) — an individual
  mathematician, not a resourced group.
- **Risk note:** the conjecture-posing is nearly free; the actual work is a correct,
  validated, fast exact tau(n) pipeline. That's squarely an engineering task, not a
  theory task — good fit, but budget real implementation time, not just core-hours.

### 2. Odd untouchable numbers (score 11)
- **Source:** [OEIS A005114](https://oeis.org/A005114); Pomerance & Yang, ["On untouchable
  numbers and related problems"](https://math.dartmouth.edu/~carlp/uupaper3.pdf) (2012).
- **Statement:** 5 is conjectured to be the only odd untouchable number (a positive integer
  that is never sigma(m)-m for any m). Follows from a mild strengthening of Goldbach.
- **What we'd compute:** A near-linear sieve of s(m) = sigma(m)-m over all m up to a bound
  large enough to certify every odd k below N is "touched," re-implementing and first
  reproducing Pomerance-Yang's published list as a correctness gate.
- **Current frontier / who set it:** N = 10^8, Pomerance & Yang, 2012 — fourteen years
  stale, and their own paper states the algorithm is N^(1+o(1)), i.e. near-linear.
- **Risk note:** memory (bitset size for the sieve), not CPU, is likely the real binding
  constraint when pushing to 10^10-10^11 — profile that first.

### 3. Ideal Prouhet-Tarry-Escott solutions, size 11 (score 11)
- **Source:** [arXiv:2304.11254](https://arxiv.org/abs/2304.11254) "Ideal solutions in the
  Prouhet-Tarry-Escott problem"; [arXiv:2506.11429](https://arxiv.org/abs/2506.11429),
  2025 368-page survey.
- **Statement:** Do two disjoint 11-element integer multisets exist whose k-th power sums
  agree for all k=1..10 (the "ideal" case)? Known for sizes up to 10 and for size 12;
  unknown for size 11 and for every size >=13.
- **What we'd compute:** Reproduce the published exhaustive/parametrized search up to its
  stated height bound as a calibration check, then extend the height bound for size 11
  (and opportunistically 13) using a meet-in-the-middle search over the power-sum
  equations, parallelized across cores by height range / residue class.
- **Current frontier / who set it:** earlier surveys report searches to height ~2000
  with nothing found for size 11; the 2023-2025 papers "significantly extend" this but
  the exact new bound was not recoverable from the abstracts alone — first task below.
- **Risk note:** must first establish whether the published search is truly exhaustive
  over all integer tuples up to the height bound, or restricted to symmetric/parametrized
  families — that changes what a negative result actually proves.

### 4. Zarankiewicz numbers z(m,n;3,3) (score 11)
- **Source:** [arXiv:2203.02283](https://arxiv.org/abs/2203.02283) "An attack on
  Zarankiewicz's problem through SAT solving"; [arXiv:2605.01120](https://arxiv.org/html/2605.01120)
  "New Bounds for Zarankiewicz Numbers via Reinforced LLM Evolutionary Search" (2026).
- **Statement:** z(m,n;3,3) is the max number of 1s in an m x n 0/1 matrix with no all-ones
  3x3 minor (equivalently, max edges in a K_{3,3}-free bipartite graph). Exact values are
  known for only a scattered set of small (m,n).
- **What we'd compute:** SAT/ILP exhaustive search with permutation-symmetry breaking (as
  in the 2022 paper) to prove matching *upper* bounds for specific still-open small cells —
  complementing the 2026 paper, which only improved *lower* bounds (via a $30-per-instance
  LLM evolutionary search) for 41 cells that are "within one edge of the best known upper
  bound." Closing those gaps with an exact proof is exactly our profile.
  - **Current frontier / who set it:** jointly by the 2022 SAT paper (corrected + extended
  the classical tables) and the 2026 paper (Z(11,21,3,3)=116, Z(11,22,3,3)=121,
  Z(12,22,3,3)=132 newly exact; 41 more cells with improved lower bounds only).
- **Risk note:** first task is pure bookkeeping — merge both papers' tables to find a
  concrete open cell before writing any SAT encoding; this is an actively contested area.

### 5. "Neither square nor square+prime" (score 11)
- **Source:** [OEIS A020495](https://oeis.org/A020495).
- **Statement:** integers that are neither a perfect square nor (prime + square); only 22
  are known (largest 21679), conjectured to be a complete, finite list — a form of
  Hardy-Littlewood Conjecture H.
- **What we'd compute:** bit-sieve marking n = p + k^2 representable, for every prime p up
  to a new bound X, then scan for unmarked non-squares — direct extension of the existing
  method.
- **Current frontier / who set it:** verified to 3x10^9 by James Van Buskirk, noted in OEIS
  by Giovanni Resta, Jul 16 2019 — seven years stale.
- **Risk note:** Hongze Li proved at most O(n^0.982) such numbers exist below n, so this is
  a softening lead, not a coin flip; still fully rigorous and cheap either way.

### 6. Norin's conjecture, hypercube antipodal colorings, n=9 (score 10)
- **Source:** [arXiv:2511.08386](https://arxiv.org/abs/2511.08386) (Nov 2025).
- **Statement:** every 2-edge-coloring of the hypercube Q_n with antipodal edges
  differently colored contains a monochromatic antipodal path. Verified n<=7 (Frankston &
  Scheinerman, 2024); this paper extends to n=8 via a new compact SAT encoding with
  symmetry breaking and cube-and-conquer.
- **What we'd compute:** apply the same encoding/pipeline to n=9.
- **Current frontier / who set it:** n<=8, by this very recent (Nov 2025) paper. Their
  own reported cost: a prior estimate of 57.3 CPU-years for n=8 collapsed to 5 CPU-days
  with their improved encoding — a >4000x speedup from encoding cleverness alone.
- **Risk note (two-fold):** (a) their own clause-count table shows roughly a 4x jump from
  n=8 to n=9 already before solving starts, and SAT difficulty routinely scales far worse
  than clause count — the true cost could land anywhere from "trivial" to "10-100x over
  budget," we cannot tell without running it; (b) this is a hot, just-published technique
  on a named conjecture — the paper's own authors (and adjacent SAT-combinatorics groups)
  are the obvious next movers, real scooping risk.

### 7. Greedy B_5-set growth constant (score 9)
- **Source:** [arXiv:2312.10910](https://arxiv.org/abs/2312.10910) "Bounds for Greedy
  B_h-sets."
- **Statement:** for the greedy B_h-set, the 5th-smallest-index growth term gamma_5(h)
  is proven to satisfy (1/8)h^4 <= gamma_5(h) <= 0.467214h^4 + O(h^3), conjectured to
  equal (1/3)h^4 + O(h^3).
- **What we'd compute:** exactly construct the greedy B_5-set for a large systematic range
  of h (cheap — only the first 5 elements are needed per h) and regress the leading
  constant against the proven bounds and the 1/3 conjecture.
- **Current frontier / who set it:** the bounds above are the current published state;
  no large-scale numerical exploration of the constant across many h was found.
- **Risk note:** this is asymptotic-constant refinement, not a binary conjecture — weak
  fit for "publishable either way" even though the computation itself is trivial.

### 8. Unsolved octal games (score 8)
- **Source:** Achim Flammenkamp, [Sprague-Grundy values of octal games](http://wwwhomes.uni-bielefeld.de/achim/octal.html)
  (individual combinatorial-game-theory database, referenced throughout the "Games of No
  Chance" MSRI proceedings).
- **Statement:** Guy's conjecture: every octal game with a finite code has an eventually
  periodic nim-sequence. 65 two-place and 8 three-place octal games, plus Grundy's Game
  and game "0.6111...", remain unsettled.
- **What we'd compute:** extend the mex-rule nim-value computation for whichever unsettled
  games currently have the *smallest* computed frontier (needs pulling the raw
  `unsettled.txt` table directly, not through a summarizer, to rank targets), watching
  for the onset of periodicity.
- **Current frontier / who set it:** Flammenkamp, over roughly 30 years, has computed
  millions of nim-values per game; e.g. game .007 pushed to 2^25, game .106 to a
  preperiod of ~4.65x10^11. A new contributor ("Tyler Satchel Orden") is listed as
  extending sequences as of July 2026.
- **Risk note:** this is the report's clearest pre-asymptotic trap — the games still open
  are open *because* they already resisted decades of dedicated large-scale computation;
  another order of magnitude of core-hours is not obviously enough to flip any of them,
  and per-game algorithmic cost is not yet characterized well enough by us to budget.

### 9. Maximal-determinant problem, orders 11 and 22 (score 8)
- **Source:** [OEIS A013588](https://oeis.org/A013588) and [OEIS A003432](https://oeis.org/A003432);
  background at Orrick & Solomon's "Hadamard Maximal Determinant Problem" site.
- **Statement:** A013588(11) — the smallest positive integer that is *not* the determinant
  of any 11x11 {0,1}-matrix — is only known to be >=739 (open whether 739 itself is
  achievable). Separately, A003432(22) — the true maximal determinant for a 22x22
  {0,1}-matrix — is conjectured to be 662671875 (matching the Ehlich-Wojtas-type upper
  bound) but marked unconfirmed ("?").
- **What we'd compute:** a symmetry-reduced structured search (circulant / two-circulant
  constructions, as the specialist literature does) either producing a matrix that
  settles a(11)>739 or attains the order-22 bound, or exhausting the structured family.
- **Current frontier / who set it:** a(12)=2173 was fully settled by Brent, Orrick,
  Osborn & Zimmermann (2010); A003432(21) was confirmed correct as of Aug 2021. Both are
  maintained by a small, specialist academic niche (Orrick et al.), not a resourced group.
- **Risk note:** the raw search space (2^121 binary matrices at order 11) is astronomical
  and only tractable via imported design theory the group would need to substantially
  absorb; and — importantly — failing to find a matrix within *our* structured search
  family does not prove the true a(n)/a(22), only that this restricted family doesn't
  contain one. Asymmetric payoff: a find is a clean win, a non-find is a weak result.

### 10. Sum-representations by numbers of form 2^a*5^b+1 (score 7)
- **Source:** [OEIS A003592](https://oeis.org/A003592), conjecture submitted by Zhi-Wei
  Sun, Apr 18 2023.
- **Statement:** every positive integer n, except 1, 4, and 12, can be written as a sum of
  finitely many numbers of the form 2^a*5^b+1 (a,b>=0), none dividing another.
- **What we'd compute:** not yet well-defined — first need to understand why the verified
  range is so small (n<=3700) for a statement that looks this cheap; likely the per-n
  search (an antichain/subset-cover search over candidate terms) is combinatorially
  expensive in a way that needs a smarter exact method (ILP / branch-and-bound) before
  a brute-force extension is even worth costing out.
- **Current frontier / who set it:** n<=3700, Zhi-Wei Sun, Apr 2023.
- **Risk note:** included at low confidence specifically because the small verified range
  is a warning sign, not an invitation — this needs a scoping spike before any commitment.

---

## Top 3: first-experiment plans

### #1 — Ramanujan tau perfect-power conjectures (A000594)
1. Implement tau(n) two independent ways (eta(q)^24 sparse power-series expansion via
   repeated squaring; Niebur's sigma-convolution formula), for n = 1..10^5, and check both
   agree with each other and with a published reference table.
2. Scale the faster/simpler method to N = 10^7 as a pilot; measure wall-clock and memory
   per 10^6 values to get a real (not guessed) cost-per-order-of-magnitude number.
3. Extrapolate that measured cost to decide the actual target N (10^9? 10^10?) that fits
   inside the ~10^4 core-hour budget, then shard by residue class/block across 56 cores.
4. Run all five tests (perfect power, distinctness, growth bound, and the two pairwise
   tests on an affordable m,n sub-range) with exact integer arithmetic throughout.
5. Any positive hit gets re-derived independently before being reported; a clean negative
   result is written up as a 3+ order-of-magnitude extension of Sun's Dec-2024 ranges.

### #2 — Odd untouchable numbers beyond 10^8 (A005114)
1. Obtain Pomerance & Yang (2012) in full and extract their exact sieve/algorithm and the
   precise relationship between the certification bound N and the required range of m.
2. Re-implement it and reproduce their published untouchable-number list up to 10^6-10^8
   exactly, as a hard correctness gate before trusting any new output.
3. Profile memory footprint of the sieve bitset(s) at the target N first — this is
   expected to be the binding constraint, not CPU.
4. Parallelize by splitting the m-range into blocks across 56 cores, merging bitsets.
5. Push N two to three orders of magnitude past 10^8 and report either a new odd
   untouchable number (extraordinary, immediate) or a fully reproducible extended bound.

### #3 — Ideal PTE solutions, size 11 (arXiv 2304.11254 / 2506.11429)
1. Read both papers (and their cited predecessors) closely enough to state, in one
   sentence, the *exact* current search bound for size 11 and whether the method is a
   genuinely exhaustive integer search or restricted to a parametrized family.
2. Reproduce their reported "no solution below height H" result at a small scale as a
   calibration check before trusting or extending it.
3. Implement a meet-in-the-middle exhaustive search over the size-11 power-sum equations,
   sharded by height range / residue class across 56 cores.
4. Track wall-clock per unit of height as the search runs, to keep the cost estimate
   honest rather than committing the full budget on a guess.
5. Push the height bound as far as budget allows; report a genuine solution (a notable
   first) or a peer-checkable extension, and cross-submit results to the existing PTE
   research community for independent validation.

---

## Explicitly rejected candidates

**Ramsey number R(5,5).** Tempting — it's the most famous unresolved small Ramsey number
(bounds stuck at 43 <= R(5,5) <= 48 since 1997/1989 on the outer ends), and it's
squarely "our kind of problem" on the surface. Rejected: the 2017 proof of R(5,5)<=48
alone required computer verification of roughly two trillion cases by Angeltveit &
McKay, who have since pushed the bound to <=46 (2024/2026) and are evidently still
actively working it with bespoke, years-in-development code. Not reachable in 10^4
core-hours, and duplicative of a team that already has a multi-year head start.

**Van der Waerden numbers beyond the ~7 known exact values (e.g. w(4,4)).** Tempting
because the definition is trivial to state and the known values (w(2,3)=9 up through
w(2,6)=1132, w(3,3)=27, w(3,4)=293) show real problems do get solved here. Rejected: a
dedicated BOINC volunteer-computing project (thousands of machines) has been grinding on
the next tier for well over a decade, producing only bound tightenings, never a new exact
value. The coloring search space grows so fast that there is no reason to expect 56 cores
to succeed where a crowd-sourced project an order of magnitude larger has not.

**Aliquot sequences / sociable-number chains (the "Lehmer five": 276, 552, 564, 660,
966...).** Tempting — completely elementary to state, decades of open fate for a handful
of small starting values. Rejected: extending these sequences requires factoring
numbers that grow to several hundred digits, which is a fundamentally different
computational discipline (GNFS/ECM factoring infrastructure) from exact enumeration or
exhaustive search. A dedicated global volunteer community (factordb.com, the
mersenneforum.org "aliquot sequences" project) has owned this space with purpose-built
tooling for 20+ years. Wrong tool for this team, not just a hard problem.

*(Also considered and set aside for the same "wrong tool, well-resourced incumbent"
reason: PrimeGrid's generalized-Fermat / Sierpinski-Riesel search space, which
OEIS A079706's "a(n) unknown for n=19,25,31,..." leads directly into.)*
