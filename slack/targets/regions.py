"""regions.py — какая ОБЛАСТЬ обогащена максимумами. Не признак, а область.

Мера: доля максимумов, обладающих свойством, делённая на долю случайных наборов того же размера,
обладающих им же. Больше единицы — область обогащена, в ней стоит искать.
"""
import sys, random, math
from math import gcd
from collections import Counter
path, n, M = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sets=[]
for ln in open(path):
    t=ln.split()
    if len(t)!=3*M: continue
    sets.append([tuple(map(int,t[3*i:3*i+3])) for i in range(M)])
cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
def prim(d):
    g=gcd(gcd(abs(d[0]),abs(d[1])),abs(d[2])); d=tuple(c//g for c in d)
    for c in d:
        if c: return d if c>0 else tuple(-x for x in d)
    return d
def ndirs(S): return len({prim((b[i]-a[i] for i in range(3)) if False else (b[0]-a[0],b[1]-a[1],b[2]-a[2])) for i,a in enumerate(S) for b in S[i+1:]})
def nlevels(S): return len({sum(p) for p in S})
def full_layers(S):
    c=Counter(p[2] for p in S); return sum(1 for v in c.values() if v==3)
def spread(S):
    c=Counter(p[2] for p in S); return max(c.values())
props={"различных направлений = C(M,2)": lambda S: ndirs(S)==M*(M-1)//2,
       "различных сумм координат <= M/2": lambda S: nlevels(S)<=M//2,
       "различных сумм координат >= M-1":  lambda S: nlevels(S)>=M-1,
       "слоёв z ровно с 3 точками >= 2":   lambda S: full_layers(S)>=2,
       "ни в одном слое z нет 3 точек":    lambda S: spread(S)<3}
rng=random.Random(11); NS=200000
rand=[rng.sample(cells,M) for _ in range(NS)]
print(f"n={n}, M={M}, максимумов {len(sets)}, случайных наборов {NS}")
print(f"{'свойство':<36} {'у максимумов':>13} {'у случайных':>12} {'обогащение':>11}")
for name,f in props.items():
    a=sum(1 for S in sets if f(S))/len(sets)
    b=sum(1 for S in rand if f(S))/NS
    e=(a/b) if b>0 else float('inf')
    print(f"{name:<36} {100*a:>12.2f}% {100*b:>11.4f}% {('×%.3g'%e) if b>0 else 'база 0':>11}")
