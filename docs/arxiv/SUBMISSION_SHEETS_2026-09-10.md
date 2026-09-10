# arXiv submission sheets — prepared 10 Sep 2026

The math.CO endorsement was granted 7 Sep 2026. Submit at https://arxiv.org/submit/ from the account
studio@nusadua.dev (the arXiv account; the endorsement notice of 7 Sep 2026 arrived there). First-time submissions from this account are held for moderation. Upload the package zip;
ancillary files must live in a folder named `anc/` inside the upload. Primary category: math.CO. License:
recommend CC BY 4.0, to match the Zenodo records. After each submission, note the resulting submit/NNNNNNN id
in this file next to the paper it belongs to.

---

## 1. A280537 — no-four-coplanar in the cube

Package: `paper/arxiv_a280537_v34/`, zipped as `paper/arxiv_a280537_v34.zip` (existing package; test-compiled
2026-09-10, 7 pages, clean).

Submit id: (not yet submitted)

**Title:** Nineteen certified configurations, eighteen independent bounds for the no-four-coplanar problem in
the cube, and what they do not establish

**Authors:** Aleksei Kudriashov

**Abstract:**
Let $a(n)$ be the largest number of points of $\{0,\dots,n-1\}^3$ no four of which are coplanar
(OEIS A280537).  Earlier versions of this note claimed that published data stop at $a(8)=20$.
\emph{That claim was false}, and this version exists to correct it: a January 2017 comment on
the OEIS entry itself records lower bounds up to $a(17)\ge42$ \cite{OEISA280537}, and a 2016
public programming contest ran exactly this problem on the first twenty-five primes, with
per-size bests recoverable from its final report \cite{AZsPCs} --- $28$ at $n=11$, $32$ at $13$,
$42$ at $17$, $46$ at $19$, $54$ at $23$, $66$ at $29$, down to ratio $1.94\,n$ at $n=97$.
Three rows of our table ($n=14,15,17$) are below the 2017 bounds and four prime rows
($n=17,19,23,29$) are below the 2016 contest bests; Section~2 gives the full comparison.

What remains, stated against that prior art.  Nineteen configurations, each verified by two
programs sharing no code, with all coordinates public --- the prior bounds come as numbers
without accessible witnesses.  Four improvements over the known bounds \emph{and their monotone
closure} under $a(n+1)\ge a(n)$: $a(12)\ge31$ against the recorded $30$, and $a(21)\ge47$,
$a(22)\ge49$, $a(27)\ge56$ against the $46$, $46$, $54$ implied by the contest values at $n=19$
and $n=23$.  The remaining composite rows ($n=18$, $20$, $24$, $25$) fall \emph{below} that
closure and are public witnesses, not records: version 3.1 called them ``apparently first
published'', and the monotone comparison that removes them is due to Hugo Pfoertner.  And two proved
statements above $n=8$, both about the cyclically invariant subspace and both exhausted by two
independent implementations: its maximum is $23$ at $n=9$ and $26$ at $n=10$.

Version 3.3 adds a search over all 33 symmetry classes of the cube group
(Section~\ref{s:strata}): no bound changes, but the best known values at $n=7$, $8$, $9$ are
attained by three pairwise inequivalent configurations each (stabilisers of orders $1$, $2$, $3$
at $n=7$ and $8$), all rigid and mutually unreachable by small exchanges, and four kinds of
symmetry are shown to be incompatible with the problem.

No upper bound above $n=8$ is known to us beyond the trivial $a(n)\le3n$; every number in the
table is a lower bound only, and the earlier failure to check the field before claiming novelty
is recorded in Section~2 rather than erased.

**Comments:** 7 pages; version 3.4 (3 September 2026); also at Zenodo doi:10.5281/zenodo.22272371;
ancillary files: verify_witness.py and 7 witness configuration files (Section 9 symmetry strata,
n = 7, 8, 9, 11).

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22023079

---

## 2. A399138 / no-three-in-line in the cube

Package: `paper/arxiv_no3_3d_v15/`, zipped as `paper/arxiv_no3_3d_v15.zip` (existing package;
test-compiled 2026-09-10, 8 pages, clean).

Submit id: (not yet submitted)

**Title:** Exact values and certified lower bounds for the no-three-in-line problem in the cube

**Authors:** Aleksei Kudriashov

**Abstract:**
Let $a(n)$ be the largest number of points of the grid $\{0,1,\dots,n-1\}^3$ no three of which are collinear.
P\'or and Wood proved $a(n)=\Theta(n^2)$, the lower bound by the construction
$\{(x,y,x^2+y^2\bmod p)\}$, which has no three collinear precisely when $p\equiv3\pmod4$
(Lemma~4 of \cite{PorWood}); no exact values appear to have been recorded, and the sequence was not in
the OEIS when this work began (it is now A399138, approved August 2026).  We determine
\[a(1),\dots,a(6)=1,\,8,\,16,\,28,\,40,\,64,\]
give certified lower bounds $a(7)\ge73$, $a(8)\ge94$, $a(9)\ge116$, $a(10)\ge138$, $a(11)\ge164$ (the bounds for $n\ge8$,
new in version 1.5, come from exact optimisation inside the symmetry classes of the cube group), and prove $a(p)\ge p^2$ for every prime $p$ by an
elementary construction from an anisotropic binary quadratic form.

The method is a certified decision procedure rather than a search: a line carrying at most two lattice points
forbids nothing, so admissibility is exactly ``at most two chosen points on every line with three or more
lattice points'', which is a propositional formula on $n^3$ variables.  Unsatisfiability is answered with a
DRAT certificate that an independent checker verifies, and the lower bounds are witnesses re-verified by
exhaustive integer arithmetic over every triple.  We are explicit about the three separate links this
requires --- that the formula expresses the problem, that it is unsatisfiable, and that the symmetry pruning
discards nothing --- because a certificate attests only to the formula it was given, and an error in the other
two links would pass through it unseen.

Along the way the optima turn out to share a layer structure that fails at exactly one of the values computed:
for $n=2,3,4,6$ the two outer layers carry the planar maximum $2n$ and the inner ones $2n-2$, giving
$2n^2-2n+4$; at $n=5$ two outer layers provably cannot both carry $2n$ at any total, and at $n=7$ the
corresponding profile is impossible as well.  We have no explanation for this.

**Comments:** 8 pages; version 1.5 (3 September 2026); also at Zenodo doi:10.5281/zenodo.22273425;
witnesses archive doi:10.5281/zenodo.22271375; ancillary files: verify_witness_lines.py and 6 witness
configuration files (n = 8..11).

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22019279

---

## 3. hjsw_window — the Hall–Jackson–Sudbery–Wild window

Package: `paper/arxiv_hjsw_window_v118/`, to be zipped as `paper/arxiv_hjsw_window_v118.zip`.
NOT YET IN THE REPOSITORY (repo write access unavailable to this session; the package is fully
assembled and test-compiled in the scratchpad — see the session report — ready to be copied in and
zipped by a session with write access).

Submit id: (not yet submitted)

**Title:** Extremal no-three-in-line subsets of a modular hyperbola in the Hall–Jackson–Sudbery–Wild window

**Authors:** Aleksei Kudriashov

*(Note: the .tex source's own \author field reads only "Alex Komang" — it does not contain
"Aleksei Kudriashov" as the other five papers' bylines do. Flagged in the session report; resolve
the byline before submitting under the real name.)*

**Abstract:**
Let $p$ be an odd prime, $c\in\Fp^*$, and $\Hc=\{(x,y):xy\equiv c\pmod p\}$ the modular hyperbola in the
$2p\times2p$ window of Hall, Jackson, Sudbery and Wild (1975), whose construction keeps $3(p-1)$ of its points
with no three collinear --- still the best known lower bound for the no-three-in-line problem.  Whether that
deletion is optimal inside its window has remained unproved, and was stated without proof by Kov\'acs, Nagy and
Szab\'o.  We prove it, for every $c$, and determine the complete extremal structure: the rich lines have slope
$\pm1$ and number $\tfrac32(p-1)-s$; even the fractional LP relaxation equals $3(p-1)$; the number of maximum
sets is exactly $9^s$, where $s\in\{0,1,2\}$ counts the quadratic residues among $\pm c$, so the HJSW set is the
unique maximum iff $p\equiv1\pmod4$ and $c$ is a non-residue; an orbit lemma gives the exact maximum
$12n_2+10n_1+8n_0+6s$ for every position of the window; near-maximum sets are stable; and the largest
no-\emph{four}-in-line subset has exactly $\tfrac72(p-1)+s$ points.  Beyond one hyperbola: the union
$H(1)\cup H(-1)$ satisfies $\alpha\le(115/32+o(1))(p-1)$, refined to $(3.4482\ldots+o(1))(p-1)$ by a block
decomposition along runs of consecutive squares of $\Fp$; and no conic, cubic graph or permutation monomial
$x^k$ reaches the hyperbola's $3(p-1)$ --- closing the natural algebraic routes toward Green's Problem~72.
The constants of the two final sections are fixed by explicit numerical quadrature rather than interval
enclosure and are labelled accordingly.

**Comments:** 46 pages; version 1.18 (3 September 2026); also at Zenodo doi:10.5281/zenodo.22275500;
ancillary files: none (all \input files are included in the package: lemma_stability, section_seven,
section_blocks, section_cubic, section_perm, section_strong, appendix_hyperbolae, lemma_run, lemma_fe).

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22063297

---

## 4. no3inline_defects — balanced orbit defects, half-turn symmetry

Package: `paper/arxiv_no3inline_defects_v13/`, to be zipped as `paper/arxiv_no3inline_defects_v13.zip`.
NOT YET IN THE REPOSITORY (see note under hjsw_window above — assembled and test-compiled in the
scratchpad, ready for hand-off).

Submit id: (not yet submitted)

**Title:** Balanced orbit defects in half-turn-symmetric no-three-in-line configurations, with new
2n-point configurations for n=36, 37, 39

**Authors:** Aleksei Kudriashov

*(Note: the .tex source's own \author field reads only "Alex Komang", as with hjsw_window — see the
same flag above.)*

**Abstract:**
A $2n$-point no-three-in-line configuration on the $n\times n$ grid with half-turn symmetry can be written as the union
of the orbits of a larger subgroup $H\le\Dfour$ (the quarter turns, or the two diagonal reflections) that it contains,
together with a set of half-turn pairs that are not $H$-orbits --- its \emph{orbit defect} relative to $H$.  We prove a
\emph{balance lemma}: the defect pairs, read as arcs on the row classes $\{i,n-1-i\}$, form a balanced directed
multigraph, hence a union of directed cycles.  With one further observation (two half-turn pairs on the same long
diagonal are collinear) this classifies the defects with at most three pairs: one pair must be a diagonal loop ---
Flammenkamp's pseudo-class rct4; two pairs are two loops on different diagonals or a directed $2$-cycle, which is an
orbit of the diagonal reflections; three pairs form a directed $3$-cycle or a loop plus a $2$-cycle.  We enumerate the
corresponding families exhaustively for small $n$ with an exact branch-and-bound program (validated against OEIS A000769
and the class counts of Flammenkamp's database): the $3$-cycle family for odd $n\le25$ and $n=33,37,39,41$, each swept to completion in both bases (and, in part, $45$); the two-loop family for even $n\le28$ and $n=36$ ($n=30,32,34$ not swept); the mixed families for $n\le27$ (all empty).  Among the
configurations found are: for $n=36$, the first located $2n$-point configurations for that $n$ whose symmetry group is exactly the
half-turn (exactly three inequivalent ones, in the two-loop family); for $n=37$ (two) and $n=39$ (four), the first located configurations of that
symmetry group outside the rct4 pseudo-class (Flammenkamp's rct4 configurations of 1997/98 already have exactly
half-turn symmetry); and a further one for $n=33$.  ``First located'' refers to the public files of Flammenkamp's
database as of 2026-08-11 (confirmed by its maintainer, who has added the configurations to the database).  Configurations,
programs and sweep journals are public.

**Comments:** 11 pages; version 1.3 (August 2026); also at Zenodo doi:10.5281/zenodo.22064192;
ancillary files: none (appendix_configs.tex, the ten configuration listings, is `\input` into the main
file and travels with it, not as a separate ancillary file).

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22063287

---

## 5. guy_kelly_error — the Guy–Kelly heuristic audited

Package: `paper/arxiv_guy_kelly_error_v19/`, to be zipped as `paper/arxiv_guy_kelly_error_v19.zip`.
NOT YET IN THE REPOSITORY (assembled and test-compiled in the scratchpad, ready for hand-off).

Submit id: (not yet submitted)

**Title:** The error of the Guy–Kelly heuristic, measured against exact counts

**Authors:** Aleksei Kudriashov

**Abstract:**
The Guy--Kelly heuristic for the no-three-in-line problem is a first-moment estimate:
$\log\binom{n^2}{m}$ is equated with the expected number of collinear triples in a random
$m$-subset, as if the triples were independent.  We audit that heuristic against exact counts
(A000755 to $n=19$, and $n=20$ from Flammenkamp's table~\cite{Flammenkamp}), not at its threshold
but on the quantity it actually predicts --- the \emph{number} of configurations.

What the audit confirms.  The corrected constant comes out in closed form: measuring
$T(n)=\tfrac{3}{\pi^2}n^4(\ln n-0.8373)$ and balancing the $n\ln n$ terms gives
$\alpha^2=\pi^2/3$, i.e.\ $\pi/\sqrt3=1.813799$; the retracted 1968 value is the root of a cubic
balance where a quadratic one belongs.  Two implementations sharing no code agree on the integer
threshold crossing at $n=493$, reproducing Prellberg.

What the audit finds against the heuristic.  Its error is a function of the \emph{shape} of the
question, not of $n$ alone: at the single $n$ where all three measurements exist ($n=20$) it
overestimates by a factor $8\cdot10^{6}$ at the hard ceiling $m=2n$, by a factor of about $80$
near the threshold ratio, and is off by less than $1.4$ at $m=1.6n$ (there an underestimate),
where two independent implementations agree to $0.18$ standard deviations.  At every ratio we can
reach, the error then declines without levelling: \emph{the multiplier is not bounded}.  An
earlier version of this note claimed the opposite, at thirteen standard deviations; Section 6
withdraws that measurement --- its two carrying points had five and one hundred sixty successful
descents per two hundred thousand attempts --- and the withdrawal is kept in the text rather than
erased.

What remains open, and provably so by this route.  Whether the residual error is $\Theta(n)$ or
$\Theta(n\ln n)$ decides whether the constant survives, and the data cannot tell: four admissible
forms fit the same tail and answer oppositely, and the two bases stay collinear to $0.9993$ out
to $n=10^4$, so no budget of the same kind of computation decides it.  The ratio that governs the
conjecture, $r\approx0.907$, is precisely where the estimator loses its depth --- the error's
summit there lies beyond reach, so on the critical shape we have measured the ascent only.  To
Kaplan's objection, that looking closely at the dependence might change the conclusion, our
answer is that we cannot tell by counting, and we have measured how far from telling we are.

**Comments:** 8 pages; version 1.9 (23 August 2026); also at Zenodo doi:10.5281/zenodo.22063379;
ancillary files: none.

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22063191

---

## 6. direction_spectrum_note — the direction spectrum of no-three-in-line solutions

Package: `paper/arxiv_direction_spectrum_note_v11/`, to be zipped as
`paper/arxiv_direction_spectrum_note_v11.zip`. NOT YET IN THE REPOSITORY (assembled and
test-compiled in the scratchpad, including the anc/ folder, ready for hand-off).

Submit id: (not yet submitted)

**Title:** The direction spectrum of no-three-in-line solutions: a line model derives its shape, not its scale

**Authors:** Aleksei Kudriashov

**Abstract:**
A \emph{solution} of the no-three-in-line problem is a set of $2n$ points of the $n\times n$ grid with no three
collinear.  For a primitive direction $v$ let $c_v(n)$ be the mean number of point pairs of a solution whose
difference is a positive multiple of $v$, divided by $n$ (averaged over the images of $v$ under the symmetries of
the square).  Measured on Flammenkamp's database of all known solutions, the short directions are nearly constant in
$n$ ($c_{(1,1)}=0.731$, $c_{(1,2)}=0.564$) and depleted against a null model with fixed row and column sums
(ratio $0.58$ and $0.75$), while long directions are slightly enriched and grow with $n$.  We show that the
\emph{shape} of this spectrum --- the ratios between directions and their order --- follows from a single rule with
no fitted parameter: distribute $2n$ points over the lines of one direction with at most two points per line, the
weight of a line of $L$ cells carrying $x$ points being $\binom{L}{x}$.  The expected number of doubly occupied lines
is given exactly by a generating function; one global renormalisation to the exact number of non-axial pairs of a
solution, $2n^2-3n$, fixes the scale.  The model reproduces fifteen measured constants within $12\%$ (model$/$data $0.89$--$1.05$ at $n=20$,
$0.88$--$1.02$ at $n\approx30$) and their order at matched $n$ up to one adjacent pair; seven of them were predicted before being measured by a second agent who had not seen the
model.  What the model does \emph{not} do is stated with equal care: the scale is imposed, not derived --- the
model's own total falls $17\%$ short of $2n^2-3n$, and the shortfall it redistributes is exactly the deficit seen in the
measured directions; the growth of long directions with $n$ is a property of the solutions that the model only
partly tracks.  A multi-channel prior-art search has now been carried out (Section~\ref{s:prior}): we found no published or
web-posted measurement of pairs per direction on actual solutions, no $\kappa$-like constant, and no per-direction
decomposition of the Guy--Kelly count; the nearest objects are listed and delimited there, and the search's own
limits are stated.

**Comments:** 6 pages; version 1.1 (3 September 2026); also at Zenodo doi:10.5281/zenodo.22278951;
ancillary files: direction_spectrum_model_values.txt, direction_spectrum_data_by_strata.txt.

**MSC classes:** none stated in the source.

**Related DOI (concept):** 10.5281/zenodo.22275037
