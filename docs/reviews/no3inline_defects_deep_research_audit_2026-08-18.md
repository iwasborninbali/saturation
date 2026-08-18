> **Note:** external LLM-assisted audit (ChatGPT deep research with sub-agents, commissioned by the author of record) of draft v0.6 of `paper/no3inline_defects.tex`, received 2026-08-18.  Not a human referee report.  The revision v0.7 addresses its blocking items (see `docs/THREAD.md` [53]): priority claim for n=37,39 corrected (rct4 has exact half-turn stabilizer), central-class 3-cycle defects added and swept, mixed families swept exhaustively for n<=27, two-loop n=36 swept exhaustively, lemma clarified, validation formula corrected, journals tracked under logs/.

# Independent Deep-Research Report

## *No-three-in-line configurations with exact half-turn symmetry for n = 36, 37, 39, and a balance lemma for symmetric defects* (draft v0.6)

**Report date:** 18 August 2026  
**Manuscript audited:** `no3inline_defects_v0.6.pdf` (9 pages)  
**Manuscript SHA-256:** `bec5cc36f1ffbc16824a8cbb48178288b3a536dc59f3c21a7deeee2d99fa3ff5`  
**Repository snapshot audited:** annotated tag `paper-v0.6`, tag object `5d8449168ef15f13bd34a9418fe27b21cdaedf6b`, peeled commit `70de92ca690dc2093f786e267c70a460881bc571`  

> **Verdict:** **Do not submit v0.6. Go after correction and completion, preferably as a focused note.** The six displayed configurations are valid, but the historical headline is overstated and the exhaustive-family claims contain a material enumeration error.

---

## 1. Executive summary

The manuscript contains a real and potentially publishable core, but draft v0.6 is not submission-ready. The central positive result of this audit is that **all six displayed coordinate sets are genuine \(2n\)-point no-three-in-line configurations with exact stabilizer \(\{1,\rho^2\}\)**. Two independently written exact-arithmetic checkers agree on distinctness, bounds, row and column sums, absence of collinear triples, the full \(D_4\) stabilizer, the stated base/defect decomposition, and same-order inequivalence. The three headline runs—the two prescribed defects at \(n=37\) and the prescribed defect at \(n=39\)—also replay successfully from the tagged code.

Two findings nevertheless force major revision.

First, the headline priority claim is wrong for \(n=37\) and \(n=39\). Flammenkamp's `rct4` configurations, found in 1996--97 and published in 1998, already have actual stabilizer exactly \(\{1,\rho^2\}\). His database treats `rct4` as a constructional pseudo-class inside `rot2`, not as a larger stabilizer. The manuscript may plausibly claim the first located exact-half-turn examples for \(n=36\), and the first located **non-`rct4` / ordinary-`rot2`-column** representatives for \(n=37,39\), subject to direct expert confirmation. It cannot claim the first exact-half-turn configurations at all three orders.

Second, the claimed exhaustive directed-three-cycle enumeration omits every odd-order defect using the central row/column class. The code explicitly excludes that class even though the balance lemma excludes only the central cell. The correct number of \(D_4\)-classes is

\[
4\binom{h}{3}+\binom{h}{2},\qquad h=(n-1)/2,
\]

not \(4\binom{h}{3}\). Re-running all omitted subclasses through \(n=25\) found valid additional exact-half-turn completions at \(n=13\) (V2 base) and \(n=21\) (C4 base), changing printed Table 1 values. The omission therefore affects results, not merely denominators. At \(n=37\), all 153 omitted V2 subclasses were exhausted with no solution, but 46 of the 153 omitted C4 subclasses timed out; the printed C4 total remains a lower bound rather than a certified complete count.

The balance law itself is sound after clarifying the canonical base/defect decomposition and central class. Its abstract content--a zero-divergence condition and cycle decomposition--is standard circulation theory. The apparently new and useful part is its application to orbit defects in symmetric no-three-in-line configurations. The manuscript currently overstates the completeness of the resulting minimal-family classification: directed 2-cycles and loop-plus-2-cycle combinations must be handled, and a statement about the stabilizer being a proper subgroup of the base group is logically invalid without a direct stabilizer computation.

The best publication path is a corrected, human-verified 10--14 page focused note built around: (i) the orbitwise balance formulation; (ii) valid exact-\(C_2\) witnesses, described with historically accurate labels; and (iii) carefully delimited, rerun enumeration data. A separate computational paper is possible only after complete reruns, an auditable canonicalization pipeline, archived raw logs/certificates, reproducible build metadata, and algorithmic comparison. The present draft should not be submitted.

## 2. Scope, methods, and limitations

This review followed the requested four axes: mathematical/scientific value, novelty and priority, mathematical and computational evidence, and publication prospects. Evidence was deliberately separated into theorem, exhaustive computation, bounded experiment, algorithm-specific failure, heuristic, extrapolation, and open question.

The audit used a staged multi-agent design. Specialist agents independently reconstructed the proof, inspected the implementation and logs, performed multilingual and grey-literature searches, and assessed publication policy. Adversarial agents attempted to falsify the specialist conclusions. Additional referees were given only the manuscript and tagged repository, with explicit instructions not to read earlier reports. All agents used the requested GPT-5.6-Sol extra-high reasoning configuration. Their conclusions were reconciled only after independent work.

Computational checks included:

- exact decoding of every printed configuration;
- two independent collinearity tests: canonical primitive-line grouping and exhaustive determinant evaluation over all triples;
- direct evaluation of all eight \(D_4\) actions and canonical comparison of \(D_4\)-orbits;
- independent reconstruction of the defect-family counts;
- recompilation and replay of tagged solvers;
- exhaustive runs on the previously omitted central-class defects for small orders and \(n=33\), plus a time-bounded \(n=37\) audit;
- sanitiser and malformed-input tests of solver interfaces;
- comparison of manuscript tables with the repository's available raw logs.

The historical search covered the principal literature indexes and public web, Flammenkamp's live and archived pages and downloadable corpora, OEIS, arXiv, repositories and source code, dissertations, conference and recreational sources, and targeted searches in Chinese, Russian, Japanese, French, German, Spanish, Portuguese, Italian, Korean, Polish, Hungarian, Czech and Slovak ecosystems. Some commercial or institutional databases could be checked only through public metadata/snippets. Search failure is therefore not proof of absence. No email was sent: the recommended expert outreach remains outstanding.

The audited repository was the annotated tag `paper-v0.6`; its PDF is byte-identical to the supplied manuscript. Exact solver runs establish trusted-program evidence, not independently checkable formal UNSAT certificates. Acceptance probabilities below are subjective scenario estimates, not forecasts.

## 3. Claim-status matrix

| Claim | Audit status | Evidence / qualification |
|---|---|---|
| Six printed coordinate sets are valid \(2n\)-point configurations | **Independently verified** | Two exact checkers; every row and column contains two points; no repeated/out-of-range points |
| No three displayed points are collinear | **Independently verified** | Primitive-line grouping and exhaustive integer determinants agree |
| Exact stabilizer is \(\{1,\rho^2\}\) | **Independently verified** | All eight \(D_4\) actions tested; each orbit has four labelled images |
| Two \(n=36\) examples and two \(n=37\) examples are pairwise inequivalent | **Independently verified** | Full \(D_4\)-canonicalization; intrinsic loop-class invariant also separates the \(n=36\) pair |
| First exact-half-turn configurations for \(n=36\) | **Plausible historical claim** | No predecessor located; database cell was blank, but direct correspondence is still required |
| First exact-half-turn configurations for \(n=37,39\) | **False** | Flammenkamp's 1997/1998 `rct4` examples already have exact \(C_2\) stabilizer |
| First non-`rct4` / ordinary-`rot2` representatives for \(n=37,39\) | **Plausible historical claim** | No predecessor located in public sources; qualify by date and expert confirmation |
| Orbitwise row-column balance lemma | **Correct after clarification** | Requires a canonical union-of-full-\(H\)-orbits base and careful treatment of the central class |
| Balanced defect decomposes into directed cycles | **Correct, standard abstraction** | A balanced directed multigraph decomposes into cycles; loops and parallel arcs must be allowed |
| Printed minimal defect-family list is complete | **Not established / false as broadly read** | Directed 2-cycles and mixed loop-plus-2-cycle cases are omitted unless extra normalization is stated |
| One off-diagonal half-turn pair alone is impossible | **Mathematically proved under the stated normalization** | A single non-loop arc violates balance |
| Table 1 directed-three-cycle subclass counts | **False** | Central class omitted; correct count is \(4\binom{h}{3}+\binom{h}{2}\) |
| Table 1 complete configuration totals | **False in at least two rows; other completeness labels compromised** | New \(n=13\) V2 and \(n=21\) C4 solutions found among omitted subclasses |
| Table 2 subclass counts are modulo \(D_4\) | **Inconsistent** | Printed values count ordered loop pairs; true swap-reduced counts are half |
| All mixed-base families are empty in the stated range | **Unsupported as worded** | Code covers a narrower one-opposite-orbit family; one path is randomized; logs are incomplete |
| Main branch-and-bound search is logically exhaustive for well-formed inputs | **Plausible trusted-code result** | Core shading/backtracking survived review and small cross-checks, but interface and PAIRS issues remain |
| Partial large-\(n\) sweep results | **Lower bounds / work-in-progress only** | Corrected denominators and raw state snapshots are required |
| Warm-start, local-search and belief-propagation failures | **Protocol-specific negative experiments** | No mathematical impossibility follows |
| Absence of simple algebraic structure | **Heuristic observation** | Depends on the tested model family, primes and metric |
| Cost growth and large-\(n\) projections | **Exploratory extrapolation** | Too few controlled measurements for an asymptotic or dependable resource forecast |

## 4. Mathematical audit: balance law and defect classification

### 4.1 What is correct

Let \(C\subseteq[n]^2\) be a saturated \(2n\)-point configuration, so every row and column contains two points. For a subgroup \(H\le D_4\) containing an element that identifies the row class indexed by \(a\) with the corresponding column class, each full \(H\)-orbit contributes equally to those row and column classes. If \(B\subseteq C\) is defined canonically as the union of the full \(H\)-orbits contained in \(C\), then the defect \(D=C\setminus B\) inherits equality of row and column incidence counts.

Encoding a half-turn pair \(\{(a,b),(n-1-a,n-1-b)\}\) as an oriented edge \([a]\to[b]\) on complement classes gives

\[
R_D(q)=2d^+(q),\qquad C_D(q)=2d^-(q).
\]

Thus row-column balance is exactly \(d^+(q)=d^-(q)\). This remains true for the singleton central class when \(n\) is odd; only the central **cell** is unavailable in a \(2n\)-point no-three-in-line configuration. The resulting directed multigraph may have loops and parallel edges and is balanced componentwise, hence decomposes into directed cycles.

The parity statement for a pure half-turn base, \(|D|\equiv n\pmod 2\), follows from orbit sizes. For reflection-generated bases the manuscript must include the parity contribution of diagonal two-orbits: if \(b\) denotes their number, the correct relation is \(b+|D|\equiv n\pmod2\), not a statement about \(|D|\) alone.

### 4.2 Necessary clarifications

The proof should define \(B\) intrinsically. If authors may arbitrarily select some \(H\)-orbits as a “base”, then two nominal half-turn pairs can themselves form a full \(H\)-orbit, and the claimed defect interpretation becomes decomposition-dependent. Defining \(B\) as all full \(H\)-orbits contained in \(C\) removes the ambiguity.

The phrase “any diagonal reflection maps column \(a\) to row \(a\)” is literally false for the anti-diagonal under the manuscript's indexing. The intended group claim is recoverable because adjoining the half-turn supplies the main-diagonal reflection, but the proof should state the precise element used.

The definition also contains a notation slip equating `rot2` symmetry with \(\rho C=C\); under the manuscript's convention the half-turn condition is \(\rho^2C=C\). Correct this wherever the symmetry classes are introduced.

“Eulerian digraph” is potentially misleading because some readers require connectedness. “Balanced directed multigraph” followed by “each nontrivial weak component admits an Euler tour and the arc set decomposes into directed cycles” is exact.

### 4.3 Classification gap

Zero divergence alone does not yield only the families emphasized in the paper. A defect of two half-turn pairs can be either two loops or a directed 2-cycle. At odd defect size three, possibilities include a directed 3-cycle and a loop plus a directed 2-cycle. No-three-in-line restrictions may eliminate particular embeddings, but that requires a separate argument; it is not a consequence of balance. Three loops are indeed incompatible, and the lawful two-loop pattern requires the long diagonals to be treated correctly.

Accordingly, the paper must either prove an additional normalization that absorbs directed 2-cycles into a C4/V2 base, or explicitly add and analyse the missing mixed components. At present, the “minimal defect families” discussion is a useful taxonomy, not a complete classification theorem.

Finally, failure of \(H\)-invariance does not imply that the stabilizer is a proper subgroup of \(H\). It may be an incomparable subgroup of \(D_4\). Exact-\(C_2\) status must be checked against all eight group elements. This audit did so for the displayed witnesses, but the general prose should be corrected.

### 4.4 Novelty of the lemma

The incidence-kernel/circulation core is standard. Balanced red-blue bipartite differences and alternating-cycle decompositions appear, for example, in [Erdős--Király--Miklós](https://arxiv.org/abs/1205.2842), while directed incidence kernels and cycle spaces are standard graph theory; see [Godsil--Guo](https://arxiv.org/abs/1609.09118). No source located in the multilingual search uses the manuscript's particular chain from \(D_4\)-orbit balance to no-three-in-line symmetry defects and their search parameterization. The novelty should therefore be presented as an application and organizing device, not as a new general theorem about Eulerian digraphs.

## 5. Independent verification of the six displayed configurations

Every displayed witness passed the following independent tests:

1. the printed/encoded point list contains exactly \(2n\) distinct in-range lattice points;
2. every row and every column has occupancy two;
3. every triple has nonzero integer determinant;
4. canonical grouping by primitive line direction finds no line with three points;
5. the point set is fixed by the half-turn and by no other nonidentity element of \(D_4\);
6. the claimed deleted half-turn pairs are exactly the defect relative to the stated C4 core;
7. same-order examples are not related by any \(D_4\) element.

The six C4 cores contain respectively \(17,17,17,17,18,15\) full four-point orbits for the two \(n=36\), two \(n=37\), \(n=39\), and \(n=33\) witnesses. Each full configuration has a \(D_4\)-orbit of size four, as required by an order-two stabilizer.

For \(n=36\), the manuscript's “different loop rows” inequivalence argument is valid only after quotienting row labels by complementation and using the intrinsic C4 defect. The resulting unordered loop-class multisets are \(\{5,6\}\) and \(\{1,9\}\), so they differ; full canonicalization independently confirms inequivalence.

There is an encoding-convention inconsistency. The first \(n=36\) string begins with `:`, while the second begins with `c`; both geometries have the same exact half-turn stabilizer and both are C4 cores modified only on the long diagonals. If `c` denotes actual stabilizer, both should be `:`. If the author intentionally extends Flammenkamp's structural `rct4` pseudo-class to even orders, both arguably merit `c`. The paper must define the convention and use it consistently rather than silently mixing prefixes. The example command for the second configuration also lacks a closing quotation mark.

The verification establishes existence and the displayed pairwise distinctions. It does **not** establish that exactly two classes exist at \(n=36\) or \(n=37\), or exactly one at \(n=39\). Those stronger statements require completed, correctly parameterized enumeration.

## 6. Defect enumeration and solver-completeness audit

### 6.1 Central-class omission in the three-cycle generator

For odd \(n=2h+1\), `cycle_family.py` constructs complement classes only from `range(h)` and explicitly rejects occurrences of \(h\). This excludes the central row/column class. The balance lemma provides no such exclusion: a cycle such as

\[
[0]\to[h]\to[1]\to[0]
\]

corresponds to six distinct points and can be internally no-three-in-line. Independent generation and canonicalization show that the number of \(D_4\)-orbits of directed-three-cycle defects is

\[
4\binom{h}{3}+\binom{h}{2}=\frac{h(h-1)(4h-5)}6.
\]

The omitted \(\binom h2\) term consists precisely of cycles using the central class. The correction is:

| \(n\) | Printed | Correct |
|---:|---:|---:|
| 13 | 80 | 95 |
| 15 | 140 | 161 |
| 17 | 224 | 252 |
| 19 | 336 | 372 |
| 21 | 480 | 525 |
| 23 | 660 | 715 |
| 25 | 880 | 946 |
| 33 | 2240 | 2360 |
| 37 | 3264 | 3417 |
| 39 | 3876 | 4047 |
| 41 | 4560 | 4750 |
| 45 | 6160 | 6391 |

All omitted defects tested were internally lawful; they cannot be discarded before the base-completion search.

An exhaustive rerun of all omitted subclasses for both C4 and V2 bases at \(n=13,15,17,19,21,23,25\) found two additional exact-half-turn configurations:

- \(n=13\), V2 base, defect `0,4;4,6;6,0`, encoding `:492419AC16570C576B023B8A38`; the corrected class total is 3 rather than 2;
- \(n=21\), C4 base, defect `0,1;1,10;10,0`, encoding `:147A5E9CEKDI245J39CH0K38BH1FGI27068B6FADGJ`; the corrected class total is 1 rather than 0.

Both configurations are valid and appear in Flammenkamp's global exact-half-turn corpus, but they were missed by the manuscript's defect-family sweep. For \(n=33\), all 120 omitted subclasses for each base were exhausted without an additional solution, so the printed configuration total survives although its subclass denominator changes. For \(n=37\), the V2 omissions were completely exhausted (153/153, no solutions); the C4 audit exhausted 107/153 and timed out on 46, with no new solution found. The manuscript's two \(n=37\) C4 witnesses remain valid, but their completeness is unproved.

### 6.2 Two-loop and mixed families

The Table 2 values (132,156,182,306) are ordered pairs (h(h-1)). The caption simultaneously says that quarter-turn symmetry swaps the two loop choices. If the table is meant to report subclasses modulo that action, the correct values are (66,78,91,153). The paper must choose one convention and make the run/canonical-count relationship explicit.

The mixed-family implementation covers a narrower case than the prose: essentially one orbit of the opposite base type, not every base containing “at least one” such orbit. Its exclusion of the odd central cross is defensible only because that orbit is simultaneously C4- and V2-invariant; the definition should say “an orbit exclusive to the opposite base type.” One search path (`sym11`) uses randomized choices, so it cannot support an exhaustive emptiness statement. “No completion found in the implemented one-opposite-orbit experiments” is currently the strongest warranted claim. During blind review, a putative \(n=13\) mixed counterexample was rejected on reconciliation: its apparent C4 orbit was the central cross, which is simultaneously a V2 orbit, and the full configuration had V2 rather than exact-half-turn stabilizer. This illustrates why the orbit semantics must be intrinsic and explicit.

### 6.3 Solver logic and class accounting

The main recursive shading/backtracking logic appears sound for valid inputs: it branches on whole orbits, enforces row/column capacity, shades every cell collinear with two selected points using primitive directions, and backtracks consistently. Small exhaustive comparisons and headline replays agree with independent checkers. This supports the reported witnesses and completed runs for which complete logs actually exist.

Several engineering defects prevent a blanket completeness claim:

- the PAIRS path assigns orbit identifiers before splitting chosen C4 orbits, while compatibility masks may still refer to the other half; bounded tests found no wrong answer, but the representation is internally inconsistent and should be rebuilt in the opposite order;
- PAIRS accepts malformed, duplicate or out-of-range coordinates without validation; sanitiser testing produced an out-of-bounds crash;
- a missing `FIX` file is silently ignored, converting a restricted run into an unrestricted one;
- timeout-resume scripts can treat an incomplete/statusless line as already finished and skip it forever;
- the Makefile does not build the `there_tw` target required by paper commands;
- output canonicalization deduplicates identical encodings rather than full \(D_4\)-orbits.

The displayed group-count identity also needs correction. The formula

\[
N_H=\sum_{K\supseteq H}c_K\frac{|D_4|}{|K|}
\]

works for the unique normal half-turn subgroup but is not valid for an arbitrary fixed reflection subgroup without a transporter/conjugacy multiplier. The manuscript's own diagonal-reflection example uses such an extra factor, contradicting the displayed formula. Moreover, `rct4` is a pseudo-class, not a subgroup, and cannot be inserted into this subgroup-lattice identity.

### 6.4 What the tables may safely say now

Each row should expose: generated subclasses; canonical \(D_4\) classes; fully exhausted classes; timeouts; found labelled solutions; distinct encodings; distinct \(D_4\)-classes; and the exact code/tag/log hash. Use `=` only for a completed family after the generator has been corrected. Use `\ge` for partial sweeps and for any class count lacking a complete canonical audit. The complete and partial sections should be visually separated.

## 7. Reproducibility audit

The supplied PDF is byte-identical to the PDF in annotated tag `paper-v0.6`, peeled commit `70de92ca690dc2093f786e267c70a460881bc571`. A clean `make && make check` passes the bundled small tests. Replaying the three headline defect subclasses gave one solution in each case, including the two \(n=37\) and the \(n=39\) searches. These are meaningful positive reproducibility results.

The release does not, however, substantiate all table-level claims. Most raw sweep logs are absent or ignored: there is no complete canonical trail for the \(n=33\) C4 row, no complete \(n=37\) log set, no adequate raw progress archive for \(n=39,41,45\), and no Table 2 two-loop logs. One legacy \(n=33\) log contains completed, dead and statusless/terminated entries and is not a complete canonical certificate. Summary lines cannot replace per-instance termination records.

Minimum publication-grade repairs are:

1. correct the family generators and rerun every claimed complete row;
2. make invalid PAIRS/FIX input fatal and validate bounds, duplicates and capacities;
3. fix timeout-resume state handling and use atomic per-instance status records;
4. perform \(D_4\)-canonicalization explicitly, recording labelled-to-unlabelled mappings;
5. archive raw instances, stdout/stderr, return status, wall time, seed and checksums;
6. supply compiler, flags, CPU/OS, thread count, memory limit and dependency versions;
7. replace `-march=native` in the portable build or document it as an optional optimized profile;
8. add a one-command deterministic verification target, CI/container, licence and citation metadata;
9. deposit an immutable release in Zenodo or an equivalent repository;
10. where nonexistence is central, emit independently checkable SAT/UNSAT certificates or provide two genuinely independent exact implementations.

The paper's second \(n=36\) command has a missing closing quote. `web/stab.py` also depends on repository-root import setup (`PYTHONPATH=.`) not documented in the command. Search timing should use a monotonic clock, and benchmarks should distinguish wall time from aggregate core-hours.

Even after repair, a branch-and-bound program plus logs yields a computer-assisted exhaustive result, not a formal mathematical proof independent of the implementation. The paper should state that epistemic status precisely.

## 8. Novelty, priority, and historical/grey-literature search

### 8.1 The decisive historical correction

Flammenkamp explicitly defines [`rct4` as a subset of `rot2`](https://wwwhomes.uni-bielefeld.de/achim/no3in/symmetry_remarks.html). His [database table](https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html) explains that `c`/`rct4` has true symmetry `:`--exact half-turn--except for the exceptional \(n=3\) case. The same table lists 21 `rct4` configurations at \(n=37\) and 33 at \(n=39\). The downloadable files contain exactly those counts, and independent stabilizer checks confirm that every one has stabilizer \(\{1,\rho^2\}\).

The dated [1997 progress page](https://wwwhomes.uni-bielefeld.de/achim/no3in/odd_results.html) records their discovery around New Year 1997. They were published in Achim Flammenkamp, “Progress in the No-Three-in-Line Problem, II,” *JCTA* 81 (1998), 108--113, [DOI 10.1006/jcta.1997.2829](https://doi.org/10.1006/jcta.1997.2829). Archived tables already show the \(n=37,39\) `c` counts. Therefore priority for exact half-turn symmetry at those two orders belongs to Flammenkamp.

The ordinary `:` cells being blank does not change this conclusion. A blank means no stored representative under that database label; exact `rot2` enumeration is complete only through \(n=31\). It is not a proof that no exact-\(C_2\) object exists, and `rct4` objects have the same actual stabilizer.

One blind referee initially treated the blank `:` cells as support for literal priority at \(n=37,39\). That interpretation was rejected in reconciliation because it ignored the populated `c` cells and Flammenkamp's explicit statements that `rct4` is a subset of `rot2` and has true symmetry `:` at these orders. This disagreement is recorded because it exposes exactly the taxonomic ambiguity the revised paper must eliminate.

No earlier exact-\(C_2\) witness at \(n=36\) was located in the live or archived database, the 1997 corpus, indexed literature, repositories, or exact-encoding searches. Because unpublished configurations may exist, the responsible wording is “first located as of 18 August 2026,” followed by direct confirmation from Flammenkamp and active solver authors.

The strongest currently defensible contribution statement is:

> We give the first located \(n=36\) configurations with stabilizer exactly \(\{1,\rho^2\}\), and new \(n=37\) and \(n=39\) exact-half-turn configurations outside Flammenkamp's `rct4` pseudo-class (the first located representatives for the database's ordinary `rot2` column).

### 8.2 Search coverage and residual uncertainty

The review followed citation trails from Flammenkamp 1992/1998, OEIS A000769/A272651, recent CP-SAT/SAT/GPU work, and downloadable configuration corpora. Formula, terminology and encoding searches covered mainstream indexes, repositories, archival web pages, dissertations, proceedings, personal sites and recreational sources. Multilingual searches used local terminology and national repositories across the languages specified in the research plan. No competing \(n=36\) witness, non-`rct4` \(n=37/39\) witness, or earlier no-three-in-line balance/circulation formulation was located.

This negative result is necessarily bounded. Some CNKI/Wanfang, Scopus/Web of Science, MathSciNet/zbMATH and thesis holdings were accessible only through public metadata, and private solver outputs are not searchable. A July 2026 database history note mentions hundreds of new `iden`/`rot2` contributions by Jacob Davies, although the current public target files remain absent. Direct outreach is therefore indispensable before retaining any “first known” language.

Relevant modern context includes Thomas Prellberg's [constraint-programming paper and code](https://arxiv.org/abs/2602.07751), whose odd-order construction is structurally `rct4`, and Mitchell Riley's [GPU repository](https://github.com/mvr/no-three-in-line). Neither located source supplies the same outside-`rct4` witnesses or defect-balance formulation.

### 8.3 Terminology

Flammenkamp also uses “defect” for the shortfall from \(2n\). To avoid collision, this manuscript should use “orbit defect” or “symmetry defect.” It should explain consistently whether `c` is a database pseudo-class, an encoding prefix, or a statement about the actual stabilizer.

## 9. Scientific value

Theoretical value is **moderate**. The balance lemma is elementary as an abstract circulation statement, but it gives a clean conceptual explanation of why symmetry-breaking pairs must balance and how search families arise. Its strongest value is organizational and algorithmic. A carefully generalized version for \(k\)-regular row/column configurations, rectangular grids, or arbitrary group actions on a bipartite incidence system could become a more substantial theorem.

Computational value is **moderate but presently under-documented**. Orbit-based branching and prescribed-pair parameterization are natural and useful, but the manuscript does not yet demonstrate a clearly novel solver architecture against SAT, CP-SAT, GPU search or canonical augmentation. The central-class bug and missing logs substantially weaken claims of completeness. Corrected full sweeps and controlled benchmarks could turn this into a worthwhile computational contribution.

Data value is **real but narrow**. The \(n=36\) exact-\(C_2\) witnesses appear to fill a genuine historical gap. The \(n=37,39\) witnesses add new structural representatives outside `rct4`, not first actual symmetry classes. The \(n=33\) witness is independently inequivalent to the six current ordinary-`rot2` database entries. These are useful database contributions, but isolated witnesses alone are unlikely to sustain a high-tier full article.

Methodological transfer is promising. The balance equation is the kernel equation of an incidence matrix, so it can drive canonical cycle augmentation, SAT symmetry breaking, or flow-based defect generation. The paper should demonstrate at least one such transfer or quantified search reduction if it wants to claim solver novelty.

Historically, the work is most valuable when framed as extending the `rct4` perspective rather than displacing it. The new configurations show that exact half-turn symmetry need not be confined to the classical one-diagonal-pair construction at these orders.

## 10. Partial, negative, and heuristic results

The manuscript should label every non-theorem according to the following matrix.

| Statement type | Correct status and wording |
|---|---|
| One off-diagonal pair cannot be the whole normalized defect | Mathematical consequence of balance |
| A generated family is empty after every canonical subclass terminates | Computer-assisted exhaustive result, tied to exact release/log hashes |
| No configuration found before timeout | Bounded negative search result; never “family is empty” |
| Warm starts did not help | Result of the specified source, transfer rule, solver and budget |
| Local search or belief propagation failed | Algorithm/implementation/protocol-specific observation |
| No simple algebraic structure was detected | Empirical statement relative to explicitly listed curve families, primes and score |
| Search cost grows by a factor \(8\)–\(10\) | Measured ratio for named instances/hardware; not a complexity law |
| \(n=71,73,75,77,\ldots\) may require \(10^5\)–\(10^7\) core-hours | Highly uncertain extrapolation with assumptions and intervals |

Partial sweeps for \(n=36,39,41,45\) must show corrected total denominators and `\ge` signs. A snapshot should contain the exact set of finished, running, timed-out and unstarted subclass identifiers so later updates cannot silently change the meaning of a table row.

The negative-method discussion is too long relative to the positive theorem in a nine-page paper. For a focused note, compress it to a short “exploratory observations” paragraph or move it to a computational supplement. None of these failures supports nonexistence or asymptotic hardness.

## 11. AI/tool-use and authorship-policy analysis

The disclosure is unusually transparent, but saying that an autonomous model performed roughly nine tenths of the technical work creates a serious editorial risk when the submitted version contains errors in priority, exhaustive generation and family classification. Responsibility language is not enough: the human author must actually be able to reproduce and defend every proof, code path and enumeration claim.

The [Electronic Journal of Combinatorics policy](https://www.combinatorics.org/ojs/index.php/eljc/about) permits AI assistance but requires authors to check mathematical details themselves. [Elsevier's generative-AI policy](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals), applicable to Discrete Mathematics, EJC and JCTA, emphasizes human expertise, verification, accountability and disclosure; AI cannot be an author. [Taylor & Francis](https://taylorandfrancis.com/our-policies/ai-policy/) similarly requires transparency and human oversight. [ACM's authorship policy](https://www.acm.org/publications/policies/new-acm-policy-on-authorship), relevant to JEA, excludes generative systems from authorship and places responsibility on named authors.

Before submission, the human author should:

- rederive the balance proof and repair the classification independently;
- review the corrected generator and every pruning rule line by line;
- rerun a deterministic verification suite from a clean environment;
- inspect the labelled-to-canonical class mapping and raw completion logs;
- preserve prompts, model/version information and a concise provenance chronology;
- rewrite the exposition in the author's own voice and explicitly state what was personally checked;
- be able to answer a referee without consulting an unavailable conversational state.

A defensible disclosure would say that generative AI assisted with conjecture generation, code drafting, search planning and prose; name the tools/versions and dates; identify the independent human checks; and state that the author personally verified all proofs, data and final claims. That statement should be made only after the work is actually done.

## 12. Journal and format assessment

The estimates below are subjective, conditional on no further predecessor and on normal editorial variability.

| Venue | Current v0.6 | Corrected focused note | Stronger completed paper | Fit assessment |
|---|---:|---:|---:|---|
| *Journal of Combinatorial Theory A* | 0–2% | 1–4% | 5–12% | Current scope and theorem depth are far below the journal's usual bar |
| *Electronic Journal of Combinatorics* | 1–5% | 12–25% | 25–40% | Topic fit, but needs a complete theorem/classification and impeccable human audit |
| *European Journal of Combinatorics* | 1–5% | 8–20% | 20–35% | Reasonable subject fit; local significance is the main obstacle |
| *Discrete Mathematics* | 1–5% | 22–38% | 35–55% | Best conventional target for a rigorous concise exact-result note |
| *Experimental Mathematics* | 1–4% | 15–30% | 30–50% | Attractive if expanded into reproducible computation with conceptual payoff |
| *Journal of Experimental Algorithmics* | 0–3% | 3–10% | 15–30% | Requires genuine algorithmic novelty and disciplined benchmarking |
| *Ars Mathematica Contemporanea* | 1–5% | 15–30% | 25–45% | Plausible for a clean theory/computation blend |
| *Australasian Journal of Combinatorics* | 2–8% | 25–45% | 40–60% | Strong realistic fit for a focused, corrected combinatorics note |
| *DMTCS* | 1–5% | 10–22% | 20–40% | Better if algorithmic/certificate content is strengthened |

The “current” estimates are low because the title claim is false and purportedly exhaustive tables are wrong. These are not merely stylistic defects.

Recommended formats:

1. **Focused mathematical/data note (best immediate path).** Retain the corrected balance proposition, exact configuration certificates, precise historical positioning, and only completed reruns. Target AJC or Discrete Mathematics.
2. **Theoretical note.** Generalize the orbit-balance lemma to \(k\)-regular bipartite incidence systems and classify normalized minimal defects rigorously. This would improve E-JC/EJC prospects.
3. **Computational paper.** Complete all sweeps, repair the solver, archive instances/logs/certificates, and compare against SAT/CP-SAT/GPU or canonical augmentation. Experimental Mathematics is then plausible.
4. **Database communication.** If theory remains elementary and sweeps remain incomplete, submit verified witnesses to Flammenkamp's database and release a short data/software report rather than stretching to a full paper.

The paper should not be split into two thin manuscripts now. First produce one corrected focused note. A separate computational article is justified only by a materially stronger, completed experimental package.

## 13. Required revisions

### Blocking corrections

1. Remove the claim that \(n=37,39\) are the first exact-half-turn configurations; cite and explain Flammenkamp's `rct4` prior art.
2. Qualify the \(n=36\) priority claim by search date and obtain direct confirmations before publication.
3. Include the central row/column class in directed-cycle generation and rerun all affected rows.
4. Correct Table 1 denominators and the \(n=13\) V2 / \(n=21\) C4 counts.
5. Mark the \(n=37\) C4 count partial until its 46 omitted timed-out subclasses finish; reevaluate all larger rows.
6. Correct Table 2's ordered-versus-\(D_4\)-reduced counts.
7. Narrow or reimplement the mixed-family claim; remove unsupported exhaustive emptiness language.
8. Define the base canonically, repair the central-class and parity statements, and address directed 2-cycles/mixed minimal defects.
9. Correct the `rot2` definition from \(\rho C=C\) to \(\rho^2C=C\), and replace the invalid stabilizer-subgroup inference by an exact \(D_4\) check.
10. Resolve the inconsistent `:`/`c` prefixes of the two structurally analogous \(n=36\) encodings by explicitly defining whether the prefix records actual stabilizer or pseudo-class; fix the missing quote.

### Required computational and reproducibility work

11. Repair PAIRS construction/validation, fatal FIX handling and timeout-resume state.
12. Implement full \(D_4\) canonicalization and preserve labelled-to-unlabelled mappings.
13. Archive every raw run with status, bounds, seed, environment and hashes.
14. Add deterministic build/verification commands, portable flags, CI/container, licence and citation metadata.
15. Supply an immutable DOI-backed archive; preferably add checkable nonexistence certificates or an independent exact solver.
16. Rebuild Tables 1--2 from a machine-readable manifest rather than hand summaries.

### Strongly recommended editorial changes

17. Retitle around orbit defects, not “first” configurations. A safe option is **“Eulerian orbit defects in half-turn-symmetric no-three-in-line configurations.”**
18. Distinguish theorem, exhaustive computation, partial sweep, negative experiment, heuristic and conjecture typographically.
19. Add diagrams of the 3-cycle, two-loop, C4 and V2 decompositions and a stabilizer table for the six witnesses.
20. Add concise solver pseudocode and move long negative/benchmark discussion to a supplement.
21. Use “orbit defect” or “symmetry defect” to avoid conflict with established “defect from \(2n\)” terminology.
22. Contact Flammenkamp, Prellberg, Riley, Heule and Davies; seek independent database inclusion of the witnesses.
23. Expand the bibliography to cover the 1992/1998 history, modern CP-SAT/GPU/SAT work, cycle-space analogues, and computational reproducibility.
24. Replace the present AI statement after a documented human proof/code/data audit, consistently with the selected journal's policy.

## 14. Final verdict

**Verdict: Go after correction and completion; in its strongest near-term form, submit a focused note. Do not submit v0.6.**

The work is not a “do not pursue” case. The displayed witnesses are correct, the \(n=36\) result appears historically meaningful, the outside-`rct4` \(n=37,39\) examples are new in the public record located by this audit, and the balance formulation offers a useful conceptual language. But the current manuscript's headline is historically false for two of three orders, and its central exhaustive table is generated from an incomplete family and already has two wrong result cells. Those defects preclude submission as-is.

A successful revision should make a smaller, sharper claim: a human-verified orbit-balance framework plus independently certified witnesses and only those enumeration statements that survive corrected complete runs. Completing all sweeps is not strictly necessary for a focused existence/theory note, provided partial results are clearly labelled and no exact class-count claim is made. It is necessary for a paper whose selling point is exhaustive family classification.

The likely ceiling of the current mathematical contribution is a solid specialist note, not a top-tier breakthrough. A genuine generalization of the balance method or a certificate-backed comprehensive symmetry classification could raise that ceiling substantially.

## 15. Sources and audit artifacts

### Principal external sources

- Achim Flammenkamp, [symmetry definitions](https://wwwhomes.uni-bielefeld.de/achim/no3in/symmetry_remarks.html), [database table](https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html), [1997 discovery chronology](https://wwwhomes.uni-bielefeld.de/achim/no3in/odd_results.html), and [downloadable configurations](https://wwwhomes.uni-bielefeld.de/achim/no3in/download/solutions_by_symmetry/).
- Achim Flammenkamp, “Progress in the No-Three-in-Line Problem, II,” *JCTA* 81 (1998), [DOI 10.1006/jcta.1997.2829](https://doi.org/10.1006/jcta.1997.2829).
- Achim Flammenkamp, “Progress in the No-Three-in-Line Problem,” *JCTA* 60 (1992), [DOI 10.1016/0097-3165(92)90012-J](https://doi.org/10.1016/0097-3165(92)90012-J).
- Thomas Prellberg, [“Constraint Satisfaction Programming for the No-three-in-line Problem”](https://arxiv.org/abs/2602.07751) and associated public code.
- P. L. Erdős, Z. Király and I. Miklós, [balanced red-blue cycle decomposition](https://arxiv.org/abs/1205.2842).
- C. Godsil and K. Guo, [“Cycle Spaces of Digraphs”](https://arxiv.org/abs/1609.09118).
- [OEIS A000769](https://oeis.org/A000769) and [A272651](https://oeis.org/A272651).
- Journal policy pages: [E-JC](https://www.combinatorics.org/ojs/index.php/eljc/about), [Elsevier](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals), [Taylor & Francis](https://taylorandfrancis.com/our-policies/ai-policy/), and [ACM](https://www.acm.org/publications/policies/new-acm-policy-on-authorship).

### Reproducible local audit artifacts

| Artifact | SHA-256 |
|---|---|
| Supplied manuscript PDF | `bec5cc36f1ffbc16824a8cbb48178288b3a536dc59f3c21a7deeee2d99fa3ff5` |
| Clean-room configuration verifier A | `1eb27a3a546cd0f2bcb11d43662430a05310e97713107dd514c5d7c3a07ee3e4` |
| Verifier A exact JSON | `cfe4bb3f3c1ceb6fb00ea4290f6589d3d4aa7e6fe05bd6c5972d68b4d5db13a9` |
| Clean-room configuration verifier B | `14e2d553bbf7908e43e8ae25f1a6b556eef69dbf8727619bb2f62e94f63673ae` |
| Verifier B exact JSON | `a5ea3ca22d0f7fa19f235e9ca2cd1a208abe1e65384323394ead77bf1f9d70cd` |
| Defect-enumeration audit script | `f930ea5aece28bf6b0459b13b8fbc73b08b096f746edcc6d31b74662aab6aa58` |
| Defect-enumeration exact JSON/log summary | `9f970a74c095ea26fce9d67da260c6d6bfc5b5d2f81fbd4a79dc4f3757fbd47f` |
| Multilingual/grey novelty report | `81135ab72cd41bcbf8cd1745ad3564ce8c16e680ab2a5bead1bdbb2bb8546ea9` |

The repository source hashes and individual run commands are recorded in the audit workspace and should be included in any public replication package. The final paper should publish its own self-contained machine-readable manifest rather than depend on this review.
