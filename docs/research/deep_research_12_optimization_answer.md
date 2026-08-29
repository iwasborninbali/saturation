# Deep research 12 — как безнадёжный расчёт сделать выполнимым

Дата среза: 2026-08-21

Статус: первичный поиск → сверка с полным реестром из 111 уже сделанных приёмов и отказов →
SAT/cross-domain audit → adversarial проверка новых лемм → cost/certificate review.

## Итог в одной строке

Самая красивая новая лемма оказалась вычислительной ловушкой. Exact-19 действительно даёт полное
покрытие из `7 399` малонаселённых слоёв вместо `19 650` содержимых одной плоскости, но свежий локальный
замер переворачивает его cost model: среди `1 226` содержимых размера 0–2 упрямы `8.1%` (`≈100`), а
среди `18 424` троек — только `0.24%` (`≈44`). Если частота переносится на другие слои, новый cover даст
около **600** упрямых ветвей вместо нынешних `≈144`. Он уменьшает число ветвей в `2.656×`, одновременно
увеличивая ожидаемый тяжёлый хвост примерно в четыре раза. Поэтому **sparse cover — корректный, но
вычислительно NO-GO ход** до появления противоположного стратифицированного замера.

Лучший следующий эксперимент — не менять покрытие, а добавить низкоарностные позиционные следствия
(`16 427` запретов коллинеарных троек и `63` central-line binary clauses) и измерить их именно на
упрямых sparse cubes. Второй — persistent assumptions + проверенные failed cores, превращающие уже
закрытые cubes в глобальные nogoods. У проекта нет основания покупать внешние ядра, пока эти два
30-минутных gate не покажут выигрыш при равной сумме CPU и proof cost.

## Контракт доказательности

Ниже используются четыре разных статуса:

- **локальный факт** — число или наблюдение уже лежит в репозитории;
- **источник** — утверждение прямо содержится в первичной статье или официальном репозитории;
- **вывод** — строгая лемма, которую можно проверить независимо;
- **сценарий** — ожидаемое ускорение, которое не является фактом до A/B-замера.

Главные локальные опоры:

- текущая формула кодирует `at-least-M`, а не exact cardinality: `slack/targets/plane4_cnf.py:116-119,217`;
- текущий plane sweep перебирает `1+49+1176+18424=19 650` содержимых **одного** слоя:
  `slack/targets/plane_sweep_second.py:9-20,41-44`;
- список содержит `346 743` богатых плоскости и независимо проверен полным:
  `logs/a280537/plane_completeness_n7.txt`;
- `16 427` коллинеарных троек независимо совпали у двух перечислителей: тот же журнал и пункт 33
  полного свода;
- profile pairs/triples и pair-layer inequality уже измерены как отрицательные результаты:
  `logs/a280537/negative_results.txt` и `logs/a280537/negative_layer_pair.txt`.

После первого draft пользователь передал более свежую стратификацию plane sweep: size `0–2` —
`1 226` leaves, `8.1%` stubborn (`≈100`); size `3` — `18 424`, `0.24%` (`≈44`). В репозитории underlying
run/log ещё не найден, поэтому проценты помечаются **user-supplied measurement · 2026-08-21 · awaiting
artifact pointer**. Для решения о runtime они важнее количества leaves; перед production их надо привязать
к manifest/base hash и независимо пересчитать.

Finite bookkeeping нового cover исполним в `docs/research/optimization_contracts.py`; семь breach tests
лежат в `docs/research/test_optimization_contracts.py`. Они проверяют 28 profiles, число `7 399`,
полноту/перекрытие и необходимость шести позиций для pair-ветвей. Они намеренно **не** утверждают
CNF-эквивалентность, скорость solver или корректность proof — это отдельные gates.

Ни один ожидаемый коэффициент ниже не выдан за замер. PASS означает разрешение следующего опыта, а не
разрешение полного счёта.

## 1. Новый точный редизайн разбиения

### 1.1. Почему можно считать ровно 19

Свойство «нет четырёх компланарных» наследуется подмножествами. Поэтому

> существует допустимое множество размера не меньше 19  
> **тогда и только тогда, когда** существует допустимое множество размера ровно 19.

Направление справа налево тривиально. В обратную сторону из любого множества размера 20 или 21 берутся
любые 19 точек. После этого к его орбите применяется одна из 48 симметрий куба и выбирается
лексикографически минимальный представитель; значит переход совместим и с нынешними 47 lex-leader
предикатами. Это **эквисовместность задачи существования**, а не тождественность множеств моделей двух CNF.

В текущем двунаправленном totalizer уже создаётся выход `O[19]`, означающий «выбрано не меньше 20».
Метод `atleast()` сейчас не возвращает список outputs, поэтому его надо явно вернуть из generator, а не
угадывать номер auxiliary variable; затем к существующему `O[18]` добавляется `¬O[19]`. Цена exact-19
в самой CNF — одна unit clause. Ошибка индекса (`O[18]` вместо `O[19]`) смертельна; корректность
проверяется на известных SAT/UNSAT случаях и независимым подсчётом модели.

### 1.2. Лемма о малом слое

Зафиксируем **одну** ось, например `x`. Семь её слоёв разбивают 19 точек, а каждый слой как плоскость
содержит не более трёх. Дефицит относительно потолка равен

`7·3−19=2`.

Поэтому профиль вдоль этой оси имеет ровно один из двух видов:

- перестановка `(3,3,3,3,3,3,1)`;
- перестановка `(3,3,3,3,3,2,2)`.

Следовательно в каждом exact-19 решении существует слой с одной или двумя точками. Более точно,
таких слоёв один или два.

### 1.3. Новое покрытие

Для каждого `t∈{0,…,6}` и каждого singleton `C⊂{x=t}` создаётся cube; для пар достаточно слоёв
`t∈{0,…,5}`. Cube фиксирует **все 49 клеток слоя**: клетки `C` истинны, остальные ложны. Число кусков

`7·C(49,1)+6·C(49,2) = 7·49+6·1176 = 7 399`.

Каждое exact-19 решение попадает хотя бы в один cube. Профиль с одним слоем размера 1 покрывается его
singleton-ветвью. У профиля с двумя слоями размера 2 хотя бы один индекс не равен 6, поэтому его ловит
одна из шести pair-ветвей. Это минимально среди покрытий такого однослойного вида: singleton нужен во
всех семи позициях, а позиции pair-ветвей должны образовать vertex cover полного графа на семи слоях,
то есть их нужно хотя бы шесть. Покрытие не является partition: если оба 2-слоя имеют индексы 0…5,
решение встречается дважды. Перекрытие безопасно для UNSAT; делать ветви неперекрывающимися через
«первый малый слой» пока не стоит, потому что дополнительные равенства для предыдущих слоёв могут
вернуть уже измеренную слабость profile constraints.

Совместимость с симметрией не требует, чтобы отдельный cube был инвариантен. Лекс-минимальная модель
тоже имеет малый `x`-слой, а перечислены все семь слоёв и все их точные содержимые. Опасная оптимизация —
самовольно оставить только `x=0` или только orbit representatives содержимых: это требует отдельной
теоремы о stabilizer action и отдельного cover checker.

**Вычислительный вердикт: NO-GO.** Покрытие оптимально по числу однослойных sparse branches, но это не
целевая функция. Новый замер даёт stubborn rate `8.1%` для size 0–2 против `0.24%` для size 3. На
`7 399` branches первый rate означает `≈599` stubborn leaves. Чтобы хотя бы сравняться со всеми нынешними
`≈143`, rate должен упасть ниже `1.93%`; чтобы сравняться только с `≈44` size-3 stragglers — ниже
`0.595%`. Это требует соответственно `4.2×` или `13.6×` необъяснённого улучшения exact19/other-layer
режима ещё до proof overhead. Поэтому count ratio `2.656×` не является даже слабым runtime forecast.
Контракт и тесты сохраняются как точный отрицательный результат и возможный fallback, но production
переход на 7 399 запрещён без отдельного замера, опровергающего эту стратификацию.

### 1.4. Почему это не повтор старого profile split

Профиль говорит: «в этом слое где-то две точки». Новый cube говорит, **какие именно две из 49**.
Он запускает unit propagation в счётчиках сотен тысяч плоскостей и в lex predicates. Новый ход использует
тот же математический запас ёмкости, что profile split, но переводит его из агрегированного ограничения
в 49 конкретных фактов — ровно тот режим, который локальный опыт показал сильным.

### 1.5. Два дополнительных точных усиления

**Коллинеарные тройки.** В множестве размера 19 три коллинеарные выбранные точки невозможны: вместе с
любой четвёртой выбранной точкой они компланарны. Поэтому можно явно добавить все `16 427` clauses
`¬x_a∨¬x_b∨¬x_c`. Это всего `0.59%` от `2 781 167` clauses. Ограничение логически выводимо из задачи,
но, в отличие от pair-layer bound, оно непосредственно работает на cell literals. Из `18 424` троек
одного слоя `824` (`4.47%`) коллинеарны и закрываются им немедленно. Остальной выигрыш неизвестен.

**Три центральные координатные прямые.** Если выбраны две точки одной grid-line `L`, остальные выбранные
точки распределяются по плоскостям через `L`, причём в каждую такую плоскость можно добавить не более
одной. Для центральной координатной прямой `{(x,3,3)}` имеется только 16 классов таких плоскостей
(неориентированные primitive directions в квадрате `[-3,3]^2`). Поэтому две точки на ней дают
`|S|≤2+16=18`, и при target 19 на каждой из трёх центральных осевых прямых можно выбрать не более одной
точки. Это всего `3·C(7,2)=63` binary clauses. Clean-room pair enumeration дал minimum 16 ровно на этих
63 парах; следующий minimum равен 20. Перед production этот расчёт должен стать сохранённым независимым
checker с mutation tests.

**Уникальность направления пары.** Две выбранные пары с одним primitive unoriented direction задают
параллельные прямые, а их четыре конца компланарны; при общем конце возникают три коллинеарные точки.
Значит у выбранного 19-множества все направления пар различны. Для `n=7` имеется `58 653` пар клеток,
собранных в `865` классов направлений. Extended formulation с переменными `y_{uv}`, односторонними
links `(x_u∧x_v)→y_{uv}` и `at-most-1` в каждом классе стоит примерно `116 441` новых переменных и
`231 152` clauses. Это projection-equivalent усиление, но его полезность значительно менее очевидна;
оно допускается только после дешёвого A/B collinear-clause теста.

## 2. Ответ на загадку «49 фактов против 14 точных равенств»

У явления есть не одно имя, а три близких языка.

1. **Propagation strength / generalized arc consistency (GAC).** Хорошая CNF-кодировка ограничения
   позволяет unit propagation выводить всё, что уже стало принудительным на уровне этого ограничения.
   Но даже GAC-кодировка `sum x_i=2` не обязана выбрать одну клетку, пока 49 клеток симметричны:
   ни один отдельный literal ещё не вынужден. Обзор encodings и propagation: [Abío et al., Artificial
   Intelligence 2022](https://doi.org/10.1016/j.artint.2021.103603).
2. **Backdoor-like assignment.** Набор конкретных значений может перевести остаточную формулу в простой
   для CDCL класс. Формально это не доказанный strong backdoor, пока не показана лёгкость **всех** его
   assignments; термин здесь описывает механизм, а не готовую теорему. Источник понятия:
   [Williams, Gomes, Selman, IJCAI 2003](https://www.cs.cornell.edu/gomes/pdf/2003_williams_ijcai_backdoors.pdf).
3. **Partial evaluation / predicate pushdown.** В компиляторах известные аргументы специализируют
   программу; в БД селективный предикат физически уменьшает промежуточные отношения. Точные cell facts
   специализируют тысячи plane counters немедленно, тогда как aggregate profile похож на поздний
   `GROUP BY/HAVING`, который не говорит, какие строки убрать.

Поэтому «информация» в смысле числа constraints или Shannon bits — неверная мера. Для этой задачи
рабочая мера должна быть операционной:

- число cell и auxiliary literals после BCP fixpoint;
- число удовлетворённых, укороченных и конфликтующих clauses;
- conflicts/decisions/propagations в одинаковом коротком CDCL probe;
- стоимость худшего ребёнка и сумма/геометрическое среднее цен детей;
- покрытая **масса**, а не число закрытых файлов.

Именно поэтому pair-layer inequality могла быть математически сильной и дешёвой по размеру, но дать
ноль: вопрос не в том, выводима ли она, а появляется ли из неё новая unit propagation на состояниях,
которые реально образуют тяжёлый хвост. Это близко к понятию **propagation redundancy**:
[Choi, Lee, Stuckey, CP 2004](https://arxiv.org/abs/cs/0412026).

## 3. Слой A — переносимые принципы

### A1. Менять представление раньше, чем ускорять исполнение

Сильнейшие ускорения часто убирают состояния до поиска: quotient по симметрии, достаточное состояние
динамики, эквисовместная постановка меньшего exact target. Здесь это exact-19 и малый слой. Это не
«оптимизация кода»: меняется множество подзадач, но не математический вопрос. Классический точный пример
из graph generation — canonical augmentation, оставляющая одного представителя каждого класса:
[McKay, 1998](https://users.cecs.anu.edu.au/~bdm/papers/orderly.pdf).

### A2. Ветвиться по измеренному эффекту, а не по энтропии

В MILP это **strong branching**: несколько кандидатов временно пробуются в обе стороны, после чего
выбирается реально усиливающий bounds/propagation. В look-ahead SAT аналогично максимизируют эффект
обеих ветвей; классическая Cube-and-Conquer работа использует product reductions, а не число формально
заданных bits: [Heule–Kullmann–Wieringa–Biere](https://www.cs.cmu.edu/~mheule/publications/cube.pdf),
[march_cu](https://github.com/marijnheule/CnC).

### A3. Cube-and-Conquer: искать границу фаз, а не заданную глубину

Look-ahead строит partition, CDCL решает листья; критичен cutoff между «ещё выгодно дробить» и
«уже выгодно решать». Published successes — Boolean Pythagorean triples и Schur Number Five — включали
специализированное cubing, proof partition и независимую проверку, а не только много CPU:
[Pythagorean proof](https://arxiv.org/abs/1605.00723),
[Schur Number Five](https://arxiv.org/abs/1711.08076).

### A4. Инкрементальность превращает дерево в сеть

При решении одной базы под разными assumptions CDCL сохраняет глобально законные learnt clauses.
Если `F∧c` UNSAT, incremental solver может вернуть subset `c'⊆c`, достаточный для UNSAT; clause `¬c'`
затем немедленно режет другие cubes. Этот механизм прямо описан в исходной CnC статье, §3,
стр. 4–5. Официальный API CaDiCaL предоставляет `assume()` и `failed()`:
[cadical.hpp](https://github.com/arminbiere/cadical/blob/master/src/cadical.hpp). На дату среза актуальный
release — CaDiCaL 3.0.1; failed core не обещан минимальным, assumptions сбрасываются после solve, а proof
tracing и `conclude()` надо калибровать end-to-end, не считать совместимыми со старым DRAT pipeline
автоматически: [releases](https://github.com/arminbiere/cadical/releases),
[SAT 2026 system paper](https://doi.org/10.4230/LIPIcs.SAT.2026.40).

### A5. Memoization полезна только при доказанном повторе состояния

Transposition tables дают огромный эффект в играх, потому что одна позиция достигается разными ходами.
В нынешнем монотонном дереве assumptions именованный набор обычно имеет единственный путь; хеш сам по
себе не доказывает равенство. Единственный перспективный аналог — не cache полных узлов, а короткие
проверенные UNSAT cores, которые совпадают по включению с кубами в других ветвях. Источник классического
position hashing: [Zobrist, 1970](https://minds.wisconsin.edu/handle/1793/57624).

### A6. Усиление должно менять локальное доказательство

Valid inequalities, lifting и extended formulations полезны не из-за истинности, а когда дают более
короткий вывод в выбранной proof system. В SAT это значит сравнивать BCP closure и conflict proof, а не
количество добавленных clauses. Collinear triples и direction-pair lift — проверяемые примеры; pair-layer
bound — локальный контрпример. Точное CP-понятие для бесполезной дубликации —
[propagation redundancy](https://arxiv.org/abs/cs/0412026).

### A7. Тяжёлый хвост требует restart/race, а не среднего времени

Runtime complete search часто имеет heavy tail; randomized restarts и независимые seeds уменьшают риск
одного катастрофического пути. Источник: [Gomes, Selman, Kautz, AAAI 1998](https://www.cs.cornell.edu/gomes/pdf/1998_gomes_aaai_iaai_boosting.pdf).
Современный solver уже рестартует внутри, поэтому внешний portfolio сохраняется только при измеренной
комплементарности solver/seed на одинаковых cubes.

### A8. Цензурированные времена анализируются как survival data

Timeout `600 s` — не наблюдение времени `600`, а правая цензура: истинное время больше 600.
Kaplan–Meier survival curve и restricted mean дают честнее capped average; стратификация должна быть по
признаку, связанному с трудностью, а validation split — по родительским поддеревьям, не по siblings.
Первичный источник метода: [Kaplan–Meier 1958](https://doi.org/10.1080/01621459.1958.10501452).

### A9. Portfolio выбирает алгоритм; модель не получает логической власти

SATzilla обучает empirical hardness models и выбирает solver по instance features:
[Xu et al., JAIR 2008](https://doi.org/10.1613/jair.2490). В нашей задаче модель может выбрать
`solve/split/solver/seed`, но не объявить cube UNSAT и не удалить его. Reject option для out-of-domain
состояний обязателен — иначе это повтор ошибки predictor без верхней области применимости.

### A10. Параллелизм полезен, когда делится знание, а не только работа

Independent cubes масштабируются почти линейно, но не уменьшают total work. HordeSAT/Mallob обмениваются
короткими learnt clauses; Mallob поддерживает proof production/checking и incremental jobs:
[Mallob](https://github.com/domschrei/mallob),
[JAIR 2024](https://doi.org/10.1613/jair.1.15827). На широкой очереди это может ухудшить core-hours;
same-cube sharing надо оставлять только для stragglers и мерить при равной сумме CPU.

### A11. Симметрия — это canonical state, а не автоматически `×|G|`

Полные 47 lex predicates уже используют геометрическую группу куба. Дополнительный резерв может лежать
в симметриях auxiliary encoding или в dynamic fixing, но цена predicates и proof обязана учитываться.
[Satsuma](https://github.com/markusa4/satsuma) строит equisatisfiable CNF и умеет выдавать SR/VeriPB proof;
SR помечен авторами stable, VeriPB experimental. Isomorph-free generation имеет смысл только с
проверяемым canonical-parent rule, а не с удалением «похожих» cubes.

### A12. Exact separator DP живёт или умирает от ширины границы

Transfer matrix, bucket elimination и meet-in-the-middle дают экспоненциальный выигрыш, только если
между половинами есть компактное достаточное состояние. Bucket elimination экспоненциален по induced
width: [Dechter, Artificial Intelligence 1999](https://doi.org/10.1016/S0004-3702%2899%2900059-4).
Здесь большинство богатых плоскостей пересекают несколько слоёв; state должен хранить capacity каждой
активной плоскости. Поэтому сначала нужен 30-минутный census boundary signatures, не реализация DP.

### A13. Approximate filters не становятся доказательством от высокой recall

BLAST/minimizers покупают скорость тем, что отбирают малую долю seeds и допускают пропуски:
[BLAST](https://doi.org/10.1016/S0022-2836%2805%2980360-2). Для UNSAT даже один false negative фатален.
Безопасный аналог seed dictionary — только необходимые условия или уже проверенные короткие nogoods.

### A14. Менять proof system иногда важнее, чем encoding внутри неё

Pseudo-Boolean solver видит исходные inequalities `Σ_{p∈P}x_p≤3` и `Σx=19`, а не сотни тысяч
auxiliary counter variables. RoundingSat/Exact могут комбинировать их cutting-plane reasoning и писать
proof для [VeriPB](https://veripb.org/). Это независимый pilot, не рекомендация немедленно бросить SAT:
его нужно убить, если на известных `n=5/6` и реальных cubes он не даёт хотя бы порядок ускорения с
приемлемым proof.

### A15. Приближённое обучение годится для расписания, не для отсечения

Active learning полезен, если дорогие labels запрашиваются там, где выбор `solve/split/solver` неясен.
Но sibling leakage, censored labels и distribution shift легко создают прекрасную offline accuracy и
плохую очередь. Модель обязана сравниваться по closed mass/core-minute на held-out parent subtrees и
иметь deterministic fallback; это extension empirical-hardness подхода
[SATzilla](https://doi.org/10.1613/jair.2490), а не право модели отсекать ветви.

## 4. Слой B — таблица переносимости

В колонке «эффект» все коэффициенты — **условия допуска**, а не прогнозы. Если PASS не выполнен на
held-out кусках при одинаковой сумме CPU, метод отбрасывается независимо от красоты источника.

| Принцип / конкретный перенос | Перенос | Тест за 10–30 минут | Условный эффект и вердикт |
|---|---|---|---|
| Exact target → sparse cover | **Математически да, вычислительно NO-GO.** Exact19; singleton во всех семи слоях, pairs в любых шести. | Контракт уже проверен. Runtime test нужен только для возможного возврата: отдельно size1/size2 по всем layers, не смешанный average. | `2.656×` меньше leaves, но измеренный stubborn rate проектирует `≈599` против нынешних `≈143`. Вернуть лишь при `<1.93%`, лучше `<0.595%`; count не speedup. |
| Failed assumptions / global nogoods | **Да.** Один persistent CaDiCaL, current plane contents как 49 assumptions; core `c'` закрывает любой cube, содержащий `c'`. | 30 easy + все доступные stubborn strata, fresh vs persistent vs persistent-reset; 30 s/tick budget; 5–10 proof-on cores. Core size/coverage — диагностика. | GO только при net held-out certified capped-work gain `≥1.3×`, включая extraction/proof/check, RSS `<2×`. Full cores или hit `<2%` — kill. **GO №2.** |
| Direct no-three-collinear + 63 central-line clauses | **Да, выводимы уже при target `≥19`.** | Base / +63 binary / +16 427 triples на одних и тех же stubborn size0–2 и size3 cubes; сначала `propagate()`, затем equal-budget solve. Exact19 — отдельный arm, не обязательная посылка cuts. | Binary cut почти бесплатен; triples GO, если `≥10%` cubes получают новый original-cell literal/conflict и certified work падает `≥1.3×`. **GO №1.** |
| Direction-pair lift | **Условно.** Сильное позиционное extended formulation, но +116k vars/+231k clauses. | Только если triples прошли: 12 hard cubes, BCP closure + 10 s solve, proof-on один известный UNSAT. Отдельный checker сверяет 865 классов и mutation с неверно слитыми directions. | Нужен `≥2×`, иначе цена encoding/proof не оправдана. **Reserve №3b.** |
| Semantic look-ahead / strong branching | **Да.** Candidates только среди 343 original cells, не 392k auxiliary vars. | 24 hard parents; 16–32 candidate cells; обе полярности BCP + 1k–5k deterministic ticks; top candidate против нынешнего column, static incidence и random на held-out parents. | GO при `≥2×` меньшем summed capped work, overhead `<10%`; kill при `<25%` gain или нестабильном winner. **GO №4.** |
| CnC fixed depth / generic march score | **Не напрямую.** Fixed depth уже опровергнут локальной неоднородностью; raw assigned count будет измерять auxiliaries. | `march_cu` только как контроль на 12 cubes; отдельно score по original implications. | Если generic score не выигрывает у semantic score, не production. Ожидание: reference, не решение. |
| Solver/seed portfolio | **Да, как dispatcher.** Локально уже есть взаимная дополнительность Kissat/Glucose; добавить CaDiCaL. | Те же 24 hard cubes × solvers/seeds, 30 s single-core; PAR-2, virtual best, total CPU, не только wall. | GO только при `≥20%` меньшем held-out capped work и accepted proof. Два удачных anecdotes не gate. Типично `1.2–2×`, не экспонента. |
| Same-cube clause sharing | **Только для stragglers.** | 6 cubes, не закрытых за 600 s: 1×single против 4-thread Gimsatul/Mallob при равных core-minutes; один known case с полностью проверенным proof. | GO при `≥1.5×` **core-efficiency** и accepted proof. Wall speedup с 4× CPU не считается. |
| Learned action selection | **Да, но только расписание.** | Existing logs + 100–200 stratified cubes; features после 1 s; right-censored labels; split по parent subtree; reject/OOD arm. | GO при `≥20%` held-out closed mass/core-minute; иначе rule-based scheduler. Модель никогда не удаляет cube. |
| Satsuma / residual symmetry | **Условно, низкий потолок.** Current geometry group уже полностью lex-broken. | `fix` и `lex` на `n=5` known proof и 10 hard `n=7` cubes; сравнить preprocessing+solve+proof check. | Нужен `≥1.5×`; иначе kill. Не обещать ещё `×48`. |
| Direct PB + VeriPB | **Условно, независимый proof system.** 343 primary vars и plane/cardinality inequalities без CNF counters. | `n=5,M=14`, один known `n=6` case и 10 hard `n=7` cubes; одинаковый 10–30 min budget; proof checker обязателен. | Из-за новой оснастки нужен `≥10×` или закрытие SAT-неразрешимого класса. Иначе оставить как независимую сверку. |
| Bucket elimination / transfer matrix | **Только kill-test.** | Для first layer посчитать exact signatures capacities всех crossing planes для 19 650 contents; затем sample layer 2. | Keep лишь если unique/state ratio быстро падает и projected states `<10^6–10^7`; kill при `>90%` unique. Binary upside, очень высокий риск. |
| Meet-in-the-middle / rainbow table | **Нет.** Нет компактного сравнимого middle state; стороны имеют `C(147,9)≈6.88·10^13` и `C(196,10)≈1.83·10^16` raw subsets. | Тот же separator-signature test исчерпывает гипотезу. | Kill, если boundary DP не сжимается. Отдельный MITM ничего не добавляет. |
| Transposition table | **Вероятно нет.** Tree state задаётся монотонным набором facts и обычно имеет один путь. | На 2–5k nodes канонизировать residual CNF; hash только индекс, equality — byte/permutation check. | Keep при `>5%` exact duplicates; ожидается около нуля. |
| Database WCOJ | **Нет как solver.** Полезен лишь для генерации forbidden tuples, уже не bottleneck. | Не требует production test; генератор плоскостей уже проверен. | Kill: global cardinality и доказательство пустоты не становятся join materialization. |
| Alpha–beta / move ordering | **Порядок — да, alpha–beta pruning — нет.** В UNSAT надо закрыть всех детей. | Текущий reverse-order опыт уже является более сильным локальным тестом. | Без переносимых nogoods меняется makespan/progress, не total tree. Late/null move pruning запрещено. |
| BLAST/minimizers, approximate filters | **Нет для доказательства.** | Только если фильтр имеет proof of no false negatives; иначе тест бессмыслен. | Kill. Проверенные failed cores — exact replacement. |
| Multigrid/renormalization | **Нет в прямом виде.** У SAT нет гладкой ошибки и exact interpolation; lossless coarse state возвращает bucket elimination. | Separator gate выше. | Kill до появления компактного exact state. |

## 5. Пять конкретных ходов по gain / цене проверки

### 1. 63 central-line binaries и 16 427 collinear-triple clauses

Почему первый: это единственные новые cuts, которые (а) сформулированы над исходными cell variables,
(б) почти бесплатны по размеру, (в) адресуют измеренный упрямый sparse-класс без замены нынешнего
выгодного распределения ветвей. Exact19 для их корректности не нужен: target `≥19` уже гарантирует
существование четвёртой точки и противоречие центрального pencil bound.

**30-минутный paired gate:** одни и те же 32–64 stubborn cubes из size0–2 и size3 strata проходят arms
`base`, `+63`, `+16 427`, `+оба`; одинаковые seed/options/CPU pinning, случайный порядок, сначала
`propagate()`, затем равный 30–300 s cutoff. Считать новые original literals/immediate conflicts, ticks,
certified closed work/core-second, proof bytes и check time; все timeouts остаются censored.

**PASS:** `+63` сохраняется, если не даёт измеримого regression; triples — только если не менее 10% hard
cubes получают новый original implication/conflict и held-out certified work улучшается `≥1.3×`, без
ухудшения любой тяжёлой stratum более чем на 20%. **KILL:** gain `≤1.1×`, proof/memory regression или
неполная независимая генерация 16 427 clauses. Коэффициенты arms не перемножаются.

### 2. Persistent assumptions + certified failed-core coverage

Текущий sweep создаёт новый DIMACS и новый процесс для каждого cube. Исходная CnC схема предлагает
держать одну базу, передавать cube assumptions и после UNSAT сохранять failed subset. Это одновременно
убирает повторный start/preprocess и создаёт non-tree reuse.

Порядок cubes тоже становится содержательным: сначала решаются потенциально широкие cores, затем их
coverage удаляет subsumed cubes. Но order не должен влиять на доказательный итог: final checker независимо
перечисляет исходные 19 650 plane-content cubes и для каждого находит checked core `c'⊆c` либо
собственный checked proof.

Безопасная схема сертификата:

1. pinned base hash и CaDiCaL version/options;
2. для каждого опубликованного core — отдельное проверяемое доказательство `F∧c'` UNSAT или корректный
   incremental proof path с `conclude()`;
3. маленький независимый containment/coverage checker;
4. deliberate missing-core mutation должна сделать coverage неполным;
5. UNKNOWN никогда не становится фактом.

### 3. Tail dispatcher: solver portfolio при равной сумме CPU

На одних и тех же stubborn cubes сравниваются Kissat, CaDiCaL и Glucose/seeds. Fair arm — не
`два solver по 600 s` против одного, а, например, один `600 s` против двух по `300 s`: одинаковые
core-seconds. Метрики — PAR-2, certified work/core-second, virtual best и complementarity по strata.

**PASS:** portfolio уменьшает held-out capped work `≥20%` при равной сумме CPU; выигравший proof проходит
independent checker. Multi-thread Gimsatul/Mallob включается
только когда live stubborn cubes меньше свободных CPU или tail определяет makespan.

### 4. Semantic strong branching на хвосте

Не перезапускать весь column tree. На каждом оставшемся тяжёлом parent пробовать обе полярности
нефиксированных **cell variables**, измерять original implications/conflict и небольшой deterministic
tick probe. Выбирать splitter по худшему ребёнку или `min(g+,g−)+ε(g++g−)`, а не по среднему числу
assigned auxiliaries.

Reliability branching позволяет после достаточного числа probes заменить часть дорогих проб накопленным
pseudocost, но сначала должна существовать held-out корреляция. Если winner меняется от sibling к sibling,
статическая эвристика не выучена.

### 5. Отдельные falsifiers: exact19, direction lift, PB, Satsuma

Exact19 как одна clause тестируется отдельно от sparse cover: она может усилить propagation, не меняя
нынешнее выгодное распределение leaves. Direction lift (`+29.7%` variables, `+8.3%` clauses), direct PB и
Satsuma получают отдельные 10–30-минутные proof-on arms. Для direction lift нужен минимум `1.3×`, для PB
из-за новой proof stack — `≥1.5×`; Satsuma должен дать stable SR chain и `≥1.3×`. Sparse 7 399 cover
остаётся NO-GO и в этот стек не входит.

## 6. План первых 24 часов

Бюджетный конверт: `44·24=1 056 core-h`. Scout/calibration получает максимум `88 core-h` (два часа),
production — `924 core-h` (21 час), финальный independent replay/manifest — `44 core-h` (час). Если все
эти core-hours платные, `$200/1 056=$0.1894/core-h` — лишь максимальная допустимая средняя ставка,
**не** тариф провайдера. Каждый фактический тариф и proof storage добавляются до запуска.

### Час 0–2: один общий scout cap `88 core-h`

- freeze base/formula/generator/solver hashes, фактическую topology CPU, RAM/free disk и pointer на
  underlying `8.1%/0.24%` logs; без последнего проценты остаются provisional;
- `16 core-h`: paired `base/+63/+triples/+оба` на нынешних stubborn cubes;
- `16 core-h`: fresh/persistent/reset CaDiCaL, core extraction, proof-on sample и coverage текущего manifest;
- `14 core-h`: equal-core Kissat/CaDiCaL/Glucose portfolio;
- `12 core-h`: semantic look-ahead против нынешнего split на held-out parents;
- `24 core-h` общим stop-loss: separate exact19, direction lift, PB и Satsuma falsifiers;
- `6 core-h`: known controls, independent generation/checking и deliberate broken proofs/manifests.

Полные дешёвые controls `n=3…5`, сохранённый `n=6` witness и checked `n=6` leaves обязательны; незакрытый
full `n=6,M=17` control не называется. Sparse 7 399 queue в scout не запускается: её cost hypothesis уже
отклонена новым измерением.

### Решение в час 2

Из переживших component gates собирается **ровно один** candidate stack. Затем на held-out текущих
stubborn cubes проводится финальный baseline-versus-stack A/B при одинаковых total CPU, включая
preprocessing, core extraction, proof writing и checking. Компонентные speedups не перемножаются.

Production разрешается, только если одновременно:

- все semantic controls и deliberate failures дают ожидаемый verdict;
- combined stack уменьшает held-out certified capped work минимум в `1.3×` и не ухудшает ни одну
  тяжёлую stratum более чем на 20%;
- conservative projection **текущего** remaining manifest, а не нового sparse cover, `<924 core-h`;
- proof bytes, disk, RSS и checker time помещаются с двукратным запасом;
- каждый failed core имеет проверяемую цепочку, UNKNOWN нигде не превращается в closure.

### Час 2–23: production текущего покрытия

- нынешние plane-content cubes сохраняются; выбранные cuts/persistent cores/dispatcher применяются к ним;
- короткие cubes остаются по одному CPU; same-cube portfolio включается только на stragglers;
- каждые 30 минут пересчитываются current remaining branches, certified core coverage, censored runtime
  summary и full-cost projection;
- если projection два раза подряд превышает бюджет, остановка и новый эксперимент, не инерционное «ещё час»;
- facts, cores, proofs и manifests пишутся атомарно, имена несут base hash, layer, content, solver side.

### Час 23–24: независимый replay

Последние `44 core-h` зарезервированы: verifier не читает scheduler counters, а восстанавливает theorem из
base, **исходного** exhaustive plane-content cover, checked cores/leaf proofs и manifest. Если этот этап не
закончился, итог суток — «solver work завершён, proof не проверен», не «доказано».

Денежный cap `$200` проверяется после локальной калибровки по фактической цене provider. Квота 800 CPU,
которой физически нет, не участвует ни в одном forecast.

## 7. Где внешняя литература противоречит опыту — и где противоречия нет

### «Более сбалансированная ветвь всегда лучше» — противоречит без cost model

Look-ahead и strong branching любят две сильные ветви, но их score — proxy. Локальный profile split
выглядит идеально сбалансированным и задаёт много exact information, однако ни один cube не закрылся.
Правильная формулировка: balanced reduction полезна **только после того, как выбранная reduction metric
предсказывает conquer cost на этой distribution**.

### «Больше implied constraints усиливает solver» — локально опровергнуто

Valid inequality literature не обещает, что всякое верное ограничение ускоряет. Pair-layer bound добавил
2.8% clauses и дал нулевой эффект. Поэтому каждый cut проходит propagation-yield gate: новый original
literal/conflict на реальных hard states и downstream A/B. Формальный статус «facet», «strong» или
«tight» сам по себе не является runtime evidence.

### «Alpha–beta move ordering экспоненциально уменьшает дерево» — механизм отсутствует

Alpha–beta использует minimax bounds, чтобы законно не смотреть siblings. В UNSAT partition все дети
обязательны. Порядок может улучшить time-to-first-core, memory locality или makespan, но superlinear
уменьшение total work появляется только через переносимый learnt nogood.

### «Database cardinality estimate помогает» — не то же, что profile cardinality

В System R селективный predicate действительно удаляет tuples до join. Exact layer count сохраняет
тысячи симметричных supports и не фиксирует ни одной клетки. Поэтому database analogy поддерживает
post-BCP selectivity probing, а не возвращает уже провалившиеся profiles.

### «Portfolio/много ядер ускоряет hard SAT» — wall time не равно core-efficiency

HordeSAT/Mallob могут сократить wall time одного straggler, но четыре workers могут потратить в четыре
раза больше CPU. Пока открытых cubes больше, чем CPU, one-core-per-cube может закрывать больше массы.
Переход разрешает только equal-core-minute A/B и проверяемый proof path.

### «ML научится на 235 000 узлах» — старый predictor уже показал domain shift

Количество labels не исправляет selection bias. Closed nodes — преимущественно лёгкие; timeout labels
censored; siblings почти одинаковы; глубина меняет режим. Parent-group holdout, survival objective,
uncertainty и reject option — условия переноса SATzilla, а не украшения.

### «BLAST/minimizers и coarse physics дают громадный выигрыш» — он куплен потерями

Approximate biological seed может пропустить alignment; coarse physical state может исправить гладкую
ошибку на fine level. Для exhaustive proof нельзя потерять ни один cube. Exact analogue обязан иметь
no-false-negative lemma, после чего обычно превращается в verified cores или separator DP.

### «MITM режет показатель пополам» — нет компактного middle key

Крипто-MITM сравнивает малое промежуточное значение двух направлений. Здесь ключ должен помнить
остаточную ёмкость каждой плоскости, пересекающей раздел. Без доказанного сжатия boundary signatures
две огромные таблицы хуже CDCL.

## 8. Разбор двадцати собственных принципов из §3.5

| № | Ваш принцип | Имя в литературе / поправка | Вердикт |
|---:|---|---|---|
| 1 | Определённость сильнее ограничений | **Propagation strength, GAC, partial assignment, backdoor-like specialization.** Не универсальный закон: сильный global constraint может победить facts, если его propagator/cuts дают новые literals. В этой CNF наблюдение подтверждено. | **Верно при измеренной BCP/CDCL отдаче**, не по числу bits. |
| 2 | Выводимое ≠ полезное | **Propagation redundancy / proof-system sensitivity.** Добавленная лемма полезна, только если сокращает локальный вывод сильнее, чем стоит её обслуживание. | **Верно; pair bound — качественный counterexample.** |
| 3 | Отказ по цене надо пересматривать | **Extended formulation / encoding-sensitive complexity.** Стоимость свойства и стоимость конкретной кодировки различны; Sinz/totalizer/network/PB могут менять её на порядки. | **Верно**, но новая дешёвая кодировка всё равно требует runtime gate. |
| 4 | Мера прогресса должна уметь стоять | **Potential function / probability mass / Kraft-type accounting.** При полном равновесном `b`-ary partition веса `b^{-d}` сохраняются при split и падают при closure. Для неравных split нужны условные веса, не глубина. | **Верно при доказанном partition measure.** |
| 5 | Известный потолок проверяет данные | **Conservation invariant, metamorphic/property-based testing.** Масса >1 — breach contract, а не «101% успеха». | **Верно и переносимо.** |
| 6 | Меру мало построить — надо сменить управление | **Goodhart/metric governance и control-loop discipline.** Старый dashboard остаётся действующим objective, пока scheduler/решение не переведены на новый. | **Верно, организационный механизм.** |
| 7 | Predictor обязан иметь область | **Out-of-distribution detection / applicability domain / concept drift.** Порог без нижней и верхней domain guard опасен. | **Верно; нужен deterministic fallback.** |
| 8 | Выборка трудности смещена | **Survivorship/length bias + right censoring + heavy tails.** Random-by-count не random-by-cost. | **Верно; KM/RMST и strata по hardness.** |
| 9 | Split или wait — режим | **Optimal stopping / adaptive cutoff / CnC phase transition.** Не существует одного бюджета для всех depths и residual regimes. | **Верно; выбирать по full capped work.** |
| 10 | Свойство оснастки принято за свойство задачи | **Measurement validity / end-to-end control.** Нужны positive, negative и deliberately broken controls, а не только return code. | **Верно; самый важный audit class вашего реестра.** |
| 11 | У watchdog три исхода | **Three-valued logic: true / false / unknown.** Fail-open/fail-closed не заменяет отдельное «измерение не состоялось». | **Верно.** UNKNOWN не меняет математический verdict. |
| 12 | Аларм ошибается к тревоге | **Signal detection + base-rate fallacy.** При редком событии даже хороший detector имеет низкий positive predictive value. | **Верно; измерять precision на собственных alarms.** |
| 13 | Process count — depth, не width | **Work–span model / runnable parallelism.** Процессы-предки могут ждать, не создавая work. | **Верно; мерить active workers, CPU occupancy и span.** |
| 14 | Сначала докажи utilization | **Amdahl/queueing/utilization discipline.** Capacity не лечит starvation, serial section, I/O или хвост из меньшего числа jobs. | **Верно; quota только после occupancy trace.** |
| 15 | Имя различает всё различимое | **Namespace, typed identifiers, data lineage, content addressing.** Имя факта — часть proof object. | **Верно; включать task/base/side/cube.** |
| 16 | Generated file регенерируется | **Hermetic/reproducible builds; source versus artifact.** Ручной merge создаёт output без generator provenance. | **Верно.** |
| 17 | Recovery обязан останавливаться | **Structured concurrency, cancellation propagation, idempotent control plane.** Родитель владеет lifecycle детей; restart token/version отменяет старую стратегию. | **Верно.** |
| 18 | Ресурс сначала ломает наблюдение | **Observability as a dependency / backpressure.** Логи, manifests и proof storage требуют reserve/quota отдельно от workers. | **Верно; disk gate должен сам иметь UNKNOWN.** |
| 19 | Молча неработающий tool хуже отсутствия | **Fail-fast + postcondition/check-the-effect.** Exit status недостаточен, если команда могла интерпретировать аргумент иначе. | **Верно; проверять след изменения.** |
| 20 | Согласие важно лишь при независимых источниках | **Common-mode failure / N-version programming.** Разные формулы на одном broken manifest проверяют арифметику, не coverage. | **Верно; независимость описывается по компонентам.** |

Главная поправка к формулировкам 1–3: в них нельзя заменять «на нашем тяжёлом распределении измерено» на
«всегда». Сильный propagator для global cardinality, PB cut или extended formulation иногда превосходит
тысячи facts; именно поэтому предлагается direct PB pilot. Ваш опыт устанавливает режим текущей CNF и
Kissat, а не универсальную теорему о типах constraints.

## 9. Что уже было в полном своде и потому не выдается за новое

- solve-or-split, короткие бюджеты, reverse order, single-layer scheduling, queue flattening;
- conserved progress mass, stratified tree estimates и предупреждение о heavy tails;
- density predictor с нижней/верхней областью применимости;
- truncated totalizer, 47 lex predicates и независимые encoding/symmetry checks;
- single-layer lower bound, измеренный нулевой pair-layer bound;
- profile pairs/triples, 3-axis orbits и обычное «больше симметрии»;
- DRAT, два solvers, независимые witnesses и многие operational watchdog rules.

Новые предложения относительно этого registry — ровно следующие:

1. exact-19 и **all-layer sparse-content cover** как новая строгая, но вычислительно отвергнутая ветка;
2. failed-assumption core subsumption между не родственными cubes;
3. direct collinear triples, 63 central-line binaries и pair-direction extended formulation;
4. semantic two-polarity probe только original variables;
5. right-censored survival evaluation и parent-group holdout;
6. independent proof-producing PB/Satsuma pilots с жёсткими kill gates.

## 10. Известная математика по самой задаче

[OEIS A280537](https://oeis.org/A280537) по-прежнему говорит, что exhaustive status установлен только до
`a(6)`, а `a(7)=18` и `a(8)=20` основаны на extensive numerical evidence. На дату среза прямого
публичного доказательства `a(7)≤18` или кода рекордсменов не найдено.

[Pór–Wood, Algorithmica 2007](https://users.monash.edu/~davidwo/papers/PorWood-No3InLine3D-Algo07.pdf)
напоминают общий moment-curve lower construction и тривиальную plane-layer верхнюю границу `3n`, то есть
для `n=7` только 21. Свежие общие grid/general-position результаты, например
[Suk, SoCG 2023](https://doi.org/10.4230/LIPIcs.SoCG.2023.59), асимптотические и не дают 18 при `n=7`.
Перебранные cap-set, flag-algebra, SDP и polynomial-method аналогии не дали валидного finite upper bound:
они либо работают над конечным полем/другим incidence structure, либо дают relaxation без exact 18.

Новая элементарная структура этого аудита — no-three-collinear, три central-line pencil bounds и
unique-pair-direction для target size 19. Она не доказывает 18 сама, но даёт низкоарностные,
position-level consequences для solver.

## 11. Что сознательно отвергнуто

- **Sparse 7 399 cover как production:** лемма и исполнимые контракты верны, но он оптимизирует число
  leaves против измеренной трудности; projected stubborn tail примерно в `4.2×` хуже нынешнего.
- **Ещё один profile/cardinality split:** уже отрицательный результат; exact19 допускается только как
  отдельная unit-clause propagation probe, не как новый aggregate split.
- **Ещё одна layer-sum inequality:** проходит только при новой original-literal propagation; pair bound
  показал, что логическая tightness недостаточна.
- **GPU SAT, переписывание обвязки, просто больше CPU:** бриф и свод уже содержат достаточные измерения.
- **AlphaMaple/MCTS cubing как первый ход:** интересный second-line tool, но часть опубликованных сравнений
  не включает DRAT verification, а локальный semantic look-ahead проще проверить и сертифицировать.
- **Paracooba как production:** полезная идея locality/incrementality, но опубликованный путь не закрывает
  нынешний proof contract; persistent API pilot дешевле.
- **Approximate pruning, late-move pruning, minimizers, neural discard:** запрещены без proof of no misses.
- **MITM/transfer/renormalization:** возвращаются только после exact boundary-state census, иначе это
  красивые названия для экспоненциальной таблицы.
- **Новая геометрическая symmetry factor:** 48 элементов уже обработаны; residual symmetry сначала мерится.

## 12. Финальный порядок решений

1. **Сегодня:** paired `base/+63/+16 427/+оба` на реальных stubborn cubes.
2. **Затем:** persistent CaDiCaL assumptions, checked failed cores и coverage нынешнего manifest.
3. **По тому же хвосту:** equal-core solver portfolio и semantic look-ahead.
4. **Только после combined held-out A/B:** production на исходном 19 650-cover.
5. **Параллельные falsifiers:** exact19 как одна clause, direction lift, direct PB, Satsuma, separator DP.

Если combined stack не проходит cost/proof gates, честный вывод не «нужно 800 ядер», а «эти новые
propagation/reuse механизмы тоже не изменили режим». Sparse 7 399 cover возвращается только при новом
стратифицированном измерении, снижающем stubborn rate с `8.1%` ниже `1.93%`; само уменьшение числа
ветвей основанием больше не является.
