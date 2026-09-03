## Q1 — the habit each principle asks for

1. **To the sources.** Treat every snippet, abstract, citing paper and search-model summary as a *shadow* of a claim, and refuse to let it rise above that status until I have opened the text myself and can point to the exact sentence I read.
2. **Measure.** Attach a status to every claim (seen / read in source / inferred / unknown), let the verdict inherit the strength of its *weakest* support, and say where my search stopped — "not found" describes my search, not the world.
3. **Decision.** Say what I actually know in the fewest clear words, lead with what the reader should do about it, and leave unsaid the part I cannot state clearly rather than dressing it in hedged prose.

## Q2 — the scenario, in order

1. **Fix the stake first:** write down what changes if it's true, and what I believe the prior state of the art is *before* searching (small orders settled by exhaustive/heuristic work — Flammenkamp 1998 and successors) — so I can tell a genuine jump from a misread sentence.
2. **Resolve the object, not the sentence:** get an identifier (arXiv ID / DOI), fetch the PDF itself, save it with URL, date, sha256. If nothing resolves to a real document, the report ends here and the claim is recorded as a rumour.
3. **Read the theorem statement and copy it verbatim:** what exactly is asserted at order 70 — existence of a 140-point configuration, exhaustive non-existence, or a solver run with a certificate — and whether the author line in the PDF actually matches the name the snippet attached.
4. **Test the load-bearing part:** is there a machine-checkable certificate, is it archived, does it pass; how does 70 sit relative to the published range; and list what I did *not* read (a preprint is unrefereed — that is a fact about its status, not a slur).
5. **Word it as:** "A 2026 preprint (arXiv:NNNN.NNNNN, opened 3 Sep 2026, sha256 …) states: '⟨verbatim theorem⟩'. Status: read in source; unrefereed; certificate ⟨checked / present but unchecked / absent⟩; I have not independently verified the result." — and if step 2 failed: "Claim seen only in a search snippet; no primary text opened; status: shadow."

## Q3 — how I would most likely fool myself

By letting *the paper's existence* stand in for *the claim's content*. The snippet arrives pre-loaded with plausibility — a known researcher, a method that fits (SAT), a specific number — so once the arXiv ID resolves and the title looks right, the verification feeling is already satisfied and I never read what "for order 70" quantifies over. That is exactly the 3 Sep failure repeating in a new costume: pages copied from a citing paper, thirty-two "re-opened" quotations with no saved text. The concrete guard is that nothing counts until the verbatim theorem sentence is in my report with a sha256 next to it.
