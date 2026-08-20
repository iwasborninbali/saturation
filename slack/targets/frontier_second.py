"""Открытый фронт = дети разбитых узлов, у которых нет собственного закрытия
и нет ни одного своего ребёнка. Это ровно те куски, которые НИКТО не считает."""
import sys
from collections import defaultdict
closed=set(); children=defaultdict(set)
for fp in sys.argv[1:]:
    for l in open(fp,encoding="utf-8"):
        l=l.strip()
        if not l or l.startswith("#"): continue
        if not l.startswith("case_"): continue
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
