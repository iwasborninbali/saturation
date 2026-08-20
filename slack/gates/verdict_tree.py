"""verdict_tree.py — вердикт по ДЕРЕВУ разбиения любой глубины.

Существует потому, что verdict19.sh проверял поддерево и МОЛЧА предполагал уровень над ним:
в нём стояло TOTAL=448, а 448 — это разбиение ОДНОГО куска верхнего уровня (case_00000).
Закрытие всех 448 само по себе не доказывает ничего: нужно ещё, чтобы были закрыты остальные
63 куска верхнего уровня, и это утверждение инструмент не проверял вовсе.

Здесь структура ВЫВОДИТСЯ из имён, а не задаётся числом. Узел закрыт, если
  (а) у него есть собственный результат UNSAT, ЛИБО
  (б) закрыты ВСЕ его дети, и детей ровно столько, сколько предписывает арифметика столбца.
Частичное покрытие не закрывает: «не знаю» не есть «нет».

usage: verdict_tree.py <n> <cap> <файлы-результатов...>
"""
import sys, re
from math import comb
from collections import defaultdict

n, cap = int(sys.argv[1]), int(sys.argv[2])
NSUB = sum(comb(n, k) for k in range(cap + 1))      # сколько детей обязано быть у разбитого узла

own = defaultdict(set)          # узел -> множество увиденных статусов
seen_child = defaultdict(set)   # узел -> множество индексов детей с результатом UNSAT
NAME = re.compile(r"^case_\d+(?:_s\d+)*$")

# Флаги ОТДЕЛЯЮТСЯ от имён файлов. Без этого "--export" уходил в список файлов,
# open() падал, и вся выгрузка молча не происходила.
FILES = [a for a in sys.argv[3:] if not a.startswith("--")]

# ФАЙЛЫ ФАКТОВ. Работа идёт на разных машинах у двух решающих независимо, и если у каждого свой
# вердикт по своей половине — общего вердикта нет ни у кого. Факт (узел с собственным UNSAT)
# публикуется в репозиторий, а вердикт ПЕРЕСЧИТЫВАЕТСЯ из объединения. Складывать чужие ЧИСЛА
# нельзя — это ровно то сложение счётчиков, что дало «584 из 448»; объединять ИМЕНА можно,
# потому что объединение множеств идемпотентно и пересечение не удваивается.
if "--facts" in sys.argv:
    i = sys.argv.index("--facts")
    for fp in sys.argv[i+1:]:
        if fp.startswith("--"): break
        try: fh = open(fp, encoding="utf-8")
        except OSError:
            print(f"  ВНИМАНИЕ: файла фактов {fp} нет — покрытие будет ЗАНИЖЕНО"); continue
        cnt = 0
        for l in fh:
            l = l.strip()
            if not l or l.startswith("#"): continue
            nd = l.split()[0]
            if nd.endswith(".cnf"): nd = nd[:-4]
            if NAME.match(nd): own[nd].add("UNSAT"); cnt += 1
        print(f"  фактов принято из {fp}: {cnt}")

for path in FILES:
    for line in open(path, encoding="utf-8", errors="replace"):
        p = line.split()
        if len(p) < 2: continue
        base = p[0][:-4] if p[0].endswith(".cnf") else p[0]
        if not NAME.match(base): continue
        # Форма строки, а не имя файла: <узел> <статус> ...  или  <узел> s<k> <статус> ...
        if len(p) >= 3 and re.fullmatch(r"s\d+", p[1]):
            child = f"{base}_{p[1]}"
            own[child].add(p[2])
        else:
            own[base].add(p[1])

# дети, известные по именам (узел X_sK — ребёнок X)
children = defaultdict(set)
for node in own:
    if "_s" in node:
        children[node.rsplit("_s", 1)[0]].add(node)

memo = {}
def closed(node):
    if node in memo: return memo[node]
    memo[node] = False                       # защита от циклов; их быть не должно
    if "UNSAT" in own.get(node, ()):
        memo[node] = True; return True
    kids = children.get(node, set())
    r = len(kids) == NSUB and all(closed(k) for k in kids)
    memo[node] = r
    return r

top = sorted(x for x in own if "_s" not in x)
missing_top = [f"case_{i:05d}" for i in range(NSUB) if f"case_{i:05d}" not in own]
sat = sorted(x for x, s in own.items() if "SAT" in s)

print(f"арифметика столбца: детей у разбитого узла обязано быть {NSUB}")
print(f"верхний уровень: имён найдено {len(top)}, ожидается {NSUB}")
if missing_top: print(f"  ОТСУТСТВУЮТ ВОВСЕ: {missing_top[:5]}{'...' if len(missing_top)>5 else ''}")
print(f"  ВЫПОЛНИМЫХ во всём дереве: {len(sat)}" + (f"  {sat[:3]}" if sat else "  — ни одного"))

open_top = [t for t in (f"case_{i:05d}" for i in range(NSUB)) if not closed(t)]
print(f"  закрыто кусков верхнего уровня: {NSUB - len(open_top)} из {NSUB}")

def explain(node, depth=0, limit=6):
    kids = children.get(node, set())
    if "UNSAT" in own.get(node, ()): return
    pad = "    " + "  " * depth
    if not kids:
        print(f"{pad}{node}: НЕ закрыт, статусы {sorted(own.get(node, ['<нет записей>']))}, разбиения нет")
        return
    if len(kids) != NSUB:
        print(f"{pad}{node}: разбит НЕПОЛНО — детей {len(kids)} из {NSUB}")
    bad = sorted(k for k in kids if not closed(k))
    print(f"{pad}{node}: не закрыто детей {len(bad)} из {NSUB}")
    for k in bad[:limit]: explain(k, depth + 1, limit)
    if len(bad) > limit: print(f"{pad}  ... и ещё {len(bad)-limit}")

for t in open_top: explain(t)

# Открытый фронт: узлы без собственного UNSAT и без ПОЛНОГО разбиения — их надо решить или разбить.
front = [nd for nd in own if not closed(nd) and len(children.get(nd, set())) < NSUB]
by_status = defaultdict(int)
for nd in front:
    for st in own[nd]: by_status[st] += 1
print(f"\nОТКРЫТЫЙ ФРОНТ: {len(front)} узлов")
for st, c in sorted(by_status.items(), key=lambda x: -x[1]):
    note = "  <- ОШИБКА решателя, кусок не решался вовсе" if st == "rc=1" else ""
    print(f"   {st:>8}: {c}{note}")

# Строка для наблюдателей: разбирать прозу они не должны.
print(f"ИТОГ верх={NSUB-len(open_top)}/{NSUB} фронт={len(front)} выполнимых={len(sat)}")

if "--export" in sys.argv:
    # САМОДОСТАТОЧНАЯ выгрузка. Множество ЛИСТЬЕВ покрытием не является: если часть узла закрыта
    # не листьями, сторонний проверяющий соберёт из листьев неполное покрытие и не поймёт почему.
    # Поэтому выгружаются АТОМАРНЫЕ ФАКТЫ — все узлы с собственным UNSAT на всех уровнях, — из
    # которых покрытие ПЕРЕСЧИТЫВАЕТСЯ по правилу, а не принимается на веру.
    out = "/tmp/verdict19/closed_all.txt"
    facts = sorted(nd for nd in own if "UNSAT" in own[nd])
    with open(out, "w") as fh:
        fh.write(f"# Атомарные факты для A280537 n={n} M=19: узлы с СОБСТВЕННЫМ UNSAT, все уровни.\n")
        fh.write(f"# Правило пересчёта: узел закрыт, если он здесь ЛИБО если здесь все {NSUB} его\n")
        fh.write(f"# потомков вида <узел>_sK, K = 0..{NSUB-1}. Вопрос закрыт, когда закрыты все\n")
        fh.write(f"# {NSUB} узлов верхнего уровня case_00000..case_{NSUB-1:05d}.\n")
        fh.write(f"# Список ЛИСТЬЕВ покрытием НЕ является — часть узлов закрыта на меньшей глубине.\n")
        for nd in facts: fh.write(nd + "\n")
    depth = defaultdict(int)
    for nd in facts: depth[nd.count("_s")] += 1
    print(f"  выгружено атомарных фактов: {len(facts)} -> {out}")
    print(f"  по глубине: {dict(sorted(depth.items()))}")

if sat:
    print("\nВЕРДИКТ: НАЙДЕН ВЫПОЛНИМЫЙ КУСОК — утверждение ЛОЖНО"); sys.exit(2)
if open_top or missing_top:
    print(f"\nВЕРДИКТ: НЕЛЬЗЯ заявлять — верхний уровень закрыт не полностью"); sys.exit(1)
print(f"\nВЕРДИКТ: ВСЁ ДЕРЕВО ЗАКРЫТО => утверждение доказано"); sys.exit(0)
