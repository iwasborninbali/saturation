"""verify_witness.py — независимая проверка свидетеля A280537: перебор ВСЕХ четвёрок в целочисленной
арифметике. Намеренно не использует ни списка плоскостей, ни какой-либо структуры перечислителя:
единственный вход — координаты точек, единственный критерий — определитель.
usage: python3 verify_witness.py n ПУТЬ | n "(x,y,z) ..." | --file ПУТЬ [n [сколько]] | --selftest"""
import re, sys, os
from itertools import combinations
def det3(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)];w=[d[i]-a[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])
def check(n, pts, expect=None):
    if len(pts) < 3:
        print(f"  ОТКАЗ: свидетель ПУСТОЙ или слишком мал ({len(pts)} точек) — проверять нечего, это НЕ подтверждение")
        return False
    if expect is not None and len(pts) != expect:
        print(f"  ОТКАЗ: точек {len(pts)}, а ожидалось {expect}")
        return False
    if len(set(pts))!=len(pts): print("  ОТКАЗ: точки НЕ различны"); return False
    if not all(0<=c<n for p in pts for c in p): print("  ОТКАЗ: точка вне куба"); return False
    bad=[q for q in combinations(pts,4) if det3(*q)==0]
    print(f"n={n}: точек {len(pts)}, компланарных четвёрок {len(bad)}"
          + (f"  ПЕРВАЯ: {bad[0]}  — СВИДЕТЕЛЬ НЕВЕРЕН" if bad else "  — свидетель ЧИСТ"))
    return not bad
# Калибровочный случай берётся из АРТЕФАКТА, а не сочиняется.
_HERE=os.path.dirname(os.path.abspath(__file__))
def _parse(txt):
    cl="\n".join(l for l in txt.splitlines() if not l.strip().startswith("#"))
    pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',cl)]
    if not pts:
        pts=[tuple(int(t) for t in l.split()) for l in cl.splitlines()
             if len(l.split())==3 and all(t.lstrip("-").isdigit() for t in l.split())]
    return pts
GOOD_N=5
def GOOD_SAMPLE(): return _parse(open(os.path.join(_HERE,"witness_n5.txt")).read())
def PLANT_BAD(pts, rnd):
    # Четыре точки с общей координатой z компланарны по построению — определитель обязан обнулиться.
    for _ in range(200):
        z=rnd.randrange(GOOD_N)
        q=[(x,y,z) for x in range(GOOD_N) for y in range(GOOD_N)]
        rnd.shuffle(q); t=q[:4]
        if len(set(t))==4:
            return list(dict.fromkeys(t+[r for r in pts if r not in t]))
    return None
if __name__=="__main__":
    a=sys.argv[1:]
    if not a:
        print("  ОТКАЗ: нечего проверять"); sys.exit(1)
    if a[0]=="--selftest":
        # Проверяльщик, ни разу не показавший ОТКАЗ, не проверен.
        import random; ok=True
        for trial in range(20):
            rnd=random.Random(trial)
            good=GOOD_SAMPLE()
            if not check(GOOD_N,good):
                print(f"  СБОЙ САМОПРОВЕРКИ: чистый вход отвергнут (попытка {trial})"); ok=False; break
            bad=PLANT_BAD(list(good),rnd)
            if bad is None: continue
            if check(GOOD_N,bad):
                print(f"  СБОЙ САМОПРОВЕРКИ: ГРЯЗНЫЙ вход принят (попытка {trial}) — проверяльщик слеп"); ok=False; break
        print("  самопроверка ПРОЙДЕНА: чистое принимается, грязное отвергается" if ok else "  самопроверка ПРОВАЛЕНА")
        sys.exit(0 if ok else 1)
    if a[0]=="--file":
        txt=open(a[1]).read(); nums=a[2:]
    else:
        txt=open(a[1]).read() if (len(a)>1 and os.path.exists(a[1])) else (a[1] if len(a)>1 else "")
        nums=[a[0]]+a[2:]
    pts=_parse(txt)
    def _num(i): return int(nums[i]) if len(nums)>i and nums[i].lstrip("-").isdigit() else None
    n=_num(0); exp=_num(1)
    if n is None:
        if not pts: print("  ОТКАЗ: свидетель ПУСТОЙ — проверять нечего"); sys.exit(1)
        n=max(c for p in pts for c in p)+1
    sys.exit(0 if check(n,pts,exp) else 1)
