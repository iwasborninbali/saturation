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

## hjsw-note-v0.7 (2026-08-19)
Note `hjsw_window` draft v0.7: new Section "Two hyperbolae: a first bound for H(1) ∪ H(−1)" — Theorem: α(P₋₁) ≤ 4(p−1) − 4 m₈(p) by an
explicit weighted line cover (verified numerically by `slack/km1_theorem_check.py` for p ≤ 101); Corollary "all conics" corrected.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `116e67ccc3496f7729439aa7874ce441013613fe4eb722a672ea893a7505e6bd` |
| `paper/hjsw_window.tex` | `be5f8e1a9a1e0aa66c92a7295c85dc7be3f12d8046d48c0bf252e01dabb81347` |

## hjsw-note-v0.7.1 (2026-08-19)
Same as v0.7 with the integral cover proof (third solver's variant) and cross-references to both verifiers.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `b93af4c50e93a09cf9f92dc4dab4586dd02e6c981069b8e6d61b1066dfe82c94` |
| `paper/hjsw_window.tex` | `9f03d7d4c81583b75842189d3eb8d8cc424a2e7841a0b2b0ae6e52738df69ab2` |

## hjsw-note-v0.8 (2026-08-19)
Note v0.8: Proposition (arithmetic formula for m₈, proved) and Proposition (m₈ = p/12 + o(p) via Bombieri + Erdős–Turán–Koksma; proof
sketch quoting standard estimates) ⇒ α(P₋₁) ≤ (11/3 + o(1))(p−1).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `00fb945d4c504b78478a75eb33c266c880dbbbead4e244a0b08ddd237571085b` |
| `paper/hjsw_window.tex` | `ed3bfe446ac67d05bd06800c734059e5d3da99196d57e72973ad1da40820de7a` |

## hjsw-note-v0.9 (2026-08-19)
Note v0.9: full proof of Proposition (m₈ = p/12 + O(p^{5/6} log³ p)) — absolute irreducibility of the cubic, the four polytopes and their
volumes, Bombieri sums, Erdős–Turán–Koksma, box-to-polytope; references added (Bombieri 1966, Iwaniec–Kowalski, Aubry–Perret,
Drmota–Tichy).  Theorem numbers in the citations to be pinned (deep-research brief 6).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `b16c4fc14f0c4371c42b8ec4aa1a5a744c7db5fe90cf87b52486eb476fc93388` |
| `paper/hjsw_window.tex` | `b19cfc988e8d5494197cd5c7863f7748c7b829bf6ccaa82a8177637862e3f86c` |

## hjsw-note-v0.9.1 (2026-08-19)
v0.9 with the third solver's two expository fixes in the proof of Prop. m8asym (W₁ explanation; boundary hyperplanes) and the intro
paragraph on Section "Two hyperbolae".

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `7e4f4fb27e5e05a6866b61bd1af85dca2a1a21705f4252fd57148d2c38e087d4` |
| `paper/hjsw_window.tex` | `d2de96435596e46639a01b4e9edc7404698a627da2ecf3fa2af5ff10a3914e95` |
