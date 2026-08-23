# -*- coding: utf-8 -*-
# Блоки против пробегов КВАДРАТОВ в F_p (включая 0; 0 склеивает пробеги у -1 и 1,
# если -1 квадрат) — правильное определение из section_blocks, лемма об edges.
from collections import defaultdict
def primes(a,b): return [n for n in range(a,b+1) if n>1 and all(n%d for d in range(2,int(n**.5)+1))]
def union_pts(p):
    return [(x,y) for x in range(-(p-1)//2,(3*p-1)//2+1) if x%p
            for y in range(0,2*p) if (x*y)%p in (1,p-1)]
ok=0; bad=[]
for p in primes(19,311):
    pts=union_pts(p); n=len(pts)
    parent=list(range(n))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def uni(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb
    key=[defaultdict(list) for _ in range(4)]
    for i,(x,y) in enumerate(pts):
        key[0][x].append(i); key[1][y].append(i); key[2][x-y].append(i); key[3][x+y].append(i)
    for kd in key:
        for v in kd.values():
            for j in v[1:]: uni(v[0],j)
    comp=defaultdict(int)
    for i in range(n): comp[find(i)]+=1
    sizes=sorted(comp.values())
    # пробеги подряд идущих КВАДРАТОВ в F_p (0 — квадрат); склейка через 0: подряд в Z/p
    sq=sorted({(a*a)%p for a in range(p)})
    S=set(sq)
    runs=[]
    seen=set()
    for t in sq:
        if t in seen: continue
        if (t-1)%p in S: continue   # не начало пробега (с учётом цикличности)
        L=[t]; seen.add(t); u=t
        while (u+1)%p in S and (u+1)%p not in seen:
            u=(u+1)%p; L.append(u); seen.add(u)
        runs.append(L)
    runs=[r for r in runs if len(r)>=2]
    exp_sizes=sorted(32*(len(r)-1) - (16 if 0 in r and r[0]!=0 and r[-1]!=0 else 0)
                     - (16 if r[0]==0 or (r[-1]+1)%p==0 or 0==r[0] else 0)
                     for r in runs)
    # закон размеров считаю проще и честнее: 32*(k-1), а каждое ребро с t=0 или t=p-1 даёт 16 вместо 32
    exp=[]
    for r in runs:
        s2=0
        for i in range(len(r)-1):
            t=r[i]
            s2 += 16 if (t==0 or (t+1)%p==0 or t%p==p-1 or (t)%p==0) else 32
        # ребро {t,t+1} вырождено при t=0 (два класса) и при t=p-1 (t+1=0)
        exp.append(s2)
    exp=sorted(exp)
    good=(len(comp)==len(runs) and sizes==exp and sum(sizes)==8*(p-1))
    if good: ok+=1
    else: bad.append((p,len(comp),len(runs),sizes[:5],exp[:5]))
print(f"простых проверено: {ok+len(bad)}, СОШЛОСЬ: {ok}, расхождений: {len(bad)}")
for b in bad[:8]: print("  РАСХОЖДЕНИЕ:",b)
