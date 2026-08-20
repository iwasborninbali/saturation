"""Открытый фронт = дети разбитых узлов, у которых нет собственного закрытия
и нет ни одного своего ребёнка. Это ровно те куски, которые НИКТО не считает."""
import sys
from collections import defaultdict

def _норм(nm):
    """НОРМАЛИЗАЦИЯ ПРИ ЧТЕНИИ. `_s7` и `_s007` — ОДИН узел, но разные строки, и узел,
    записанный двумя написаниями, не наберёт 64 детей ни под одним из них: правило покрытия
    не закроет его НИКОГДА. Направление ошибки безопасное (покрытие занижается, ложных
    закрытий нет), но работа на таком узле пропадает молча, а «никак не закрывается» мы оба
    весь день читали как трудность задачи.
    Нашёл первый решатель — не проверкой имён, а тем, что мера продвижения дала 100.0006%:
    масса больше единицы означает двойной счёт. У меня 126 узлов записаны двумя написаниями,
    но потеряно НОЛЬ полных разбиений — мои счётчики берут индекс через int(). Чиню всё равно:
    ноль ущерба сегодня — это везение, а не устройство.
    Источник — stream_subsplit.py (`__s{idx}` без подбивки), тот самый инструмент, чьи 280
    фактов уже отозваны за столкновение имён. Живые инструменты подбивают все.
    Лечим ЧТЕНИЕМ, а не переписыванием файлов: старые остаются, новые совместимы сами.
    """
    if "_s" not in nm: return nm
    p = nm.split("_s")
    try: return p[0] + "".join(f"_s{int(x):03d}" for x in p[1:])
    except ValueError: return nm

closed=set(); children=defaultdict(set)
for fp in sys.argv[1:]:
    for l in open(fp,encoding="utf-8"):
        l=l.strip()
        if not l or l.startswith("#"): continue
        if not l.startswith("case_"): continue
        l = _норм(l)
        closed.add(l)
        if "_s" in l:
            par=l.rsplit("_s",1)[0]; idx=int(l.rsplit("_s",1)[1])
            children[par].add(idx)
# узел «разбит», если у него есть хоть один закрытый ребёнок
split_nodes={p:c for p,c in children.items() if c}
work=[]
for p,got in split_nodes.items():
    if p in closed: continue          # сам закрыт — детей считать незачем
    for i in range(64):
        if i in got: continue
        nm=f"{p}_s{i:03d}"
        if nm in closed: continue
        if nm in children and children[nm]: continue   # у него уже есть свои дети — работа идёт
        work.append(nm)
work.sort(key=lambda s: (s.count("_s"), s))
print(f"ОТКРЫТЫХ КУСКОВ: {len(work)}")
from collections import Counter
c=Counter(w.count("_s") for w in work)
print("по глубине:", dict(sorted(c.items())))
for w in work[:15]: print("  ", w)
if len(work)>15: print(f"   ... и ещё {len(work)-15}")
open("/tmp/frontier.txt","w").write("\n".join(work)+"\n")
