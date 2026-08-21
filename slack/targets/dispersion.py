"""dispersion.py — рассеяны ли максимумы. Мера второго солвера, посчитанная в трёхмерии.

Вопрос: сколько точек делят между собой ДВА РАЗНЫХ максимума, и больше ли это, чем поделили бы
случайные наборы того же размера. Если ненамного больше — максимумы рассеяны, и понятие
«ближайший максимум» пусто, а локальное улучшение не может работать в принципе.
"""
import sys, random
from itertools import combinations
path, n, M = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
sets=[]
for ln in open(path):
    t=ln.split()
    if len(t)!=3*M: continue
    sets.append(frozenset(tuple(map(int,t[3*i:3*i+3])) for i in range(M)))
N=n**3
rng=random.Random(7)
K=min(len(sets), 400)
sample=rng.sample(sets, K) if len(sets)>K else sets
tot=0; cnt=0
for a,b in combinations(sample,2):
    tot+=len(a&b); cnt+=1
obs=tot/cnt if cnt else 0
exp=M*M/N                      # ожидание пересечения двух случайных M-подмножеств из N клеток
print(f"n={n}, M={M}, максимумов {len(sets)} (взято {K})")
print(f"   два РАЗНЫХ максимума делят: {obs:.2f} из {M}")
print(f"   случайные наборы делили бы:  {exp:.2f}")
print(f"   превышение: {100*(obs/exp-1):+.0f}%  ->  {'рассеяны' if obs/exp < 1.5 else 'сгруппированы'}")
