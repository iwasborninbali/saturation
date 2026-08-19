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

## hjsw-note-v1.0 (2026-08-19, 02:50 WITA)
Note version 1.0 (draft for the author's audit): Theorems 1, 3 (one hyperbola, all boxes), Corollary (conics), Theorem (two hyperbolae,
k=−1: α ≤ 4(p−1) − 4m₈), Propositions (m₈ formula; m₈ = p/12 + o(p), sketch quoting Bombieri/ETK — references to be pinned by
deep-research 6, which also suggests C₀ is smooth of genus 1 and a better error term), §6 rewritten with final data incl. the spectral
observation for the vertical-pair model, referee pass by the third agent, claim→artifact manifest `docs/MANIFEST_hjsw.md`.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `093c58f0f99df23a6cfc4e6b17f6e814fb4f274fd98b8ced07d42d5b3926b281` |
| `paper/hjsw_window.tex` | `8e32f84d4b042efdb5cc2a840c5b0bb8205f234075b011a9584cf890297e85e1` |

## hjsw-note-v1.1 (2026-08-19, 04:30 WITA)
v1.0 + §6 paragraph "The vertical-pair model": proved facts (quadratic form; symmetric-quadruple structure with the QR criterion; E ≫ p log log p
via Lemma K + multiplicativity of Gaussian norms — checked by the third solver) and the open Wigner-type edge estimate; pointers to
`docs/research/spectral_programme.md`, `model_theorem_conditional.md`.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `bc28d68aba632e9e7439595f501fa51c9a424d0d6312ef2224c792b24b641543` |
| `paper/hjsw_window.tex` | `57d660b2e33dc4717c944f503a951798f31e3de596d930aa4f79d3ef5111f577` |

## hjsw-note-v1.2 (2026-08-19, 03:50 WITA)
v1.1 + Proposition m8asym with the error term O(√p log⁴p) instead of O(p^{5/6} log³p): the four sets W_i are cut out by four linear forms
(the L-condition is implied by the sign conditions), so Selberg's polynomials for the four forms + Bombieri's bound replace the
box covering (Erdős–Turán–Koksma no longer needed).  Version strings fixed (v1.1 PDF still said "version 1.0").

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `72390623b6eac6c8b22d4d0a82dec479d28971107f8831a4597a3f565735ea43` |
| `paper/hjsw_window.tex` | `e9cb004f94c62c79aae19e651c1ac5ce04e3073dc9e22015387e917c343a8ab2` |

## hjsw-note-v1.4 (2026-08-19, 07:25 WITA)
v1.2 + Section "Every second hyperbola: the potential cover": Theorem (exact) α(P_k) ≤ 4(p−1) − (2G₈ − 2Σ_c|A_c−B_c|)/R for every k ∉ {0,1}
(potential/buffer cover along the cycles of the row/column class graph; k = −1 recovers Theorem two); Proposition G₈(k,p) = p/6 + O(√p log⁴p)
uniformly in k; Lemma (arc imbalance, first solver's proof: mixed character sums along the partner curve, Perel'muter/Castro–Moreno);
Corollary: α(P_k) ≤ 4(p−1) − c√p/log⁵p for every k with ord(k) ≥ C√p log⁵p (all primitive roots; all but p^{1/2+o(1)} values of k).
Also: §7 LP-anatomy paragraph, p ≤ 4001 spectral data, references (Ghosal'26, Perel'muter, Perret, Castro–Moreno). Reviewed by the first
solver (THREAD[119]).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `303b1caa3f9a68bef14c27db424b175663b631d500b3264fdbf6564ff8ccd213` |
| `paper/hjsw_window.tex` | `49d8f3fc4acee4845ccd088495effaef5a30965dea2b9dc0156b68e6a3e3399f` |

## hjsw-note-v1.5 (2026-08-19, 08:15 WITA)
v1.4 + Section "Cubic graphs do not reach the HJSW value" (first solver; checked by the second): projection lemma α ≤ 4|f(F_p)|; Theorem
(permutation cubics, p ≡ 2 mod 3): α ≤ 4p − (15/2)N₃ + O(√p log³p) = (11/4)p + O(√p log³p) in every 2p×2p box (±1-line cover; root conics;
Kummer twist); Corollary: for every cubic f and every 2p×2p box α ≤ (11/8 + o(1))·2p < 3(p−1) — no cubic graph reaches HJSW. Abstract/intro/
disclosure updated; refs Dickson 1897, Lidl–Niederreiter. Files: paper/section_cubic.tex (\input).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `ed9b20ab9a3d58acb7f353d0b76cf79c2884f066a6a1f84b79eaf10ceb1d3dd0` |
| `paper/hjsw_window.tex` | `3b25eaa5a5e03659533bf593df34c4037aba6cfad4ac1591ebcb4be9cb8519bd` |
| `paper/section_cubic.tex` | `24f59a557c6ec406fcf4f27807ab085b9644fa83bb001efa3889e8e81306d4e2` |

## hjsw-note-v1.5.1 (2026-08-19, 08:30 WITA)
v1.5 + first solver's fixes in Section 8 (the t ↦ −t remark replaced by N₃⁻ = N₃ + O(1) via the two conics; wording of the Kummer twist; quotes).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `90dddbe7db71e332cc47f959b28d188b949b66ad55e53f0d22fcd934cd17e48d` |
| `paper/hjsw_window.tex` | `4cdb407a150e7653959b11d200e9690278a59078e039010e3d1c362808ceae0e` |
| `paper/section_cubic.tex` | `6920baf299410b32b9ecea3f20d02f9c850fb41e9d04ca54e0e5a11d2b7806bc` |

## defects-v0.8 (2026-08-19, 08:30 WITA)
v0.7 + the fourth n=39 configuration (C4-base sweep of the 3-cycle family complete: 4 configurations, V2 base none), Table 3-cycle family row 39
"complete (both bases)", 41 progress (3396/4750), appendix configuration 4, ten configurations pairwise inequivalent; sent to Flammenkamp (Letter 4).

| file | SHA-256 |
|---|---|
| `paper/no3inline_defects.pdf` | `16e651f80a67b687331963bb3c0088db835b102530587fe5db5d6eb3b8b1a8a6` |
| `paper/no3inline_defects.tex` | `1461bee84a53a48db2de56504a12196b19895efd1bbfa04f8e11dfed70782d1a` |
| `paper/appendix_configs.tex` | `c0214c287ae0c37189189c8023ebe3ac2c0255e36adafefd0f81dedb9166f36e` |
| `docs/configs.json` | `d119f21667fa54fcc0369333ec8ed045228ba82162d4de97f4a513c89bf6fd12` |

## hjsw-note-v1.6 (2026-08-19, 08:55 WITA)
v1.5.1 + Section 9 "Permutation monomials: the same cover, the same conclusion" (first solver; checked by the second): lift-accounting lemma; three
local-law lemmas for x^k (root counts via S_k monodromy and Chebotarev; root positions via k-transitivity and Bombieri; the two slopes via linear
disjointness — Res(D₊,D₋) ≠ 0 for every odd k by an ℓ-adic argument); Theorem: for every odd k ≥ 3, gcd(k,p−1) = 1, p ∤ k(k−1)Res: α(x^k,B) ≤ (C_k+ε_k+o(1))p
with exact rational C_k (C₃ = 11/4, C₅ = 28183/10080, C₇ = 15265237/5443200, C₉ ≈ 2.80488, C_∞ = 2.80488…), 0 ≤ ε_k ≤ 2/(k−1)! + 8/k! ⇒ ≤ (1.474+o(1))·2p < 3/2·2p
for every odd k. Refs Wan93, NR82. Abstract/intro/disclosure updated.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `bc9afe87767c794af3b4139b421b7a90c5c9d9f7b2cc72bd546816fe64881d86` |
| `paper/hjsw_window.tex` | `8c67f3f31720afc74da4f65a8b6ca6f89d4e3237acb74f5ca58eb7923d01c749` |
| `paper/section_cubic.tex` | `6920baf299410b32b9ecea3f20d02f9c850fb41e9d04ca54e0e5a11d2b7806bc` |
| `paper/section_perm.tex` | `bb5c243194d419381052cdc78666772a5e13d2227e85759a9e58455f0f53fa27` |

## hjsw-note-v1.7 (2026-08-19, 08:50 WITA)
v1.6 + Corollary (generic permutation polynomials: S_k monodromy on both slopes + coprime discriminants => the same C_k, eps_k) and the corrected
Lipschitz bound |C_k - C_inf| <= 2^(k+3)(k+5)/(k+1)! (first solver); conclusion unchanged.

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `84fdb58a3843aa8f0b5773e7e2dd140a6aa45fec89fe9897424dc40af90921d4` |
| `paper/hjsw_window.tex` | `ea579eeb440d3bd83cb3ff2d383ec881b1b75a59f487aeee2a2c6e71a3454bdb` |
| `paper/section_perm.tex` | `9e6f37e09aae5798fb9cca83e2e717ea84b208338ab63aae38ad99fdbd53ab79` |

## hjsw-note-v1.8 (2026-08-19, 09:10 WITA)
v1.7 + verification paragraph for Sections 6-9 (scripts per statement; AUDIT_CHECKLIST_v1.7.md) + first solver's correction of Remark (b) in Section 9
(why the hyperbola sits at 3/2: two roots per residue and P(same)=1/2 from the linear relation c = t1 + t2; W4 costs 3p regardless of slope correlation).

| file | SHA-256 |
|---|---|
| `paper/hjsw_window.pdf` | `9ee1423c1cf17e3b18eb75f8207d759510aa127da91314464abe28613362f84b` |
| `paper/hjsw_window.tex` | `fca4609682235e118d476253f14e95c896c59531e56789c8487d53640fea70d2` |
| `paper/section_perm.tex` | `c361a86d42fbc9fcfc5ab9761a12466d3039e129077e2cf963dabd79847e1b70` |

## hjsw-note-v1.9 — 2026-08-19 09:59 WITA
- paper/hjsw_window.tex, version 1.9 (36 pp.): Section 10 «The strong form for cubic graphs: W4 plus a matching» (`paper/section_strong.tex`, first solver; Lemma FE `paper/lemma_fe.tex`, second solver): certificate and matching lemmas, local law U, constants γ1 ∈ [0.1287, 0.1362], γ2 ≈ 0.028–0.031, Theorem strong α ≤ (11/4 − γ1 + γ2 + o(1))p ≤ (2.652+o(1))p = (1.326+o(1))N for permutation cubics, Corollary G3: every cubic graph ≤ (4/3+o(1))N; abstract/intro/verification/disclosure updated; the constants are floating-point quadrature (stated explicitly; margin ≥ 10× error; safe constant 2.657 with a margin on γ2 for unsampled box positions).
- SHA-256(paper/hjsw_window.pdf) = f650ac3118978cf870efbeb1b5cde3f65987eaf5cd4880c311213baef0c98817

## hjsw-note-v1.10 — 2026-08-19 10:56 WITA
- paper/hjsw_window.tex, version 1.10 (39 pp.): new subsection of Section 5 «The seven-point groups: a second block» (`paper/section_seven.tex`): Lemma klein (Klein orbits: 16 lines pairwise disjoint, row/column closed, |S∩Ω| ≤ 4Σmin(n_i,2)), Lemma neighbours (Ω_d ∩ Ω_e ≠ ∅ iff e² ≡ d² ± 4; 8 classes), Theorem seven: α(P₋₁) ≤ 4(p−1) − 4m₈ − 4c₇ (c₇ = clean seven-orbits; exact for all p), Prop m7asym (first solver: m₇ = p/12 + O(√p log⁴p)), Prop clean (local law: c₇ = (7/16)(m₇/2) + O(√p log⁶p) ⇒ α ≤ (115/32 + o(1))(p−1) = 3.594(p−1)); abstract/intro/verification/disclosure updated. Numerics: clean fraction 0.4424 pooled to 10⁵ (7/16 = 0.4375), four dirty/clean categories match the local law; orbit cover checked p ≤ 500.
- SHA-256(paper/hjsw_window.pdf) = ef1f46a3da46d6586f544d5589c0760669bc9dbe6d08254c32123699a9bc3567

## hjsw-note-v1.11 — 2026-08-19 11:56 WITA
- paper/hjsw_window.tex, version 1.11 (43 pp.): block decomposition (`paper/section_blocks.tex`, second solver; `paper/lemma_run.tex`, first solver): Lemma edges (every point has an edge {t,t+1} of consecutive squares, 8 classes = 32 points per edge), Theorem blocks (the blocks indexed by maximal runs of consecutive quadratic residues partition P_{-1}, are row/column closed, and no rich line crosses a block; the rank-1 LP is block diagonal), Lemma run + Proposition descent (the type chain along a run is the descent pattern of k i.i.d. uniforms: density D_k(S)/k!; exact identity via sin(2π(v+w))sin(2π(w−v)) = (cos4πv − cos4πw)/2), Corollary blockconst: alpha(P_{-1}) <= 4466767/1290240 (p−1) + o(p) = 3.46199...(p−1) (K = 8 truncation; the full certificate constant is in [3.427, 3.462], numerically 3.4413) — below the LP with all rows/columns/±1 lines (~3.45).
- SHA-256(paper/hjsw_window.pdf) = 0edf24488063f517ba8f735044bacdaf8e9ea63588c939e72d8bb711af885d81

## hjsw-note-v1.11.1 — 2026-08-19 11:57 WITA
- ИСПРАВЛЕНИЕ (замечено хозяином): в аннотации v1.11 было сказано, что константа 3.462 «ниже значения линейной релаксации со всеми этими прямыми» — это неверно: 3.462 > 3.45. Верно: (i) при каждом фиксированном p блочная оценка не превосходит LP(1) и строго ниже неё, когда внутри блока работает целочисленность (3.4343 против 3.4545 при p = 199; 3.4100 против 3.4300 при p = 401); (ii) ДОКАЗАННАЯ асимптотическая константа 3.46199 больше численного значения того же сертификата (3.4413) только из-за усечения на K = 8. Формулировки в аннотации и в замечании исправлены.
- Независимая перепроверка таблицы (мой широкий скан до p = 20000, 133 сигнатуры): свёртка даёт 3.4616(p−1) — совпадает с 4466767/1290240 = 3.46199.
- SHA-256(paper/hjsw_window.pdf) = faa70287322fab0d313a6522dffa31349edeb6760a0d399affdb98e67fe03407

## hjsw-note-v1.11.2 — 2026-08-19 12:03 WITA
- Corollary blockconst: точная константа с дотабулированными редкими сигнатурами (первый солвер добрал 7 из 9 при p = 3000…9000; мой независимый скан до p = 20000 — 133 сигнатуры): экономия ≥ 2778667/5160960 ⇒ **α(P₋₁) ≤ 17865173/5160960 (p−1) = 3.46160(p−1)**; две сигнатуры длины 8 (плотность 10⁻⁶) по-прежнему считаются нулём, что оценку только ослабляет — так и написано.
- SHA-256(paper/hjsw_window.pdf) = 520598b753ac8d666b820fd0ccb9e084fef58c69952a2495d1b20a413e9d2939

## hjsw-note-v1.12 — 2026-08-19 12:16 WITA
- paper/lemma_stability.tex (второй солвер): Lemma orbdec (задача ОДНОЙ гиперболы распадается на V‑орбиты: ни одна прямая с ≥3 точками ЛЮБОГО наклона не покидает орбиту — проверено при p ≤ 19 по всем наклонам), Lemma orbopt (генерическая орбита: 4 класса, 16 точек, оптимум 12, максимум ЕДИНСТВЕНЕН, c(d) = d; исключительная: 8 точек, оптимум 6, ровно 9 максимумов, c(d) = 0 — все орбиты всех p ≤ 31), Proposition stability: **допустимое S с |S| = 3(p−1) − t отличается от некоторого максимума не более чем в t точках** (резко). Это объясняет и счёт 9^s.
- SHA-256(paper/hjsw_window.pdf) = c9436be710eaa6d032ba400b1e641751524c298d6d0be2f6efa218e466c845cc

## hjsw-note-v1.13 — 2026-08-19 12:24 WITA
- Стандартная модель блока (`slack/t221/standard_model.py`, второй солвер): блок строится из вещественных позиций (точная рациональная арифметика), без простого; даёт s(ε) для ЛЮБОЙ сигнатуры, включая слишком редкие для умеренных p. Сверка с двумя «простыми» таблицами: 500 сравнений при k ≤ 9, 0 расхождений. ⇒ Corollary blockconst с K = 9: сумма = 68350729/123863040, **α(P₋₁) ≤ 427101431/123863040 (p−1) = 3.44817(p−1)** (было 3.46160); хвост k > 9 ≤ 0.0196 ⇒ константа сертификата в [3.4286, 3.4482], численно 3.4413.
- Уточнено доказательство Lemma orbopt: генерическая орбита — это {A,A,D,D} или {B,B,C,C} (лемма partners), обе изоморфны при отражении (x,y)↦(y,x), профиль богатых прямых (4,4,3,3,3,3); ровно два типа орбит (проверено для всех орбит всех p ≤ 19).
- SHA-256(paper/hjsw_window.pdf) = a03954e7fe1c34d7fb37ac8131ba1334a59bbf84b0073d29f77d89c4da375f69
