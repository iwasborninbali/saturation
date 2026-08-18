# HUMAN_AUDIT.md — contribution and verification log of the author of record

Purpose: journals' AI policies (E-JC, Elsevier, AJC, Springer — see `docs/reviews/hjsw_window_deep_research_audit_2026-08-18.md`
§11) require that a human author has personally checked every proof and detail, and that the human contribution is stated
truthfully.  This file is the place where the author of record (Alex Komang) records what he has personally done.  It is
written by the agents as a checklist; entries are to be filled in **by him, in his own words**, and dated.  Nothing here
should be claimed that did not happen.

## What the AI systems did (for the record)
- posed no question; the author posed the problem (blinded), directed scope, and made all publication decisions;
- wrote all programs, ran all searches, found and proved all lemmas/theorems, drafted both notes, corrected them after audits;
- verified each other's results with independent programs; kept the correspondence in `docs/THREAD.md`.

## What the author of record did (fill in / correct)
- [ ] posed the problem, provided machines and credit, directed the work (dates: 2026-08-16 … )
- [ ] commissioned two external LLM-assisted audits of the HJSW note (2026-08-18) and returned them to the agents
- [ ] sent the letter to A. Flammenkamp (2026-08-17); authorised the letter to Kovács–Nagy–Szabó (sent 2026-08-18)
- [ ] reproduced the computational checks of the NOTE: `python3 slack/hjsw_window_check.py 31`, `python3 slack/hjsw_boxes_check.py 13 13`,
      `python3 slack/gadget11_check.py 13 6` (date, machine, output kept where?)
- [ ] reproduced the checks of the MAIN PAPER: `make check` (A000769 count, rot4 n=24, rct4 n=21, the first n=37 sub-class,
      the n=13 central sub-class); `python3 -c "import json,sys; sys.path.insert(0,'web'); import stab, saturation; ..."` or simply
      `python3 kit71/certify_book.py N "<tokens>"` for each of the seven configurations in `docs/SUBMISSION.md` (law + stabilizer);
      one sub-class sweep by hand, e.g. `ALL=1 PAIRS="6,6;5,30" ./there 36 2` (7 min) and compare with `logs/sweeps/twoloop_n36_exh.txt`
- [ ] read `docs/reviews/*_deep_research_audit_2026-08-18.md` (both audits) and checked that every blocking item is addressed
      in the current drafts (`docs/THREAD.md` [50], [53])
- [ ] rederived on paper (NOTE): Lemma 1 (two classes per line), Lemma 2 (square of copies), Lemma 4 (partner table), Proposition 5
      (rich lines), the double count (§4), the equality classification and 9^s, the orbit lemma (§5), the gadget counts
      (9+54+81), Corollary (no-four)
- [ ] rederived on paper (MAIN PAPER): the balance lemma (row/column counts of an H-orbit), the arc interpretation on row classes
      (in/out-degree), Proposition (defects with at most three pairs: two loops on one diagonal are collinear; a 2-cycle is a
      dia2- or a C4-orbit), the parity statements, the corrected validation formula N_H
- [ ] read every citation against the primary source
- [ ] rewrote / edited passages of the text (which?)
- [ ] decided the venue and the wording of the disclosure for that venue

## Contribution log (append entries: date — what — by whom)
- 2026-08-18 — this file created (agent 2, at the request implied by the audit §11.3)
