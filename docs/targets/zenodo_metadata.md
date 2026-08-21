# Записи Zenodo

## 1. Трёхмерный no-three-in-line — ОПУБЛИКОВАНА 2026-08-20, версия 1.1
* **Concept DOI (указывать везде):** 10.5281/zenodo.22019279
* DOI версии 1.0: 10.5281/zenodo.22019280
* **DOI версии 1.1: 10.5281/zenodo.22023207** — https://zenodo.org/record/22023207
* Содержание: a(1..6) = 1, 8, 16, 28, 40, 64 — точные значения; a(7) >= 73, a(8) >= 93; a(p) >= p^2.
* Что нового в 1.1: перекрёстная проверка вторым решателем (Glucose) при n=5 закрывает единственную
  дыру версии 1.0 — но ТОЛЬКО при n=5, и это сказано отдельно; границы подняты с 71 и 89;
  отозвано утверждение про размер группы симметрии; исправлен провенанс оценки дерева.

## 2. A280537, без четырёх компланарных — ОПУБЛИКОВАНА 2026-08-20
* **DOI версии:** 10.5281/zenodo.22023080
* **Concept DOI:** 10.5281/zenodo.22023079
* Запись: https://zenodo.org/record/22023080
* Содержание: a(2..5) воспроизведены (a(5)=13 с сертификатом drat-trim); a(6) >= 16 (4 свидетеля);
  a(7) >= 18 (6 свидетелей, у записи OEIS их не было девять лет); тройная сверка по числу классов
  с Пеггом (1, 232, 38); верхняя граница при n=7 ОТКРЫТА и названа открытой.
* **ВЕРСИЯ 2.9 ОПУБЛИКОВАНА 2026-08-22** — https://zenodo.org/record/22051302
  * DOI версии 2.9: 10.5281/zenodo.22051302 (concept DOI прежний: 10.5281/zenodo.22023079)
  * Что нового: диапазон расширен с n<=7 до **n<=29**; девятнадцать свидетелей, каждый
    проверен двумя программами без общего кода; восемнадцать независимых нижних границ
    от a(9)>=23 до a(29)>=59; два доказанных утверждения выше n=8 — симметричные максимумы
    23 при n=9 и 26 при n=10, оба исчерпаны ДВУМЯ реализациями (при n=10: 1.52 млрд узлов,
    8.93 ядро-часа, покрытие записано подолям).
  * Названо прямо, чего НЕ установлено: верхних границ выше тривиальной 3n нет ни одной;
    оба доказанных утверждения — о ПОДПРОСТРАНСТВЕ, а не об a(n), и при n=6 подпространство
    максимума не содержит (15 против a(6)=16).
  * Контрольные суммы файлов:
    a280537_note.pdf  78d098886bcab8d5d73284c59ddeb1915c80094835c21fc9d3ab446f7663363b
    a280537_note.tex  3791f6a8d9d8a4694e8c578fc14f2b883ae2c049aaea79665c55bedae2c15c57
    a280537_zenodo.zip aed8f03c9aae0faf06c85c04084248f85f935af51db2e9b2acaf1df2d124ec20

---

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
