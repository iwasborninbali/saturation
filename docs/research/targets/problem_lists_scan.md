# Curated open-problem-list scan: computational research targets

Scope: candidates drawn specifically from **curated open-problem lists** — Ben Green's
"100 Open Problems" (updated through Jan 2026), Guy's *Unsolved Problems in Number
Theory* topics with an explicit finite verified range, Brass-Moser-Pach-style discrete
geometry, combinatorics on words, small/multicolor Ramsey-type numbers, finite geometry
(arcs/caps/blocking sets/MDS), design theory, extremal graph/hypergraph small cases, and
packing/covering records — as opposed to raw OEIS/arXiv trawling (that source type is
already covered by `oeis_arxiv_scan.md` in this directory) or the group's own prior
project experience (`SELECTION.md`). Method: 4 parallel research passes (async forked
agents) covering number theory, finite geometry/design theory, discrete
geometry/packing-covering, and combinatorics-on-words/extremal graphs, plus direct work
by this scout on Ben Green's list itself and the small/multicolor Ramsey number survey
(Radziszowski's DS1, live PDF pulled and grepped directly rather than trusting
summarizer output). Same C1-C4 rubric as the rest of this directory: C1 decisive
computation specifiable in advance (publishable either way), C2 cost estimable to an
order of magnitude quickly, C3 small cases actually informative (not pre-asymptotic),
C4 verification exact and cheap. Baseline throughput assumption used throughout:
56 cores x ~10^9 simple ops/s =~ 5.6x10^10 ops/s =~ 1.5x10^17 ops/month (SAT-bound
problems are far slower per "logical step" than this — flagged per-item where relevant).

**Deconfliction against this directory's existing documents (read before either was
duplicated):**
- `SELECTION.md` (linux-12c's internal contribution, same date) already claims **Costas
  arrays n=32/33** as its own "first candidate for measurement" and a **3D analogue of
  the group's current no-three-in-line project** ([n]^3, no three collinear) as a fourth
  internal candidate. Neither is proposed again here. Their C1-C4 protocol is identical
  to the rubric used below, which let some of this scan's estimates be cross-checked
  against theirs directly (see "Cross-verification notes" below).
- `oeis_arxiv_scan.md` already covers Zarankiewicz numbers, odd untouchable numbers,
  Ramanujan tau conjectures, PTE solutions, and has already independently rejected
  R(5,5), van der Waerden numbers beyond the known values, and aliquot sequences. None
  of those are re-proposed as new here; R(5,5) is repeated in the rejected section below
  only because the parent task explicitly requires it, with the independent-rejection
  match noted.
- Per task instructions, **Ben Green's Problem 72 (no-three-in-line) is out of scope —
  already taken.**

---

## Table of the 10 best candidates

| # | Candidate | Source | Statement | What we'd compute | Current frontier (who/when) | C1 | C2 | C3 | C4 | Total | Risk (one line) |
|---|-----------|--------|-----------|--------------------|------------------------------|----|----|----|----|-------|------------------|
| 1 | (k,3)-arcs / "no four collinear" extremal sets in PG(2,q), next unclassified q | [Green Problem 68](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf); [arXiv:1908.10772](https://arxiv.org/pdf/1908.10772); [arXiv:1201.2260](https://arxiv.org/pdf/1201.2260) | Largest point set in PG(2,q) meeting every line in <=3 points; Green asks whether the true growth constant is 1 or 2 (a factor-2 gap between (1+o(1))q and (2+o(1))q) | Isomorph-free canonical-augmentation classification of maximum (k,3)-arcs for the next open q beyond the published tables (q>32) | Exact classification published up to q~=31-32 (Marcugini-Pambianco-Napolitano school, ongoing 20+ yr program) | 2 | 3 | 3 | 3 | **11** | Green's problem is stated over the *affine* plane F_p^2, existing tables are *projective* PG(2,q) — verify the translation before coding anything; also a crowded specialist niche |
| 2 | Erdos-Straus conjecture: extend verified range | [Guy UPINT]; [arXiv:2509.00128](https://arxiv.org/abs/2509.00128) | Is 4/n = 1/x+1/y+1/z solvable in positive integers for every n>=2? | Push the residue-class-covering sieve (mod 840, or the finer mod-25878772920 covering of the 2025 paper) from 10^18 to 10^19-10^20; report a clean extension or a counterexample | n<=10^18, Mihnea & Dumitru, Aug 2025 (an individual/small-team result, not a large distributed project) | 3 | 3 | 2 | 3 | **11** | A second small team is actively working the same frontier right now — real but low-stakes duplication risk since any extension is independently citable |
| 3 | Small Ramsey number: close the gap on R(3,10) or the next-tightest classical Ramsey gap | [Radziszowski DS1 survey](https://www.combinatorics.org/files/Surveys/ds1/ds1v17-2024.pdf); [arXiv:2401.00392](https://arxiv.org/pdf/2401.00392) | Is R(3,10) equal to 40 or 41? (Gap of exactly 1 — smallest live gap in the classical 2-color table) | Orderly/canonical generation of triangle-free graphs on 40 vertices with independence number <=9, encoded as SAT with DRAT proof certificates, OR independent re-verification of any claimed resolution | R(3,10) in {40,41}: lower bound 40 (explicit construction), upper bound 41, Angeltveit, Jan 2024 | 3 | 2 | 3 | 3 | **11** | Independently proposed by this same group's own `SELECTION.md` (linux-12c) — convergent validation, but also means real internal + external competition for the same target |
| 4 | Near-diagonal "minus-edge" Ramsey numbers: next open case after R(K5,K5-e)=30 | [arXiv:2602.11459](https://arxiv.org/html/2602.11459); [arXiv:2107.04460](https://arxiv.org/pdf/2107.04460) | R(K5,K5-e) was just determined exactly; the same census-generation + LP + SAT-gluing pipeline is a template for the next case in the Kk(-e) vs Kl(-e) family | Re-run Goedgebeur/Angeltveit-style pipeline (Kissat SAT + LP-filtered census + graph gluing) on the tightest still-open pair in this family (candidates: R(K5-e,K6), R(K6-e,K5-e) — needs a fresh live-table check to confirm which is tightest) | R(K5,K5-e)=30 exactly determined, Feb 2026, "a few months of CPU time," 13 GB peak memory, 322M graphs — i.e. already within easy reach of a 56-core group | 3 | 2 | 3 | 3 | **11** | Exact next target is not yet pinned down (needs a same-day literature check before committing); paper's own authors are the obvious next movers |
| 5 | Minimal period k for 2-abelian-square avoidance over a 2-letter alphabet | [arXiv:1705.04055](https://arxiv.org/html/1705.04055) "Ten Conferences WORDS: Open Problems and Conjectures" | For binary alphabets, what is the smallest period k for which 2-abelian squares can be avoided? Open range reported as 2<k<60 | Exhaustive backtracking / de Bruijn-graph reachability search over the full open range of k, settling each k exactly | Range reported open as of the survey's compilation (~2015) | 3 | 2 | 2 | 3 | **10** | Source list is a decade old — real chance part of the range has already been closed; must re-verify current status before running anything |
| 6 | Perfect cuboid / Euler brick: extend exhaustive non-existence search | [Guy UPINT]; [Euler brick, Wikipedia](https://en.wikipedia.org/wiki/Euler_brick) | Does an integer rectangular box exist with integer edges, face diagonals, and space diagonal all simultaneously integers? | Extend the parametrized exhaustive search (Pythagorean-triple edge families) past the current odd-side bound of 2.5x10^13 / min-edge bound 5x10^11 | Odd side searched to 2.5x10^13, minimum edge to 5x10^11 (Rathbun et al., ongoing small-group project, not a large distributed effort) | 3 | 2 | 2 | 3 | **10** | Current record-holder's exact algorithm/throughput isn't publicly detailed enough to size the next step with full confidence |
| 7 | MOLS(10): further automorphism-class elimination for 3 mutually orthogonal 10x10 Latin squares | [arXiv:2503.10504](https://arxiv.org/pdf/2503.10504) (Myrvold, 2025) | Do three pairwise-orthogonal 10x10 Latin squares exist? (Open since Tarry, 1900) | NOT full resolution (open-ended) — a scoped extension: reproduce and push further the 2025 SAT-based automorphism-class elimination, reporting exactly which classes are newly ruled out | N(10)<9 known (Lam-Thiel-Swiercz); no nontrivial-automorphism triple exists (McKay-Meynert-Myrvold); 2025 SAT paper narrows further but leaves the space open | 2 | 2 | 2 | 3 | **9** | Genuine risk of sliding into the "decades stuck on one hard case" trap this group's own SELECTION.md explicitly warns against — frame strictly as a bounded negative-result extension, never as "solve MOLS(10)" |
| 8 | Football pool problem / covering code T(9) | [Linderoth-Margot-Thain](https://jlinderoth.github.io/papers/Linderoth-Margot-Thain-07-TR-2.pdf); [OEIS A004044](https://oeis.org/A004044) | Minimum number of radius-1 balls needed to cover the ternary Hamming space {0,1,2}^9 | ILP/branch-and-cut with heavy symmetry reduction to decide T(9)=67 or 68 | 67<=T(9)<=68 (Cohen-Honkala-Litsyn-Lobstein school; ILP results via Linderoth-Margot-Thain) | 2 | 2 | 2 | 3 | **9** | Freshness of the 67/68 gap needs re-confirming — this exact numeral pair has been quoted in the literature for years without a visible recent update |
| 9 | Practical numbers: C(2n,n) non-practical exceptions past 10^6 | [arXiv:2004.05376](https://arxiv.org/abs/2004.05376); [arXiv:1905.12023](https://arxiv.org/pdf/1905.12023) | Are n=4, 10, 256 the only n<=10^6 for which the central binomial coefficient C(2n,n) is *not* practical? | Kummer's-theorem carry-counting sweep (avoids factoring the huge binomial coefficient directly) extended to 10^8-10^9 | Verified <10^6 (no exceptions besides 4, 10, 256 found in that range) | 2 | 3 | 1 | 3 | **9** | Minor/narrow result even if it succeeds — good cheap filler, not a headline target |
| 10 | Heilbronn triangle problem, unit square, n=10 | [arXiv:2603.11107](https://arxiv.org/html/2603.11107); [arXiv:2607.15021](https://arxiv.org/html/2607.15021v1) | Largest guaranteed minimum-area triangle among n points in the unit square | Certified interval-arithmetic branch-and-bound (MIQCP) to find and *prove* the optimal n=10 configuration | n<=9 certified optimal, Sudermann-Merx 2026 (n=9 took ~1 day compute) | 2 | 2 | 2 | 3 | **9** | Continuous global optimization, not discrete enumeration — a real domain-fit tension against this group's core strength; needs interval-arithmetic/MIQCP tooling, not just a bigger search |

---

## Top 3: five-line first-experiment plans

### #1 — (k,3)-arcs in PG(2,q): next open q (Green Problem 68 corollary)
1. Fix the affine-vs-projective translation explicitly on paper first: Green's problem is
   "A subset of F_p^2 (affine) meeting every line in <=3 points"; confirm exactly how this
   maps to the projective (k,3)-arc literature's m_3(2,q) before writing any code.
2. Pull the Marcugini-Pambianco-Napolitano table (and any 2020s follow-ups) to identify
   the smallest q with no published exact/complete classification — expect q roughly in
   the high-30s to 50s (prime or prime power).
3. Implement isomorph-free canonical augmentation (nauty-style point-by-point extension
   with canonicity pruning) for (k,3)-arcs at that q; calibrate first by reproducing the
   published exact value at q=31 or 32 before trusting new output.
4. Run the real target on 56 cores with checkpointing; independently re-verify the final
   maximum-arc certificate via a from-scratch second implementation (ILP or a different
   search order) before reporting.
5. Publish the extended table entry either way, and explicitly relate the new exact value
   to Green's (1+o(1))p vs (2+o(1))p asymptotic question as a fresh data point.

### #2 — Erdos-Straus conjecture: push the verified range
1. Obtain Mihnea & Dumitru (2025, arXiv:2509.00128) in full; reproduce their residue-class
   covering construction (modulus G8=25878772920, ~2.1M residue classes) on a small range
   as a correctness gate.
2. Extend their covering-set elimination method (their "S_k" construction) one or two
   levels further to shrink the residual "hard" prime set for a larger modulus.
3. Shard the remaining brute-force check of surviving prime candidates up to 10^19-10^20
   across 56 cores with a checkpointed, resumable sieve.
4. Cross-verify: independently hand-check (or re-derive with a second implementation) a
   random 1% sample of "eliminated" residue classes before trusting the full run.
5. Report either a clean extension of the verified range or — in the astronomically
   unlikely case — a counterexample; both are immediately publishable, and the method
   itself (residue-class covering) is reusable for other 4/n-type Egyptian-fraction
   conjectures if this one runs dry.

### #3 — Small Ramsey number frontier sweep (led by R(3,10))
1. Fetch Radziszowski's live DS1 survey plus the last 6 months of arXiv "Ramsey number"
   postings same-day to confirm the single tightest unresolved gap right now (starting
   assumption: R(3,10) in {40,41}; check R(4,6) in [36,40] and the near-diagonal
   "minus-edge" family from candidate #4 as backups).
2. Re-implement the standard R(3,k) attack: canonical-construction-path generation of
   triangle-free graphs with independence number <=9 on up to 40 vertices.
3. Encode the exhaustive non-existence side as a 56-core cube-and-conquer SAT run
   (Kissat/CaDiCaL-class solver), producing an independently checkable DRAT certificate.
4. If another group resolves it mid-project, pivot immediately to independently
   re-verifying their proof certificate — a fast, still-publishable negative/confirmation
   result that plays directly to this group's stated strength.
5. If R(3,10) proves too contested or resolves faster than expected, fall back at once to
   the next-tightest gap identified in step 1, so no wall-clock time is spent idle.

---

## Rejected: famous but hopeless, with order-of-magnitude estimates

**R(5,5) exact value.** 43<=R(5,5)<=46 (lower: Exoo 1989; upper: Angeltveit & McKay,
[Journal of Graph Theory 2026](https://onlinelibrary.wiley.com/doi/10.1002/jgt.70029),
improved from 48 via a preprint in [Sept 2024](https://arxiv.org/abs/2409.15709)).
Deciding 44/45/46 by exhaustive graph search needs checking non-isomorphic graphs on
44-46 vertices for a monochromatic K5 in both colors. Crude estimate for n=45: raw graph
count ~2^C(45,2)/45! = 2^990 / 45! =~ 10^298 / 1.2x10^56 =~ **10^242** graphs even after
full symmetry-quotienting — about 223 orders of magnitude past the 5.7x10^18-node
computation that already broke this group's budget once. (Independently rejected on
essentially the same grounds in this directory's `oeis_arxiv_scan.md`.)

**Schur number six, S(6).** S(5)=160 was settled by Heule (2017/2018) only via a
2-petabyte SAT proof produced by cube-and-conquer across 800+ cores on the Stampede2
supercomputer over about 2 days. Each step in this family (S(4)->S(5)) inflated the
proof/search size by roughly 2-3 orders of magnitude; a comparable jump for S(6) implies
a proof on the order of **10-1000s of petabytes** — beyond both the compute and the raw
storage this group has access to, and explicitly described in the literature as
"possibly beyond any computational method."

**Existence of a projective plane of order 12.** Order 10 was settled *non-existent* by
Lam, Thiel & Swiercz (1989) using a coding-theoretic weight-distribution shortcut
specific to that code, at a cost of ~2000-4400 hours on a Cray-1/VAX-class machine (111
points). Order 12 (157 points) is not covered by Bruck-Ryser-Chowla and has no known
analogous algebraic shortcut — 35+ years untouched by any comparable method. Estimated
**10^25-10^30 operations**, i.e. roughly **millions to hundreds of trillions of years**
even at this group's full 56-core throughput. The blocker here is explicitly a missing
piece of *theory* (an order-12 analogue of the order-10 coding trick), not just raw
compute — doubly disqualifying given this group's stated weakness.

**Exact count of Latin squares of order 12.** Order 11 was computed exactly (McKay,
Meynert & Myrvold): reduced count ~5.36x10^33, total ~7.77x10^50 — itself a serious
distributed effort. Order 12 is only estimated (~1.62x10^44 reduced squares), roughly
10 orders of magnitude harder than order 11. Even optimistically placing order 11's true
cost at ~10^17-10^18 operations, order 12 needs **~10^27-10^29 operations**, i.e.
**~10^16-10^18 seconds at full 56-core throughput** — on the order of, or beyond, the
age of the universe (4.35x10^17 s).

**Van der Waerden number W(2,7) / any new exact multicolor van der Waerden value.**
W(2,6)=1132 already required Beowulf clusters plus FPGA acceleration (Kouril & Paul,
2008); the authors themselves note their preprocessing does not reduce W(2,7)'s search
space to anything computable with comparable methods. A decade-plus BOINC volunteer
project has since ground on the next tier without producing a single new exact value —
matches this directory's existing rejection in `oeis_arxiv_scan.md`.

**Honorable mention "look-alike trap":** R(4,6) in [36,40] and R(4,7) in [49,61] have
gaps that *look* almost as tight as R(3,10)'s (4 and 12 respectively, vs. 1) but are
searches over *general* graphs rather than the triangle-free-restricted graphs that make
R(3,k) tractable — the structural pruning that makes R(3,10) plausible simply isn't
available here. Numeric gap size is not a reliable proxy for search-space size; this is
the single most important general lesson from this scan.

---

## Cross-verification notes (against this directory's other documents)

- **Heilbronn triangle problem — likely stale estimate in `SELECTION.md`.** linux-12c's
  internal candidate #2 proposes n=17-18, citing "exact values known to about n=16."
  This scan found two 2026 papers ([arXiv:2603.11107](https://arxiv.org/html/2603.11107),
  [arXiv:2607.15021](https://arxiv.org/html/2607.15021v1)) establishing *certified*
  optimality (via interval-arithmetic branch-and-bound) only up to **n=9**, with n=9
  itself taking about a day of compute — suggesting n=17-18 is far outside reach and the
  n=16 figure may reflect an uncertified best-known configuration rather than a proven
  optimum, or a different problem variant (disc vs. square). Recommend re-scoping that
  internal candidate to n=10 before spending any measurement time on it.
- **R(3,10) / DRAT-certificate Ramsey approach — independently convergent.** This exact
  target was proposed independently by linux-12c ("second candidate for measurement") and
  by this list-driven scan. Two different sourcing methods landing on the same target is
  itself a mild positive signal; see candidate #3 above.
- **Costas arrays — cost data point for linux-12c's pending measurement.** Not
  re-proposed here (already their internal candidate #1), but this scan's discrete-
  geometry research pass turned up concrete historical numbers that may help calibrate
  the "hour of measurement" linux-12c's protocol calls for: order 28 took 70 CPU-years,
  order 29 (2011) took 366.55 CPU-years (~5.2x jump per order). Naive extrapolation
  places order 30 around 1800-2000 CPU-years (~32-36 wall-years on 56 cores) and order
  31/32 higher still — consistent with linux-12c's own "probably NO" preliminary read,
  though their claim that orders up to 31 are already fully solved by census is more
  recent than what turned up in this pass and should be taken as their more current
  information.
- **Aliquot sequences — this scan's number-theory pass called it "TRACTABLE," but
  defer to the existing rejection.** `oeis_arxiv_scan.md` already rejected this space
  ("wrong tool, well-resourced incumbent": factordb.com / mersenneforum.org have owned
  it with GNFS/ECM infrastructure for 20+ years) with better reasoning than this scan's
  own pass produced. Not included above; flagging the disagreement for the record rather
  than silently picking one.

---

## Also scanned, set aside (lower confidence or needs dedicated scoping)

- **Cap set maximum in F_3^7 (AG(7,3)).** First unsolved dimension after Potechin's
  exact n=6 result (112, via 2008 exhaustive search); current bounds roughly
  [236(?), 288]. Excluded from the top 10: full resolution is not crisply specifiable in
  advance (no clean scaling law from the n=6 method), so C1/C2 are weak even though C3/C4
  are strong. A *bounded* sub-computation (tighten the upper bound, or search a
  restricted symmetric ansatz for a construction beyond 236) would be a legitimate scoped
  project if the group wants to pursue it.
- **Hadamard conjecture, order 668.** Smallest open multiple of 4, unmoved for ~20 years.
  Full search is astronomically hopeless (2^668-scale); a structured sub-search
  (Williamson matrices of order 167) is the only realistic angle, but this scan could not
  confirm the current exhaustive-search frontier for that structured family — needs a
  dedicated scoping pass before it could be trusted at any score.
- **Biplane (106,15,2) existence.** Next open symmetric 2-design after the known k=13
  case. Point count (106) is smaller than the order-10 projective plane's 111, which is
  numerically tempting, but structural comparability to that problem is unconfirmed and
  no primary source was pinned down in this pass. Lowest-confidence item encountered;
  flagged rather than scored.
- **Small Ramsey numbers for books/wheels/fans.** A 2025 paper
  ([arXiv:2407.07285](https://arxiv.org/pdf/2407.07285)) just closed several cases
  (R(W5,W7)=15, R(W5,W9)=18, R(B2,B8)=21, R(B3,B7)=20) via flag algebras and polycirculant
  enumeration. Likely contains the next tractable target in its own "remaining open"
  list, but this scan did not extract that list directly — worth one follow-up read
  before the next scan cycle.
- **Zarankiewicz problem, further small cells.** Already covered in depth by
  `oeis_arxiv_scan.md` (candidate #4). Separately, this scan's combinatorics-on-words/
  extremal-graphs research pass flagged an apparent cluster of very recent (Aug 2026)
  arXiv preprints on "augmented/limited Zarankiewicz numbers" with near-identical,
  slightly-off titles suggestive of a paper-mill or spam cluster — a caution about source
  verification worth carrying into any Zarankiewicz work regardless of which document
  proposed it.
