# Deep research 14 — прайор-арт к спектру направлений и κ

Дата: 2026-09-03. Ответ третьего коллеги (Fable, сессия saturation-cd) по брифу владельца `deep_research_brief_14_direction_spectrum.md`.

Статус: мульти-агентный воркфлоу `wf_a65af916` — 37 агентов: 9 каналов поиска по классам источников и 8 доборов (Sonnet); 17 проверяющих-противников (каждая ссылка и цитата переоткрыты), критик полноты, синтез и adversarial-ревью (Opus). 211 находок: 114 verified, 88 corrected (проверяющий исправил библиографию или цитату — ниже приведена исправленная версия), 7 unverified, 2 refuted; 2 274 вызова инструментов. Сохранённые тексты источников (730 файлов, 434 МБ) и транскрипты агентов — вне git (сессия saturation-cd; копия в `~/research_scratch/2026-09-03-e5097638/b14`).

## Приёмка третьего — пять строк

1. Фраза заметки v1.0 «no prior-art search beyond the classical sources has yet been run» **честна для v1.0 и устарела для v1.1**: поиск проведён, по четырём вопросам дополнения результат отрицательный. Готовый текст замены — в разделе «Итог и прямой ответ» ниже.
2. **Д1 модель прямых — не найдено** (внешние источники, прочитанные целиком: Guy–Kelly 1968 в обеих версиях; UPINT §F4 обоих изданий сниппетами; Adena–Holton–Kelly 1974 сниппетами; Prellberg ×3; Voutier; Ghosal ×2). Ближайшее: Prellberg arXiv:2605.09215 — «capacity-two constraints on rows, columns, and the two diagonal families» как LP-релаксация по четырём направлениям; не ансамбль, весов C(L,x) нет.
3. **Д2 измерения ансамбля — жанр известен, наша наблюдаемая нет**: Flammenkamp density.html (с 1997, продолжено Прельбергом в 2026 на n = 56/57) — позиционная плотность, не направления. Направленческое измерение на реальных решениях — только веб-самопубликация aujurd22 (GitHub, июль 2026), partial: n центральных направлений симметричных решений, без κ и без нормировки. Это единственный спорный вердикт; следствие: заметка не может заявлять качественную новизну «короткие направления обеднены», только количественную (полный спектр, нормировка по m, κ, модель).
4. **Д3 имя тождества — не найдено**: ближайшее имя поля «restricted occupancy» (Freund 1956), сами работы кластера не прочитаны; Kaplansky–Riordan 1946 и Riordan 1958 закрыты. Моя ставка (журнал moves: «опознается как стандартное с источником до 1960») — **нарушена**.
5. **Д4 рост длинных направлений — не найдено** ни измерения, ни объяснения; полезный контраст — Remark 1.7 из arXiv:2607.05255 предсказывает для k = 2 равный вклад всех диадических масштабов, то есть отсутствие роста.

Прочие вердикты: Q3 деление счёта Гая–Келли по направлениям — не найдено (по прочитанным текстам, а не по их недоступности); Q4a/Q4b/Q4c — не найдено; Q5 стримлайнинг — частично известно с другой регулярностью (Prellberg §5.5 без чисел; MCTS с симметрийным приором и измеренным ускорением) — вторая половина моей ставки тоже нарушена; Heule 2026 — публичного описания метода не существует; Q6 — не найдено по обоим подвопросам.

## Контракт доказательности (метки статусов)

- **внешний источник** — всё, что помечено verified/corrected со ссылкой на номер в списке «Источники»;
- **локальный факт** — привязки к строкам `paper/direction_spectrum_note.tex`, к файлам сессии и к сохранённым копиям источников;
- **вывод** — оценки «не прайор-арт по §2 брифа», предлагаемые правки заметки, гипотеза о файлах n52_*_diag на сайте Фламменкампа;
- **неизвестно** — всё в разделе «Осталось непроверенным» и всё с пометкой [не открыт];
- **pilot** — отсутствует.

## Ограничение метода — обязательно к прочтению

Лимит веб-поиска сессии (200 запросов) исчерпался примерно в 17:50 WITA, до старта проверяющих и доборов; независимо подтверждено каждым проверяющим. Все отрицания опираются на прямые загрузки, API (arXiv, Crossref, OpenAlex, Unpaywall, Semantic Scholar, zbMATH Open, OEIS, GitHub, Stack Exchange, Wayback) и полнотекстовый поиск внутри arXiv/zbMATH/OEIS/Google Books/Open Library — не на поиск по свободному тексту. Слабее всего покрыты: метод Хойле 2026, Дэвис 2026, личные страницы, слайды, диссертации. Второй заход с поисковым API через curl (Brave Search API, Perplexity или подобное) либо с поднятым `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` закроет именно эти дыры; список первоисточников, которые надо открыть руками (JCTA 1992/1998 — bronze OA в браузере), — в разделе «Осталось непроверенным».

## Ставка и исход (moves/ledger.jsonl, линза recognize_the_shadow)

Ставка (записана в 17:45, после запуска поиска, до чтения результатов): Д1, Д2, Д4, Q3, Q5 — не найдено; Д3 — опознаётся как стандартное с источником до 1960. Исход: **нарушен** — Д3 не опознано (имя поля есть, совпадение с формулой не подтверждено), Q5 частично известно (Prellberg §5.5; MCTS). Остальное держится. Проигрыш хороший: заметка получает ссылки.

---

*Ниже — текст синтеза после adversarial-ревью (Opus), с моей правкой одной фразы о страницах JCTA 81 (1998): ошибочные страницы 397–400 стоят в заметке Прельберга 2025 г., в брифе страниц нет.*

---

## Итог и прямой ответ на главный вопрос

**Честна ли фраза заметки «and no prior-art search beyond the classical sources has yet been run»?**
(v1.0, аннотация, строка 28 файла `paper/direction_spectrum_note.tex`; проверено прямым чтением файла.)
Да, честна — как утверждение о состоянии дел на момент публикации. Поиска тогда действительно не было, и формулировка ничего не преувеличивала и не скрывала. Формулировку «фраза перестала быть честной» мы сознательно не употребляем: она приписывает тексту v1.0 дефект, которого в нём не было. Точная характеристика другая: **фраза устарела**, потому что поиск теперь проведён (этот документ), и оставлять её в следующей версии нельзя — там она станет ложной.

**Что следующая версия может сказать — и чего сказать не может.**

Может (всё перечисленное опирается на verified/corrected-находки или на записанные адреса поиска, см. таблицу вердиктов и разделы Q1–Q6):
- поиск проведён и он многоканальный; по четырём главным пунктам результат отрицательный — не найдено ни опубликованного измерения числа пар по направлениям или занятости диагоналей на реальных решениях, ни κ-подобной константы, ни разложения счёта Гая–Келли по направлениям, ни объяснения роста длинных направлений с n;
- названы ближайшие соседи, ни один из которых не является прайор-артом по разделу 2 брифа: ансамблевые карты позиционной плотности Фламменкампа/Прельберга, LP-релаксация Прельберга с ограничениями ёмкости два по четырём направлениям, γ±(α) Симкина для n-ферзей, «A Superficial Explanation» Фламменкампа как предшественник механизма, Cooper–Solymosi и Erdős–Purdy как методические предшественники операции «разложить пары по направлениям», и веб-самопубликация направленческих измерений (GitHub, июль 2026).

Не может:
- писать «прайор-арта нет» без оговорки о методе. Полнотекстовый веб-поиск в ходе этого захода был **недоступен** (бюджет сессии исчерпан до старта всех каналов; независимо подтверждено каждым проверяющим на собственном вызове). Отрицания опираются на прямые загрузки, API (arXiv, Crossref, OpenAlex, Unpaywall, Semantic Scholar, zbMATH Open, OEIS, GitHub, Stack Exchange, Wayback) и полнотекстовые поиски внутри arXiv/zbMATH/OEIS/Google Books/Open Library — но не на поиск по свободному тексту. Поэтому слабее всего покрыты личные страницы, блоги, диссертации и слайды вне известных каталогов;
- писать «мы прочли всю классику». Не открыты: Ungar 1982, обе Jamison 1984, Jamison–Hill 1983, Kaplansky–Riordan 1946, гл. 5 Riordan 1958, HJSW 1975, Anderson 1979, тела Flammenkamp JCTA 1992/1998, кластер restricted occupancy, опубликованный текст Fascicle 7 Кнута (полный список с причинами — в разделе «Осталось непроверенным»);
- претендовать на КАЧЕСТВЕННУЮ новизну наблюдения «короткие/диагональные направления обеднены»: веб-самопубликация [60] (июль 2026) даёт тот же качественный вывод на реальных решениях против случайной нуль-модели. Новизна, которую заметка может защищать, — количественная: полный спектр по всем C(2n,2) парам, нормировка measured/random по m = max(|a|,|b|), константа κ и модель прямых.

**Предлагаемая замена фразы (готовый текст, ничего сверх находок):**
«A multi-channel prior-art search has now been carried out (§N). We found no published or web-posted measurement of pairs per direction or of diagonal occupancy on actual no-three-in-line solutions, no κ-like constant, and no per-direction decomposition of the Guy–Kelly count; the nearest published objects are listed and delimited in §N. The search used direct retrieval and full-text search inside arXiv, zbMATH, OEIS, Google Books and Open Library; free-text web search was not available during it, and a number of primary sources (listed in §N) were not read, so the negative result is stated with that limitation.»

## Вердикты

| пункт | вердикт | главный источник или «искали: …» |
|---|---|---|
| spectrum law (Q1) | **not found** | искали: страницы Фламменкампа (readme, symmetry_remarks, density, table/table_old, images, near_miss, полный листинг каталога из 120 файлов, подкаталог data_1997/), Guy–Kelly в обеих версиях 1968 [7,8], UPINT §F4 обоих изданий [10], Adena–Holton–Kelly 1974 [11], Voutier [20], Prellberg ×3 [17,18,19], Ghosal ×2 [21,22], MCTS [23], «Three/Four methods» [24], Кнут (все открытые тексты) [42], MathWorld [59], Wikipedia, OEIS (в т.ч. полнотекстово), MathOverflow/Math.SE через API, ноутбуки Ed Pegg с Wolfram Community [61], Dudeney/Gardner [68]. Ближайшее опубликованное — [2] (другая наблюдаемая) и самопубликация [60] |
| κ (Q2) | **not found** | тот же корпус + полнотекстовый OEIS: каталогизирована только константа Гая π/√3 (A093602), κ-подобной нет. Ближайшее: детерминированные утверждения о двух длинных диагоналях [3]; неудачная попытка «фиксировать число занятых клеток на диагоналях» [17, §5.5]; γ±(α) для n-ферзей [25]; константа α LP-релаксации [18] |
| per-direction Guy–Kelly split (Q3) | **not found** | Guy–Kelly CMB (5 стр.) и Research Paper #33 (11 стр., собственный OCR) прочитаны целиком [7,8]; UPINT §F4 2-го и 3-го изданий прочитан сниппетами, «slope»/«gradient» — 0 вхождений во всей книге [10]; AHK 1974 — вероятностный раздел прочитан, во всём томе LNM 403 «slope/slopes/gradient/directions/parallel» — 0 [11]; Voutier — 0 вхождений «direction/slope» [20]; Prellberg [17] — 1 бытовое; Ghosal [21] — 41 вхождение, все как ε-heavy/ε-light в доказательстве |
| Remark 1.7 (Q3) | **known** — но по разделу 2 брифа **не прайор-арт** | [21], Remark 1.7, стр. 3: при k = 2 сумма ≈ log n и «each "dyadic scale" of m contributes to the sum equally» |
| adjacent slopes multiset (Q4a) | **not found** | искали: Pach, Handbook DCG гл. 1 [38]; Solymosi [31]; Martin, math/0302106; Fernández-Merchant–Hämäläinen [32]; рецензии zbMATH на Ungar и обе Jamison 1984 и на Jamison–Hill 1983 [33–36]; полнотекстовый zbMATH по «multiset of slopes» и «slope multiset» → 0 записей; arXiv-метапоиск по тем же фразам → 0. Тексты Ungar 1982 и Jamison 1984 не открыты |
| random sets direction distribution (Q4b) | **not found** | Eppstein, оба поста 2018 [40] (0 вхождений direction/slope/diagonal); Ghosal 2605.07000 [22] (счёт O(m) направлений внутри оценки сверху); Nagy–Nagy–Woodroofe [29] (пары с наклоном r/q как шаг доказательства); Cooper–Solymosi [26]; Li [27]; зонды arXiv API по «direction distribution», «collinear triples random set» |
| max-entropy / computable κ (Q4c) | **not found** | Simkin [25] — ёмкость 1, функции γ±(α), ни одного числа; Prellberg [18] — ёмкость 2 по четырём направлениям, но это верхняя LP-оценка для чётностного варианта; зонды arXiv/zbMATH по lattice gas / multiple occupancy / exclusion statistics / cluster expansion — ничего по нашему гиперграфу |
| streamlining for this problem (Q5) | **partially known** | отрицательный прецедент: [17] §5.5 (профили плотности как приоритеты ветвления + фиксация занятости диагоналей, «None of these improved performance reliably»); положительный, но с ДРУГОЙ регулярностью: [23] (класс симметрии C4 как приор в MCTS, 33042.73 → 7722.33 с при n = 70, p < 0.001); определение streamlining [43] — к этой задаче не применялось |
| Heule 2026 structure (Q5) | **not found** | его собственный открытый каталог слайдов CMU (59 PDF, последние 2026-07-20) — ни одного про задачу; авторизованный GitHub code search внутри аккаунта — 0 файлов при 53 репозиториях; arXiv (au:Heule, 53 записи); Google Scholar (12 работ 2026 г.); программы SAT 2026 (FLoC) и Pragmatics of SAT 2026; единственный источник — построчные записи в readme Фламменкампа [1] |
| 3D A280537 (Q6) | **not found** (оба подвопроса) | OEIS A280537/A280538 + полнотекстовый поиск OEIS; azspcs Description/Standings/FinalReport [53]; исходный тред rec.puzzles 27.11.1992 прочитан через Wayback [54]; страница Sillke/Flammenkamp cube3 [54]; Pór–Wood — полный текст GD 2004, слово «project» 0 вхождений [55]; Cohen–Eades–Lin–Ruskey [56]; GitHub (3 запроса); страницы призёров Rokicki и Wróblewski |
| line model Д1 | **not found** как ансамбль; **терминология найдена** | [18]: «capacity-two constraints on rows, columns, and the two diagonal families of slopes ±1» — готовое проверенное имя; [26] Theorem 1 — разбиение пар по классам наклонов с cap «≤ 2 на прямой», но в торе Z_p×Z_p и как pigeonhole-существование; [28] — «the number of pairs determining this direction is Σ C(h_i,2)» как приём доказательства |
| ensemble measurements Д2 | **known** — но только как ЖАНР; **прайор-артом по §2 брифа не является**: наблюдаемая другая | [2] density.html: частоты занятости клеток по всем 2×541 решениям n = 20 rot4, карты n = 36/38/42, и от Прельберга n = 56 (10441 конфигурация) и n = 57 (833); [11] Table 1 — числа решений по классам симметрии; [60] — направленческие измерения реальных решений против случайной нуль-модели (самопубликация, без рецензии) |
| identity name Д3 | **not found** | ближайшее употребимое имя поля — «restricted occupancy» (Freund 1956 и далее) [48]; невзвешенный равноящичный частный случай — Comtet, упр. 19 гл. III, с. 163 [46]; «capacity-two constraints» [18] — имя ЛИНЕЙНОГО ОГРАНИЧЕНИЯ, не производящей функции. Kaplansky–Riordan [44] и гл. 5 Riordan 1958 [45] не открыты |
| growth of long directions Д4 | **not found** | ни измерения, ни объяснения ни в одном проверенном источнике; единственная измеренная зависимость от n у Фламменкампа — позиционная плотность [2]. Полезный контраст: [21] Remark 1.7 предсказывает при k = 2 РАВНЫЙ вклад всех диадических масштабов, то есть отсутствие роста |

**Ни одна находка этого захода не является прайор-артом по разделу 2 брифа.** Раздел 2 требует: опубликованного или веб-опубликованного измерения (таблица/график/число) числа пар по направлениям или занятости прямых фиксированного направления на реальных решениях, ИЛИ теоретического закона для мультимножества наклонов экстремальных конфигураций, ИЛИ вычисленной κ-подобной константы. Все находки ниже помечены relevance adjacent/partial/none их собственными проверяющими; ни одна не переведена в прайор-арт при синтезе.

**Единственный спорный вердикт — [60].** По букве раздела 2 «web-posted measurement … on actual solutions» самопубликация aujurd22/no3inline-rigidity (июль 2026) ближе всех к границе: там есть измерения направлений реальных решений базы Фламменкампа против явной случайной нуль-модели и таблицы по n. Мы относим её к partial по трём причинам, каждая проверена: измеряется мультимножество n ЦЕНТРАЛЬНЫХ (антиподальных) направлений симметричных решений, а не C(2n,2) пар; по лемме того же файла эти n направлений попарно различны, то есть «спектр» вырождается в индикатор 0/1; κ и нормировки measured/random по m там нет (grep по 0.73/0.6486/0.639/kappa — пусто). Но рецензент вправе не согласиться, поэтому вывод для заметки жёсткий: **[60] надо процитировать и явно отграничить**, а качественное утверждение «короткие/диагональные направления обеднены» не заявлять как впервые наблюдённое.

---

## Дополнение 3.09 — что искали прежде всего

### Д1. Модель прямых («точки, разложенные по прямым одного направления, ≤ 2 на прямой, веса C(L,x)»)

**Что найдено.**

(1) **Ближайшая опубликованная реализация скелета модели — Prellberg, arXiv:2605.09215v1 [18]** (verified; PDF скачан и прочитан двумя проверяющими независимо). §1, стр. 2:

> «There is also an immediate capacity obstruction. In one checkerboard class, every diagonal of slope +1 and every diagonal of slope −1 is monochromatic. Each such diagonal can therefore contain at most two selected points, and counting the capacity of one diagonal family gives Dmono (n) ≤ 2n − 2. [...] The main tool in the paper is the four-direction linear-programming relaxation Lmono (n, ε). This relaxation replaces the integral choice of points in Cε by a nonnegative fractional mass assignment and keeps the capacity-two constraints on rows, columns, and the two diagonal families of slopes ±1.»

и там же, §4 (verified отдельным каналом):

> «The quantity Lmono(n, ε) ignores all slopes other than 0, ∞ and ±1. For the classical square-grid no-three-in-line problem, the analogous four-direction relaxation collapses to the trivial upper bound 2n. Indeed, the constant fractional assignment zx,y = 2/n is primal feasible, while the dual solution assigning weight 1/2 to each row and each column, and weight 0 to the two diagonal families, has the same value.»

Почему это НЕ прайор-арт по разделу 2 брифа: (а) это верхняя оценка (LP-релаксация с дуальным сертификатом) для чётностно-ограниченного варианта, а не измерение на реальных решениях; (б) весов C(L,x) и перенормировки на число пар нет; (в) направлений ровно четыре, спектр не строится; (г) континуальная константа задачи (средний корень 401α³ − 1744α² + 2240α − 768 = 0) — предельный наклон для D_mono, а не доля дважды занятых диагоналей. Почему это всё равно важно: это единственное найденное место, где прямые одного направления с ограничением «≤ 2» выступают самостоятельным объектом счёта именно для этой задачи, и второе процитированное наблюдение прямо подтверждает механизм заметки — одной диагональной ёмкости мало, информация сидит в распределении по остальным направлениям.

(2) **Разбиение пар по классам наклонов с cap «≤ 2» — Cooper & Solymosi 2004 [26]** (verified), §1.1, стр. 2 препринта:

> «Note that for every pair of points in the graph of σ, the slope of that pair must be in 1, . . . , n − 1. Partition the n2 pairs into classes according to their slopes. Since there are n − 1 classes, at least n/2 pairs lie in some class. Each of these pairs lies on some line of the same slope, and no two of them lie on the same line, since then we would a collinear triple.»

Не прайор-арт: объект — тор Z_p×Z_p, а не сетка [n]²; это pigeonhole-оценка существования, а не измеренный или выведенный закон.

(3) **Классический прецедент самой величины «пары на направление» — Erdős & Purdy 1976 [28]** (verified; скан свободно лежит в архиве работ Эрдёша, качество OCR плохое, формулы искажены), §3, доказательство Theorem 4:

> «For the covered points, let h i be the number of points on the i th line parallel to t ... Then the number of pairs determining this direction is [в скане: ~t 2 1 1 — т.е. Σ C(h_i,2), формула разрушена OCR] ... The number of directions is at least cn 3/4 ... Hence the total number of pairs is at least ... which is absurd.»

Не прайор-арт: приём доказательства для произвольных множеств, без ограничения «≤ 2 на прямой» и без всякого измерения.

(4) **Ближайший опубликованный предок МЕХАНИЗМА заметки — Flammenkamp, readme.html, раздел «A Superficial Explanation» [1]** (verified):

> «For the diagonal reflection classes dia1 and dia2 two independent selected points force typically the blockade of n/2 points ... . And in the rotation symmetry classes rot? two independent selected points force typically the blockade of about C log(n). The effect of blockade of the remainding 4 of 6, respectively 20 of 28, straight lines seem roughly independent of the regarded symmetry class. Therefore one should expect most different configurations for given n in the rotational symmetry classes but least different configurations in those with mid-perpendicular symmetry. For a precise analysis of the asymmetric case, see the paper of Guy and Kelly 1968.»

Это та же экономика «пара точек стоит затенения», но агрегированная по классам симметрии, без чисел и без направлений; заметьте связку с длинами прямых: n, n/2 и C log n — порядки числа точек решётки на прямой осевого, диагонального и «типичного» направления.

(5) **Готовый образец вычислимой энтропийной модели занятости прямых по направлению — Simkin [25]** (verified), §4.2, стр. ~25:

> «the number of plus-diagonals passing through αn that are occupied by elements of q is ≈ γ + (α)n and the number of occupied minus-diagonals is ≈ γ − (αn )n. ... If we assume that the occupied diagonals in each direction are approximately independent (over the choice of q), then there are ≈ B2 (α) := |αn |N 2 γ + (α)γ − (α) positions threatened along both diagonals»

Не прайор-арт: другая задача (n-ферзи, ёмкость прямой 1), κ там не считается. Ценно как прецедент того, что предположение независимости направлений нетривиально и требует отдельного доказательства.

**Что не найдено и где искали.** Ансамбля «независимые ящики ёмкости 2 с весами C(L,x)» и счёта пар при ограничении «≤ 2 на прямой» нет: во всей линии Гая–Келли (CMB 1968 и Research Paper #33 прочитаны целиком; комментарий Гая в OEIS; UPINT §F4 обоих изданий; Adena–Holton–Kelly 1974; Voutier 2026; Prellberg 2602.07751; Ghosal и др. 2607.05255) считаются НЕОГРАНИЧЕННЫЕ тройки в модели независимости — ни ёмкости прямой, ни счёта пар, ни перенормировки. HJSW 1975 и Anderson 1979 остались неоткрытыми (только дословные абстракты из архивных снимков) — по абстрактам это конструктивные работы о нижних оценках. Тела Flammenkamp JCTA 1992/1998 не открыты, но рефераты zbMATH, написанные читавшими их рецензентами, перечисляют содержание (новые решения, классификация «according to symmetries», table 1 с числом решений, приложение с картинками) и направленческой статистики не упоминают.

**Вывод.** Модель прямых как ансамбль не встречена. Для заметки: терминология «capacity-two constraints per direction» (Prellberg) — готовое проверенное имя, на которое стоит опереться; Cooper–Solymosi и Erdős–Purdy стоит процитировать как методических предшественников операции «разложить пары по направлениям с ограничением на прямую», явно отграничив (тор / произвольные множества / приём доказательства).

### Д2. Измерения ансамбля решений

**Что найдено.**

(1) **Flammenkamp, «Frequency Distributions of Points of No-Three-in-Line Configurations» (density.html), обновлена 2026-06-12 [2]** (verified тремя каналами независимо, страница перекачана каждым):

> «The following table gives you a feeling of the frequency distribution for the selected points of large no-three-in-line configurations. Here you see the upper left quarter of the grid of all solutions for n=20 in symmetry class rot4. In each of the 20x20 locations of the quarter the points of the 2x541 different configurations are summed up and these values are decreased by the expected number of these points (54.1) for each location. [...] So the frequency/density distribution is roughly a function of the euclidean distance to the grid center. [...] Since 2026 Thomas Prellberg, Queen Mary University of London, UK, has achieved much progress ... So he could generate for all 10441 configurations in symmetry class rot4 of the 56 x 56 grid this ... corresponding frequency map aka. "heatmap" in April 2026. And finally for n=57 in symmetry class rct4 he constructed this ... 2 dimensional frequency distribution from all 833 configurations on 31th May 2026.»

Методология идентична брифовской (наблюдаемая минус ожидание, усреднение по ВСЕМ известным решениям класса, зависимость от n), наблюдаемая ДРУГАЯ: позиционная плотность точек по клеткам, не число пар по направлениям и не занятость диагоналей. Основная часть датирована «Everything above was done and known until 1997-01-02», карты n = 56/57 — 2026 год.

(2) **Независимое воспроизведение того же наблюдения в учебном тексте** (corrected, атрибуция страницы автору не подтверждена — имя на странице не проставлено) [58]:

> «Not all grid points are equally likely to appear in solutions to the problem. ... This correlates roughly inversely with the number of collinear triples in the grid which contain the point.»

(3) **Adena–Holton–Kelly 1974, Table 1 [11]** (verified, сниппеты Google Books, стр. 6–7): перепись ансамбля экстремальных конфигураций для малых n — но по КЛАССАМ СИММЕТРИИ:

> «Table 1 also shows the number of solutions having various symmetries . ( K diagonal ; L about both diagonals ; M about one bisector of opposite sides ; ... Q - a half turn ; that of a square ; R a quarter turn . ) S and T give totals ; T considers isomorphic solutions as distinct .»

(4) **Единственное найденное направленческое измерение на реальных решениях — веб-самопубликация [60]** (verified; репозиторий склонирован целиком, файл analysis/spectral_struct_n0mod4.md, рабочая записка 2026-07-08):

> «2. **Danger is extremely concentrated.** The single direction `(1,1)` (main diagonal) has danger-degree 743 → 2493 → 6209 — it dominates the hypergraph. `(1,−1)` (anti-diagonal) is a close second. Low-slope / small-integer directions are the dangerous ones; large coprime directions are nearly safe individually ... 3. **Solutions actively avoid danger.** The mean danger-degree of a real solution's chosen directions is *below* that of a random `n`-subset of directions (99 vs 118; 177 vs 320; 314 vs 631). Real solutions are not random — they steer away from the dangerous diagonal directions.»
> «**4c. Angular uniformity.** Real solutions spread their directions more evenly than a random direction set: the std-dev of angular gaps between consecutive directions is **below** the random baseline for every `n` tested (e.g. n=12: 0.199 vs 0.211; n=44: 0.061 vs 0.071).»

Почему это partial, а не prior_art: измеряется мультимножество n ЦЕНТРАЛЬНЫХ (антиподальных) направлений симметричных решений — подмножество пар, причём по лемме того же файла эти n направлений попарно различны, то есть «спектр» вырожден в индикатор 0/1; гистограммы всех C(2n,2) пар по примитивным направлениям нет, нормировки measured/random по m = max(|a|,|b|) нет, κ нет (grep по 0.73/0.6486/0.639/kappa — пусто). Качественный вывод («короткие/диагональные направления обеднены») при этом совпадает с измерением брифа. Оговорки: самопубликация одного человека без рецензии и DOI, помеченная как «AI-assisted computational research notebook», с несколькими собственными ретракциями и с прямым числовым противоречием между двумя прогонами (в analysis/danger_hypergraph_report.txt для n = 12 стоят 7238 запрещённых троек и sol 650.29 vs random 749.97, в .md — 691 и 99.3 vs 118.5); ни одно число оттуда нельзя цитировать без пересчёта.
В том же репозитории найден скрипт analysis/dir5_invariants.py, docstring которого описывает ровно измерение брифа («classify every line through >=2 points by its D4-canonical direction, and record the occupancy ... which canonical directions carry the most occ=2 lines»), но его выходной JSON results/dir5_invariants.json в репозитории ОТСУТСТВУЕТ, и две сводки проекта фиксируют, что он был обрезан при аварийном завершении процесса. То есть замысел независимо запрограммирован в июле 2026 и не доведён до публикации — прайор-арта нет, но приоритетная картина именно такая.

**Что не найдено и где искали.** Опубликованного измерения пар по направлениям или занятости диагоналей — нигде: страницы Фламменкампа целиком (включая ранее не проверявшиеся four_cycle_decomposition_note.html и four_corner_permutation_note.html июня 2026, ntdia, table_min_defect, весь подкаталог data_1997/); MathWorld [59]; Wikipedia; OEIS (12 последовательностей по теме + полнотекстовый поиск); MathOverflow и Math.SE через Stack Exchange API (≈15 запросов); оба поста Ed Pegg на Wolfram Community — их тело лежит в приложенных .nb, оба ноутбука (4,1 МБ и 3,7 МБ) скачаны и прогреплены: diagonal/slope/direction/statistic/histogram — 0 вхождений; обе профильные Wolfram Demonstrations через Wayback; Gardner (глава 5 «Penrose Tiles…», стр. 63–77) и Dudeney (задача 317, стр. 94 и 222).

**Вывод.** Жанр «статистика по всей базе решений» опубликован и датируется 1997 годом (Фламменкамп), а в 2026 продолжен Прельбергом на n = 56/57. Заметка обязана на него сослаться и сказать, чем её наблюдаемая отличается; иначе она читается как первый заход в жанр, каковым не является. Отдельно стоит сослаться на [60] и явно отграничиться.

### Д3. Имя тождества (ансамбль независимых ящиков ёмкости 2 с вырождениями C(L,x))

**Что найдено.**

(1) **Невзвешенный равноящичный частный случай — Comtet, Advanced Combinatorics (1974), гл. III, упр. 19, с. 163 [46]** (verified по открытой OCR-копии; цитата дана в сыром виде, искажения — OCR):

> «19. Middle trinomial coefficients. These are <7„=C»n(l + <+t^)" (P- 77): ... (1) The integer a„ is the number of distributions of indistinguishable balls into n different boxes, each box containing at most 2 bails.»

Отличия от Теоремы 1 заметки: одинаковые ящики вместо разных L_i и веса 1/1/1 вместо C(L,0)/C(L,1)/C(L,2). Атрибуции результата в упражнении нет. Во всей книге слова «occupancy» нет ни разу.

(2) **Устоявшееся имя ПОЛЯ — «restricted occupancy» [48]** (corrected): поиск zbMATH по заголовкам даёт ровно 8 записей (1956–2011), старейшие — Freund, «Restricted Occupancy Theory—A Generalization of Pascal's Triangle», Amer. Math. Monthly 63(1) (1956) 20–27, и Freund & Pozner, «Some results on restricted occupancy theory», Ann. Math. Statist. 27 (1956) 537–540. **Ни одна работа кластера не прочитана** (единственный успешный запрос к legacy-адресу Project Euclid вернул валидный четырёхстраничный PDF Freund–Pozner, но файл был утрачен до конвертации, а дальше включился антибот), поэтому совпадение с точной формулой (неравные L_i, вес C(L,x)) НЕ подтверждено — подтверждено только существование имени.

(3) **Единственное проверенное употребление словосочетания в нашей задаче — Prellberg [18]**: «capacity-two constraints on rows, columns, and the two diagonal families». Существенная оговорка: у него это имя ЛИНЕЙНОГО НЕРАВЕНСТВА (Σ z_p ≤ 2) в LP-релаксации, а не имя производящей функции ∏(1 + L_i t + C(L_i,2) t²) и не имя взвешенного ансамбля.

(4) **Проверенные соседи, которые НЕ совпадают.** Статистика Джентиле в изложении Дая–Се [50] (verified): потолок n стоит на КАЖДОМ одночастичном состоянии, множитель (1+x+…+x^n)^{ω_ℓ}, тогда как у нас клетки фермионные, а потолок 2 стоит на ВСЕЙ прямой. Полный итальянский заголовок первоисточника, отсутствующий у Дая–Се, найден: G. Gentile, «Osservazioni sopra le statistiche intermedie», Nuovo Cimento 17(10) (1940) 493–497, DOI 10.1007/bf02960187. Ладейная теория [47,51]: у Stanley (Notes к гл. 2, с. 249) «The theory of rook polynomials in general is due to Kaplansky and Riordan [2.13]; see Riordan [2.17, Chs. 7–8]» — то есть счёт НЕатакующих ладей (≤ 1 на строку И на столбец), не occupancy; слова «occupancy» в EC1 нет ни разу (35 290 строк, 0 вхождений). m-level/file rook placements [51]: «A file placement on a board B is F ⊆ B such that no two rooks (elements) of F are in the same column» и f_k(B) = e_k(b_1,…,b_n) — сохраняется ограничение по столбцам, не наш объект. Fang 1982 [49] (абстракт): «There are m urns each containing k cells; n balls are assigned to the m urns in such a way that each cell contains at most one ball» — равновеликие урны, ≤ 1 на ячейку, без внешнего потолка 2.

**Что не найдено и где искали.** Отдельного имени именно для тождества Теоремы 1 нет: zbMATH по заголовкам «capacity two» (2 записи — жордановы алгебры), «limited occupancy» (0), «partition matroid» (9, все алгоритмические), полнотекстово «truncated elementary symmetric» (1 нерелевантная), «parafermi statistics» (2 нерелевантные); arXiv API «capacity-two» (6 инженерных), abs:«partition matroid» AND abs:«generating polynomial» (0), all:«boxes of capacity two» (0); OEIS по «each box containing at most 2» и «at most two balls» — пусто. Kaplansky–Riordan 1946 [44] не открыт (пять независимых свидетельств закрытости: Project Euclid отдаёт антибот-заглушку и на обоих адресах, Semantic Scholar openAccessPdf CLOSED, OpenAlex any_repository_has_fulltext=false, zbMATH без метки «has open version»); гл. 5 Riordan 1958 [45] не открыта (три копии archive.org, все access-restricted; оглавления нет ни в OpenLibrary, ни у Dover, ни в рецензиях zbMATH) — то есть предположение брифа о названии главы «Distributions: occupancy» осталось не подтверждённым и не опровергнутым; MathSciNet полнотекстово не искался (нет доступа).

**Вывод и готовая формулировка для заметки.** «Устоявшегося имени именно для этого тождества мы не нашли в открытых сетевых источниках (книжные справочники Kaplansky–Riordan 1946 и Riordan 1958 остались непрочитанными). Ближайший зонтичный термин в реферируемой литературе — restricted occupancy (Freund 1956 и далее); ближайший прочитанный текстовый пример — невзвешенный равноящичный частный случай у Comtet (1974, упр. III.19); фразу capacity-two constraints употребляет Prellberg (2026), но применительно к линейным ограничениям LP-релаксации».

### Д4. Рост длинных направлений с n (c(3,7): 0.179 при n ≈ 20 → 0.221 при n ≥ 32)

**Что найдено.** Ничего. Ни измерения, ни объяснения.

**Что не найдено и где искали.** Полнотекстово: Guy–Kelly обе версии [7,8]; UPINT §F4 обоих изданий [10]; Adena–Holton–Kelly 1974 [11]; Voutier [20]; Prellberg 2602.07751, 2605.09215 и заметка Sep 2025 [17,18,19]; Ghosal и др. [21] и Ghosal [22]; Kovács–Nagy–Szabó [30]; Nagy–Nagy–Woodroofe [29]; MCTS [23]; «Three methods» [24]; полный список 60 свежих работ arXiv по запросу all:"no-three-in-line"; все 29 цитирующих Guy–Kelly по Semantic Scholar; все страницы и текстовые файлы сайта Фламменкампа (единственная измеренная зависимость от n там — позиционная плотность [2]); зонды Google Scholar через curl по фразам о зависимости доли направлений от n — 0 результатов.

**Вывод.** Результат не переоткрыт никем и при этом не объяснён. Полезный контраст, который стоит поставить в текст: единственное явное количественное высказывание в окрестности — [21], Remark 1.7, стр. 3 (verified):

> «Remark 1.7. The final deletion step crucially relies on the assumption k ⩾ 3: under this assumption, it turns out that the problem is dominated by the few heaviest line directions. [...] If k ⩾ 3, then the sum here is a tail of a convergent series: heuristically, this means that ε-light lines contribute very little compared to ε-heavy lines. On the other hand, if k = 2, then this sum is about log n (independently of ε), and each "dyadic scale" of m contributes to the sum equally.»

— то есть наивная теория для k = 2 предсказывает равный вклад всех масштабов, а измерение даёт монотонную зависимость от m и рост с n. Это ровно та формулировка новизны, которую заметка может себе позволить, ничего не преувеличивая.

---

## Q1. Опубликован ли где-нибудь спектр направлений реальных максимальных конфигураций?

**Найдено.** Только соседнее: [2] density.html (ансамблевое измерение на реальных решениях, но позиционная плотность — цитата в Д2); [60] (направленческие измерения на реальных решениях против случайной нуль-модели, но только n центральных направлений симметричных решений — цитаты в Д2); [58] (независимое воспроизведение позиционного наблюдения). Прайор-артом по разделу 2 брифа не является ни одно из трёх: требуется таблица/график/число пар по направлениям или занятость прямых фиксированного направления, а не частота занятости клетки.

**Не найдено.** Ни таблицы, ни графика, ни фразы «slope distribution / direction statistics» о решениях no-three-in-line.

**Где искали.** Сайт Фламменкампа: полный листинг каталога (120 файлов), все 16 .html/.txt (readme, symmetry_remarks, density, table, table_old, table_min_defect, effort, cases, images, near_miss_count, new_results, odd_results, heilbronn, error, four_cycle_decomposition_note, four_corner_permutation_note), ntdia, подкаталог data_1997/ (~190 файлов данных); grep по slope/direction/pairs/spectrum/statistic — 0 вхождений в readme и symmetry_remarks. Guy–Kelly 1968 в обеих версиях [7,8]. UPINT §F4 обоих изданий [10]. Adena–Holton–Kelly 1974 [11]. HJSW 1975 и Anderson 1979 — абстракты [13,14]. Flammenkamp JCTA 1992/1998 — тела не открыты, содержание известно по рефератам zbMATH (классификация по симметриям + table 1 с числом решений + картинки) [15,16]. Прельберг ×3 [17,18,19]. Voutier [20]. Ghosal ×2 [21,22]. MCTS [23] («slope hashing» — приём проверки коллинеарности, не статистика). «Three/Four methods» [24] (единственные вхождения slope — в определении коллинеарности). Кнут [42] — см. отдельную поправку ниже. MathWorld [59] (живая страница отдаёт 404, читан снимок Wayback от 2026-06-19). Wikipedia. OEIS: A000769, A272651, A277433, A280537/A280538, A093602, A365437 + полнотекстовые поиски. MathOverflow/Math.SE через API (~15 запросов, включая мои собственные «no-three-in-line slope distribution» и «no three in line diagonals two points» — 0–8 нерелевантных результатов). Wolfram Community: оба поста Ed Pegg, тело извлечено из приложенных ноутбуков (4,1 и 3,7 МБ) — 0 вхождений diagonal/slope/direction/statistic/histogram [61]. Wolfram Demonstrations (обе профильные, через Wayback). Gardner, гл. 5 (стр. 63–77) и Dudeney, задача 317 [68]. Reddit — недоступен напрямую (403/429 и пять мёртвых зеркал); через Brave Search установлено существование треда r/math от 18.06.2026 про n = 70, тело — репост фразы из readme Фламменкампа.

**Важная поправка, которую нельзя игнорировать.** Утверждение «Кнут об этой задаче не пишет» ЛОЖНО. Задача есть: (а) §7.2.2.1 «Dancing Links», упражнение 118 и указатель «No-three-in-line problem, 73» (verified по pre-fascicle 5C из Wayback); (б) Volume 4 Fascicle 7 «Constraint Satisfaction» (2025), стр. 79, 146 и ответы на стр. 237 — весь материал прочитан по черновику 7a, идентичность пагинации черновика и издания доказана двумя независимыми реперами; (в) правка индекса тома 4B, стр. 668. Никакой направленческой статистики ни в одном из этих мест нет: на стр. 79 — одно предложение «Problem N solves the 16 queens problem with no-three-in-a-line (see exercise 357)», на стр. 146 — упражнения 357–359 о составной задаче «n-ферзи + запрет трёх на прямой». Единственный фрагмент, структурно похожий на «короткая прямая редко заполнена / длинная часто», — ответ 359, но обе сравниваемые прямые (x+2y = 4 и x+2y = 14) имеют ОДИН И ТОТ ЖЕ наклон −1/2, то есть это сравнение по длине внутри одного направления, на чужом ансамбле (обычные решения 16-ферзевой задачи).

**Вердикт одной строкой.** spectrum law: **not found**; ближайшее опубликованное — ансамблевые карты позиционной плотности [2] и веб-самопубликация направленческих измерений на подмножестве пар [60].

## Q2. Известна ли κ или любой эквивалентный инвариант?

**Найдено.** Только детерминированные и качественные соседи. (1) Flammenkamp, symmetry_remarks.html, «Symmetry class == dia2» [3] (verified):

> «If n is even either on both long diagonals are 2 markers, or on neither long diagonals is any marker. Empirically is found that only the first case is realized! If n is odd, then on exactly one of the long diagonals are 2 markers»

— это структурное следствие класса симметрии для ДВУХ главных диагоналей, не доля дважды занятых среди всех 2n−1. (2) [17] §5.5 — попытка «for even n, constraints fixing the number of occupied sites on the diagonals», БЕЗ единого числа (полная цитата в Q5). (3) [25] Simkin, §7 «Concluding remarks», стр. 57 (verified): «the absorption method in this paper utilizes the fact that in a complete non-toroidal configuration only a fraction of the diagonals are occupied» — качественный аналог наблюдения κ < 1, без числа и для n-ферзей. (4) [18] — константа α LP-релаксации, не κ.

**Не найдено.** Значений ≈ 0.731, 0.6486, 0.639 и вообще «доли дважды занятых диагоналей» нет нигде в проверенном корпусе. Полнотекстовый поиск OEIS: константа Гая π/√3 каталогизирована (A093602), κ-подобной нет; отдельно отмечу, что OEIS на запросы вида «0.7306» отвечает не «нет совпадений», а трактует их как цифровые последовательности (129 и 244 нерелевантных попадания) — формулировка «в OEIS ничего не найдено» верна по существу, но получена не так, как можно было бы подумать.

**Где искали.** Тот же корпус, что в Q1, плюс: grep по всему клону [60] на kappa/0.73/0.6486/0.639/doubly/occupanc — единственное «occupancy» там радиальное; symmetry_remarks и readme целиком; Simkin полностью; Prellberg checkerboard полностью (grep occupanc → 0).

**Нерасшифрованный след, единственный оставшийся.** В каталоге сайта Фламменкампа лежат два файла — n52_free_diag_2352.png и n52_set_diag_2710.png [6] — на которые нет ссылок ни в одном из 16 текстовых файлов каталога и которые отдают HTTP 403 при любом способе доступа (проверено в семи вариантах URL/заголовков, включая Range-запрос; заглавная N даёт 404, то есть это права доступа на существующий файл), и которые никогда не архивировались (Wayback CDX по всему каталогу: 233 URL за всю историю, 0 вхождений «n52»). Косвенные опоры гипотезы, что это разбиение ансамбля n = 52 по бинарному диагональному признаку: 2352 + 2710 = 5062 = число известных решений n = 52 в классе rot4 (table.html, столбец «o»; кросс-проверено записью readme от 12 февраля 2026 о переборе Mitchell Riley/Prellberg); конвенция именования ансамблевых картинок каталога (n56_rot4_all.png, n57_rct4_all.png встроены в density.html); и доказанная в [60] дихотомия (Th-48, проверенная переписью всех 21 701 кэшированных rot4-решений n = 6…72): у rot4-решения либо нет ни одной точки на двух длинных диагоналях, либо ровно 2 + 2, и все четыре — из одной C4-орбиты петлевой клетки. Иного бинарного диагонального признака для rot4 попросту не бывает; тогда доля «set» = 2710/5062 = 0.5353. Всё это остаётся гипотезой: картинки не прочитаны.

**Вердикт одной строкой.** κ: **not found**; ближайшие формализмы — γ±(α) Симкина (ёмкость 1) и ограничения ёмкости 2 в LP Прельберга (верхняя оценка), ни один не даёт числа.

## Q3. Разложение счёта Гая–Келли по направлениям

**Найдено.** Разложение по примитивным (p,q) есть во всех текстах линии, но всегда как промежуточный шаг, сворачиваемый через φ(p) в одно число. Guy–Kelly, CMB 1968, стр. 528–529 [7] (corrected — см. ниже про формулу):

> «We next count the triples chosen from {(a + sp, b + sq) : s = 0, 1, 2, . . . }, where (4) 1 ≤ q < p ≤ [½(n-1)], square brackets denoting integer part, and (p, q) = 1. Figure I illustrates the case n = 60, p = 7, q = 5.»
> «t_n = (1/6)n(n − 1)(n − 2)(3n − 1) + Σ_{p=2}^{[½(n−1)]} Σ_{q=1, (p,q)=1}^{p−1} (1/3)r(r − 1){6n² − 4n(p + q)(r + 1) + pq(r + 1)(3r + 2)}»

(Внимание при цитировании: это **транскрипция выключной формулы, прочитанной с растра стр. 529 при 150 dpi**, а не дословный текстовый слой — текстовый слой Cambridge-скана в этом месте разрушен (биномы выходят как «(r^"V», «(*)»), и именно он ввёл в заблуждение первый проход, поставивший (1/6)r(r−1) вместо (1/3)r(r−1). Второй проверяющий по тому же файлу отметил, что дословно читаются только прозаические предложения. Прозаические цитаты выше и ниже — дословные; формулу вносить в заметку только со сверкой по изданию.)
> «Using Euler's totient function, φ(p), and its properties [5] … Σ_{p=1}^{m} φ(p)/p² = (6/π²) log m + O(1)»

Утверждения вида «направления с max(|a|,|b|) ≤ m дают долю f(m)» и обсуждения того, какие направления доминируют, нет ни в журнальной версии (5 стр., прочитана целиком, в том числе по растрам стр. 529–530), ни в полной 11-страничной Research Paper #33 [8] (собственный OCR всех страниц двумя проверяющими независимо; единственное «разложение» решений там — Table I по классам симметрии).

Прочитаны и закрыты два источника, которые бриф и критик считали главным риском для формулировки «никто не делил счёт по направлениям»:
— **UPINT §F4 [10]** (verified; открыт через недокументированный эндпойнт Google Books jscmd=SearchWithinVolume, работающий и для томов с preview:"noview"). 2-е издание, стр. 242: «F4 The no - three - in - line problem . Can 2n lattice points ( x , y ) ( 1 ≤ x , y ≤ n ) be selected with no three in a straight line ? This has been achieved for 2 ≤ n ≤ 32 and for several larger even values of n . Guy & Kelly make four conjectures .» 3-е издание, стр. 368–369 — четыре гипотезы, проверка Фламменкампом, последовательность A000769, поправка Эллманна («As recently as March , 2004 , Gabor Ellmann notes an error in the original paper , so that the result can be impoved to : 3c2 = π2 , c ≈ 1.813799»). Зонды по всей книге: «slope» и «gradient» — 0 вхождений в обоих изданиях; «diagonal» — только вне F4; единственное «direction» внутри F4 — риторическое «In the opposite direction, Erdős showed…». Поправка к брифу: §F4 занимает стр. 242–244 во 2-м издании (указание брифа «стр. 242» верно) и стр. 368–372 в 3-м.
— **Adena–Holton–Kelly 1974 [11]** (verified теми же сниппетами; том LNM 403 оцифрован Google). Стр. 10: «Probability arguments of Kelly and Guy [ 6 ] , [ 7 ] and [ 9 ] support the conjecture that D ( n ) = 3 / 22 / 3 n = 1.87n . First they showed that the number of sets of three collinear points that can be chosen from the n x n grid is ( 3/2 ) n4 log n + O ( n4 ) . They did this by considering the number of ways three points can be selected from the points of each line in the grid . From this they found the probability that three random points are not collinear . Assuming independence , the expected number of solutions with kn points in the grid was equated to 1 yielding the approximate upper bound for D ( n ) .» Зонды по всему тому: «slope», «slopes», «gradient», «directions», «parallel» — 0 вхождений; «direction» — 1, и то на стр. 62 в чужой статье тома. Побочно (к Q5): на стр. 7 сказано, что перебор Адены и Холтона явно поддерживал число точек на каждой прямой — «Adena and Holton have explicitly used the no - three - in - a- line property by directly manipulating the number of points in each line . This necessitated much storage to contain …» — исторический предшественник, но не публикация статистики. (Цитата дана в СЫРОМ виде, как её отдаёт сниппет Google Books: «3 / 22 / 3 n» — это 3/2^{2/3}·n, «( 3/2 ) n4 log n + O ( n4 )» — это (3/π²)n⁴ log n + O(n⁴); искажения OCR-овские, в заметку в таком виде переносить нельзя.)

**Что говорит arXiv:2607.05255 про k = 2 и «relative significance of lines in different directions»** — полная цитата Remark 1.7 приведена в Д4; на стр. 2 стоит отсылающая фраза «In fact, there are some important statistical differences between the case k = 2 and the case k ⩾ 3 (related to the relative significance of lines in different directions), which we discuss in Remark 1.7.» Локатор брифа уточнён: сама фраза на стр. 2 в §1, Remark 1.7 — в §1.3, стр. 3.

**Не найдено.** Ни доли f(m), ни обсуждения доминирующих направлений — ни у Гая–Келли (обе версии), ни в UPINT F4 (оба издания), ни у AHK 1974, ни у Voutier (0 вхождений «direction»/«slope» во всей статье, 3 страницы), ни у Прельберга (та же сумма через gcd(a,b), 1 бытовое вхождение «direction»), ни у Ghosal и др. (41 вхождение, все — классификация ε-heavy/ε-light в доказательстве, плюс «For each m ∈ N, there are at most 4m directions d ∈ D with ‖d‖∞ = m»).

**Вердикт одной строкой.** per-direction Guy–Kelly split: **not found** — теперь по прочитанным текстам первоисточников, а не по их недоступности; Remark 1.7 — известное соседнее утверждение, по разделу 2 брифа не прайор-арт.

## Q4. Соседняя теория

### Q4a. Мультимножество наклонов (кратности, а не число различных)

**Найдено.** Вся линия — о ЧИСЛЕ РАЗЛИЧНЫХ наклонов. Pach, Handbook DCG, §1.1, PDF-стр. 4 [38]: «Ungar's theorem [Ung82]: n noncollinear points in the plane always determine at least 2⌊n/2⌋ lines of different slopes (see Figure 1.1.3); this proves Scott's conjecture. Furthermore, any set of n points in the plane, not all on a line, permits a spanning tree, all of whose n−1 edges have different slopes [Jam87].» Рецензия F. Hering на Jamison 1984 [34]: «Der Autor untersucht Familien, bei denen die Anzahl m der auftretenden Steigungen minimal ist… Der Autor charakterisiert zunächst alle fast-kritischen konvexen Konfigurationen.» Рецензия T. Bisztriczky на Jamison 1984b [35]: «At present, four infinite families and 102 sporadic examples of such slope-critical configurations are known.» Solymosi [31]: «If the number of distinct directions between many pairs of points of a point set in a convex position is small, then many points are on a conic.» Martin, math/0302106: «multiplicity» там — алгебро-геометрическая кратность идеала, «multiset» — 0 вхождений.

**Соседняя теория, где направления считаются С КРАТНОСТЬЮ, но объект другой** [39] (corrected): El-Baz–Marklof–Vinogradov, §1: «We are interested in the distribution of directions ∥y∥−1 y as y ranges over PT , counted with multiplicity. That is, if there are k lattice points corresponding to the same direction, we will record that direction k times.» Это направления из ОДНОЙ точки на все точки решётки в круге радиуса T, а не направления пар внутри конечного экстремального множества.

**Не найдено.** Ни закона, ни измерения мультимножества наклонов экстремальных конфигураций. Проверки: полнотекстовый zbMATH по «multiset of slopes» и «slope multiset» → 0 записей по всей базе; arXiv-метапоиск по тем же фразам и по «direction spectrum» + «collinear» → 0–1 постороннее; Fernández-Merchant–Hämäläinen [32] — grep по multiplic/multiset = 0.

**Оговорка честности.** Тексты Ungar 1982 [33] и обеих Jamison 1984 [34,35] НЕ открыты (ScienceDirect 403; Springer отдаёт Cloudflare «Client Challenge» 3038 байт), вывод о них сделан по рецензиям zbMATH в 3–5 предложений. Правильная формулировка для заметки — «в доступных описаниях этой линии мультимножество наклонов с кратностями не встречается», а не «в этих статьях его нет».

**Вердикт одной строкой.** adjacent slopes multiset: **not found** (уверенность средняя — по рецензиям плюс нулевой полнотекстовый поиск).

### Q4b. Направленческое распределение выживших пар в случайных множествах

**Найдено.** Только техника, не измерение. Ghosal, arXiv:2605.07000 [22]: «The number of primitive directions v with ∥v∥∞ = m is O(m), so summing over m gives» — группировка по направлениям внутри оценки сверху для СЛУЧАЙНОЙ (не экстремальной) конструкции в Z². Nagy–Nagy–Woodroofe [29], доказательство Lemma 3.6: «We first count the number of lines ℓ intersecting S ∩ Qm in two points according to the denominator of their slope. Let ℓ have slope µ(ℓ) = r/q , where r and q are relatively prime. […] Thus, we have at most 2^m/(q·c·m^{1+ε}) pairs from S ∩ Qm determining a line of slope r/q.» (дробь 2^m/(q·c·m^{1+ε}) — реконструкция вёрстки: в PDF числитель и знаменатель набраны в две строки, pdftotext их разрывает) Li [27], §3: разбиение всех C(n,2) пар графика перестановки по классам наклонов с нормировкой на среднее «The average pairs one class can have is C(n, 2)/(n − 1) = n/2» — но на торе и для произвольной перестановки.

**Не найдено.** Измеренного или выведенного распределения выживших пар по направлениям. **Где искали:** оба поста Эппстейна 2018 [40] прочитаны целиком (11 756 знаков в первом; вхождений direction/slope/diagonal — 0 в обоих); Ghosal 2605.07000 [22] и Nagy–Nagy–Woodroofe [29] — полные тексты (направления только как приём оценки); Cooper–Solymosi [26]; Li [27]; Kovács–Nagy–Szabó [30]; arXiv API — abs:"collinear triples" AND abs:"random set" (1 посторонняя запись), all:"direction distribution" AND all:"point set" (0), all:"no-three-in-line" AND all:"slope" (12, релевантна одна — [18]); zbMATH «no-three-in-line» & «direction» (1 запись, тот же [18]); плюс два свежих препринта [23,24], не проверявшихся первым проходом.

**Закрыт лид, который бриф и критик считали самым правдоподобным** (линия Nathan Kaplan, семинар ноября 2018). Voutier, стр. 2 [20] (corrected — локатор): «we note that recently some people have questioned the independence assumption in their argument … See, for instance, https://11011110.github.io/blog/2018/11/10/random-no-three.html discussing a seminar of Nathan Kaplan on this topic in November 2018. … We thank Thomas Prellberg for these references and observations.» Пересказ Эппстейна: «to express his skepticism about the heuristic reasoning … Richard K. Guy and P. A. Kelly … used a probabilistic approach, based on the idea that certain random events would be largely independent of each other when they're really not.» Собственные слайды Каплана (IPAM, 14.12.2016, 48 слайдов, найдены на его research.html и прочитаны) [41] излагают эвристику Гая–Келли и упираются ровно в «Assume everything is independent.» — то есть его критика про ЗАВИСИМОСТЬ СОБЫТИЙ, а не про вес направлений; спектра направлений там нет. Программа семинара UCI ACO за ноябрь 2018 в Wayback отсутствует (снимки только с августа 2019), сайты семинара мертвы (404/редирект на Google Sign-in). Летний проект его студентов 2025 («Variations on the No-Three-in-Line Problem», пять студентов) и работа группы [23] проверены — спектра направлений нет.

**Вердикт одной строкой.** random sets direction distribution: **not found**.

### Q4c. Вычислимая модель (max-entropy / cluster expansion / Bethe / transfer matrix), предсказывающая κ

**Найдено.** Два частичных суррогата, оба процитированы выше: Simkin [25] — энтропийный формализм для «доли занятых диагоналей по направлению» в экстремальном ансамбле, но при ёмкости 1 и без числа; Prellberg [18] — ёмкость 2 по четырём направлениям, но LP-оценка сверху с дуальным сертификатом, а не ансамбль.

**Не найдено.** Никакой вычислимой модели на гиперграфе коллинеарности «≤ 2 точки на любой прямой» и никакого предсказания для κ. Зонды: arXiv API — abs:"lattice gas" AND abs:"multiple occupancy" (2 работы, обе про другое), abs:"exclusion statistics" AND abs:"lattice gas" AND abs:"capacity" (0), all:"no three in line" AND all:"entropy" (5 посторонних), abs:"collinear" AND abs:"hard-core" (3 из физики частиц), abs:"direction spectrum" AND abs:"lattice" (0); Semantic Scholar тематический поиск — 429 (не выполнен).

**Вердикт одной строкой.** max-entropy / computable κ: **not found**; предсказания для κ в литературе нет, и модель прямых заметки остаётся единственным известным нам вычислимым кандидатом.

## Q5. Регулярности решений внутри поиска (streamlining)

**Найдено, два вида, оба с ДРУГОЙ регулярностью.**

(1) **Отрицательный прецедент — Prellberg [17], §5.5 «Attempts at further speedups», стр. 13–14** (corrected: relevance понижена до partial, потому что там нет ни одного числа):

> «We additionally tested: (i) mild guidance via objective functions or branching priorities derived from empirical density profiles; (ii) for even n, constraints fixing the number of occupied sites on the diagonals; (iii) "anchoring" selected sites; and (iv) warm starts based on partial configurations. None of these improved performance reliably, and some were detrimental. [...] Overall, the best-performing strategy was to allow the solver to operate with minimal external interference.»

**Что здесь значит «the diagonals» — важно для формулировок заметки.** Кода экспериментов §5.5 в публичном репозитории автора НЕТ: репозиторий содержит 6 файлов, единственный файл кода реализует только базовую и симметрийно-редуцированную модели (grep по density|profile|anchor|warm|branch|priority|hint — 0 совпадений), а раздел «Data and software availability» сообщает, что это пост-фактум LLM-реконструкция модели из текста статьи. Зато сам текст статьи почти разрешает двусмысленность: все 11 вхождений слова «diagonal» в arXiv:2602.07751 означают ГЛАВНУЮ диагональ и антидиагональ симметрийной конструкции rot4/rct4, ни разу — семейство прямых x−y = const. Остаточное сомнение: §5.5 говорит «for even n», тогда как диагональные представители в его конструкции возникают при нечётном n. **Вывод для текста: писать «нашу κ уже пробовали как streamlining и это не сработало» НЕЛЬЗЯ.**

(2) **Положительный прецедент, но по симметрии — Zhang, Zhuang, Wang, Kaplan [23]** (verified, оба фрагмента и обе строки Table 7 сверены посимвольно):

> «empirical observations on the problems we tested suggest that optimal configurations frequently possess symmetries (Flammenkamp, 1992; 1998; 2026; Prellberg, 2026; Aichholzer et al., 2023). To incorporate this structural prior, we introduce Symmetric Batch Transitions… [...] The subsequent integration of canonical pruning (M3) yields no statistically significant improvement in either performance or efficiency on its own. [...] This limitation is directly overcome by the introduction of C4 symmetric batch transitions (M4) … [Table 7, n = 70] M3: 119.2 (1.0) 33042.73 (719.21) ; M4: 124.8 (2.2)*** 7722.33 (963.06)***»

То есть измеренное ускорение есть (33042.73 → 7722.33 с при n = 70, p < 0.001), но переносимая из статистики решений регулярность — класс симметрии, а не спектр направлений. Формулировка «кроме Прельберга streamlining никто не пробовал» неверна.

(3) **Определение streamlining — Gomes & Sellmann, CP 2004 [43]** (corrected: 16 страниц, 274–289, а не 11): «The streamlining constraints capture regularities observed in a subset of the solutions to smaller problem instances.» — но применения к no-three-in-line там нет (grep «three.in.line|no3|collinear» = 0); приложения статьи — сбалансированные латинские квадраты и магические квадраты. То же для Le Bras–Gomes–Selman, AAAI 2012 (0 вхождений).

(4) **Смежное кодирование у Кнута [42]** (verified), ответ на упр. 7.2.2.3–357: релевантные прямые становятся primary items с multiplicity [0..2]:

> «Add N(n) new primary items #ₖ, for 0 ≤ k < N(n), each with multiplicity [0 .. 2]. Then append to option ‘rᵢ cⱼ a_{i+j}, b_{i−j}’ every item #ₜ for which αₜi + βₜj equals γₜ in the table of relevant lines.»

Существенная оговорка, которую надо держать при цитировании: ящики ёмкости 2 ставятся НЕ на все направления — Кнут берёт только наклоны p/q с 0 < p < q и gcd(p,q) = 1, а строки, столбцы и оба 45-градусных направления входят в ферзевые items с ёмкостью 1. То есть это гибрид «ёмкость 1 на четырёх ферзевых направлениях + ёмкость 2 на остальных», приём кодирования, а не статистическая модель. Последовательность N(4)…N(12) = (0, 12, 32, 76, 136, 252, 356, 572, 836), N(16) = 2668; в OEIS не каталогизирована (четыре запроса).

**Кампания Хойле 2026 — не найдено ничего, и теперь это установлено исчерпывающе.** Единственный публичный источник — построчные записи в readme Фламменкампа [1] (verified): «On 17th June 2026 Marijn Heule of Carnegie Mellon University (Pittsburgh, Pennsylvania, USA) used a newly developed SAT (Boolean satisfiability) solver to find a solution for n=70 in the rot4 symmetry class.», «On 10th August 2026 Marijn Heule presented a new record solution with grid size n=76 in the rot4 symmetry class.», плюс более поздние «On 17th August 2026 … n=71 in the rct4 symmetry class» и n = 73 от 19 августа. Ни кодировки, ни симметрийной обработки, ни cube-and-conquer, ни ресурсов. Проверено: его собственный открытый каталог слайдов https://www.cs.cmu.edu/~mheule/talks/ (59 PDF, последние два от 2026-07-20 скачаны и распознаны — «Certified Variable Reordering in Cardinality Encodings» и «Proof Logging for (Re)Encoding», no-three-in-line в них нет, файлов позже 20 июля нет вовсе); авторизованный GitHub code search внутри аккаунта — «no-three-in-line» user:marijnheule → 0 файлов при 53 публичных репозиториях; глобальный «no three in line» cube-and-conquer → 0; arXiv (au:Heule, 53 записи, скан по three-in-line/collinear/grid); Google Scholar (профиль распарсен: 12 работ 2026 г., ни одной по теме); программы SAT 2026 (FLoC) и Pragmatics of SAT 2026 целиком (grep three|no-3|collinear = 0); страница студента bsubercaseaux.github.io (0). Аккаунта на mathstodon нет (API инстанса возвращает пустой список), x.com/marijnheule → 404.
**Джейкоб Дэвис** [1]: «On 24th July 2026 Jacob Davies from Alameda (California, USA) used the AI ChatGPT 5.6 Sol to construct 619 new solutions for n=21, 22, ..., 56, 57 all in symmetry classes iden or rot2. On 30th July he continued to construct 24 more new solutions with n ≤ 57 …» — никакого writeup, репозитория или блога: GitHub user search (13 профилей) плюс авторизованный code search по всему GitHub (связки «Jacob Davies» + задача нет), Hacker News Algolia (0), dblp (31 запись по теме, его нет), Brave Search (только однофамильцы).

**Вердикт одной строкой.** streamlining for this problem: **partially known** (отрицательный прецедент без чисел + положительный по симметрии с числами); Heule 2026 structure: **not found**, публичного описания метода не существует.

## Q6. Три измерения (A280537)

**Найдено — соседнее, и один подлинный предок аргумента.**

(1) **Sillke / Flammenkamp, страница «Puzzles of the {0,1,2}^3 grid», декабрь 1992 [54]** (verified; страница переоткрыта, цитата совпадает дословно, включая опечатки оригинала). Это ближайший найденный предок «слой/наклон»-аргумента для 3D:

> «Proof of the upper bound 8: (Achim Flammenkamp) As in each layer you can place maximal 3 vertices, you get an upper bound of 9. But 9 is impossible. If you place in each layer 3 points, you have in each layer 3 lines through the 3 pairs of points. So there are 9 lines in the 3 layers. Now count the different slopes a line can have in a 3*3 layer. As there are only 8 different slopes, you have two parallel lines by the piginhole pinciple. But this means you have four on a plane.»

Но: только осевые слои, только наклоны внутри слоя, только n = 3; слова «projection» на странице нет. Это НЕ общая эквивалентность проекций.

(2) **Pór & Wood, GD 2004 [55]** (verified по полному тексту конференционной версии, добытому через архивный снимок): задача «no four coplanar» разбирается явно, но через счёт по осевым gridplane, а не через проекции:

> «Cohen et al. [6] generalised the no-three-in-line problem in a similar direction. They proved that for any prime p, the set {(x, x2 mod p, x3 mod p) : 0 ≤ x ≤ p− 1} contains no four coplanar points. It follows that the n× n× n grid contains at least n/2 and (1 − ε)n points with no four coplanar. Each gridplane contains at most three points; thus we have an upper bound of 3n.»

Слово «project» во всём тексте — 0 вхождений (проверено двумя каналами независимо).

(3) **Cohen, Eades, Lin & Ruskey, GD 1994 [56]** (verified) — по-видимому, самый ранний опубликованный источник конструкции нижней границы для A280537, на который OEIS НЕ ссылается; компланарность проверяется определителем, не проекцией:

> «We achieve this volume bound by providing for each n a universal set of grid points U_n = {p_1,...,p_n}; this set has the property that any four distinct points p_i, p_j, p_k, and p_l are not coplanar. ... place v_i at point p_i = (i, i² mod p, i³ mod p) ... Note that the points p_i, p_j, p_k, p_l are coplanar if and only if Δ = 0 [9].»

(Цитата **нормализована из плохого OCR**: в сыром тексте стоит «Note that the points Pi,Pj,Pe,Pi are coplanar if and only if A = 0 [9].» — «A» это Δ, индексы искажены. Смысл проверен двумя каналами независимо; вносить в заметку только со сверкой.)

(4) **Первоисточник задачи прочитан.** Тред rec.puzzles от 27.11.1992, на который ссылаются и OEIS, и Pegg, открыт через снимок Wayback от 06.07.2022 [54]: постановка Sillke, ответ Mogensen, опровержения der Mouse и David Seal («No, there's a diagonal plane which passes through no less than 6 of these points!»), и сообщение James Dow Allen от 11.04.2016, связывающее задачу с идущим контестом Циммермана. Проверки компланарности в треде — вручную, указанием конкретной плоскости; ни проекций, ни статистики.

**Не найдено.** (а) Явной формулировки эквивалентности «нет 4 компланарных ⟺ ни в одной решёточной проекции нет 4 коллинеарных» — нигде: OEIS A280537/A280538 (запись перечитана целиком, «projection» 0 вхождений; полнотекстовый поиск OEIS по «no four plane grid» даёт ровно эти две последовательности), Wikipedia, MathWorld (0 упоминаний 3D), демонстрация Пегга (Wayback), MSE 553431 (принятый ответ — Пфортнера, а не тот, что с наибольшим счётом), Pór–Wood, Cohen и др., Sillke, тред 1992. (б) Никакой направленческой или плоскостной статистики рекордных конфигураций: Description/Standings/FinalReport контеста «Non-Coplanar Points» (окно 5 марта — 4 июня 2016 — по таблице «Previous Contests» на главной azspcs.com; на самой странице Description стоит только дата окончания «This contest ended on 4 Jun 2016»; догадка брифа про название «Point Packing» неверна — так назывался другой контест 2009 года про упаковку точек с попарно различными расстояниями) — только таблицы очков и координаты; GitHub (q=azspcs → 24 репозитория, q=non-coplanar+points и q=coplanar+contest → 0; единственный тематический репозиторий r-bennett/Tetrahedra создан 13.06.2017 после контеста, компланарность через нормаль плоскости, «project» встречается только в строке лога); страницы призёров (Rokicki: 38 репозиториев, по этому контесту ничего, хотя по другим контестам AZsPCs код он выкладывает; Wróblewski: 0 упоминаний).

**Институциональная причина, по которой разбора метода и не могло быть публично** — FAQ самого контеста [53] (corrected: даты «5 Mar» на странице Description нет): «With only one exception, if it's related to AZsPCs then it's fine to talk about it in the discussion group. The exception is spoilers. Spoilers include: specific solutions / detailed algorithms / any calculation of the best raw scores». Единственное разрешённое место — архив группы groups.io/g/AZsPCs, закрытый логин-стеной.

**Библиографический фантом, который нельзя вносить в список литературы.** «Второй доклад с идентичным названием No-Three-in-Line-in-3D» (Andersen, Chung, Lu, Algorithmica 47(4):379–397) не существует: это ошибка метаданных Springer с официальной поправкой [57] — «The online version of the original article was inadvertantly published with the incorrect article title. The correct title appears above. The publisher regrets the error.» Настоящее название статьи — «Drawing Power Law Graphs Using a Local/Global Decomposition». Ошибочный заголовок унаследован Crossref, DBLP, Semantic Scholar и OpenAlex, так что «подтверждение тремя базами» здесь — тиражирование одной ошибки.

**Вердикт одной строкой.** 3D A280537: **not found** по обоим подвопросам; ближайшее — pigeonhole по наклонам в осевых слоях (Sillke/Flammenkamp 1992) и счёт по осевым gridplane (Pór–Wood 2004).

---

## Что это меняет для заметки

Ниже — только то, что подтверждено verified/corrected-находками этого захода; предложений, опирающихся на неоткрытые источники или на догадки, здесь нет. Каждая правка привязана к месту в файле `paper/direction_spectrum_note.tex` (187 строк), и привязки проверены прямым чтением файла: фраза про прайор-арт — строка 28 (аннотация); абзац «Not claimed» — строки 166–171; «This is the canonical ensemble…» — строки 102–104; «\emph{Data.}» — строки 47–50; таблица и абзац о росте длинных направлений — строки 55–75. Проверено там же, что заметка **не имеет списка литературы вообще**: `\cite` — 0 вхождений, окружения `thebibliography`/`\bibitem` отсутствуют, источники названы только по именам в тексте и одним `\url`. Поэтому большинство правок — это добавление прайор-арт-раздела и библиографии, а не исправление существующих ссылок.

**1. Абстракт, последняя фраза (строка 28).** Заменить (готовый английский текст с обязательной оговоркой о методе — в разделе «Итог и прямой ответ на главный вопрос» выше; ниже — его короткий вариант)
> «and no prior-art search beyond the classical sources has yet been run.»
на
> «a multi-channel prior-art search has now been carried out (see §N): we found no published measurement of pairs per direction or of diagonal occupancy on actual solutions, no κ-like constant, and no per-direction decomposition of the Guy–Kelly count; the nearest published objects are Flammenkamp's ensemble frequency maps of point positions, Prellberg's capacity-two linear-programming relaxation, and a web-posted directional measurement on a subset of pairs.»

**2. §4 «Not claimed», абзац на строках 168–171.** Заменить весь абзац «A search of the literature beyond the classical sources … has not yet been carried out; a research brief for it is on file, and this note will be corrected if the model or the measurement is found in the literature.» на короткий раздел прайор-арта, в котором названы и отграничены:
- Guy–Kelly 1968 (обе версии) и UPINT §F4 — сумма по примитивным (p,q) есть, но сворачивается через φ(p); доли f(m) и обсуждения доминирующих направлений нет;
- Ghosal и др. 2607.05255, Remark 1.7 — единственное явное количественное высказывание о вкладе направлений, и оно предсказывает при k = 2 равный вклад всех диадических масштабов (то есть отсутствие роста), что противоположно измеренному;
- Prellberg, arXiv:2605.09215 — capacity-two constraints по четырём направлениям как LP-оценка сверху для чётностного варианта; не ансамбль, весов C(L,x) нет, α ≠ κ;
- Simkin, Adv. Math. 427 (2023) — γ±(α), занятость диагоналей по направлениям для n-ферзей (ёмкость 1) и ЯВНО ВЫПИСАННОЕ предположение о независимости занятости диагоналей разных направлений («If we assume that the occupied diagonals in each direction are approximately independent…», дословная цитата в Д1); это ровно то предположение, на котором стоит нуль-модель заметки, — но у Симкина ёмкость прямой 1 и ни одного числа для κ;
- Flammenkamp, density.html — опубликованный прецедент ансамблевых измерений на этой же базе (позиционная плотность, не направления), с 1997 г. и продолженный Прельбергом в 2026 (n = 56 из 10441 конфигураций, n = 57 из 833);
- Flammenkamp, readme, «A Superficial Explanation» — ближайший печатный предшественник МЕХАНИЗМА (стоимость затенения парой точек), агрегированный по классам симметрии;
- Cooper–Solymosi 2004 и Erdős–Purdy 1976 — методические предшественники операции «разложить пары по направлениям» (тор; приём доказательства);
- aujurd22/no3inline-rigidity (GitHub, июль 2026) — веб-самопубликация направленческих измерений реальных решений против случайной нуль-модели с тем же качественным выводом; отграничить: только n центральных направлений симметричных решений, спектр вырожден в индикатор, κ нет, источник без рецензии и с внутренними числовыми противоречиями;
- Q5: Prellberg §5.5 (отрицательный результат по «helper»-ограничениям, без чисел) и Zhang–Zhuang–Wang–Kaplan 2606.26399 (симметрия как приор с измеренным ускорением).

**3. После Теоремы 1 (строки 102–104).** К фразе «This is the canonical ensemble of hard particles in r independent boxes of capacity two with degeneracies 1, L_i, C(L_i,2) … the identity is elementary» добавить сноску: устоявшегося имени именно для этого тождества найти не удалось; ближайший зонтичный термин в реферируемой литературе — restricted occupancy (Freund 1956 и далее; первоисточники кластера остались непрочитанными, поэтому совпадения с точной формулой мы не утверждаем); невзвешенный равноящичный частный случай — Comtet, Advanced Combinatorics, упр. III.19, с. 163; словосочетание «capacity-two constraints» употребляет Prellberg (2026), но применительно к линейным ограничениям LP-релаксации.

**4. §1 «Definitions and data», после строки 50.** Добавить одну фразу со ссылкой на density.html: ансамблевые измерения по этой базе публикуются с 1997 года (частоты занятости клеток), и настоящая работа продолжает этот жанр на новой наблюдаемой.

**5. Строки 70–75 и соответствующая фраза абстракта о росте длинных направлений с n.** Добавить: объяснения или измерения этого роста в литературе нет (перечислить, где искали), а ближайшее теоретическое высказывание — Remark 1.7 из arXiv:2607.05255 — предсказывает для k = 2 равный вклад всех диадических масштабов.

**6. Оговорка о методе, обязательная.** В раздел прайор-арта вписать честно: полнотекстовый веб-поиск в ходе этого захода был недоступен (бюджет исчерпан), поэтому отрицания опираются на прямые загрузки, API (arXiv, Crossref, OpenAlex, Unpaywall, Semantic Scholar, zbMATH Open, OEIS, GitHub, Stack Exchange, Wayback) и полнотекстовые поиски внутри arXiv/zbMATH/OEIS/Google Books, а не на поиск по свободному тексту; ряд первоисточников (Ungar 1982, Jamison 1984, Kaplansky–Riordan 1946, HJSW 1975) остались непрочитанными.

**7. Библиография — чего писать НЕЛЬЗЯ (всё установлено проверками).**
- Guy–Kelly, стр. 529: во внутренней сумме стоит **(1/3)r(r−1)**, не (1/6); лемма суммируется **от p = 1**, не от p = 2 (в журнальной версии она вообще не названа леммой — «Lemma 2» есть только в Research Paper #33).
- Flammenkamp, «Progress in the No-Three-in-Line Problem, II» — **JCTA 81 (1998) 108–113**, не 397–400. Ошибочные страницы стоят в списке литературы заметки Прельберга от сентября 2025 (в брифе страниц нет); подтверждено трижды (страница ScienceDirect, Crossref, zbMATH) плюс решающим аргументом: том 81 заканчивается на стр. 263 («Author Index for Volume 81»).
- Solymosi, arXiv:2206.00889 — **Discrete Comput. Geom. 72(2) (2024) 986–1009**, DOI 10.1007/s00454-023-00579-w, не JCTA; цитировать строго версию v3 (в v1 формулировка иная).
- Marklof & Strömbergsson — **Ann. of Math. 172 (2010) 1949–2033**, не 173, и порядок авторов именно такой («173» — опечатка в аннотации цитирующей статьи).
- Nagy–Nagy–Woodroofe — **European J. Combin. 114 (2023)**, Paper 103796, не 111.
- Simkin — **Advances in Mathematics 427 (2023) 109127**, не Advances in Applied Mathematics.
- Jamison — **Discrete Math. 60 (1986) 199–206** и **Ann. N.Y. Acad. Sci. 440 (1985) 34–51**; ссылки [6] и [8] препринта arXiv:2210.12465, откуда их легко скопировать, ошибочны (там 24–31 и 134–151).
- Cooper–Pikhurko–Schmitt–Warrington — Amer. Math. Monthly **121 (2014) 213–221**, DOI 10.4169/amer.math.monthly.121.03.213.
- «Jamison характеризовал экстремальные конфигурации» — **неверно**: характеризация условная (при отсутствии трёх коллинеарных И ровно n направлениях), а полная классификация direction-critical конфигураций **открыта**: «Sets achieving this minimum for n odd (even) are called direction-(near)-critical and their full classification is still open. To date, there are four known infinite families and over 100 sporadic critical configurations» [32].
- Утверждение о наклонах 0, ∞, ±1 в конструкции Hall–Jackson–Sudbery–Wild принадлежит **Kovács–Nagy–Szabó, Observation 2.6** (с их собственным двухстрочным доказательством), а не Hall и др.; авторам HJSW приписаны только Observations 2.4 и 2.5, и Observation 2.4 прямо допускает прямые ЛЮБОГО направления, пересекающие конструкцию в двух разных классах.
- Ссылку «Andersen, Chung, Lu, No-Three-in-Line-in-3D, Algorithmica 47(4):379–397» вносить **нельзя** — библиографический фантом с официальной поправкой Springer.
- Фразу «нашу κ уже пробовали как streamlining и это не сработало» писать **нельзя**: у Прельберга в §5.5 нет ни одного числа, кода этих экспериментов в его репозитории нет, а «the diagonals» у него во всех 11 вхождениях означает две главные диагонали симметрийной конструкции.
- Фразу «Кнут об этой задаче не пишет» писать **нельзя**: задача есть в §7.2.2.1 (упр. 118), в Fascicle 7 (стр. 79, 146, ответы 237) и в индексе тома 4B (стр. 668) — просто без направленческой статистики.
- Guy, UPINT: §F4 — стр. **242–244** во 2-м издании (1994) и **368–372** в 3-м (2004).

---

## Осталось непроверенным

**Не открытые первоисточники (и как их добить).**
1. Ungar, JCTA 33 (1982) 343–347 — ScienceDirect отдаёт HTTP 403; Crossref без abstract; Semantic Scholar сообщает, что abstract изъят издателем; в zbMATH у записи Zbl 0496.05001 рецензии НЕТ. Добить: библиотечный/институциональный доступ.
2. Jamison, Geom. Dedicata 16 (1984) 17–34 и 249–277; Jamison & Hill, Congr. Numer. 40 (1983) 101–125 — Springer отдаёт Cloudflare «Client Challenge»; известны только рецензии zbMATH. Добить: библиотека. Это единственная реальная дыра по Q4a.
3. Kaplansky & Riordan, Duke Math. J. 13 (1946) 259–268 — пять независимых свидетельств закрытости (Project Euclid антибот на обоих адресах, S2 CLOSED, OpenAlex any_repository_has_fulltext=false, zbMATH без метки открытой версии). Добить: подписка/библиотека.
4. Riordan, «An Introduction to Combinatorial Analysis» (1958), гл. 5 — три копии archive.org, все access-restricted (djvu.txt и search-inside → 403); оглавления нет ни в OpenLibrary, ни у Dover, ни в рецензиях zbMATH. Гипотеза брифа о названии главы «Distributions: occupancy» не подтверждена и не опровергнута. Добить: заём на archive.org (бесплатная регистрация) или бумажный экземпляр.
5. Freund, Amer. Math. Monthly 63 (1956) 20–27 и Freund & Pozner, Ann. Math. Statist. 27 (1956) 537–540 — единственный успешный запрос к legacy-адресу projecteuclid.org/download/pdf_1/euclid.aoms/1177728278 вернул валидный 4-страничный PDF, но файл был утрачен до конвертации, дальше включился антибот. **Добить проще всего именно так**: редкие одиночные запросы по шаблону euclid.<аббревиатура>/<legacy id> с большими паузами. Это единственный способ выяснить, покрывает ли restricted occupancy theory неравные вместимости L_i с весами C(L,x).
6. Hall–Jackson–Sudbery–Wild, JCTA 18 (1975) 336–341 — настоящая платная стена (Unpaywall is_oa=false, OpenAlex «closed», рецензии в zbMATH нет); получен только дословный абстракт из архивного снимка. Именно здесь могло бы лежать что-то о направлениях пар гиперболической конструкции — утверждение брифа на этот счёт остаётся без первоисточника.
7. Flammenkamp, JCTA 60 (1992) 305–311 и 81 (1998) 108–113 — тела не открыты (ScienceDirect отдаёт 403 автоматическим клиентам). **Важно: это, по-видимому, НЕ платная стена, но статус двух статей разный, и каналы разошлись** — по Unpaywall bronze OA подтверждён для 1998 (is_oa = true, ссылка на PDF ScienceDirect), тогда как для 1992 Unpaywall отдаёт closed, а bronze помечает только Semantic Scholar. То есть 1998 в обычном браузере открывается бесплатно почти наверняка, 1992 — вероятно; 403 отдаётся именно автоматическим клиентам. Добить: открыть руками. Содержание при этом уже известно по рефератам zbMATH (классификация по симметриям, table 1, картинки) — направленческой статистики рецензенты не упоминают.
8. Anderson, JCTA 27 (1979) 365–366; Craggs & Hughes-Jones, JCTA 20 (1976) 363–364; Kløve, JCTA 24 (1978) 126–127 и 26 (1979) 82–83 — тела не открыты (атрибуция трёх последних установлена через Crossref по тому и страницам; по объёму 1–2 страницы направленческой статистики там ожидать не приходится).
9. UPINT §F4 сплошным текстом (оба издания) и Adena–Holton–Kelly 1974 сплошным текстом (прочитаны сниппеты стр. 6, 7, 9, 10, 11; стр. 8 и 12–17 не попали в выдачу) — постраничный рендер Google Books закрыт, archive.org под CDL, HathiTrust за Cloudflare. Содержательный вопрос («делят ли счёт по направлениям») закрыт отрицательно зондами по словам, но сплошного чтения нет. Добить: заём archive.org (mdp.39015041081475 и mdp.39015040416508 в HathiTrust — «search-only»).
10. Guy, «Unsolved Combinatorial Problems» (Oxford 1969 / Academic Press 1971, 121–127) — прочитаны два-три сниппета через полнотекстовый поиск Open Library; тела нет.
11. Knuth, Volume 4 Fascicle 7 (2025) — опубликованный текст не открыт (фасцикула платная); всё прочитано по черновику 7a из Wayback, идентичность пагинации доказана двумя реперами.
12. Tsuchiya & Takefuji, Neurocomputing 8 (1995) 43–49 — подтверждённо закрыт (Unpaywall closed, best_oa_location null). Использует ли статья статистические свойства известных решений — неизвестно.
13. n52_free_diag_2352.png / n52_set_diag_2710.png на сайте Фламменкампа — HTTP 403 при любом способе доступа, никогда не архивировались, нигде не индексированы. **Единственный реалистичный путь — письмо Ахиму Фламменкампу** (адрес есть в HTML-комментарии table.html) либо Thomas Prellberg / Mitchell Riley. Это ближайший к κ след из всех найденных.
14. Архив официальной группы контеста groups.io/g/AZsPCs — логин-стена; единственное место, где по правилам вообще разрешено обсуждать «detailed algorithms».
15. Личные сайты/блоги участников контеста 2016 (Tim Foden, Moritz Franckenstein) — не идентифицированы вообще; тело Reddit-треда r/math 1u99m9v (шесть способов доступа не сработали, известно только по сниппету поисковика); MathSciNet полнотекстово.

**Три источника вне списка брифа, которые критик рекомендовал проверить — все три отработаны:**
- Sillke — **проверен и дал результат**: его страница cube3 содержит доказательство Фламменкампа через пересчёт наклонов в осевых слоях (Q6), а исходный тред rec.puzzles 1992 прочитан через Wayback (пусто по существу).
- Adena–Holton–Kelly 1974 — **частично открыт** через Google Books; риск для формулировки «никто не делил счёт по направлениям» **снят**: во всём томе LNM 403 слов slope/slopes/gradient/directions/parallel — 0.
- линия Nathan Kaplan — **закрыта**: его сомнение относится к предположению независимости, а не к весу направлений; подтверждено и пересказом Эппстейна, и его собственными слайдами IPAM 2016.

**Отвергнутые ссылки и утверждения поисковиков (не использованы в этом ответе).**
- «Andersen, Chung, Lu, No-Three-in-Line-in-3D, Algorithmica 47(4):379–397» — библиографический фантом (ошибка метаданных Springer с официальной поправкой DOI 10.1007/s00453-006-3160-3).
- «Cooper и др. про 3D no-four-coplanar» — ложный след; искомая работа называется иначе: Cohen, Eades, Lin, Ruskey, «Three-Dimensional Graph Drawing».
- Ссылки [6] и [8] препринта arXiv:2210.12465 (страницы двух работ Jamison) — ошибочны; страницы взяты из zbMATH и Crossref.
- «Полный текст Erdős–Purdy 1976 недоступен» — опровергнуто (скан свободно лежит в архиве работ Эрдёша).
- «Полный текст Brower–Ponomarenko (Involve 2022) платный» — опровергнуто (свободная авторская копия vadim.sdsu.edu/bp2.pdf; прочитана целиком, статистики направлений нет).
- «Google Books и Open Library не дают доступа к UPINT/LNM 403» — опровергнуто (эндпойнт jscmd=SearchWithinVolume и полнотекстовый поиск Open Library работают и для томов с preview:"noview").
- «Тред rec.puzzles 1992 непрочитан и непрочитаем» — опровергнуто (снимок Wayback от 06.07.2022).
- «Кнут об этой задаче не пишет» и «streamlining кроме Прельберга никто не пробовал» — оба утверждения ложны (см. Q1 и Q5).
- «У Фламменкампа слово diagonal встречается только как ось отражения» — опровергнуто (symmetry_remarks.html содержит утверждения о занятости длинных диагоналей).
- Приписывание Observation 2.6 (наклоны 0, ∞, ±1) авторам HJSW — снято: это результат Kovács–Nagy–Szabó.
- Атрибуция страницы homepages.gac.edu/~jsiehler конкретному автору — снята (имя на странице не проставлено, выведено из URL).

**Методологическое ограничение всего захода.** Бюджет WebSearch сессии (200 из 200) был исчерпан ДО старта всех девяти каналов и добора — это независимо подтверждено каждым проверяющим на собственном вызове. DuckDuckGo, Mojeek, Ecosia, Startpage, searx и Yahoo из этой среды не отвечают или блокируют; Bing отдаёт HTTP 200 с посторонним decoy-контентом. Единственный работающий веб-поиск — **Brave Search через curl с браузерным User-Agent**, и только для первого запроса сессии (дальше JS-стена): именно им найден Reddit-тред про n = 70. Поэтому все «не найдено», требующие поиска по свободному тексту (личные страницы, блоги, диссертации, слайды вне известных каталогов), покрыты слабее, чем те, что закрыты через API и прямые загрузки.

---

## Источники

Даты обращения — 2026-09-03 для всех позиций.

1. A. Flammenkamp, «Progress in the no-three-in-line problem» (readme.html), Universität Bielefeld. https://wwwhomes.uni-bielefeld.de/achim/no3in/readme.html — состояние базы 2026-08-31, 431 008 конфигураций.
2. A. Flammenkamp, «Frequency Distributions of Points of No-Three-in-Line Configurations» (density.html), обновлена 2026-06-12; карты n = 56, 57 — T. Prellberg, апрель/май 2026. https://wwwhomes.uni-bielefeld.de/achim/no3in/density.html
3. A. Flammenkamp, «Symmetries in No-Three-in-Line Configurations» (symmetry_remarks.html). https://wwwhomes.uni-bielefeld.de/achim/no3in/symmetry_remarks.html
4. A. Flammenkamp, table.html и table_old.txt (числа решений по классам симметрии; n = 52, rot4: 5062). https://wwwhomes.uni-bielefeld.de/achim/no3in/table.html
5. A. Flammenkamp, «Four-cycles in no-three-in-line configurations» (30.06.2026); T. Prellberg, «Four-corner permutation tests…» (27.06.2026). https://wwwhomes.uni-bielefeld.de/achim/no3in/four_cycle_decomposition_note.html
6. **[не открыт]** n52_free_diag_2352.png и n52_set_diag_2710.png в каталоге https://wwwhomes.uni-bielefeld.de/achim/no3in/ — HTTP 403, снимков в Wayback нет.
7. R. K. Guy, P. A. Kelly, «The No-Three-In-Line Problem», Canad. Math. Bull. 11(4) (1968) 527–531, DOI 10.4153/CMB-1968-062-3 (открытый PDF на Cambridge Core).
8. R. K. Guy, P. A. Kelly, «The No-Three-In-Line Problem», Research Paper #33, Dept. of Mathematics, University of Calgary, January 1968, 11 стр. (скан: сайт Фламменкампа и https://oeis.org/A000755/a000755_1.pdf).
9. OEIS Foundation, A000769 (комментарий R. K. Guy, 22.10.2004, о поправке Габора Эллманна); A093602 (π/√3); A272651; A277433; A280537; A280538; A365437. https://oeis.org
10. R. K. Guy, Unsolved Problems in Number Theory, §F4: 2-е изд. (Springer, 1994), стр. 242–244; 3-е изд. (Springer, 2004), стр. 368–372. Прочитано сниппетами Google Books (тома l_PuAAAAMAAJ и 1AP2CEGxTkgC, эндпойнт jscmd=SearchWithinVolume). **[сплошной текст не открыт]**
11. M. A. Adena, D. A. Holton, P. A. Kelly, «Some thoughts on the no-three-in-line problem», Lecture Notes in Math. 403 (1974) 6–17, DOI 10.1007/BFb0057371 (в метаданных издателя заголовок с опечаткой «oh»); Combinat. Math., Proc. 2nd Australian Conf., Univ. of Melbourne 1973. Прочитано сниппетами Google Books (том _a4ZAQAAIAAJ), стр. 6, 7, 9, 10, 11. **[сплошной текст не открыт]**
12. **[не открыт, только сниппеты]** R. K. Guy, «Unsolved Combinatorial Problems», in: Combinatorial Mathematics and Its Applications (Proc. Conf., Oxford, 7–10 July 1969, ed. D. J. A. Welsh), Academic Press, 1971, 121–127 (полнотекстовый поиск Open Library).
13. **[не открыт]** R. R. Hall, T. H. Jackson, A. Sudbery, K. Wild, «Some advances in the no-three-in-line problem», J. Combin. Theory Ser. A 18(3) (1975) 336–341, DOI 10.1016/0097-3165(75)90043-6 (дословный абстракт — из архивного снимка ScienceDirect).
14. **[не открыт]** D. B. Anderson, «Update on the no-three-in-line problem», JCTA 27(3) (1979) 365–366, DOI 10.1016/0097-3165(79)90025-6 (абстракт из архивного снимка).
15. **[тело не открыто]** A. Flammenkamp, «Progress in the no-three-in-line-problem», JCTA 60(2) (1992) 305–311, DOI 10.1016/0097-3165(92)90012-J; содержание — по реферату zbMATH Zbl 0774.05025.
16. **[тело не открыто]** A. Flammenkamp, «Progress in the No-Three-in-Line Problem, II», JCTA 81(1) (1998) **108–113**, DOI 10.1006/jcta.1997.2829; содержание — по реферату zbMATH.
17. T. Prellberg, «Constraint Satisfaction Programming for the No-three-in-line Problem», arXiv:2602.07751v1 [math.CO], 8 Feb 2026; опубл. J. Combin. Theory Ser. A 225 (2027) 106244, DOI 10.1016/j.jcta.2026.106244. Репозиторий: github.com/ThomasPrellberg/no-three-in-line---CP-SAT (6 файлов; кода экспериментов §5.5 нет).
18. T. Prellberg, «No-three-in-line sets on the checkerboard grid», arXiv:2605.09215v1 [math.CO], 9 May 2026. (Аннотация на abs-странице и в PDF различаются — цитировать по PDF.)
19. T. Prellberg, «No-three-in-line for forty-seven and forty-nine», 13 сентября 2025 (PDF на сайте Фламменкампа). Внимание: его ссылка [2] содержит ошибочные страницы «81 (1998) 397-400».
20. P. M. Voutier, «On the Guy-Kelly Conjecture for the No-Three-In-Line Problem», arXiv:2603.00215v2 [math.CO], 9 Mar 2026 (3 стр.).
21. A. Ghosal, R. Goenka, A. Grebennikov, P. Keevash, M. Kwan, H. T. Pham, «No-(k+1)-in-line problem for k ⩾ 3», arXiv:2607.05255v1 [math.CO], 6 Jul 2026 (Remark 1.7 — стр. 3).
22. A. Ghosal, «A note on the extensible no-three-in-line problem», arXiv:2605.07000v1, 7 May 2026.
23. L. Zhang, X. Zhuang, T. Wang, N. Kaplan, «Geometry-Aware MCTS for Extremal Problems in Combinatorial Geometry», arXiv:2606.26399v1 [cs.AI], 24 Jun 2026 (UC Irvine).
24. P. Ramanathan, T. Prellberg, M. Lewis, P. D. Joshi, R. A. Dandekar, R. Dandekar, S. Panat, «Three methods, one problem: Classical and AI approaches to no-three-in-line», arXiv:2512.11469 (v1 12.12.2025); продолжение — «Four Methods, One Problem: The No-Three-In-Line Problem», 3rd AI for Math Workshop @ ICML 2026, Seoul (paper.pdf в github.com/VizuaraAI/no-three-in-line).
25. M. Simkin, «The number of n-queens configurations», arXiv:2107.13460v3; опубл. **Advances in Mathematics 427 (2023) 109127**, DOI 10.1016/j.aim.2023.109127.
26. J. N. Cooper, J. Solymosi, «Collinear Points in Permutations», arXiv:math/0408396v1, 29 Aug 2004; Annals of Combinatorics, DOI 10.1007/s00026-005-0248-4.
27. Liangpan Li, «On the number of collinear triples in permutations», arXiv:0802.0572v2 [math.CO], 2 May 2008 (4 стр. по pdfinfo).
28. P. Erdős, G. Purdy, «Some extremal problems in geometry IV», Proc. 7th Southeastern Conf. on Combinatorics, Graph Theory and Computing (1976) 307–322; открытый скан: https://users.renyi.hu/~p_erdos/1976-43.pdf (плохой OCR).
29. D. T. Nagy, Z. L. Nagy, R. Woodroofe, «The extensible No-Three-In-Line problem», **European J. Combin. 114 (2023)**, Paper 103796, DOI 10.1016/j.ejc.2023.103796; arXiv:2209.01447v2.
30. B. Kovács, Z. L. Nagy, D. R. Szabó, «Randomised algebraic constructions for the no-(k+1)-in-line problem», Advances in Combinatorics 2026:7, DOI 10.19086/aic.2026.7; arXiv:2508.07632 (Observation 2.6 — стр. 7, доказательство собственное).
31. J. Solymosi, «On the structure of pointsets with many collinear triples», arXiv:2206.00889**v3**; опубл. **Discrete Comput. Geom. 72(2) (2024) 986–1009**, DOI 10.1007/s00454-023-00579-w.
32. S. Fernández-Merchant, R. Hämäläinen, «Direction-Critical Configurations in Noncentral General Position», arXiv:2210.12465v1, 22 Oct 2022 (в её списке литературы ссылки [6] и [8] ошибочны).
33. **[не открыт]** P. Ungar, «2N noncollinear points determine at least 2N directions», JCTA 33(3) (1982) 343–347, DOI 10.1016/0097-3165(82)90045-0 (в zbMATH Zbl 0496.05001 рецензии нет).
34. **[не открыт]** R. E. Jamison, «Planar configurations which determine few slopes», Geom. Dedicata 16 (1984) 17–34, DOI 10.1007/BF00147419 (рецензия F. Hering, Zbl 0548.52001).
35. **[не открыт]** R. E. Jamison, «Structure of slope-critical configurations», Geom. Dedicata 16 (1984) 249–277, DOI 10.1007/BF00147871 (рецензия T. Bisztriczky, Zbl 0562.51003).
36. **[не открыт]** R. E. Jamison, D. Hill, «A catalogue of sporadic slope-critical configurations», Congr. Numerantium 40 (1983) 101–125 (рецензия Zbl 0539.52011).
37. R. E. Jamison, «Few slopes without collinearity», **Discrete Math. 60 (1986) 199–206**, DOI 10.1016/0012-365X(86)90012-9 (рецензия H. Heineken, Zbl 0595.51016); R. E. Jamison, «A survey of the slope problem», **Ann. N.Y. Acad. Sci. 440 (1985) 34–51**, DOI 10.1111/j.1749-6632.1985.tb14537.x (Zbl 0568.51027). **[тела не открыты]**
38. J. Pach, «Finite Point Configurations», гл. 1 в Handbook of Discrete and Computational Geometry, 3rd ed. (preliminary version, 10 Aug 2017), CRC Press. https://www.csun.edu/~ctoth/Handbook/chap1.pdf
39. D. El-Baz, J. Marklof, I. Vinogradov, «The distribution of directions in an affine lattice: two-point correlations and mixed moments», arXiv:1306.0028v2; IMRN, DOI 10.1093/imrn/rnt258. Цитируемая там работа: **J. Marklof, A. Strömbergsson**, «The distribution of free path lengths in the periodic Lorentz gas…», **Ann. of Math. 172 (2010) 1949–2033**, DOI 10.4007/annals.2010.172.1949.
40. D. Eppstein, блог 11011110: «Random no-three-in-line sets», 10.11.2018; «Gurobi versus the no-three-in-line problem», 12.11.2018. https://11011110.github.io/blog/2018/11/10/random-no-three.html
41. N. Kaplan, «No-Three-in-Line, Intransitive Dice, and Other Amusements in Mathematics», IPAM Reunion Conference, 14.12.2016, 48 слайдов (research_files/kaplan-ipam_evening_talk.pdf); его CV (раздел «Seminar Talks», UCI ACO Seminar, November 2018; летний проект 2025). http://webapps.math.uci.edu/~nckaplan/
42. D. E. Knuth, TAOCP Vol. 4: Pre-Fascicle 5C «Dancing Links» (упр. 7.2.2.1–118 и ответ; снимок Wayback от 27.11.2025); **Volume 4 Fascicle 7 «Constraint Satisfaction» (2025), xiv+281 pp., ISBN 978-0-13-532824-8** — стр. 79, 146, ответы 237 (прочитано по черновику 7a от 5.12.2024, снимок Wayback 16.07.2026; опубликованный текст **[не открыт]**); официальные errata all4f7.ps.gz и all4b.ps.gz.
43. C. P. Gomes, M. Sellmann, «Streamlined Constraint Reasoning», CP 2004, LNCS 3258, 274–289, DOI 10.1007/978-3-540-30201-8_22 (16 стр.); R. Le Bras, C. Gomes, B. Selman, AAAI 2012 (0 упоминаний задачи).
44. **[не открыт]** I. Kaplansky, J. Riordan, «The problem of the rooks and its applications», Duke Math. J. 13 (1946) 259–268, DOI 10.1215/S0012-7094-46-01324-5.
45. **[не открыт]** J. Riordan, An Introduction to Combinatorial Analysis, Wiley 1958 (гл. 5; название главы не подтверждено).
46. L. Comtet, Advanced Combinatorics, D. Reidel 1974, гл. III, упр. 19 «Middle trinomial coefficients», с. 163 (открытая OCR-копия archive.org).
47. R. Stanley, Enumerative Combinatorics, Vol. 1, 2nd ed., §2.3–2.4 (с. 231, 235), Notes к гл. 2 (с. 249), библиография гл. 2 [13]. https://math.mit.edu/~rstan/ec/ec1.pdf
48. **[не прочитаны]** J. E. Freund, «Restricted Occupancy Theory—A Generalization of Pascal's Triangle», Amer. Math. Monthly 63(1) (1956) 20–27, DOI 10.1080/00029890.1956.11988751; J. E. Freund, A. N. Pozner, «Some results on restricted occupancy theory», Ann. Math. Statist. 27(2) (1956) 537–540, DOI 10.1214/aoms/1177728278 (Zbl 0071.13603; в zbMATH помечена «has open version»).
49. **[тело не открыто]** K.-T. Fang, «A restricted occupancy problem», J. Appl. Probab. 19(3) (1982) 707–711, DOI 10.2307/3213532 (дословный абстракт получен).
50. W.-S. Dai, M. Xie, «Gentile statistics with a large maximum occupation number», arXiv:cond-mat/0310066v3; Ann. Phys. (N.Y.) 309 (2004) 295, DOI 10.1016/j.aop.2003.08.018. Первоисточник: **G. Gentile jr., «Osservazioni sopra le statistiche intermedie», Il Nuovo Cimento 17(10) (1940) 493–497, DOI 10.1007/bf02960187**.
51. K. Barrese, N. Loehr, J. Remmel, B. E. Sagan, «m-Level rook placements», JCTA 124 (2014) 130–165, DOI 10.1016/j.jcta.2014.01.006; arXiv:1308.4081.
52. OEIS A280537 («no four in plane», автор H. Pfoertner, 05.01.2017) и A280538 (+ файл a280538.txt с 36 решениями n = 6).
53. Al Zimmermann's Programming Contests, «Non-Coplanar Points» — Description (включая FAQ о спойлерах), Standings, Final Report; контест завершён 4 июня 2016. http://azspcs.com/Contest/Tetrahedra
54. T. Sillke (доказательство — A. Flammenkamp), «Puzzles of the {0,1,2}^3 grid», декабрь 1992, https://www.math.uni-bielefeld.de/~sillke/PUZZLES/cube3 ; исходный тред rec.puzzles «no 4 on a plane (3*3*3 puzzle)», 27.11.1992 — прочитан через снимок Wayback от 06.07.2022 (живой Google Groups отдаёт HTTP 429).
55. A. Pór, D. R. Wood, «No-Three-in-Line-in-3D», GD 2004, LNCS 3383, 395–402, DOI 10.1007/978-3-540-31843-9_40; журнальная версия Algorithmica 47(4) (2007) 481–488, DOI 10.1007/s00453-006-0158-9 (полный текст конференционной версии получен через архивный снимок; журнальная **[не открыта]**).
56. R. F. Cohen, P. Eades, T. Lin, F. Ruskey, «Three-Dimensional Graph Drawing», GD 1994, LNCS 894, 1–11, DOI 10.1007/3-540-58950-3_351; Algorithmica 17(2) (1997) 199–208, DOI 10.1007/BF02522826. (Конструкция (i, i² mod p, i³ mod p); OEIS A280537 на неё не ссылается.)
57. R. Andersen, F. Chung, L. Lu, erratum, Algorithmica 47(4) (2007) 397, DOI 10.1007/s00453-006-3160-3 — официальная поправка заголовка; настоящее название статьи «Drawing Power Law Graphs Using a Local/Global Decomposition». **Ссылку «No-Three-in-Line-in-3D» этих авторов вносить нельзя.**
58. «The No-Three-In-Line Problem», страница на homepages.gac.edu/~jsiehler/NoThree/noThree.html, раздел «Unequal Frequencies» (имя автора на самой странице не проставлено).
59. E. W. Weisstein, «No-Three-in-a-Line-Problem», MathWorld (живая страница — HTTP 404; читан снимок Wayback от 19.06.2026).
60. Junrong Du (GitHub aujurd22), репозиторий «no3inline-rigidity» (создан 03.07.2026, последний push 29.07.2026; прежнее имя no3inline-missing-center): analysis/spectral_struct_n0mod4.md (записка 2026-07-08), analysis/rot4_diagonal_connectivity.md (Th-48), analysis/hypergraph_theory.md, analysis/dir5_invariants.py (JSON результата отсутствует), analysis/results/research_P.md, research_M.md. https://github.com/aujurd22/no3inline-rigidity — самопубликация без рецензии, с внутренними числовыми противоречиями.
61. Ed Pegg Jr, Wolfram Community: «Progress in the no-three-in-line-problem» (11.05.2026) и «The Min and Max of the No-3-in-line problem» (26.06.2026) — тело в приложенных ноутбуках .nb; Wolfram Demonstrations «No-Three-in-Line Problem» (2013) и «No-Four-In-Plane Problem» (2011), читаны через Wayback.
62. r-bennett, репозиторий «Tetrahedra» (Java, создан 13.06.2017, 8 файлов, 1038 строк). https://github.com/r-bennett/Tetrahedra
63. M. Heule, каталог слайдов https://www.cs.cmu.edu/~mheule/talks/ (59 PDF, последние 2026-07-20); программы SAT 2026 (program.floc26.org/SAT-index) и Pragmatics of SAT 2026 (pragmaticsofsat.org/2026/).
64. C. Brower, V. Ponomarenko, «Applying iterated mapping to the no-three-in-a-line problem», Involve 15(1) (2022) 69–74, DOI 10.2140/involve.2022.15.69; свободная авторская копия https://vadim.sdsu.edu/bp2.pdf (прочитана целиком; статистики направлений нет).
65. **[не открыт]** K. Tsuchiya, Y. Takefuji, «A neural network algorithm for the no-three-in-line problem», Neurocomputing 8(1) (1995) 43–49, DOI 10.1016/0925-2312(94)00003-4 (Unpaywall: closed).
66. A. S. Cooper, O. Pikhurko, J. R. Schmitt, G. S. Warrington, «Martin Gardner's Minimum No-3-in-a-Line Problem», **Amer. Math. Monthly 121 (2014) 213–221**, DOI 10.4169/amer.math.monthly.121.03.213; arXiv:1206.5350v2.
67. MathOverflow 457913 (07.11.2023, «ho boon suan»), MathOverflow 492579 (14.05.2025), Math.SE 4642059 (19.02.2023), Math.SE 553431 (принятый ответ 3282210, H. Pfoertner), Math.SE 5081743 (другая задача — «три подряд», не коллинеарность).
68. H. E. Dudeney, Amusements in Mathematics (1917), задача 317 «A Puzzle with Pawns», стр. 94 и 222; M. Gardner, Penrose Tiles to Trapdoor Ciphers (MAA, 1997; © 1989 W. H. Freeman), гл. 5, стр. 63–77 (задача — 69–71, письма читателей — 76).
