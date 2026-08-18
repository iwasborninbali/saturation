# MANIFEST — claim → artifact map for `paper/hjsw_window.pdf` (note v1.0)

Every non-trivial claim of the note points to a script (re-runnable) and, where applicable, a log or witness file.  Witness files contain
point lists that `saturation.the_law` re-checks in exact integer arithmetic; "solver-proved" upper bounds have no independent certificate.

| claim (note) | kind | script(s) | log / witness | scope checked |
|---|---|---|---|---|
| Thm 1 (rich lines slope ±1; count; max 3(p−1); LP value; 9^s) | theorem; sanity check | `slack/hjsw_window_check.py` | `slack/verification/hjsw_window_check_all.log` | all p ≤ 101 (all c for p ≤ 31) |
| Thm 3 (every 2p×2p box: 12n₂+10n₁+8n₀+6s; orbit lemma; gadget counts) | theorem; sanity check | `slack/hjsw_boxes_check.py`, `slack/gadget11_check.py` | `slack/verification/hjsw_boxes_check.log`, `gadget11_check.log` | all boxes p ≤ 13; orbit lemma p ≤ 31; identities p ≤ 199; (1,1) gadgets p ≤ 31 |
| Cor. no-four (7/2(p−1)+s) | theorem | (covered by hjsw_window_check) | same | p ≤ 101 |
| Cor. conics (only shifted hyperbolae reach 3(p−1); example (x−y)y=1, p=7: 16) | theorem + example | inline CP-SAT (docs/research/pair_bound_notes.md §13) | — | p=7 example |
| Table of shifted boxes p=11 | computation (MIP) | `slack/hjsw_boxes_check.py` (MIP step) | `hjsw_boxes_check.log` | p=11, all boxes |
| Remark larger boxes (N from 2p to 3p; 3p×3p; 2p×4p) | computation (MIP, zero gap) | `slack/liftmax.py`/`slack/milp_max.py` (third) | `slack/verification/windows_2p_to_3p.txt` | p ≤ 23 |
| Thm two hyperbolae: α(P₋₁) ≤ 4(p−1) − 4m₈(p) | theorem; explicit cover verified | `slack/km1_theorem_check.py`, `slack/block_cover_km1.py` | `slack/verification/block_cover_km1.log` | cover checked p ≤ 101 / p < 320 |
| Prop m₈ formula (pairs (a,b) on the cubic, least residues) | proposition; check | `slack/km1_lines.py` + inline count (notes §12) | — | 4m₈ = count, p ≤ 199 |
| Prop m₈ ~ p/12 (Bombieri + ETK) | proposition (proof quotes standard estimates) | `slack/km1_lines.py` (data) | — | m₈/p mean 0.0825 over 200 ≤ p ≤ 1500 |
| §6 pairs table (exact maxima all k) | computation (SAT/MIP/CP-SAT) | `slack/cpsat_max.py`, `slack/milp_max.py`, `slack/maxlawful_pysat.py` | `slack/verification/pairs_allk_p11_p13.txt`, `pairs_allk_p17.txt`, `pairs_p19.txt`; witnesses `slack/witnesses/pair_*` | p ≤ 19 exact; p=23: 70–74; p=29: ≥84 |
| §6 rich-line generator cross-check | independent regeneration | `slack/lines_crosscheck.py` | `slack/verification/lines_crosscheck.log` | p ≤ 19 |
| §6 LP(1)/IP(1) statements | computation (LP/MIP) | `slack/lp1_dual.py`, `slack/lp1_general.py`, third's `bench/ip1_km1.log` | `slack/verification/ip1_km1.log`, `lp1_general_k{2,3}.txt` | k=−1 p ≤ 199; k=2,3 p ≤ 199; IP(1) p ≤ 59 |
| §6 structure of optima; orbit blocks; block locality | computation | `slack/pair_structure.py`, `slack/orbit_blocks.py`, `slack/block_pairs.py`, `slack/block_subsets.py` | `slack/verification/orbit_blocks_km1.txt`, `orientation_km1.txt` | p ≤ 19 (23 partial) |
| §6 restricted / periodic models | computation | `slack/cpsat_max.py R`, `slack/periodic_model.py`, `slack/inner_pairs_model.py` | `slack/verification/restricted_R.txt` | p ≤ 29 |
| §6 vertical-pair model: T quadratic; spectral bound | computation (exact algebra) | `slack/vp_fourier.py`, `slack/vp_quadratic.py` | `bench/vp_quadratic_large.log` (in repo? see notes §20) | p ≤ 71 |
| §6 parabola+hyperbola, triples, two primes, cross triples | computation | third's MIP; `slack/crosstriples.py`, `slack/liftmax.py` | `slack/verification/ph_triples.txt`; witnesses `slack/witnesses/triple_*`, `union_*` | as stated |
| §6 blocking heuristic (log p, unblocked 0–2) | computation | third's scripts (THREAD [36]) | — | p ≤ 101 |

Tags: `hjsw-note-v1.0` (this manifest), checksums in `docs/RELEASES.md`.  Environment: `docs/RELEASES.md`.
