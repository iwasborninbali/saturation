# Метаданные записи Zenodo (заполнить при загрузке)

**Title:** Certified exact values for the no-three-in-line problem in the three-dimensional grid

**Authors:**
- Aleksei Kudriashov (Alex Komang) — ORCID `0009-0006-8885-5338` — affiliation: **Nusa Dua Studio (nusadua.dev)**

**Resource type:** Dataset / Software (записать оба: заметка + код + журналы + сертификаты)

**Description (черновик):**
> Exact values of the maximum number of points in the n x n x n grid with no three collinear, together with
> the machinery that certifies them: a Boolean encoding whose semantics is verified against the direct
> collinearity criterion, DRAT certificates checkable by drat-trim, witness configurations checked by
> exhaustive integer arithmetic, and a complete case split whose coverage is verified mechanically.
> Includes a step-by-step protocol for an independent checker who trusts none of the authors' code, an
> explicit statement of what is *not* claimed, and the errors caught during the work.

**Keywords:** no-three-in-line, combinatorial geometry, lattice points, exhaustive search, SAT solving,
DRAT certificate, OEIS

**Related identifiers:**
- `isSupplementTo` — запись OEIS (после присвоения A-номера)
- `isSupplementedBy` — https://github.com/iwasborninbali/saturation

**License:** CC BY 4.0 для текста и данных, MIT для кода.

**Disclosure (обязательно, в поле Description или Notes):**
> The computations, the code and the drafting were performed by AI agents (Claude) under the direction of
> the author of record, who posed the question, chose what to compute, decided what to claim, and is
> responsible for the content.

## Что загружать
- `paper/no3_3d_note.pdf` — заметка;
- `docs/VERIFICATION.md` — протокол независимой проверки;
- `certs/` — конфигурации-свидетели и проверяльщики;
- `slack/targets/` — кодировки, разбиение, агрегатор;
- `logs/` — журналы прогонов;
- один сертификат DRAT целиком (для демонстрации цепи) — остальные воспроизводимы.

## Порядок
1. Zenodo (DOI) → 2. OEIS со ссылкой на DOI → 3. arXiv, когда появится поручитель.
