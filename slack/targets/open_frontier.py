"""open_frontier.py — очередь НЕЗАВИСИМЫХ открытых кусков, вычисленная из фактов.

Рекурсия последовательна по устройству: родитель вызывает ребёнка и ждёт, поэтому одна цепочка
занимает ровно одно ядро, сколько бы их ни было. Лечится не веером внутри рекурсии (он растёт
как 64^глубина), а выпрямлением работы в очередь: параллелизм отдаётся xargs снаружи, а рекурсия
внутри куска остаётся последовательной.

Открытый кусок — ребёнок РАЗБИТОГО узла, у которого нет ни собственного закрытия, ни своих детей.
Узел считается разбитым, если среди фактов есть хоть один его потомок.

    python3 open_frontier.py > очередь.txt
"""
import glob, sys
from collections import defaultdict

def norm(nm):
    """Нормализация имени: каждое звено _sN к трёхзначному виду.
    У сторон разная запись индексов — _s7 против _s007, — и один узел под двумя именами даёт
    родителю 128 детей вместо 64, после чего правило «закрыт при всех 64» не сработает НИКОГДА.
    Нормализуем при ЧТЕНИИ, чтобы старые файлы не пришлось переписывать."""
    import re as _re
    return _re.sub(r"_s(\d+)", lambda m: "_s%03d" % int(m.group(1)), nm)

BRANCH = 64
facts = set()
for p in glob.glob("logs/a280537/facts_*solver*.txt"):
    if "ОТОЗВАН" in p: continue
    for ln in open(p, errors="replace"):
        s = ln.strip()
        if not s or s.startswith("#"): continue
        nm = s.split()[0]
        facts.add(norm(nm[:-4] if nm.endswith(".cnf") else nm))

children = defaultdict(set)
for nm in facts:
    cur = nm
    while "_s" in cur:
        par = cur.rsplit("_s", 1)[0]
        children[par].add(cur)
        cur = par

memo = {}
def closed(nm):
    if nm in memo: return memo[nm]
    memo[nm] = False
    if nm in facts: memo[nm] = True; return True
    k = children.get(nm, set())
    r = len(k) == BRANCH and all(closed(x) for x in k)
    memo[nm] = r
    return r

out = []
for parent in list(children):
    if closed(parent): continue
    for i in range(BRANCH):
        ch = f"{parent}_s{i:03d}"
        if closed(ch): continue
        if ch in children: continue          # уже разбит — его дети сами попадут в очередь
        out.append(ch)
for nm in sorted(set(out)):
    print(nm)
print(f"# открытых независимых кусков: {len(set(out))}", file=sys.stderr)
