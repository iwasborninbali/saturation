"""verdict_tree_glucose.py — древесный вердикт по независимому прогону Glucose.

Написано после того, как второй солвер обнаружил у себя худший вид ошибки: инструмент вердикта
измерял ПОДДЕРЕВО (448 кусков — это разложение одного куска верхнего уровня из шестидесяти
четырёх) и докладывал это как состояние всей задачи. Закрытие всех 448 само по себе не доказало бы
ничего, а инструмент об уровне выше не знал вовсе.

Здесь структура НЕ зашита: она выводится из имён кусков. `case_00007_s013_s002` — потомок
`case_00007_s013`, тот — потомок `case_00007`. Узел закрыт, если у него есть собственный UNSAT
ИЛИ закрыты все 64 его потомка. Корень закрыт, если закрыты все 64 куска верхнего уровня.

Правило трёх статусов прежнее: закрывает только явный UNSAT; SAT где угодно рушит заявление;
всё прочее — отсутствие сведений.

    python3 verdict_tree_glucose.py журнал [журнал ...]
"""
import sys
from collections import defaultdict

BRANCH = 64                       # подмножеств размера <= 3 из 7
own_unsat, sat_lines, other = set(), [], defaultdict(list)
for path in sys.argv[1:]:
    for ln in open(path, errors="replace"):
        t = ln.split()
        if not t or not t[0].startswith("case_"):
            continue
        name = t[0][:-4] if t[0].endswith(".cnf") else t[0]
        words = set(t)
        if "UNSAT" in words:
            own_unsat.add(name)
        elif "SAT" in words or "ВЫПОЛНИМ" in ln:
            sat_lines.append((name, path))
        else:
            other[name].append(" ".join(t[1:3]))

# Промежуточные узлы могут не встречаться в журналах вовсе: если кусок дробили, его собственной
# строки нет, есть только строки листьев. Поэтому цепочку предков надо достраивать целиком, иначе
# лист третьего уровня не свяжется с корнем и вердикт занизит покрытие (в безопасную сторону,
# но неверно). Эта ошибка была в первой версии и найдена первым же прогоном.
seen = set(own_unsat) | set(other)
children = defaultdict(set)
for nm in list(seen):
    cur = nm
    while "_s" in cur:
        par = cur.rsplit("_s", 1)[0]
        children[par].add(cur)
        cur = par

memo = {}
def closed(nm):
    if nm in memo: return memo[nm]
    memo[nm] = False                       # защита от цикла
    if nm in own_unsat:
        memo[nm] = True; return True
    kids = children.get(nm, set())
    r = len(kids) == BRANCH and all(closed(k) for k in kids)
    memo[nm] = r
    return r

top = [f"case_{i:05d}" for i in range(BRANCH)]
top_closed = [t for t in top if closed(t)]
top_open = [t for t in top if not closed(t)]
print(f"верхний уровень: закрыто {len(top_closed)} из {BRANCH}")
for t in top_open:
    kids = children.get(t, set())
    ck = sum(1 for k in kids if closed(k))
    print(f"  НЕ закрыт {t}: потомков увидено {len(kids)} из {BRANCH}, из них закрыто {ck}")
print(f"строк UNSAT всего: {len(own_unsat)}; строк «нет сведений»: {sum(len(v) for v in other.values())}")
print(f"ВЫПОЛНИМЫХ: {len(sat_lines)}  {sat_lines[:2]}")
if sat_lines:
    print("ВЕРДИКТ: ЗАЯВЛЕНИЕ РУШИТСЯ — найден выполнимый кусок"); sys.exit(9)
print("ВЕРДИКТ:", "ВСЯ ЗАДАЧА ЗАКРЫТА Glucose" if not top_open
      else f"НЕ ЗАКРЫТА — открыто {len(top_open)} кусков верхнего уровня. "
           f"Доля закрытых НЕ есть мера близости: незакрытые куски наименее ограничены.")
