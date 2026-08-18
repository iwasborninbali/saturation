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
- [ ] reproduced the computational checks: `python3 slack/hjsw_window_check.py 31`, `python3 slack/hjsw_boxes_check.py 13 13`,
      `python3 slack/gadget11_check.py 13 6`, `python3 web/stab.py 36 …` on the configurations of `docs/SUBMISSION.md`
      (date, machine, output kept where?)
- [ ] rederived on paper: Lemma 1 (two classes per line), Lemma 2 (square of copies), Lemma 4 (partner table), Proposition 5
      (rich lines), the double count (§4), the equality classification and 9^s, the orbit lemma (§5), the gadget counts
      (9+54+81), Corollary (no-four); balance lemma of the defects note
- [ ] read every citation against the primary source
- [ ] rewrote / edited passages of the text (which?)
- [ ] decided the venue and the wording of the disclosure for that venue

## Contribution log (append entries: date — what — by whom)
- 2026-08-18 — this file created (agent 2, at the request implied by the audit §11.3)
