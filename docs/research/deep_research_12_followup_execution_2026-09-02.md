# Deep research 12 — execution-отчёт follow-up-аудита

Дата запуска и остановки: 2026-09-02

Статус: scout остановлен по просьбе пользователя; завершённые результаты сохранены, незавершённые явно
помечены.

## Итог

Три заранее поставленных вопроса получили разные ответы:

1. **Persistent assumptions полезны как инфраструктура, но failed-core reuse не прошёл алгоритмический
   gate.** Повторная загрузка базы почти исчезла, однако на `16` stubborn cubes fresh и persistent потратили
   практически одинаковые ticks и не закрыли ни одного. Easy cores дали `38` новых сертифицированных
   plane-cubes, но `0/286` исторически stubborn.
2. **`63` central-line binary clauses — KILL.** Они создали шесть новых BCP implications ровно на одном
   cube, но не добавили closures и не уменьшили ticks; на адресном длинном запуске были примерно на `20%`
   медленнее по wall-time.
3. **Proofix как единый route — NO-GO; как источник dispatcher-сигнала — перспективен, но не подтверждён
   вслепую.** На восьми parents Proofix и column дали почти одинаковую совокупную стоимость, при этом на
   отдельных parents победитель отличался в `2–19×`. Post-hoc признак «Proofix выбрал хотя бы две auxiliary
   variables» идеально разделил крупные победы кроме практически равного случая, но финальная blind-проверка
   была остановлена до получения результатов.

Production-run по итогам scout **не запущен**.

## 1. Зафиксированная база и выборка

Base CNF:

- задача: A280537, `n=7`, target `M=19`, `47` lex leaders;
- `392 351` variables;
- `2 781 167` clauses;
- SHA-256: `031dfc2ff1cbcf4638b4127f1b1f017556091ffab65e4c37357a5976b4d2f4b7`;
- solver: CaDiCaL `3.0.1`.

Frozen manifest: `logs/a280537/followup_audit_manifest.tsv`.

- SHA-256: `fe5906e2559e63c7f68b57adc8025d328a04e950d2218a01c5b0292dde42a068`;
- seed: `20260902`;
- `32` parents, по `8` в каждом stratum:
  `easy_low`, `easy_triple`, `stubborn_low`, `stubborn_triple`;
- внутри strata parents выбраны по квантилям полного индекса `0..19 649`, затем порядок детерминированно
  перемешан.

Исторические labels не переинтерпретировались: `easy` означает наличие старого closure-факта, `stubborn` —
timeout в `logs/a280537/plane_stubborn_pieces.txt`. Это не гарантирует ту же классификацию у CaDiCaL.

## 2. Persistent assumptions и failed cores

### 2.1. Paired stage: все 32 parents, cap 10M ticks

| Режим | Закрыто | Search ticks | Загрузка базы | Solve wall |
|---|---:|---:|---:|---:|
| fresh instance на каждый cube | `16/32` | `160 632 353` | `45.097 s` | `8.465 s` |
| один persistent instance | `16/32` | `160 470 378` | `1.387 s` | `9.648 s` |

Оба режима закрыли ровно `8/8 easy_low` и `8/8 easy_triple`. Все `16` stubborn остались UNKNOWN по cap.
Отношение search ticks практически `1.00`; ускорение полного wall-time `4.85×` происходит только из-за
однократного чтения и построения 52-МБ базы.

### 2.2. Hard-only stage: 16 stubborn parents, cap 100M ticks

| Режим | Закрыто | Search ticks | Загрузка базы | Solve wall |
|---|---:|---:|---:|---:|
| fresh | `0/16` | `1 600 670 396` | `26.733 s` | `85.782 s` |
| persistent | `0/16` | `1 600 370 935` | `1.376 s` | `51.847 s` |

Persistent выполнил тот же capped объём быстрее по wall-time (`1.65×` на solve, `2.11×` вместе с загрузкой),
но не создал ни одного closure/core на тяжёлом хвосте. По заранее объявленному критерию это **не**
cross-cube algorithmic PASS. Это отдельный **operational PASS** для amortization и тёплого solver state.

### 2.3. Форма и покрытие cores

Из `16` easy closures получено `16` failed cores.

- сумма индивидуальных покрытий: `7 304` plane-cubes;
- точное объединение: `6 956 / 19 650 = 35.40%`;
- уже присутствовали в объединении старых facts: `6 918`;
- новые относительно двух facts-файлов: `38`;
- исторически stubborn, покрытых cores: `0 / 286`.

Только четыре cores добавили новое покрытие:

| Source cube | `(p,q)` | Полное покрытие | Новое | Kissat DRAT | drat-trim |
|---|---:|---:|---:|---:|---:|
| `plx0_18-20` | `(1,25)` | `277` | `28` | `0.488 s`, `441 599 B` | VERIFIED, `2.482 s` |
| `plx0_24-41` | `(1,41)` | `29` | `5` | `0.459 s`, `455 855 B` | VERIFIED, `2.054 s` |
| `plx0_44-45` | `(2,38)` | `10` | `5` | `0.536 s`, `468 777 B` | VERIFIED, `2.065 s` |
| `plx0_44-45-46` | `(2,36)` | `12` | `5` | `0.538 s`, `468 783 B` | VERIFIED, `2.067 s` |

Из-за overlap четыре строки дают `38`, а не `43` уникальных новых cubes. Каждый core независимо replayed как
`base ∧ core`, Kissat вернул UNSAT и `drat-trim` проверил proof. Эти `38` — настоящий сертифицированный
прогресс, но они составляют меньше `1%` видимого остатка и не касаются известного тяжёлого класса.

### Вердикт

- **KEEP:** persistent runner как способ не перечитывать базу и сохранять тёплое состояние.
- **NO-GO как основная оптимизация:** текущие failed cores не переиспользуются на stubborn tail.
- **Не сделано:** incremental proof composition для одного длинного persistent-сеанса; proof проверялись
  отдельным replay полезных cores.

## 3. `63` central-line binary clauses

В generator добавлен флаг `--central-lines`. Код не просто добавляет `63` clauses для текущего случая, а
проверяет soundness gate: `n` нечётно и `M > 2 + число классов центрального pencil`; при `n=7` это
`M>18`. Mutation test требует отказа при `M=18`.

CNF с cuts:

- те же `392 351` variables;
- `2 781 230` clauses, ровно `+63`.

### 3.1. Все 32 parents, cap 10M ticks

| Arm | Закрыто | Все ticks | Stubborn ticks |
|---|---:|---:|---:|
| base | `16/32` | `160 632 353` | `160 631 280` |
| `+63` | `16/32` | `160 820 365` | `160 819 292` |

`+63` использовал в `1.00117×` больше stubborn ticks — чистый шум, но точно не требуемый выигрыш `≥1.1×`.
BCP result изменился на `1/32` cubes: в `plx0_24` выбор центральной клетки слоя `x=0` сразу запретил шесть
остальных точек центральной x-оси. Immediate conflict не появился.

### 3.2. Адресный длинный stage на `plx0_24`, cap 500M ticks

| Arm | Result | Ticks | Conflicts | Solve wall |
|---|---:|---:|---:|---:|
| base | UNKNOWN | `500 034 500` | `27 925` | `33.503 s` |
| `+63` | UNKNOWN | `500 057 560` | `27 814` | `40.069 s` |

При практически равных ticks cuts были в `1.196×` медленнее по wall-time и ничего не закрыли.

### Вердикт

**KILL.** Лемма и реализация корректны, но performance gate уверенно не пройден. Флаг оставлен для
воспроизводимости, не как рекомендуемый production default.

## 4. Исправленный Proofix comparator

### 4.1. Отзыв раннего mini-pilot

Ранее сообщённые `0/16` и `0/64` closures недействительны: временный conquer-скрипт обновлял `$4` в первой
строке файла, но первой строкой был комментарий `c ...`, а не `p cnf`. В результате число добавленных unit
clauses в header не менялось. Этот результат полностью отозван; ниже используются только CNF, созданные
header-aware materializer и прочитанные CaDiCaL API runner.

Proofix потребовал две compatibility-оговорки:

- официальный wrapper передаёт CaDiCaL `-q`, которого нет в CaDiCaL `3.0.1`; во временной копии аргумент
  удалён;
- parser Proofix ожидает `p cnf` в первой строке, поэтому parent CNF подавались без валидного, но не
  поддержанного им начального комментария.

### 4.2. Общий протокол

На каждом parent сравнивались три исчерпывающих 64-leaf split:

- Proofix: depth `6`, cutoff `20 000`, `4` samples, score `sum`, seed `1`;
- column: все `64` допустимых содержимых следующего z-столбца `(x,y)=(1,0)`;
- random: полный hypercube по шести случайным original-cell variables — только в calibration.

Каждый leaf решался **fresh** CaDiCaL `3.0.1`, cap `10M` ticks. Поэтому learned state между siblings не
переносился и не мог предпочесть один schedule.

### 4.3. Calibration, четыре parents

| Parent | Proofix aux vars | Proofix | Column | Random |
|---|---:|---:|---:|---:|
| `plx0_24` | `0/6` | `8/64`, `561 983 666` | **`62/64`, `29 287 402`** | `8/64`, `562 848 585` |
| `plx0_47-48` | `2/6` | `56/64`, `80 318 002` | `56/64`, `80 163 411` | `1/64`, `633 353 037` |
| `plx0_13-15-42` | `6/6` | **`63/64`, `10 011 909`** | `40/64`, `247 665 406` | `51/64`, `180 901 296` |
| `plx0_20-23-33` | `3/6` | **`52/64`, `120 674 600`** | `35/64`, `291 215 011` | `31/64`, `344 609 993` |
| **Сумма** | — | `179/256`, `772 988 177` | **`193/256`, `648 331 230`** | `91/256`, `1 721 712 911` |

Здесь фиксированный Proofix проиграл column и по closures, и в `1.19×` по ticks. При этом два
triple-parents показали крупный выигрыш Proofix, а `plx0_24` — катастрофический проигрыш.

### 4.4. Discovery holdout, ещё четыре parents

Random-arm после явного проигрыша удалён; параметры двух остальных arms не менялись.

| Parent | Proofix aux vars | Proofix | Column |
|---|---:|---:|---:|
| `plx0_20-42` | `2/6` | **`50/64`, `140 656 734`** | `35/64`, `291 228 334` |
| `plx0_37-39` | `1/6` | `32/64`, `320 807 562` | **`59/64`, `50 223 269`** |
| `plx0_13-40-43` | `5/6` | **`60/64`, `40 071 781`** | `46/64`, `181 831 825` |
| `plx0_18-31-36` | `2/6` | **`48/64`, `160 979 051`** | `38/64`, `264 805 608` |
| **Сумма** | — | **`190/256`, `662 515 128`** | `178/256`, `788 089 036` |

Proofix выиграл эту четвёрку в `1.19×`, что ниже заранее установленного gate `1.5×`.

### 4.5. Aggregate и post-hoc dispatcher

На всех восьми измеренных parents:

| Fixed route | Закрыто | Capped ticks |
|---|---:|---:|
| Proofix | `369/512` | `1 435 503 305` |
| Column | `371/512` | `1 436 420 266` |

Разница всего `0.06%`: **Proofix как единый route не выигрывает**.

Однако результат сильно коррелировал с числом auxiliary variables среди шести выбранных Proofix vars:

- `0` или `1` auxiliary: column резко лучше;
- `2`: один почти tie и два выигрыша Proofix;
- `3`, `5`, `6`: Proofix лучше.

Post-hoc правило `aux_count >= 2 ? Proofix : column` на тех же восьми строках дало бы:

- `450/512` closures;
- `632 222 748` capped ticks;
- `2.27×` меньше ticks, чем always-column, при `79` дополнительных быстрых closures.

Это **не PASS**, потому что predictor сформулирован после просмотра результатов.

### 4.6. Что не успело завершиться

Перед финальной проверкой был сохранён blind protocol:
`logs/a280537/followup_audit_blind_protocol.txt`.

В нём заранее зафиксированы:

- правило `aux_count >= 2`;
- восемь оставшихся stubborn parents frozen manifest;
- тот же Proofix/column протокол;
- PASS: `≥1.5×` меньше capped ticks и не меньше closures против always-column.

По просьбе пользователя run остановлен во время построения Proofix splits:

- полностью построенных blind ICNF: `0/8`;
- conquer batches: `0/16`;
- blind closures/ticks: **нет данных**.

Следовательно, dispatcher остаётся главным незавершённым кандидатом, а не production-рекомендацией.

## 5. Созданная воспроизводимая оснастка

- `slack/targets/a280537_followup_manifest.py` — frozen stratified manifest и hashes;
- `slack/targets/cadical_assumption_audit.cpp` — fresh/persistent/BCP runner с ticks и failed cores;
- `slack/targets/materialize_assumption_cnf.py` — корректное добавление assumptions к DIMACS;
- `slack/targets/verify_a280537_failed_cores.py` — Kissat+DRAT replay полезных cores;
- `slack/targets/a280537_partition_manifest.py` — одинаковые 64-leaf Proofix/column/random manifests;
- `plane4_cnf.py --central-lines` — soundness-guarded реализация `63` clauses.

Локальные contracts после изменений: **12/12 PASS**.

## 6. Финальные решения

| Направление | Решение | Почему |
|---|---|---|
| Persistent process | **KEEP operationally** | резко убирает повторную загрузку и улучшает wall throughput |
| Failed-core reuse на hard tail | **NO-GO сейчас** | `0/16` stubborn closures; `0/286` stubborn покрыты easy cores |
| 38 новых core-covered cubes | **CERTIFIED local progress** | четыре независимых Kissat DRAT, все VERIFIED |
| `+63` central-line clauses | **KILL** | те же closures/ticks, длинный адресный тест медленнее |
| Fixed Proofix route | **NO-GO** | aggregate практически равен column, gate `1.5×` не достигнут |
| Aux-count dispatcher | **PROMISING, UNVERIFIED** | post-hoc `2.27×`, blind batch не выполнен |
| Production sweep | **НЕ ЗАПУЩЕН** | ни один новый алгоритмический route пока не прошёл честный blind gate |

## 7. Если к работе возвращаться

Единственный следующий опыт, прямо оправданный этими данными: завершить уже замороженный blind protocol
без изменения порога, parents или правила. Если `aux_count>=2` не даст `≥1.5×` на восьми blind parents,
dispatcher закрывается. Если даст — затем нужен proof-on pilot выбранного маршрута; только после него можно
обсуждать production.

Satsuma, PB и полный Proofix depth/cutoff sweep **не запускались**. Они сознательно оставлены за границей
этого отчёта, а не записаны как отрицательные результаты.
