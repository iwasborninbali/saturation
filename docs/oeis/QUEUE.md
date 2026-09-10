# OEIS queue — what waits for a free draft slot

At most three drafts may be pending. Pending on 10.09.2026: A398172 (editing), A398184 (proposed), A398580 (new: the
triangle by size). Nothing else is opened until one of them is approved.

Rule (Alex, 10.09.2026): every edit reaches him as the FULL record text and he pastes it whole; he never changes
single lines. File uploads go through the widget on the edit page (it writes the %H line; never add it by hand).
An a-file (witnesses, programs, tables) is uploaded with the "This is a b-file" box UNTICKED; only a real b-file
(index and term per line) gets the tick.

1. **A399138 — edit prepared 3.09, not yet submitted.** New bounds a(8) >= 94, a(9) >= 116, a(10) >= 138,
   a(11) >= 164 in the %C line and the extended a-file `docs/oeis/a399138.txt` (an a-file, box unticked; Text for
   Link line: "Witness configurations for a(1)-a(6) and for the bounds a(7) >= 73, a(8) >= 94, a(9) >= 116,
   a(10) >= 138, a(11) >= 164"). The two replacement lines are in `A399138_edit_2026-09-03.md`; the full record
   is generated from the live entry when a slot frees.
2. **Maximal subsets by size** — the triangle M(n,k) of A398184, rows n = 1..7 in
   `2026-09-10/maximal_by_size.txt`, recounted independently (tri.c). A separate sequence if the editors want
   one; today it is the attachment a398184.txt.
3. **Quotients by the symmetries of the square** of A398172 / A398184 (counts up to D4) — named as candidates on
   3.09, not computed.
4. **A280537 — certified exhaustion of a(7) = 18 and a(8) = 20**, promised to Pfoertner in the Discussion
   (23.08): research on the machine, not a paste.
