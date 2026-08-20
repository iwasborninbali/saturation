"""verdict_union.py — пересчёт покрытия из ОБЪЕДИНЕНИЯ атомарных фактов обеих сторон.

Складывать числа нельзя: пересечение удвоится (так получилось «584 из 448»). Объединять имена
можно: объединение множеств идемпотентно, и сколько бы раз один и тот же кусок ни перерешали,
покрытие не завысится. Здесь читаются ВСЕ файлы фактов, и покрытие ВЫВОДИТСЯ заново — потому что
покрытие есть вывод, а не измерение, и каждая сторона обязана делать его сама.

Правило: узел закрыт, если он есть среди фактов ЛИБО если закрыты все 64 его потомка вида _sK.
Вопрос закрыт, когда закрыты все 64 узла верхнего уровня.

    python3 verdict_union.py facts1.txt facts2.txt ...
"""
import sys
from collections import defaultdict

BRANCH = 64
facts, src = set(), defaultdict(set)
for p in sys.argv[1:]:
    n0 = len(facts)
    for ln in open(p, errors="replace"):
        s = ln.strip()
        if not s or s.startswith("#"): continue
        nm = s.split()[0]
        nm = nm[:-4] if nm.endswith(".cnf") else nm
        facts.add(nm); src[p].add(nm)
    print(f"  {p}: имён {len(src[p])}, новых {len(facts)-n0}")

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
    kids = children.get(nm, set())
    r = len(kids) == BRANCH and all(closed(k) for k in kids)
    memo[nm] = r
    return r

top = [f"case_{i:05d}" for i in range(BRANCH)]
op = [t for t in top if not closed(t)]
inter = set.intersection(*src.values()) if len(src) > 1 else set()
print(f"объединение фактов: {len(facts)} имён; пересечение источников: {len(inter)}")
print(f"верхний уровень: закрыто {BRANCH-len(op)} из {BRANCH}")
for t in op:
    kids = children.get(t, set())
    print(f"  открыт {t}: потомков увидено {len(kids)} из {BRANCH}, из них закрыто "
          f"{sum(1 for k in kids if closed(k))}")
print("ИТОГ:", "ЗАКРЫТО ЦЕЛИКОМ" if not op else f"НЕ ЗАКРЫТО, открытых сверху {len(op)}")
