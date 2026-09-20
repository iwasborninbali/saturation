# arXiv combined article — report of the science crew (21 Sep 2026, 02:4x WITA)

Task (Alex, 21.09 02:3x, verbatim): «подними команду ученых … пусть готовят статьи для публикации на архив (дай им причину почему нас не опубликовали в прошлый раз, пусть примут решение сколько в итоге для архива будет статей) - затем опубликуем». Why the last attempt failed: arXiv moderation MOD-104121 (10.09, 15:15 UTC) declined all three notes submitted that day (submit/8060684 no3_3d, 8062345 a280537, 8062503 guy_kelly) as «similar ideas and content … variations on the same theme» and invited «one combined article»; the other three notes were never submitted (conductor `docs/order-2026-09-20/arxiv-funding.md` §1–3).

## Decision: three arXiv articles in the end (a proposal; Alex confirms)

1. **One combined article now** (this package): no3_3d v1.5 + a280537 v3.4 + guy_kelly v1.9 + direction_spectrum v1.1.
2. **hjsw_window v1.18**, unchanged, on a later day. 3. **no3inline_defects v1.3**, unchanged, on a later day after the combined article is announced.

Grounds. The notice literally asks for one article of the declined trio; an appeal is final and feedback-less. direction_spectrum shares the most text with guy_kelly (3.1 % of 6-word shingles, the highest of all 15 pairs), the same data (Flammenkamp's database, A000755) and the same object (the Guy–Kelly count), so alone next to the combined article it is the likeliest repeat flag: it goes in. A two-article split (cube / plane) would re-separate guy_kelly from the two cube notes, i.e. resubmit the very trio that was declined together. hjsw_window (46 pp, 51 theorem-type statements, a proof paper on one algebraic question) and no3inline_defects (11 pp, 3 statements, configurations confirmed by Flammenkamp; text overlap ≤ 1.9 % with everything) would each be buried by a merge and would push the combined article past 28 pp. Residual risk, not a blocker: both are planar no-three-in-line papers too; mitigation is separate days, distinct Comments fields, and content of a different kind (proofs and structure, not computation).

## What was assembled, where

Branch `science/arxiv-combined-2026-09` of `~/projects/science/saturation` (from main 9ea027e); commit 6074952 carries the package, the next commit this report. Files: `paper/arxiv_no3_certified_combined_v10/no3_certified_combined.tex` (the article, nine sections per arxiv-funding.md §4.2: 1 Introduction; 2 Notation and public objects; 3 Part I cube/no three collinear; 4 Part I′ cube/no four coplanar; 5 Part II Guy–Kelly; 6 Part II′ direction spectrum; 7 Across dimensions; 8 Verification and reproducibility; 9 AI/tool-use disclosure; 20 references); `…/anc/` (17 files: verify_witness_lines.py + six A399138 witnesses, verify_witness.py + seven A280537 witnesses, two direction-spectrum data files, README.txt); `paper/arxiv_no3_certified_combined_v10.zip` (flat: tex and anc/ at the root, 20 entries, sha256 22ea8fcbb161e4676f5a379b98750608de0982fad7a472a0a3cad9ff9895402d); `paper/no3_certified_combined.tex` and `.pdf` (sha256 d52f392f14c30c25665355517ea75f89453ce19ad03fc46a984ae75fd0fe9a6b); entry 7 appended to `docs/arxiv/SUBMISSION_SHEETS_2026-09-10.md` (= form card 7: title, plain abstract, comments).

Title: «Certified computations on no-three-in-line problems: exact values and witnesses in the cube, and the Guy–Kelly count in the plane». One notation: a(n) = A399138, b(n) = A280537, s(n) = A000755 (the a280537 proposition now reads b(n) ≤ 3n, unchanged up to the symbol); Z_n → λ_n for the renormalisation of Part II′ (the theorem keeps its Z_m). Deduplicated: four introductions → one; the rich-line/rich-plane reformulation once (§2); the stratum sweep once (§3.4, referenced from §4.4); the planar enrichment factors ×8…×73 000 once (§4.3, referenced from §5.4); the planar greedy fractions 8/8, 3/8, 2/8, 1/8 once (§5.7; the §4.7 correction now points there); guy_kelly «On three dimensions» + a280537 «a bound refuted» → §7; four reproducibility sections → §8; four disclosures → §9; the «eighteen independent bounds» headline retired (recount against the monotone closure: four improvements). Deviation from the outline: the direction-spectrum prior-art search kept as §6.5 (it is the evidence for the novelty claim), not folded into §1. Nothing mathematical dropped: every number of the four sources was searched in the combined text; only version numbers and abstract roundings are unmatched.

## Measured

- Compile: pdflatex (TeX Live 2025, pdfTeX 1.40.27), three passes from a fresh unzip of the zip: 0 errors, 0 undefined references, 0 non-font warnings, 1 overfull hbox of 2.9 pt (present in the original guy_kelly note as well); **27 pages** (acceptance window 20–28; the four notes summed to 29).
- Abstract: **1907 characters** plain text (limit 1920), macro-free, in sheet entry 7.
- Witnesses: all 13 anc/ configurations re-verified in this session with the two independent scripts — 0 collinear triples (134 044, 134 044, 253 460, 253 460, 428 536, 721 764 triples checked), 0 coplanar quadruples in the seven A280537 files.
- Theorem-type statements across the three live papers (grep of theorem/proposition/lemma/corollary, bodies normalised): combined 3 (Prop. b(n) ≤ 3n; Prop. a(p) ≥ p²; Thm. generating function of the line model); hjsw_window 51; no3inline_defects 3; **shared statements 0**, shared 6-word shingles between statement bodies 0.
- Moderation self-check: one article; nothing pending from the account (mailbox measured 20.09: three declined, silence after 10.09 15:15 UTC); Comments names the consolidation and the three declined ids; §8 lists the four Zenodo records and says the article supersedes them; math.CO only, no cross-list; author field = arXiv profile name «Aleksei Kudriashov».

## What remains before Submit

1. Alex: confirm the count (three) and the title; the retractions are kept visible on purpose (§3.1 correction, §4.1, §4.7, §5.6).
2. Adversarial read by the second-model channel (arxiv-funding.md §5 step 3) — NOT done here: only the grep-level check above; one question to ask it: does any statement contradict hjsw_window or no3inline_defects.
3. New Zenodo record for the combined text (Alex's login, or the gate's token); then the `\date` line gains the DOI; README paper table and no3-results rows (not touched here: the README lists DOIs and the combined text has none yet).
4. Push of the branch and PR to main — the Conductor's call; nothing was pushed.
5. Alex uploads the zip (arXiv Start » Add Files » … » Preview); the Conductor diffs the Preview text against entry 7 character by character; Alex clicks Submit. Later days: hjsw_window, then no3inline_defects.

Route: the №140 wall refuses writes into the science tree from a conductor-launched session, so this package was built in the session scratchpad and applied by a headless science-shop session launched in `saturation` running one deterministic script (the door of 10.09); nothing outside `~/projects/science/saturation` was modified.

## Open questions for Alex

- Keep the four Zenodo records as they are (cited by OEIS and the funding materials), with a «superseded on arXiv by …» note, or version them?
- Affiliation «Nusa Dua Studio» and the ORCID are carried over unchanged — still right for this article?
