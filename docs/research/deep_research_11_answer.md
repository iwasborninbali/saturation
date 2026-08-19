# Deep research 11 — перезапуск отбора вычислительных задач

Дата среза: 2026-08-20

Статус: разведка по классам источников → слепая перекрёстная верификация → oppose → counter →
adversarial-аудит конвенций → аудит стоимости и сертификатов → главный review.

## Итог в одной строке

**Production-победителя нет.** Все 15 кандидатов нарушают хотя бы один из C0–C4 или лимит
`10^5` core-hours. Лучший следующий шаг — не проект, а **один час аудита Grimm `T(10^14)`**:
проверить, можно ли превратить активные, но неаудируемые рекордные self-reports в два независимых
полных прохода с boundary-safe manifest и корпусом критических prime gaps. Даже полный PASS разрешает
только вторую калибровку, а не production-run.

В брифе ресурс назван `~65 cores`, но перечислено `32+12+12+8=64`. Ниже используется **64
перечисленных CPU**, пока не установлено, являются ли они физическими ядрами или логическими потоками.

## Контракт доказательности

В колонке `evidence · date · confidence` используются ровно значения брифа:

- `primary` — сама статья, запись OEIS, авторский репозиторий или исходный self-report;
- `inferred` — арифметический или алгоритмический вывод этого аудита;
- `verified` — граница независимо переустановлена по согласующимся первичным артефактам;
- `single-source` — утверждение реально есть у автора, но независимо не воспроизведено;
- `unconfirmed` — точная граница или полнота не установлена.

Ни одна ключевая граница ниже не основана на search snippet.

## Матрица 15 кандидатов

| Rank | Кандидат и заранее названное вычисление | Граница | evidence · date · confidence | Конкуренты | Публикуемость двух исходов | Стоимость на 64 CPU / калибровка | Вердикт |
|---:|---|---|---|---|---|---|---|
| **1** | **Grimm `T(10^14)`**: для каждого полного максимального composite block между соседними простыми с левым простым `q≤10^14`, включая блок, пересекающий правую границу, сертифицировать SDR различных простых делителей. | Peer-reviewed theorem: все исходные интервалы с `n≤19,236,701,629`; self-reports: `10^11` и `10^13`. | [Laishram–Shorey](https://www.isid.ac.in/~shanta/PAPERS/Grimm-IJNT.pdf): `primary · 2006 · verified`; [две записи в одном thread](https://www.reddit.com/r/LLMmathematics/comments/1qbepk5/verified_grimms_conjecture_to_10%C2%B9%C2%B9_extending_the/): `primary · 2026-01-13/2026-06-15 · single-source`. | Два активных вычислителя уже заявили `10^11` и `10^13`, но не выложили code/corpus. | Hall-obstruction — сильный компактный counterexample. Null `10^14` достоин artifact/data note только при двух реализациях, новом публичном critical-gap corpus и заранее подтверждённой площадке; простая цифра несимметрична. | Неаудированный rate даёт сценарий `5,133 core-h` для двух полных проходов, `3.34 d` ideal на 64 CPU; реальная цена устанавливается часовым pilot. Код рекордсменов отсутствует. | **Первый reproducibility pilot; не project winner.** |
| **2** | **Cubic `P14` rescue**: доказать или опровергнуть, что каждый конечный простой cubic `P14`-free graph содержит цикл длины степени двойки. | Общий min-degree-3 результат доказан для `P13`; `P14` авторский run завершился OOM. Cubic finite cutoff в 12,286 vertices следует из diameter/Moore bound. | [Статья](https://arxiv.org/html/2410.22842v2) и [repo](https://github.com/rbsandeep/Erdos-Gyarfas): `primary · 2025-02-11 · verified`; cubic cutoff: `inferred · 2026-08-20 · verified algebraically`, не опубликованная теорема авторов. | Исходные авторы и свежие certified cubic/min-degree работы 2026 года; высокий bar сертификатов. | Граф-контрпример опровергнет общую гипотезу; полное cubic exhaustion даст новую restricted theorem. | `P13`: 17m17s/72 CPU, около 20.7 allocated core-h. Для `P14` неизвестны число состояний и цена; Cilk создаёт `new Graph` на ветвь без `delete`. Finite cutoff не является cost bound. | **Не проект; оставить только memory/certificate calibration ticket.** |
| **3** | **Circular sorting, сначала `t(22)`**, а не scout-цель `t(24)`: решить существование permutation, у которой каждый cyclic shift имеет не более трёх циклов, fixed points включены. | `t(22)∈{18,19}` — первый неизвестный; `t(24)∈{20,21}`. | [Статья v3](https://arxiv.org/html/2510.18529v3) и [ancillary table](https://arxiv.org/src/2510.18529v3/anc/tn_bound_summary.json): `primary · 2026-06-17 · verified`. | Активная группа из пяти авторов прямо выделяет `t(22),t(24),t(30)`. | SAT witness закрывает верхнее значение; LRAT exhaustion — нижнее. Для `t(24)=20` результат особенно силён, но positive witness, вероятно, станет дополнением к их paper. | Для `t(24)` raw normalized space `23!≈2.585·10^22`; опубликованный strong-complete-mapping code решает другой predicate. Ни runtime, ни representative UNSAT calibration нет. | **Kill: прямой race и C2 fail.** |
| **4** | **Tetrahedral rooks `a(28)`**: под точной A345716-конвенцией предъявить dominating nonattacking placement из 136 rooks и доказать UNSAT для `≤135`. | OEIS показывает 136, но прямо говорит: brute force verified only through `n=27`; `a(28)` conjectural. | [OEIS A345716](https://oeis.org/A345716): `primary · 2021-06-24 · single-source`; [repo](https://github.com/fletchc/rookount): `primary · 2021-06-28 · verified available`, но это exploratory Python, а не exact solver. | Текущая гонка не найдена; авторская группа 2021 года известна. | `≤135` исправит таблицу; exact 136 добавит один уже отображаемый OEIS-term и без общего метода слишком слаб для симметричного paper outcome. | Natural SAT core: 4,060 vertices, 164,430 pair clauses, 4,060 domination clauses и cardinality. Размер формулы не предсказывает UNSAT; exact n27 timing/proof отсутствует. | **Kill как paper project; допустим короткий formalization probe.** |
| **5** | **Primorial maximal-gap positions, `n=55`**: при уже известном `h(55)=858` найти least positive start и/или все start residues modulo `P_55`, с доказательством полноты. | `h(n)` reported through `n=64`; exhaustive positions/least starts публичны лишь through `n=54`. | [Ziller–Morack](https://arxiv.org/abs/1611.03310): `primary · 2017-05-31 · verified` для position catalogue through 54; [A048670](https://oeis.org/A048670): `primary · 2021-03-14 · single-source` для поздних `h(n)`. | Ziller, Morack, Gerbicz, Bożek; свежая активность после 2021 не подтверждена. | Новый complete row — умеренная computational note; найденный меньший witness исправит author report. Incomplete search не публикуем. | Work unit после compression не зафиксирован; переход 54→55 и proof size не измерены, maintained code нет. Raw residue universe не является допустимым прогнозом. | **Return: сначала specification + C2.** |
| **6** | **Mixed OA lattice `a(36)`**: определить height poset `Λ_36` feasible parameter sets strength-2 mixed orthogonal arrays, не число массивов или классов. | OEIS называет 36 первым неизвестным run count; конструкции с 36 runs не дают полноты poset. | [Определения](https://arxiv.org/abs/math/0205299): `primary · 2002 · verified`; [OEIS A039930](https://oeis.org/A039930): `primary · 2026-07-20 · single-source` для first-unknown status. | Область активна; точная команда на `a(36)` не установлена. | Более длинная chain — lower-bound result; exact height требует глобального upper certificate. | Нет фиксированного enumerator, timed smaller truth или certificate design. OA library — constructions, не calibration of completeness. | **Return: C1/C2 ещё не сформулированы исполнимо.** |
| **7** | **BHR claim audit**: проверить, покрыты ли все labelled multiplicity vectors для каждого integer `2≤v<32`, а не один представитель каждой frequency partition. | Препринт заявляет все `v<32`, но его reduction не доказана; full `v=31` universe содержит `C(44,14)=114,955,808,528` lists. | [Naik v4](https://arxiv.org/html/2507.00059v4): `primary · 2025-07-31 · verified claim`, но `confidence=unconfirmed` для theorem; stars-and-bars count: `inferred · 2026-08-20 · verified`. | Несколько активных BHR-групп; сам claim не peer-reviewed. | Настоящий BHR-counterexample велик; полный certified census может быть paper. Репликация 5,096 representatives или ошибка в одном arXiv preprint — слабый audit outcome. | `v=16`: 167,898 lists/20h ≈2.33 lists/s. Перенос на full `v=31` даёт ≈13.7m core-h; код/manifest не опубликованы. | **Kill: invalid reduction и >100× budget.** |
| **8** | **Quaternary Legendre pair, length 42**: решить existence точно, с conjugate periodic autocorrelation и доказанными symmetry reductions. | 42 — smallest unresolved after constructions 28–40. | [Kotsireas–Koutschan–Winterhof](https://arxiv.org/abs/2408.16318) и [Jedwab–Pender](https://arxiv.org/abs/2408.08472): `primary · 2024/2025 · verified`. | Две профильные группы; active race. | Pair(42) закрывает smallest case; certified nonexistence опровергает all-even-length conjecture. | Exhaustive `ℓ=28` стоил 46 CPU-days. Raw half-sequence scaling `4^7` даёт `≈18.1m core-h` для 42 — inference, не forecast, но нужен >180× rescue до cap. Source/certificate не public. | **Kill до новой reduction.** |
| **9** | **Perfect `(16,4)` difference triangle set, scope 160**: решить existence; `k=4` здесь означает четыре differences/пять marks per block. | Scope 160 — counting lower bound. Current FPGA paper gives fast heuristic at scope 165, не exhaustion at 160. | [Статья](https://arxiv.org/html/2502.19517v2) и [HDL repo](https://github.com/applecoffeecake/dts-search-hdl): `primary · 2025 · verified`. | Авторы активно улучшают records. | Witness at 160 immediately proves optimum. UNSAT at 160 proves only `m(16,4)≥161`, не exact value без construction at 161. | Heuristic scope165: 150s FPGA vs 1,100s/32 CPU; эти числа не калибруют exact negative search. Exact work unit/node count отсутствует. | **Kill as exact two-outcome project.** |
| **10** | **Practical + two `s`-gonal, `s∈{4,5,6,7,8,10}`**: derive effective cutoff and exhaust it. | Authors checked `<10^8`; theorem covers sufficiently large `n`, но constructive cutoff имеет минимум 48–84 digits even under weak lower bounds. | [Somu–Tran](https://arxiv.org/html/2403.13533) и [notebooks](https://github.com/ducvktran/On-Sums-of-Practical-Numbers-and-Polygonal-Numbers): `primary · 2024 · verified`; cutoff arithmetic: `inferred · 2026-08-20 · verified`. | Исходные авторы владеют теорией и code; публичной активности после 2024 не найдено. | Counterexample refutes one of six claims; empty interval proves claim только вместе с effective theorem. | Direct finite closure astronomically beyond `10^5 core-h`; уменьшение cutoff на десятки порядков требует новой additive/analytic theory. | **Kill: theory-first, не compute-first.** |
| **11** | **Oriented powerful problem**: найти `n≥2`, где `n` is 2-full и `n+1` is 3-full; reverse orientation не считается. | Public 2026 repo self-reports no solution through `10^25`; old OEIS pair tables не являются этим утверждением. | [Erdős #366 certificate repo](https://github.com/techno-optimist/erdos-frontier-atlas): `primary · 2026-07-26 · single-source`; literature definitions: `primary · 2025/2026 · verified`. | Прямой активный вычислитель; дешёвый следующий decade легко забирается им. | Witness решает existence; ещё один finite null bound сам по себе слаб. | Self-report: 1.62b cubefull candidates/6.27 core-h. Dual replay through `10^26` — scenario ≈27 core-h, но race/publication, а не CPU, является fatal gate. | **Kill: active race и asymmetric output.** |
| **12** | **Brocard–Ramanujan extension**: certify `n!+1` nonsquare for `8≤n≤B`; не смешивать с Brocard prime-gap conjecture. | Peer-reviewed `10^9`; public author repo self-reports `10^15` after about five months/32 cores. | Berndt–Galway: `primary · 2000 · verified`; [Epstein–Glickman repo](https://github.com/jhg023/brocard): `primary · 2020 · single-source`. | Публичный код есть; большая текущая гонка не найдена. | New solution major; ещё один null decade без нового метода слаб. | `10^15` run ≈115,200 core-h under 30-day-month normalization; next decade linear scenario ≈1.15m core-h, likely optimistic. | **Kill: budget and weak null.** |
| **13** | **Factorial twin `k(7)`**: least `k≥7` such that `k!/7−1` and `k!/7+1` are both prime, if it exists. | OEIS says only `k(7)>25,000`; provenance/certificates не опубликованы. | [A139186/A139187](https://oeis.org/A139187/internal): `primary · 2020-03-30, modified 2026-08-17 · single-source`. | Активный worker не найден. | Pair plus minimality fills a term; finite no-hit gives only a larger lower bound and слабую публикацию. | At 25,000 operands already ≈99k decimal digits; no survivor rate, primality-certificate timing or target endpoint. | **Kill: no symmetric finite decision and C2 fail.** |
| **14** | **Tribonacci–Niven run of five** under greedy `1,2,4,7,…` representation: find start `x` with five consecutive qualifying integers. | Entry claims none through `10^10`, without run manifest; A352092 itself lists starts of runs of four. | [A352089/A352092](https://oeis.org/A352092): `primary · 2022, modified 2026-08-06 · single-source`. | Competition not found. | Five-run is a clean counterexample; empty extension is not a proof and has little independent value. | Rolling scan likely cheap, но hardware/rate/next `B` отсутствуют; rare-run tail and representation carries are pre-asymptotic trap. | **Kill: weak null and C2 fail.** |
| **15** | **Unimodality of `d_k(p)`**. | Уже классифицировано: unimodal for `k≤3`, non-unimodal for every `k≥4`. | [Wang–Crapis](https://arxiv.org/abs/2605.08542): `primary · 2026-05-08 · verified`; предыдущие `k≤20` cases: `primary · 2025/2026 · verified`. | Не применимо. | Открытой цели нет. | Production cost 0. | **Kill: theorem-dominated/solved.** |

Лид про «multiplicity of largest prime-power factor in prime gaps, checked to `10^8`» не вошёл в
15: независимый поиск не нашёл такой OEIS-объект, а ближайшая A053706 формулирует другую величину и уже
содержит author report до `2^63`. Это не кандидат, а неидентифицированная гипотеза.

## Ранжирование действий, а не обещаний

1. **Grimm `T(10^14)` — первый часовой audit target.** Он единственный имеет дешёвую ожидаемую цену,
   строгий finite target и естественный corpus/certificate contribution. Его убивают race и пока не
   доказанная публикационная ценность null-result; поэтому это не winner проекта.
2. **Cubic `P14` — второй calibration ticket.** Сначала исправить ownership/leak, воспроизвести `P10…P13`,
   добавить детерминированный transcript checker и измерить capped cubic frontiers. Не запускать full tree.
3. **Circular sorting — только после координации с авторами и решения меньшего `t(22)`.** SAT/LRAT
   постановка корректна, но нет representative UNSAT и cost model.
4. **Rook `a(28)`, primorial positions, OA(36)** — задачи на формализацию и C2, не на production.
5. Остальные кандидаты вычёркиваются до изменения литературы или появления новой reduction.

## Точный часовой эксперимент для Grimm

### Утверждение

Для `B=10^14` определить `T(B)`:

> Для каждой пары соседних простых `q<r` с `q≤B`, включая единственную пару `q≤B<r`, множество
> `q+1,…,r−1` допускает injective assignment различных простых делителей.

SDR полного maximal block автоматически даёт SDR каждому его подинтервалу. Поэтому `T(B)` доказывает
Grimm для всех all-composite intervals, начинающихся не правее `B`. Остановка на последнем `r≤B` этого
не доказывает.

### Предварительные race/publication gates

До написания production code:

1. связаться с обоими авторами self-reports `10^11`/`10^13`, запросить code и critical-gap list;
2. получить письменное мнение предполагаемой площадки/соавтора, что `T(10^14)` плюс dual replay,
   crossing-safe manifest и critical corpus является достаточным artifact/data result при null outcome;
3. зафиксировать non-overlap/collaboration или kill. Публичный certified artifact `≥10^14`, появившийся
   до freeze, также убивает target.

### Две независимые реализации

- **A:** segmented prime/factor sieve; большие простые факторы сразу назначаются как private divisors;
  matching запускается только на `k`-smooth части gap длины `k`.
- **B:** отдельный prime-stream/factor path, другой parser, chunker и matching implementation.

Общие библиотеки допустимы только для низкоуровневой arithmetic после отдельной проверки; implementations
не должны делить generator, boundary logic, matching code или manifest writer.

### Один час на четырёх хостах

Сначала зафиксировать реальные physical/logical CPU, модели процессоров, RAM, compiler и source hashes.
Затем:

1. обе реализации полностью воспроизводят peer-reviewed `B0=19,236,701,629`, включая terminal crossing gap;
2. обе независимо обрабатывают окно `[10^14−2·10^11,10^14]`, расширенное с обеих сторон до соседних
   простых, и сравниваются **gap-by-gap**, а не только totals/digests;
3. A запускается на каждом из хостов при `1`, `8` и максимальном числе подтверждённых физических ядер;
4. independent `primecount` checkpoints сверяют prime/gap counts;
5. checker принудительно прогоняет Hall-tight interval `24…28`, synthetic obstructions, boundary chunks и
   все найденные nontrivial matching cases;
6. записываются integers/s, gaps/s, fallback frequency, min Hall slack, p50/p95/p99/max matching time,
   peak RSS, bytes/output, restart determinism и per-host efficiency.

Неаудированный self-report `10^11` за 7.7 min на 20 threads соответствует `10.82m positions/(core·s)`.
Это даёт только сценарий:

- двухсторонний pilot выше: `≈11.25 core-h`, `≈10.5 min` ideal на 64 CPU;
- два полных прохода до `10^14`: `≈5,133 core-h`, `≈3.34 d` ideal на 64 CPU;
- при 50% efficiency: `≈10,267 core-h`, `≈6.68 d`.

Эти числа не становятся evidence до локального замера.

### PASS / AMBER / KILL

**PASS к второй калибровке**, только если одновременно:

- A/B/primecount совпадают по каждому gap, critical record и boundary; terminal pair присутствует;
- все factor/matching certificates проходят отдельный checker; restart даёт те же records;
- rare matching branch реально exercised, а не пропущена удачной выборкой;
- per-host efficiency не ниже 50%, peak RSS укладывается в RAM каждого хоста;
- conservative dual-run projection не превышает **14 wall-days и 25,000 core-h** на перечисленных
  64 CPU, включая второй проход, merge, checking и storage;
- race и publication gates выше закрыты.

**AMBER, не выбор проекта:** projection 14–45 days или 25k–69,120 core-h. Нужна ещё одна заранее
зарегистрированная calibration, а не production.

**KILL:** любой mismatch, missing crossing gap, неразрешённая factorization/overflow ambiguity, неупражнённая
rare branch, projection больше **45 days / 69,120 core-h**, либо race/publication failure. Абсолютный cap
брифа `100,000 core-h` остаётся backstop, но не заменяет более строгий 45-day gate.

Даже PASS не является разрешением production-run.

## Что обязан содержать возможный Grimm artifact

- точную half-open chunk convention и отдельную запись crossing pair;
- source/compiler/flags/host hashes и deterministic restart state;
- полный nonoverlap/coverage manifest;
- prime-count checkpoints и first/last/successor prime для каждого boundary;
- для каждого critical gap: complete factorizations, bipartite graph, matching, Hall slack, timings;
- два полных независимых replay outputs и маленький third-party checker;
- для counterexample: полный maximal block, primality/factor certificates и Hall subset `S` с
  `|N(S)|<|S|`.

Hashes подтверждают неизменность файлов, но не заменяют доказательство полноты generator.

## Вычеркнуть и почему

- **`d_k(p)`** — уже закрыто общей теоремой в мае 2026.
- **BHR claim audit** — frequency partitions потеряли labels; полный universe на два порядка выше budget.
- **Quaternary LP(42)** — оба исхода сильны, но лучший имеющийся baseline даёт raw цену порядка 18m core-h.
- **DTS** — FPGA search эвристический; отрицательный исход не exact и не сертифицирован.
- **Practical + polygonal** — effective cutoff имеет десятки цифр; уменьшение требует новой теории.
- **Brocard** — следующий decade превышает budget и даёт слабый null-result.
- **Oriented powerful** — дёшево, но уже мелется активным worker; новый finite bound слаб.
- **Factorial twin и Tribonacci–Niven** — counterexamples интересны, но отрицательный finite outcome не
  решает утверждение и не даёт симметричной публикации.
- **`P14`, circular sorting, rook** — точные математические цели, но нет честного C2 и/или активен прямой race.
- **Primorial positions и mixed OA(36)** — реальные frontiers, но decisive exhaustive computation и
  certificate format ещё не сформулированы.

## Продуктивность классов источников

| Класс | Что дал после verification | Вердикт для следующего цикла |
|---|---|---|
| Свежие arXiv papers с явным next boundary и ancillaries | `P14`, circular sorting, qLP42, DTS; быстро показали точную формулировку и ограничения метода. | **Продуктивен для кандидатов и быстрых kill.** |
| Публичные repos, commit history и source inspection | Пойманы heap leak `P14`, restricted predicates circular/DTS, отсутствие certificate architecture; даны реальные calibration anchors. | **Самый продуктивный класс для falsification.** |
| Author-hosted/institutional papers | Надёжно восстановлена peer-reviewed Grimm boundary. | **Продуктивен для C0.** |
| OEIS с прямыми entry/comments/code links | Хорош для определения объектов и first-unknown hints; rook/OA/factorial/Tribonacci не пережили publication/artifact audit. | **Supporting source, не frontier authority без второй опоры.** |
| Curated problem databases | Быстро обнаруживают ориентацию, related theorems и active workers; почти все top scores исчезли после C0–C4. | **Продуктивны для разведки и kill, не для cost claims.** |
| Broad arXiv/MO/TheoremDB keyword search | Много theorem-first, уже решённых, active-race или неограниченных задач. | **Низкий yield; применять только после точного predicate.** |
| Reddit/self-reports | Обнаружили race и дали гипотезу throughput Grimm. | **Только race/workload evidence; никогда certified frontier.** |

## Что осталось непроверенным

1. Код и full logs двух Grimm self-reports `10^11`/`10^13`; endpoint/crossing convention; их намерения.
2. Принимает ли конкретная площадка Grimm null-result как публикацию при полном artifact package.
3. Реальная topology 64 CPU: physical/logical counts, per-host models/RAM и межхостовый throughput.
4. Grimm rare-tail distribution вне self-report totals и реальная стоимость второго независимого прохода.
5. Стоимость leak-free/certifying cubic `P14`; finite bound `12,286` не даёт runtime.
6. Текущий статус работы circular-sorting authors над `t(22)/t(24)`.
7. Exact lower-bound solver для rook `n=27`: GitHub доступен через `git`, но найденные Python scripts сами
   помечают части generator как broken/probably broken и не содержат proof package.
8. Независимый proof package для primorial `h(58)…h(64)` и точная цена position row `n=55`.
9. Полный formal specification/enumerator для mixed OA `Λ_36`.
10. Не появился ли после 2025 новый qLP(42) construction; negative cost всё равно не проходит текущий cap.

## Сеть агентов

Среда допускает root плюс три concurrent workers и не позволила создать новые thread IDs после заполнения
исторического лимита. Поэтому работа шла волнами: **18 отдельных role assignments** трем subagents — три
source-class scouts, три blind verification passes, шесть candidate-specific oppose passes, три counter
passes, adversarial edge audit, cost audit и final winner audit — затем независимый главный review. Один
и тот же worker не верифицировал собственный scout lead; oppose и counter для восстановимых кандидатов
выполняли разные workers.

Окончательная формулировка результата: **не начинать новую production-тему. Сначала провести один час Grimm
artifact pilot; при любом незакрытом gate закончить отбор ответом “победителя нет”.**
