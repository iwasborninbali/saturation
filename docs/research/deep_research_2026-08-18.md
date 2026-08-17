# Обзор литературы и методов по задаче «no-three-in-line» (2n точек на сетке n×n) с оценкой новизны

## TL;DR
- Асимптотическая нижняя граница **3n/2 − o(n)** (Hall–Jackson–Sudbery–Wild, 1975) **не улучшена до сих пор**: ни одна из проверенных статей (arXiv 2106.15621, 2209.01447, 2605.07000, 2508.07632, 2502.00176, 2607.05255, 2510.17743) не даёт (3/2+ε)n для k=2; все прорывы 2025–26 относятся к k≥3 либо к вычислительным рекордам, а не к конструкции.
- Ключевое препятствие едино во всех работах: линейные конструкции алгебраичны (дуги коник/гипербол над F_p), а по теореме Сегре дуга в AG(2,p)/PG(2,p) ограничена ~p+1≈n точками; «целочисленный зазор» (тройка, коллинеарная mod каждого p, но не в Z²) в литературе **сформулирован лишь как вопрос Бена Грина**, и ни одной конструкции, его эксплуатирующей, не опубликовано — это незанятая ниша.
- Метод Джейкоба Дэйвиса (619 решений через «ChatGPT 5.6 Sol», июль 2026) **нигде не описан** — в базе Флямменкампа стоит только однострочный кредит; ваша «balance lemma» в терминах эйлерова орграфа дефектных пар в литературе **не встречается** (ближайший аналог — псевдокласс rct4 Флямменкампа, введённый в январе 1997, но без степенно-балансового/эйлерова обоснования).

## Key Findings
1. Рекорд конструкции = 3n/2 − o(n), 1975; за 50 лет прогресса нет (подтверждено пятью независимыми источниками 2023–2026).
2. Все известные линейные конструкции — «алгебраические» (кривые степени ≤2 над F_p); барьер — теорема Сегре и отсутствие максимальных дуг в дезарговых плоскостях нечётного порядка.
3. Для k≥3 задача асимптотически закрыта (f_k(n)=kn) вероятностно-комбинаторными методами (Kovács–Nagy–Szabó; Grebennikov–Kwan; Ghosal–Goenka–Grebennikov–Keevash–Kwan–Pham); при k=2 эти методы принципиально не работают — «бюджет» ≤2 точки на прямую не оставляет запаса для шага удаления/абсорбции.
4. Эвристика Guy–Kelly (исправл. Ellmann 2004, Voutier 2026, Prellberg 2026) даёт предел π/√3 ≈ 1.814n; та же эвристика для симметричных конфигураций даёт «<1 ожидаемого решения», что прямо противоречит их существованию — Прельберг называет это слабостью эвристики.
5. Плотность симметричных решений объясняется у Флямменкампа («superficial explanation»): в ротационных классах две точки блокируют ~C·log(n) прямых, а не ~n, как в ортогональных.
6. Программный/ИИ-поиск (FunSearch, PatternBoost, PPO) применён к задаче только на малых n (≤15) и рекордов не дал; метод Дэйвиса не документирован.
7. На торе и в 3D тривиальная граница достигается алгебраически именно потому, что там условие «нет трёх на прямой» слабее (в 3D — коразмерность 2); в Z² теорема Сегре это блокирует.

---

## Details

### Вопрос 1. Нижние границы (конструкции) после 1975

**Прямой ответ.** 3n/2 − o(n) остаётся лучшей асимптотической конструкцией для k=2. Улучшения до (3/2+ε)n нет; нет и условной/эвристической конструкции, дающей больше 3n/2.

- **Hall, R. R.; Jackson, T. H.; Sudbery, A.; Wild, K.**, «Some advances in the no-three-in-line problem», *J. Combin. Theory Ser. A* 18(3) (1975) 336–341, doi:10.1016/0097-3165(75)90043-6. Конструкция: точки на модулярной гиперболе xy≡c (mod p) в сетке 2p×2p, дающая 3(p−1) точек.
- **arXiv:2508.07632** (Kovács–Nagy–Szabó, «Randomised algebraic constructions for the no-(k+1)-in-line problem»): *"although it has been studied extensively, no progress has been reported concerning the lower bound, up to our best knowledge, since the result of Hall, Jackson, Sudbery, and Wild"*; раздел 2.2: *"which gives a no-three-in-line set of size 3(p-1) in a 2p × 2p grid for any prime p ≥ 3"*.
- **arXiv:2511.03526** («Rational normal curves as no-(d+2)-on-Q-quadric sets»): *"The current best known lower bound of 3/2 n − o(n) by Hall, Jackson, Sudbery and Wild stands since 1975 [HJSW75]. This construction uses degree 2 algebraic curves over finite fields."*
- **arXiv:2510.17743** (Grebennikov–Kwan): *"the best known lower bound (1.5−o(1))n comes from the modular hyperbola construction of Hall, Jackson, Sudbery, and Wild [17]"* и *"all known linear-size constructions for the no-three-in-line problem are algebraic in nature (though there are random constructions [9,13] of size about n/√log n)."*

**Проверка конкретных arXiv-ID (все верифицированы через fetch/поиск):**

- **arXiv:2106.15621** — резолвится в **Theophilus Agama, «On the general no-three-in-line problem»** (v1 29 Jun 2021, v10 13 Apr 2026), https://arxiv.org/abs/2106.15621. Даёт нижнюю границу в d-мерии: `≫ n^{d-1} · (d)^{1/2d}` методом «компрессии». При d=2 это ≈ n·2^{1/4} ≈ 1.19n — **хуже** 1.5n, для k=2 ничего не даёт. Обструкция: метод «induced balls» даёт точки на (d−1)-мерном скелете; в 2D это кривая с ~n точками и константой ниже 3/2. Замечание: препринт пережил 10 версий, не в сильном рецензируемом источнике — цитировать с осторожностью. Прельберг (2602.07751) **ошибочно** цитирует эту статью как «Y.C.R. Lin, arXiv:2106.15621»; фактический автор — Agama.
- **arXiv:2209.01447** — **Nagy, D. T.; Nagy, Z. L.; Woodroofe, R., «The extensible No-Three-In-Line problem»**, *European J. Combin.* 114 (2023) 103796. Это про *extensible*-версию (бесконечное S⊂Z² с большой плотностью в каждом [n]²): даёт Θ(n/log^{1+ε}n). К классической задаче ничего к 1975 не добавляет.
- **arXiv:2605.07000** — **Anubhab Ghosal, «A note on the extensible no-three-in-line problem»** (7 May 2026, Oxford), https://arxiv.org/abs/2605.07000. Verbatim: *"We show the existence of a set S⊂Z² avoiding collinear triples satisfying |S∩[n]²|=Ω(n/√(log n)) for sufficiently large n. This improves on the best-known lower bound... due to Nagy, Nagy and Woodroofe by √(log n)... Our construction is random."* Классической 2n не касается.
- **arXiv:2508.07632** — **Kovács, Nagy, Szabó, «Randomised algebraic constructions for the no-(k+1)-in-line problem»** (2025). Улучшают константы для малых k через модулярные гиперболы + рандомизацию; verbatim Theorem 1.6: *"f3(n)≥1.973n for n sufficiently large"*; abstract: *"(1−2/k)kn ≤ f_k(n) ≤ kn"* (чётное k), *"(1−3/k)kn ≤ f_k(n) ≤ kn"* (нечётное k). Почему при k=2 ничего: их метод берёт коники/гиперболы (арки, capped Сегре ~p≈n) и добавляет случайный «излишек», который существует только когда допустимо >2 точек на прямую; при k=2 излишка нет.
- **arXiv:2502.00176** — **Kovács, Nagy, Szabó, «Settling the no-(k+1)-in-line problem when k is not small»** (2025): f_k(n)=kn при k>C√(n·log n). Метод «essentially purely probabilistic ... built from carefully constructed blockwise» конструкций. При k=2 не применим (порог по k слишком высок).
- **arXiv:2607.05255** — **«No-(k+1)-in-line problem for k≥3»**, авторы **Anubhab Ghosal, Ritesh Goenka, Alexandr Grebennikov, Peter Keevash, Matthew Kwan, Huy Tuan Pham** (v1, 6 Jul 2026; Oxford / ISTA Austria / Caltech). Доказывает f_k(n)=kn для всех k≥3 и больших n. Техника (verbatim abstract): *"in the regime k≥3, the problem is dominated in a certain statistical sense by the influence of a small number of 'heavy' lines with many grid points. We apply a result of Ehard-Glock-Joos on pseudorandom hypergraph matchings to construct a set of size kn−o(n)... then a crude deletion argument yields a no-(k+1)-in-line set... Finally, we use a randomised switching procedure to complete the construction (building upon ideas of Simkin and Luria)."* Что ломается при k=2 — авторы говорят прямо: *"Of course, the assumption k ≥ 3 means that in this paper we do not say anything new about the no-three-in-line problem (which corresponds to the case k = 2)"* и *"there are some important statistical differences between the case k = 2 and the case k ≥ 3 (related to the relative significance of lines in different directions)"* (Remark 1.7). Механизм: при k≥3 после случайной укладки ~kn точек можно удалить o(kn) точек, чтобы исправить переполненные прямые, и относительная потеря →0; при k=2 потеря — константная доля, метод даёт лишь ~1.5–1.8n.
- **Смежное: arXiv:2510.17743** — **Grebennikov, A.; Kwan, M., «No-(k+1)-in-line problem for large constant k»**. Verbatim abstract: *"We prove that for n≥k≥10³⁷ the maximum number of points is exactly kn. Our proof builds on the recent work of Kovács, Nagy, and Szabó... incorporating ideas of Jain and Pham."*

**Прочие post-1975 работы:** Erdős/Roth (модулярная парабола (i,i²) mod p, ~n точек; K. F. Roth, *J. London Math. Soc.* 26 (1951) 198–204); Payne–Wood вероятностная конструкция (*SIAM J. Discrete Math.* 27 (2013) 1727–1733); обзоры **Brass–Moser–Pach**, «Lattice Point Problems», в *Research Problems in Discrete Geometry*, Springer 2005 (doi:10.1007/0-387-29929-7_11) и **Eppstein, D., «Forbidden Configurations in Discrete Geometry», Cambridge Univ. Press, 2018**; Pegg Jr. «Math Games: Chessboard Tasks», MAA Online, 2005.

**Что было бы ново:** любая конструкция, дающая (3/2+ε)n или тем более (2−o(1))n; это было бы первым улучшением за >50 лет.

---

### Вопрос 2. Сегре, дуги и «целочисленный зазор»

**Прямой ответ.** Все линейные конструкции — дуги алгебраических кривых по mod p, а размер дуги в AG(2,p)/PG(2,p) ограничен ~p+1≈n теоремой Сегре; модулярные конструкции упираются в ~n, а гипербола HJSW обходит это лишь до 3n/2, комбинируя классы в сетке 2p×2p. «Целочисленный зазор» как явная конструкция в литературе отсутствует; он присутствует лишь как **вопрос Бена Грина**.

- **Segre, B.**, «Ovals in a finite projective plane», *Canad. J. Math.* 7 (1955) 414–416; «Curve razionali normali e k-archi negli spazi finiti», *Ann. Mat. Pura Appl.* 39 (1955) 357–379. Формулировка (arXiv 1310.6482, Tao): *"Segre's theorem. Let F be a finite field of odd prime order, and let P be an arc in PF² of cardinality |F| + 1. Then P is a conic curve."* Верхняя граница дуги: |P| ≤ |F|+2.
- **Отсутствие максимальных дуг** (нечётный порядок): Ball–Blokhuis–Mazzocca, «Maximal arcs in Desarguesian planes of odd order do not exist» — барьер, не дающий модулярным аркам приблизиться к 2n. Обзор арок: **Ball, S.; Lavrauw, M.**, «Arcs in finite projective spaces», *EMS Surv. Math. Sci.* 6(1) (2020) 133–172.
- **Связь «коллинеарность в Z² vs mod p»**: наиболее явная формулировка — из arXiv 2607.05255: *"All previous constructions for small k have been 'algebraic', in the sense that they are based on algebraic curves in an affine plane (Z/pZ)² for some prime p ≤ n (in fact, Green [17] asked whether every 'large' no-three-in-line set reduces to an algebraic curve modulo some prime)."* Источник вопроса: **Ben Green, «100 open problems»** (manuscript, people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf).
- **Дуги в модулярной решётке Z²_{2p}**: **Stępień, Z.; Szymaszkiewicz, A.; Szymaszkiewicz, L.**, «Arcs in Z²_{2p}», *J. Combin. Optim.* 35(2) (2018) 341–349, doi:10.1007/s10878-017-0171-8 — прямое развитие HJSW в терминах арок.
- **Кривые высших степеней/рациональные нормальные кривые**: arXiv 2511.03526 обобщает конику до Q-квадрик и рациональных нормальных кривых, но в 2D всё равно упирается в дугу ~p+1.

**Что было бы ново:** любое явное множество, эксплуатирующее целочисленный зазор (тройка коллинеарна mod каждого p, но не в Z²), с плотностью выше арочной границы Сегре — в литературе такой конструкции нет; есть только постановка вопроса Грина.

---

### Вопрос 3. Почему симметричные решения плотнее

**Прямой ответ.** Есть и эвристическое, и качественное объяснение, но строгой теоремы нет. Прельберг прямо отмечает, что вероятностная эвристика ломается на симметричных конфигурациях; Флямменкамп объясняет это через число блокируемых прямых.

- **Prellberg, T., «Constraint satisfaction programming for the no-three-in-line problem», arXiv:2602.07751 (2026)**, https://arxiv.org/abs/2602.07751. Эвристический счёт C(n,k)=C(n²,k)·(1−q_n)^{C(k,3)}, где λ_c=π/√3≈1.81; *"the heuristic count C(n, 2n) becomes smaller than one once n ≥ 493"*; и решающее: *"if one additionally incorporates rotational symmetry into this heuristic (180-degree symmetry suffices), the expected number of solutions drops immediately below one, even though solutions having rotational symmetry clearly exist. This exposes a clear weakness of this heuristic and casts doubts as to its validity."* Это источник вашего пункта о провале эвристики на симметричных конфигурациях.
- **Flammenkamp, «A Superficial Explanation»** (readme.html): *"in the orthogonal symmetry class ort1, resp. ort2, two independent selected points force typically the blockade of n points for 2 of 6, respectively for 8 of 28, straight lines... And in the rotation symmetry classes rot? two independent selected points force typically the blockade of about C log(n)."* Вывод: *"one should expect most different configurations for given n in the rotational symmetry classes but least different configurations in those with mid-perpendicular symmetry."* Это объясняет, почему rot4/rct4 «доживают» до больших n: в них симметрия «стоит дёшево» (логарифмическая блокада вместо линейной).
- Энтропийный/орбитный аргумент (rot4-орбита = 4 точки, но один выбор) в явном виде в найденной литературе **не оформлен** как second-moment/Poisson-clumping/LLL. Флямменкамповское «C log(n)» — по сути указание, что показатель в (1−q_n)^{C(k,3)} для симметричного класса другой; но строгого second-moment-расчёта нет.
- **Subercaseaux, B.; Mackey, E.; Qian, L.; Heule, M. J. H., «Automated Symmetric Constructions in Discrete Geometry», arXiv:2506.00224**, CICM 2025, LNCS 16136, pp. 29–47 (Best paper award). Метод: *"directly embedding rotational symmetry into the combinatorial encoding of geometric configurations"* + *"a novel local-search realizability solver"* для ∃ℝ-полной задачи реализуемости. Код: https://github.com/bsubercaseaux/automatic-symmetries (использует allsat-cadical и localizer https://github.com/bsubercaseaux/localizer).
- Симметрия-как-эвристика в других задачах (cap sets у FunSearch, PatternBoost): «symmetry hypothesis» как общий принцип экстремальной комбинаторики в найденных источниках специально не теоретизируется.

**Что было бы ново:** строгий second-moment / энтропийный расчёт, показывающий, что ожидаемое число rot4/rct4-конфигураций остаётся >1 (или →∞) далеко за порог n≈493 асимметричной эвристики — это формализовало бы наблюдение Прельберга/Флямменкампа, чего в литературе нет.

---

### Вопрос 4. Программный/ИИ-поиск

**(a) FunSearch / AlphaEvolve / PatternBoost / RL.**
- **Romera-Paredes, B. et al., «Mathematical discoveries from program search with large language models», Nature 625 (2024) 468–475**, doi:10.1038/s41586-023-06924-6; код https://github.com/google-deepmind/funsearch. Новые cap set’ы, но **к no-three-in-line не применялся**.
- **AlphaEvolve**: Novikov et al. (2025) — «generalizes the loop to whole-codebase evolution»; применений к нашей задаче не найдено.
- **PatternBoost**: Charton, Ellenberg, Wagner, Williamson, «PatternBoost: Constructions in Mathematics with a Little Help from AI», arXiv:2411.00566 (2024). Локально-глобальная итерация (жадный поиск + трансформер makemore).
- **Применение к no-three-in-line есть, но слабое**: **Ramanathan, P.; Joshi, P. D.; Prellberg, T.; Dandekar, R. A.; Panat, S., «Three methods, one problem: Classical and AI approaches to no-three-in-line», arXiv:2512.11469 (Dec 2025)**. *"ILP achieves provably optimal solutions up to 19×19 grids, while PatternBoost matches optimal performance up to 14×14 grids... PPO achieves perfect solutions on 10×10 grids but fails at 11×11 grids"*; *"PatternBoost did not scale beyond n=15"*. ML-подходы **не дотягивают** даже до перебора.

**(b) КРИТИЧНО: Джейкоб Дэйвис (июль 2026).** Метод **нигде не описан**. Единственный первоисточник — кредит в базе Флямменкампа (readme.html, якорь #B, обновл. 2026-08-11): *"On 24th July 2026 Jacob Davies from Alameda (California, USA) used the AI ChatGPT 5.6 Sol to construct 619 new solutions for n=21, 22, ..., 56, 57 all in symmetry classes iden or rot2."* и *"On 30th July he continued to construct 24 more new solutions with n ≤ 57 in symmetry classes iden or rot2 and one solution for n=66 in symmetry class rot4."*

Существенно: для **всех** прочих контрибьюторов Флямменкамп приводит метод и/или ссылку (Прельберг → «constraint satisfaction approach on a massive multithreading hardware» + PDF Prellberg_Sep_2025.pdf; Хьюле → «a newly developed SAT solver»; Collier → «wrote a program»). У Дэйвиса — **ни PDF, ни описания метода**, только глагол «construct» и название инструмента «ChatGPT 5.6 Sol». Проверены (все негативные): якорь #B readme.html; поиск «Jacob Davies» + no-three-in-line / Flammenkamp / ChatGPT / Alameda / grid; Reddit r/math; Hacker News; OEIS A000769 и A272651 (комментарии/история). Является ли метод поисковым, конструктивным или пертурбацией известных решений — **установить нельзя**. По существу: exhaustive search класса «iden» при n≥21 недостижим (у Флямменкампа полные перечисления «iden» есть лишь до n≈19–20), поэтому метод Дэйвиса качественно иной — но это логический вывод, а не подтверждённый факт. Для выяснения нужно писать Флямменкампу (achim@uni-bielefeld.de).

**(c) Прочие LLM/агентные попытки 2024–26:** arXiv 2512.11469 (выше); LLM как ассистент кодирования у Прельберга (2602.07751): *"A reference implementation of the CP-SAT model ... was generated ... using an LLM-based coding assistant (ChatGPT)"*. Более сильных результатов от LLM/агентов не найдено.

**Что было бы ново:** документированный конструктивный (не переборный) метод для класса «iden» при n≥21 — если метод Дэйвиса именно таков и не опубликован, его формализация и обобщение были бы новым вкладом.

---

### Вопрос 5. Новизна «balance lemma» и семейств дефектов

**Прямой ответ.** Формулировка через **эйлеров орграф дефектных пар на классах строк {i, n−1−i}** в литературе **не встречается**. Ближайший известный аналог — псевдокласс **rct4** Флямменкампа.

- **Определение rct4** (Flammenkamp, symmetry_remarks.html, «A new Pseudo Symmetry Class», дата страницы 2026-03-17): *"This is a subset of the symmetry class rot2 which has rot4 symmetry except on the long diagonals of the grid. It is denoted by [rct4] and was invented in January 1997."* Подтверждение (Wolfram MathWorld): *"rct4 denotes quarter-turn symmetry except on the long diagonals."* Это в точности ваш «одиночный дефект = диагональная петля = rct4», но у Флямменкампа rct4 задан **статически** (как подмножество rot2), без степенно-балансового/эйлерова обоснования.
- 9 классов симметрии (характеры кодировки `. : / - o c x + *` = `iden rot2 dia1 ort1 rot4 rct4 dia2 ort2 full`): iden (асимметричный), rot2 (полуоборот), rot4 (четвертьоборот), full (полная D4, 8-кратная), ort1/ort2 (отражение в средних перпендикулярах), dia1/dia2 (отражение в длинных диагоналях). rct4 — псевдокласс, вставленный между rot4 и dia2.
- Невозможность rot4 при нечётном n (причина, почему rct4 — «самый симметричный» доступный класс для больших нечётных n): *"Symmetry class == rot4 and n odd — There must be a total of 2n markers which is not dividable by 4... A contradiction! Therefore if n is odd in class rot4 there are no solutions."* Эмпирически: рекордные нечётные n (57,59,61,63,65,67,69) — все rct4; рекордные чётные (60,62,64,66,68,70,72,74,76) — все rot4.
- В arXiv:2602.07751 (Прельберг) симметрия вводится только через ρ(i,j)=(j,n−1−i) и fundamental domain; **эйлерова/балансового аргумента нет**. В arXiv:2506.00224 (Subercaseaux et al.) симметрия кодируется в SAT напрямую; аргумента о балансе дефектных пар нет.
- Аналогов «почти-симметричных» семейств со степенно-балансовым/эйлеровым аргументом, применённым к дефектам симметрии в решётчатых конфигурациях, не найдено.

**Что было бы ново:** сама «balance lemma» (дефектные пары rot2-конфигурации относительно rot4/dia2 образуют эйлеров орграф на классах строк, одиночная петля ⇒ rct4), исчерпывающие перечисления «defect families», и первые конфигурации с точной rot2-симметрией для n=36,37,39 — всё это, судя по проверенным источникам (Флямменкамп, Прельберг, Subercaseaux et al.), **не опубликовано**. rct4 существует как класс, но не как следствие эйлерова/балансового условия — это ключевой пробел, который заполняет ваша лемма.

---

### Вопрос 6. Структура больших решений

**Прямой ответ.** Систематического статистического анализа формы больших 2n-конфигураций мало; есть эвристика предельной формы Guy–Kelly, страница плотности Флямменкампа и «континуальный» подход в checkerboard-статье.

- **Guy, R. K.; Kelly, P. A.**, «The no-three-in-line problem», *Canad. Math. Bull.* 11 (1968) 527–531 (+ Research Paper #33, Calgary, 1968; скан у Флямменкампа). Исправление Ellmann (2004) — verbatim, R. K. Guy в OEIS A000769 (Oct 22 2004): *"Guy & Kelly conjecture that... at most (c+eps)*n points can be selected, where 3*c^3 = 2*Pi^2, i.e., c ~ 1.87. As recently as last March, Gabor Ellmann pointed out an error in our heuristic reasoning, which, when corrected, gives 3*c^2 = Pi^2, or c ~ 1.813799."* Документировано также в **Voutier, P. M., «On the Guy-Kelly Conjecture for the No-Three-In-Line Problem», arXiv:2603.00215 (2026)**: *"We provide details of the error Gabor Ellmann found in 2004 in a heuristic argument of Guy and Kelly... This led to a correction of their conjectured upper bound."*
- **Flammenkamp, «Distribution of Selected Points»** — страница density.html (обновляется), посвящённая распределению выбранных точек в базе — прямой источник для профиля плотности/радиальной структуры.
- **Континуальный предел**: arXiv 2605.09215 («No-three-in-line sets on the checkerboard grid», 2026) строит *"an exact continuum dual certificate for the formal continuum problem"* через LP-релаксацию по 4 направлениям (строки, столбцы, две диагонали ±1) — методологический прообраз континуальной/ренормализационной картины.
- Гипербола-подобная плотность: конструкция HJSW сама намекает на «гиперболический» профиль; строгой «continuum density conjecture» с автокорреляцией/распределением наклонов в найденных источниках нет.

**Что было бы ново:** количественный статистический анализ базы (профиль плотности центр/край, спектр используемых наклонов, автокорреляция, сравнение с гиперболическим/континуальным пределом) как приор для поиска или подсказка для конструкции — по существу отсутствует в литературе.

---

### Вопрос 7. Варианты, где достигается граница типа 2n, и почему

**Прямой ответ.** На торе и в 3D тривиальная граница достигается алгебраически, потому что там условие «нет трёх на прямой» слабее; в Z² Сегре это блокирует.

- **Тор**: Misiak, Stępień, Szymaszkiewicz, Szymaszkiewicz, Zwierzchowski, «A note on the no-three-in-line problem on a torus», *Discrete Math.* 339(1) (2016) 217–221, doi:10.1016/j.disc.2015.08.006: *"at most 2 gcd(m,n) points can be placed with no three in a line on an m×n discrete torus... when gcd(m,n) is a prime, we completely solve the problem."* Периодичность: Skotnica, *Discrete Math.* 342 (2019) 111611. Fowler, Groot, Pandya, Snapp, arXiv:1203.6604: T(Z_p×Z_{p²})=2p, T(Z_p×Z_{pq})=p+1. m-мерный тор: Ku, Wong, *Graphs Combin.* 34 (2018) 355–364.
- **3D**: **Pór, A.; Wood, D. R., «No-Three-in-Line-in-3D», *Algorithmica* 47 (2007) 481–488** (GD 2004, LNCS 3383): *"the maximum number of points in the n×n×n grid with no three collinear is Θ(n²)."* Верхняя граница 3n на плоскость, конструкция — плотное подмножество модулярного параболоида / moment curve {(x, x²+y², ...) mod p}.
- **Почему 2n не переносится в Z²**: в 3D «нет трёх на прямой» — условие коразмерности 2, гораздо более слабое; кривая-момент {(x,x²,x³) mod p} не содержит 4 компланарных, что даёт Θ(n²) без арочного ограничения. В 2D любое множество на кривой упирается в дугу Сегре ~p+1≈n. Именно арочная граница Сегре — то свойство Z²/F_p², которое мешает переносу.
- **F_p²**: дуги ≤ p+1 (конформно с общим случаем). Обобщение (rational normal curves): arXiv 2511.03526.

**Что было бы ново:** явная демонстрация, какое именно свойство целочисленной решётки (в отличие от тора Z_n² или 3D) допускает/запрещает 2n, с конструкцией, обходящей арочный барьер за счёт целочисленного зазора.

---

### Вопрос 8. Публичные инструменты и вычислительные затраты

- **Prellberg (CP-SAT)**: arXiv:2602.07751; модель + данные из Table 1 доступны по ссылке в статье; код CP-SAT «was generated ... using an LLM-based coding assistant (ChatGPT)»; запуски — «384 independent CP-SAT runs executed in parallel on an AMD EPYC 9965 CPU». Полное перечисление n=20: *"generated all 118057 solutions for n=20 using 3536 GPUh"* (Флямменкамп, readme).
- **Riley (CUDA branch-and-bound)**: код «uses GPUs via CUDA and was run by Thomas Prellberg on the Queen Mary University HPC cluster» (Флямменкамп, readme). Прямой публичной ссылки на репозиторий в найденных источниках нет — пробел.
- **Heule (SAT)**: «used a newly developed SAT (Boolean satisfiability) solver» (readme). Личная страница https://www.cs.cmu.edu/~mheule/. Отдельный релиз кода именно для no-three-in-line не локализован; для симметричного подхода см. код Subercaseaux et al. https://github.com/bsubercaseaux/automatic-symmetries.
- **База Флямменкампа**: readme http://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html, таблица (обновл. 2026-08-11), download-каталог, decode.c; в БД 430991 конфигураций; рекорд n=76 (Heule, rot4, 10 авг 2026).

**Что было бы ново:** публичный, документированный CUDA/SAT-код Riley/Heule с воспроизводимыми метриками core/GPU-часов на рекорд — сейчас разрознено.

---

## Recommendations

### (A) Пять наиболее перспективных направлений для КОНСТРУКЦИИ (не поиска), по убыванию перспективности

1. **Целочисленный зазор поверх HJSW («вопрос Грина наоборот»).** Строить множества, коллинеарные mod каждого малого p, но не в Z², чтобы обойти арочную границу Сегре. Опора: постановка Грина (arXiv 2607.05255, Remark 1.2) и то, что все известные конструкции алгебраичны mod p — незанятая ниша. Порог смены рекомендации: получена хотя бы (3/2+ε)n на бесконечной серии.
2. **Комбинация нескольких простых p (CRT-склейка дуг).** HJSW уже склеивает классы в 2p×2p; систематическая склейка дуг по разным p через КТО может дать константу >3/2. Опора: Kovács–Nagy–Szabó (2508.07632) показали, что «blockwise» рандомизация над кониками даёт прирост при k≥3 — перенести идею блоков в k=2 с жёстким контролем целочисленных коллинеарностей.
3. **rct4/rot4 с контролируемыми дефектами (ваша balance lemma как генератор конструкции).** Поскольку эйлерово условие на дефектные пары нигде не опубликовано, оно может дать **параметрическое семейство** rot2-решений, продолжаемое по n. Опора: rct4 доживает до рекордных нечётных n (57…69), rot4 — до чётных (60…76); симметрия «стоит C·log n» (Флямменкамп). Порог: семейство даёт бесконечную серию точных 2n при n→∞.
4. **Континуальный/ренормализационный предел как приор.** Использовать LP-континуум-сертификат (2605.09215) и профиль плотности (Флямменкамп density.html) для угадывания предельной формы, затем дискретизировать. Порог: дискретизация стабильно даёт ≥3n/2 с нужным профилем наклонов.
5. **Перенос 3D-конструкции проекцией.** Проекция плотного подмножества moment curve/параболоида из n×n×n (Pór–Wood, Θ(n²)) в 2D с контролем возникающих коллинеарностей. Опора: Pór–Wood; обструкция известна (Сегре) — цель локально её обойти. Порог: проекция сохраняет ω(n) точек без троек.

### (B) Что стоит прекратить пробовать (и почему)

- **Чисто модулярные арки (парабола/гипербола/коника mod p) в надежде превзойти 3/2.** Теорема Сегре жёстко ограничивает дугу ~p+1≈n; максимальных дуг в дезарговых плоскостях нечётного порядка нет (Ball–Blokhuis–Mazzocca). Тупик.
- **Локальный поиск / warm-start / обмен пар / drop-k для точных 2n при больших n.** Ваши негативные результаты согласуются с литературой: PPO ломается на 11×11, PatternBoost не масштабируется за n=15 (arXiv 2512.11469); известные решения локально жёстки. Это метод поиска, а не конструкции — асимптотики не даст.
- **Опора на вероятностную эвристику как на предсказание для симметричных классов.** Эвристика Guy–Kelly/Prellberg даёт «<1 решения» уже при включении rot2, что заведомо ложно (Прельберг: «casts doubts as to its validity»). Не использовать её как ограничитель для симметричных конструкций.
- **Ожидание, что методы k≥3 (Kovács–Nagy–Szabó; Grebennikov–Kwan; Ghosal–Goenka–Grebennikov–Keevash–Kwan–Pham, 2607.05255) дадут что-то при k=2.** Авторы явно заявляют, что при k=2 их результаты ничего не дают; шаг абсорбции/удаления требует запаса >2 на прямую.
- **Метод Агамы (2106.15621) как источник улучшения в 2D.** При d=2 даёт ≈1.19n < 1.5n; в 2D бесполезен.

## Caveats
- **Метод Джейкоба Дэйвиса не документирован** нигде, кроме однострочного кредита Флямменкампа; любые утверждения о его природе (конструкция vs поиск vs пертурбация) были бы спекуляцией. Проверены readme #B, поиск по имени, Reddit, Hacker News, OEIS — везде пусто. Для выяснения — прямой запрос Флямменкампу.
- **arXiv:2106.15621** — не рецензирован в сильном источнике, 10 версий; Прельберг ошибочно приписывает его «Y.C.R. Lin», тогда как автор — **Theophilus Agama**. Проверяйте при цитировании.
- **arXiv:2607.05255** — авторы **Anubhab Ghosal, Ritesh Goenka, Alexandr Grebennikov, Peter Keevash, Matthew Kwan, Huy Tuan Pham** (v1, 6 Jul 2026); результат f_k(n)=kn для k≥3 подтверждён. Это отдельная работа от Grebennikov–Kwan (2510.17743, только большие k) и от Kovács–Nagy–Szabó (2502.00176, k>C√(n log n)).
- Прямых публичных репозиториев Riley (CUDA) и специализированного SAT-кода Heule именно под эту задачу локализовать не удалось; известны лишь косвенные упоминания и общая страница Heule.
- Строгого second-moment/энтропийного обоснования плотности симметричных решений в литературе нет — только эвристика Флямменкампа («C log n») и замечание Прельберга; это область для новой работы, а не установленный факт.
- Число известных конфигураций в базе (430991) и рекорд n=76 (Heule, rot4, 10 авг 2026) — по состоянию readme на 2026-08-11. Известность: все n ≤ 70 и n=72,74,76; открыты n=71,73,75 и ≥77 — согласуется с вашим контекстом.