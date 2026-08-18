# RELEASES.md — immutable tags and checksums

Rule (from 2026-08-18): a tag, once pushed, is never moved.  Each document version gets its own tag; the PDF and TeX
committed at that tag are the released version, with the SHA-256 below.  Older tags: `paper-v0.5` (2026-08-18 04:xx, main
paper v0.5 with note v0.1 — **not** the note v0.5; the audit of 2026-08-18 pointed this out) and `paper-v0.6` (main paper
v0.6 first build, note v0.5).  Do not cite those two for the note.

## defects-v0.6 / hjsw-note-v0.6 (2026-08-18)
Main paper `no3inline_defects` draft v0.6 and note `hjsw_window` draft v0.6 (after the second external audit).

| file | SHA-256 |
|---|---|
| `paper/no3inline_defects.pdf` | `c5a29b94d9ba6070cf9aac3c6ac8f0303ac197cb94bd559e0908f84025a62a4b` |
| `paper/no3inline_defects.tex` | `1a70ca3a7c036c47116d9a428025091694e46042be409f228a9c76824adf52c0` |
| `paper/appendix_configs.tex` | `84a41fe4ea2d655936f6541f54271399bc91d3a025af2715807825fe46b47b8f` |
| `paper/hjsw_window.pdf` | `60f566965e1466c4df90f34319c95ec942fae040a1d5c3921b4451e932e7a3cb` |
| `paper/hjsw_window.tex` | `a5ccddb9ce394734033f43ad576c91dd0bfb5b0f451021ee883b53b928e9c31c` |

Environment used to build and verify (this release): macOS 26.5 (Apple M3), Python 3.14.6, TeX Live 2025 (pdfTeX 1.40.27);
VM checks (VM2): Debian 12, Python 3.11.2, OR-tools 9.15 (CP-SAT), scipy 1.17.1 (embedded HiGHS), python-sat 1.9.dev15,
kissat 4.0.4.
Solver runs that are only lower bounds (feasible witnesses without proof of optimality) are marked as such in the notes.

## defects-v0.7 (2026-08-18)
Main paper `no3inline_defects` draft v0.7 — after the external audit of v0.6 (`docs/reviews/no3inline_defects_deep_research_audit_2026-08-18.md`).

| file | SHA-256 |
|---|---|
| `paper/no3inline_defects.pdf` | `a401e316e11a94f5b02bfb4a6c3577c9ce88b42ecf84c4dda839310ea74206ad` |
| `paper/no3inline_defects.tex` | `2ba8bdac8608e507c2376232a0e257c85150a4a59a0477ca1eb46c735899dedb` |
| `paper/appendix_configs.tex` | `0e187738a4ba7c875df9209f860494d4f73ef566906de3d93b3df6cc9ccdda05` |
