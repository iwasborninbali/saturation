# Deep research 10 — verification and ranking of the next-project shortlist

Date: 2026-08-20

Status: multi-agent primary-source audit, independent cost review, adversarial review

## Executive answer

**There is no production-project winner: all ten candidates fail at least one mandatory gate today.**  The
required ranking names E first only as a bounded diagnostic audit.  Several premises in the shortlist are
materially stale or conflate different problems:

- the odd-untouchable frontier is not `10^8` but at least `4·10^18+1` via the verified Goldbach range;
- Green's Problem 68, ordinary arcs through `q=32`, and `(k,3)`-arcs are different questions;
- the Prouhet--Tarry--Escott computation excludes only symmetric solutions of bounded height;
- Norine's conjecture was claimed proved for every dimension in July 2026;
- the certified Heilbronn frontier in the unit square is `n=9`, not `n≈16`;
- candidate G does not specify a Zarankiewicz cell at all.

In the requested single-winner ranking, **E ranks first only as the first one-hour diagnostic audit**:

> **E, the Erdős--Straus verification pipeline.**  It has the best public calibration material and naturally
> parallel batches.  It has only a conditional path to a paper-quality negative outcome: rebuild the
> computation with a complete manifest, independent verification and an additional scientific contribution.
> It is not yet authorized for a full `10^19` run.

Candidate D, reformulated as existence of a `(29,3)`-arc in `PG(2,17)`, is the only meaningful reserve
problem formulation, not yet a valid pilot.  It lacks the public record code, proof pipeline and timing
needed for an absolute cost forecast.  If E fails, the conclusion is "no selected full project"; D is not
promoted automatically.

## Evidence standard and scout integration

The two scout files named by the brief, `oeis_arxiv_scan.md` and `problem_lists_scan.md`, arrived in a
parallel repository update during this audit and were read in full; the independent `erdos_scan.md` was
also reviewed.  They are useful candidate-generation passes, and they explicitly warn that some leads came
from snippets, proxy sources or unresolved problem-identification questions.  They are therefore treated as
scouting evidence rather than frontier authority.  The primary-source audit below corrects several of their
preliminary scores and premises: in particular B's `10^8` frontier, D's `q≈31–32` target, E's completeness
and race assumptions, H's open status, and J's claimed scale.  The Erdős Problems scan independently flags
E as a live, moving frontier, reinforcing its status here as an audit target rather than an approved project.

Every load-bearing boundary below is labelled according to its actual evidence: peer-reviewed result,
preprint, author's record entry, or unaudited report.  "Author report" means that the claim really is made
by its author, not that this audit independently replayed the computation.

The four-slot runtime permits only three subagents at once, so the network ran in waves: nine distinct
subagent nodes, thirteen independent role passes, then main-agent review.  Roles covered domain research,
frontier verification, adversarial tests, source auditing, cost modelling, certificates/reproducibility,
publication/race, brief compliance, link checking, arithmetic replay and a final opposing-winner pass.
Cost statements explicitly distinguish measurements from extrapolations.

## Ranked scorecard

| Rank | Candidate | Confirmed frontier and source | Active competition | Publishability of both outcomes | Realistic 56-core cost | Public calibration | Verdict |
|---:|---|---|---|---|---|---|---|
| **1** | **E. Erdős--Straus** | Mihnea--Dumitru, arXiv preprint, 29 Aug 2025: author-reported verification through `10^18` by modular filters; 2,101,514 residues modulo 25,878,772,920, 140,000 filters, and last index `k=38,641,709` (34,777,540 new batches after the prior `10^17` record) ([paper](https://arxiv.org/html/2509.00128), [repo](https://github.com/esc-paper/erdos-straus)). | The 2025 authors are the direct priority risk. A 2026 8×B200 project self-reports solution counting complete through `10^8` and in progress at `10^9`, so it is same-domain activity, not yet a `10^19` sieve race ([project](https://huggingface.co/cahlen/erdos-straus-cuda)). | Counterexample: major, after exact nonexistence proof for that `n`. Empty decade: a paper is plausible, not guaranteed, and needs an independent implementation, complete batch manifest, survivor certificates and a methodological contribution. | Continuing after the last published batch adds 347,775,376 batches, almost exactly 10× the preceding interval. The old "two weeks on a medium setup" lacks hardware metadata. If that meant 8–32 effective cores, a provisional 56-core scenario is **3–12 weeks / 27k–108k core-h**; only the audit can replace this guess. | **Best in list but incomplete:** code, filters, residues and about 393 MB of compressed survivor chunks are public; no single full-run manifest/proof is supplied. | **Ranked first diagnostic audit; not a project winner.** |
| **2** | **D. `(k,3)`-arcs** | Coolsaet--Sticker's peer-reviewed isomorph-free classification reaches `q≤13` ([paper](https://biblio.ugent.be/publication/2118958)); Bartoli--Marcugini--Pambianco separately proved `m_3(2,16)=28` by exhaustive search ([paper](https://arxiv.org/abs/1201.2260)). A precise next decision is whether a `(29,3)`-arc exists in `PG(2,17)`. The advertised `q=31–32` source concerns ordinary no-three-collinear arcs, not this problem. | `PG(2,17)` is active; a 2026 construction reaches 28 points ([Hamed--Hirschfeld](https://ijs.uobaghdad.edu.iq/index.php/eijs/article/download/13609/7645/164700)). | A 29-point witness improves the lower bound and is potentially publishable; certified UNSAT would prove `m_3(2,17)=28` and should be publishable with a new replayable proof package. | Incidence core only: 307 point variables and 939,420 four-point clauses, before the size-29 cardinality encoding and auxiliaries. That is not a runtime model. `q=16` is characteristic two and may be a poor pre-asymptotic predictor for prime `q=17`; absolute cost is unknown. | Constructions are public, but record search code/proof logs and timing were not found. Must first reproduce `q=13` and `q=16`. | **Reserve formulation; pilot not yet defined.** |
| **3** | **I. Neither square nor square-plus-prime** | [OEIS A020495](https://oeis.org/A020495/internal) records 21 exceptions, last 21679, and `a(22)>10^11`. The often quoted `1.6·10^13` is a 2020 pseudonymous author report using a word-parallel bitset, with no code or audit ([method description](https://math.stackexchange.com/questions/3710032/conjecture-all-but-21-non-square-integers-are-the-sum-of-a-square-and-a-prime)). | No verified large institutional race found; provenance is instead too weak. | A 22nd exception is a clean result. No exception through `10^15` is probably an OEIS/problem-list update, not a paper. | Extrapolating the **unaudited claimed** throughput gives an ideal lower bound around 1,400 core-h to `10^15` (25 h on 56 cores); memory bandwidth could make it **5–15 days**. These are scenarios, not a cost estimate. | No source or auditable record output for the claimed frontier. | **Cheap moonshot, reject as paper project.** |
| **4** | **A. Sun's Ramanujan-τ bundle** | Zhi-Wei Sun's OEIS entries of 18–29 Dec 2024 report Mathematica checks: three single-value claims through `10^6`; `τ(m)^2+τ(n)^2` through 1000; `abs(τ(m)τ(n))` through 5000 ([author entries](https://oeis.org/A000594/internal)). This is five experiments, not one frontier or publication. | Sun and commenters are active, but no record computation package was found. | A counterexample to a named claim is publishable. A routine range extension without a new method/data result is likely only an OEIS/MO update. | Singles require `N` exact coefficients plus tests; distinctness adds sort/hash, and pair variants are `Θ(M²)` without a reduction. At `N=10^9`, 192-bit payload alone is 24 GB; two tight sort buffers are 48 GB, or 64 GB with 32-byte aligned records, before generator scratch. Runtime is not defensibly known without an end-to-end `10^7` pilot. | PARI/FLINT provide generic τ implementations; Sun's Mathematica code and run data are not public. | **Reject bundled form; split before reconsideration.** |
| **5** | **F. `R(3,10)`** | Angeltveit's peer-reviewed 2025 census/gluing computation proves the exact interval `40≤R(3,10)≤41` ([paper](https://www.combinatorics.org/ojs/index.php/eljc/article/view/v32i4p30)). | Angeltveit, McKay, Goedgebeur and Radziszowski already own specialised census/gluing machinery and data. | A 40-vertex witness proves 41; exhaustive exclusion proves 40. Both are major results if independently certified. | The whole `R≤41` project cost about 3 CPU-years; its final extension stage about 3 CPU-months. The paper warns that the `n=40` intermediate census may be many orders larger. Naive SAT has 780 edge variables but 847,660,528 ten-set clauses before symmetry. Not credible on 56 cores. | No official full input census, program or DRAT-style proof package was found. | **At most a bounded calibration study; kill full run.** |
| **6** | **C. Ideal PTE size 11** | Coppersmith--Mossinghoff--Scheinerman--VanderKam, Math. Comp. 2024: general ideal solutions are known through size 10 and at 12; size 11 remains open. Their modular-filter/Gröbner computation excludes only **symmetric** size-11 solutions of height at most 3500 ([paper](https://arxiv.org/html/2304.11254)). The 2025 368-page GPTE survey is not the record-search code ([survey](https://arxiv.org/abs/2506.11429)). | The record authors remain active; a [March 2026 talk](https://qseries.org/alladi70/talks/mossinghoff/) reports new PTE searches. | A witness solves the general existence question. Another bounded symmetric nonexistence range does not solve it and is weak without a new method. | The search exposes seven bounded integers; fixed-density extrapolation is roughly `H^7`: 3500→5000 is ×12.1 and 3500→7000 is ×128. No runtime/hardware makes absolute 56-core cost knowable. | Record-search source, logs and an independently replayable exhaustion certificate were not found. | **Kill: fails finite-decision and calibration gates.** |
| **7** | **G. Zarankiewicz `z(m,n;3,3)`** | No `(m,n)` cell or threshold is specified. It is a two-dimensional family, not a single frontier. An arXiv preprint submitted 8 August 2026 claims several certificate-based cells ([paper](https://arxiv.org/abs/2608.08154)). | Direct, fast-moving race; a public artifact repo exists but its own README says the AI-generated work awaits independent expert review ([artifacts](https://github.com/dfield/finite-zarankiewicz-closures)). | Depends entirely on an unspecified cell. "Search found nothing" is not an upper bound. | Cannot be estimated without the cell and direction of proof; neighbouring cells are strongly non-monotone. | Current proof artifacts are public but pending validation; there is no chosen target to calibrate. | **Kill as undefined.** |
| **8** | **J. Heilbronn `n=17–18`** | Sudermann--Merx's March 2026 preprint gives unit-square `ε`-global MINLP certification and exact incumbent coordinates through `n=9`; it calls `n=10` the next difficult case ([paper](https://arxiv.org/html/2603.11107)). The July unit-right-triangle preprint is a different domain and reaches `n=8` ([paper](https://arxiv.org/abs/2607.15021)). | Two active optimisation groups published in the last eight months. | A better 17/18 construction may improve a lower bound; failure to improve is not a result. Exact certified global optimality would be major but is not a costed finite experiment here. | Published square runtimes rise from 14 s at `n=8` to 908 s at `n=9` (about ×65). Even a deliberately optimistic ×10 scenario per added point gives about **51 years** on 56 cores at `n=17` and 514 years at 18; this is a lower warning, not a forecast. | Excellent open models/configurations exist ([repo](https://github.com/spiralulam/heilbronn)), but the global upper certificate is numerical and calibrates only through 9. | **Kill wrong frontier and scale.** |
| **9** | **B. Odd untouchables** | Pomerance--Yang's 2012 paper enumerated all untouchables to `10^8` in `N^(1+o(1))`; that is not the odd frontier ([paper](https://math.dartmouth.edu/~carlp/uupaper3.pdf)). The published Goldbach verification through `4·10^18` implies that 5 is the only odd untouchable through at least `4·10^18+1`: if `u-1=p+q` with distinct primes, then `u=s(pq)` ([Goldbach project](https://sweet.ua.pt/tos/goldbach.html)). | The distributed Gridbach project self-reports that it is extending the relevant Goldbach computation ([project](https://gridbach.com/)). | A genuine odd untouchable would be notable, but proving it requires excluding every aliquot preimage; Goldbach failure alone is not enough. Another subordinate finite negative range is not an independent paper. | A later full enumeration to `2^40` used 128 GB and about 25 CPU-days ([paper](https://arxiv.org/abs/2110.14136)). A deliberately naive linear projection to `4·10^18` is roughly 4,450 years on 56 cores and 0.47–0.50 EB, depending on GB/GiB convention, before superlinear factors; it is a warning, not a forecast. The Goldbach route is already occupied. | Related enumeration methods/data exist, but not a tractable direct decisive pipeline at the real frontier. | **Kill: stale by ten orders and direct distributed race.** |
| **10** | **H. Norine hypercube `n=9`** | Kirchweger et al.'s Nov 2025 SAT preprint reached `n=8`; Wu--Yang then posted a claimed proof for **every `n≥2`** on 21 July 2026 ([universal proof](https://arxiv.org/abs/2607.19276)). Pending normal review of that preprint, `n=9` is no longer an honest open-target claim. | The SAT group has public code and was already targeting 9; the universal-proof authors supersede the finite target. | SAT counterexample would now refute a general preprint; UNSAT at 9 merely confirms a claimed theorem and races the original SAT group. | No target cost is relevant until the general proof is refuted. Historically `n=8` cost about 5 CPU-days, while encoding changes improved the prior estimate by about 4000×, so clause extrapolation is unsafe ([SAT paper](https://arxiv.org/abs/2511.08386)). | Public SAT code exists ([repo](https://github.com/bsubercaseaux/norinSAT)); no need to run it for target selection. | **Kill as stale/claimed solved.** |

## Cost mechanism and pre-asymptotic audit

An "unknown" absolute cost is a failed C2 gate, not missing arithmetic.  The table below names the work unit
that would have to be measured and the reason a nearby case may lie.

| ID | Growth mechanism and work per unit | What can honestly be said for 56 cores | Pre-asymptotic alarm |
|---|---|---|---|
| A | Generate `N` exact coefficients; `Θ(N)` single tests, `Θ(N log N)` sort for distinctness, `Θ(M²)` pairs without a reduction. | Memory lower bounds are known; runtime is **unknown** until the same end-to-end pipeline reaches at least `10^7`. | The `10^6→10^9` path changes integer width and arithmetic regime; primes, prime powers and highly composite indices may have different cost. |
| B | Full inverse-`s` enumeration is `N^(1+o(1))`; the useful certificate route is instead one Goldbach representation per odd integer. | Direct full enumeration is thousands of years by even naive scaling; the relevant Goldbach computation is an external distributed project. | Higher numbers are usually easier to witness; a small-range inverse-`s` run measures the wrong method and regime. |
| C | Seven bounded coordinates before modular/algebraic filters: raw scale `Θ(H^7)`. | Outer tuples parallelise, but no published node rate means absolute time is **unknown**. | Filter density, collision buckets and algebraic families can change with `H`; a symmetric box says nothing about the unrestricted first solution. |
| D | Direct model has `q²+q+1` variables and `(q²+q+1)·C(q+1,4)` no-four clauses; proof search is symmetry-dominated. | Formula size is small enough to pilot; target time is **unknown** without a replayable `q=16` run. | `GF(16)` has characteristic two and different subfield/automorphism structure from prime `GF(17)`; proof hardness need not track the 1.446× clause growth. |
| E | Each batch starts with 2,101,514 residues and early-exits through up to 140,000 modular filters; the new decade starts 730,854,821,519,264 residue checks before early exits. | A 45-day cap requires at least **89.45 aggregate batches/s**, all verification included. This is directly measurable in an hour. | Filter order was trained on the first 7,100 batches; hit depth, survivor rate and memory-bandwidth scaling may drift near `k≈386m`. |
| F | Naive `n=40` SAT has 847,660,528 independence clauses and 38.145 billion literal occurrences; the published method instead glues specialised graph censuses. | The `n=41` project alone is 19.6 ideal wall-days when 3 CPU-years are divided by 56; `n=40` may be orders worse, so there is no credible production estimate. | Even 40 admits a 9-regular branch eliminated by parity at 41. Runtime is not monotone when one vertex is removed. |
| G | For a fixed cell, `mn` edge variables and `C(m,3)C(n,3)` forbidden-`K_{3,3}` constraints, then degree/symmetry cases. | No cell or edge threshold means no work count and no 56-core estimate. | Neighbouring cells and lower/upper directions have non-monotone proof difficulty; current certificates close isolated slices. |
| H | Hypercube edges grow by 2.25× from dimension 8 to 9 before auxiliary variables; cube-and-conquer cost is controlled by the slow tail. | Historical `n=8` timing exists, but the target is stale. | A new encoding changed the estimate by >4000×; early completed-cube fractions systematically understate the tail. |
| I | Blocked prime/square bitsets scan an interval; average representation count grows roughly like `√n/log n`, while rare singular-series deserts determine exceptions. | The only throughput behind the 25-hour ideal scenario is unaudited. Measure several logarithmic strata; otherwise cost is **unknown**. | Average early exits get easier while the scientifically important minimum-count tail gets rarer; averages and p99 can both miss it. |
| J | Orientation binaries grow as `C(n,3)` and spatial branch-and-bound closes a continuous global gap. | The observed 8→9 jump is about 65×; even the artificial ×10 warning already gives 51/514 years for 17/18. | A regime break has already occurred at 9, and eight/nine uncertified transitions separate 17/18 from calibration. |

## Ranked first audit target: exact first experiment for E

This is a calibration and integrity audit, not the beginning of the `10^19` computation.

The audit found an important gap in the public package.  [`Checker.cpp`](https://raw.githubusercontent.com/esc-paper/erdos-straus/main/section1/Checker.cpp)
applies the modular filters and writes survivors; its `validate(p,x,y,z)` function is never called, and it
neither tests survivor primality nor constructs decompositions.  The public Python generator is not a
turnkey reconstruction of the exact `R_8`/filter assets.  The paper separately says that all saved survivors
were later found composite.  The five split compressed archives, however, have no joined count/hash or
batch-completion manifest.  A sample cannot reconstruct historical coverage: a full prior-range replay or
the authors' original immutable manifest remains a separate mandatory gate.

### Target

Before timing, freeze every upstream hash, independently regenerate/check `R_8`, and verify the mathematical
identity behind every filter family.  Two loops over the same incorrect static files are a common-mode
failure, not independent evidence.  Failure to reconstruct the inputs kills E before a performance run.

Then use one timed hour: 5 minutes on one worker, 5 minutes on eight workers, 40 minutes on 56 physical
cores, and 10 minutes to merge/check the sample manifests.  Pre-register a deterministic seed and draw
non-overlapping pseudorandom contiguous windows within each arithmetic stratum.  If the throughput gate is
met, process at least 200,000 batches in total, balanced between:

- a **replay sample** across
  `k=3,864,170…38,641,709`;
- a **future-range sample** in windows near `k=100m, 200m, 300m, 380m` and the final
  `k≈386.4m` required for `10^19`.

Contiguous windows keep the official CLI path intact; stratification prevents one early, easy prefix from
standing in for the new decade.  This matters because the published filter ordering was learned on only the
first 7,100 batches.

For every replay batch, retain the exact set of integers escaping all 140,000 filters.  Reconstruct the
matching set from the published compressed survivor archive using `k=floor(n/G_8)`, compare the sorted sets
bit-for-bit, and independently prove every survivor composite.  In the future-range sample, require exact
agreement of the two implementations and compositeness certificates or factors for all survivors.  Run a
fixed subset on 1, 8 and 56 workers.  Record batches/s, core time, peak RSS, the full filter-hit-depth
distribution, p50/p95/p99/max batch time, survivor rate, per-survivor verification time, output bytes and
parallel efficiency.  The sample is a falsification tool; its p99 is not a proof that a rarer tail is absent.

The represented `n<10^19` fit in `uint64_t`, but all intermediate arithmetic must use checked 128-bit
arithmetic or GMP after an overflow audit.  The independent implementation must not share the record program's parser,
filter loop or output code.  Hash every input, batch assignment and output shard; a final manifest must prove
that batch intervals are disjoint and cover the requested range.

### Success gate

All of the following are required:

1. exact agreement on the replay sample between the upstream program, the independent implementation and
   the matching published-archive records, plus independent regeneration/semantic checking of shared inputs;
2. deterministic independent compositeness checking for every sampled survivor;
3. at least 65% parallel efficiency, defined as `(throughput_56/throughput_8)/(56/8)` on the actual physical
   cores, and no unstable long tail (`p99/p50≤10`);
4. no future stratum below 70% of replay-range throughput, no more than 2× the replay survivor rate, and
   throughput coefficient of variation at most 20%;
5. measured projection for the 347,775,376 new batches of at most **45 wall-days on 56 cores** (60,480
   core-hours), requiring at least 89.45 aggregate batches/s with storage and verification included;
6. before further scale-up, a direct priority check with the record authors, a differentiated scientific
   contribution, and a timestamped preregistration of target, method, budget and certificate format.

The 45-day limit is an explicit project-management threshold, not a fact from the literature.  If the group
wants a 10,000-core-hour cap, E is expected to fail and the shortlist has no production winner.  Even a PASS
only authorizes a larger preregistered calibration and a full prior-range replay; it does **not** authorize the
`10^19` production run or establish that a null decade is publishable.

### Failure gate

Stop immediately on any mismatch, missing coverage evidence, inability to map archive records back to
batches, unchecked arithmetic overflow, projected cost above the threshold, pathological tail, or direct
priority race.  Do not "fix and continue" inside the same evidence chain: regenerate the calibration from
the beginning after any semantic change.

### What a production result would have to contain

- a versioned definition of `R_8`, `G_8` and every modular filter;
- independent GMP and `uint64_t` implementations with differential tests;
- immutable input/output hashes and a complete non-overlapping batch manifest;
- survivor lists with deterministic compositeness certificates or factors;
- explicit unit-fraction witnesses, or formally checked filter lemmas, sufficient to turn filtering into a
  proof rather than a solver status;
- a small verifier that does not depend on the search implementation.

Without this layer, a longer range is an author report rather than the kind of exact negative result this
group says it wants to publish.

## What D must become before it is a pilot

The direct `q=17` question is: **does a `(29,3)`-arc exist?**  D is not yet a C2-valid reserve pilot.  Before
it can be promoted, its pipeline must:

1. generate `PG(2,q)` incidence independently in two implementations and use a small semantic checker for
   incidence, size cardinality, symmetry constraints and cube coverage;
2. reproduce both halves of `m_3(2,13)=23`: a checked 23-point witness and LRAT/FRAT for nonexistence at 24;
3. reproduce both halves of `m_3(2,16)=28`: a checked 28-point witness and proof of nonexistence at 29, with
   the same generator intended for `q=17`;
4. freeze a complete hashed `q=17` cube partition, a 10,000-core-hour/2-TB all-in budget and a deterministic
   sampling rule **before** solving any target cube;
5. run at least 10,000 structurally stratified target cubes so the top 1% has at least 100 observations, and
   report conflicts, p50/p95/p99/max time, proof bytes, I/O, checker time and work concentration;
6. perform the same priority/novelty check required for E, because `PG(2,17)` is active in 2026.

Kill D on any failed known truth, unverified semantic/symmetry step, missing cube-cover proof, unstable tail,
or all-in projection above the frozen budget.  The `q=13` and `q=16` replays validate correctness; they do not
identify the `q=17` runtime because the former is much smaller and the latter changes field characteristic.
Until this protocol exists, D is a reserve problem formulation, not a fallback compute project.

## Cross these out, and why

- **B:** the premise is obsolete, the real range is dominated by Goldbach, and an active distributed project
  already owns that frontier.
- **C:** a bounded symmetric search cannot decide unrestricted existence at size 11; no absolute cost or
  negative certificate is available.
- **F:** the question is exact and valuable, but the known structural computation says the 40-vertex case is
  many orders harder than the already expensive 41-vertex case; the expert data/machinery are not public.
- **G:** no exact finite decision was named, while the table is changing during the week of this audit.
- **H:** a general proof preprint supersedes the `n=9` target.
- **J:** `n=17–18` is not the next exact frontier and is far outside any defensible extrapolation.
- **A in its current form:** it bundles five predicates with different bounds and cost mechanisms.  It may
  return only after being split and after the negative-outcome publication case is defended.
- **I as a main project:** accessible computation, but a null result is weak and the claimed prior record is
  unaudited.

The shortlist therefore yields one useful action, not one approved research programme: run the E audit for
one hour, apply the kill gate literally, and be willing to finish with no selected project.
