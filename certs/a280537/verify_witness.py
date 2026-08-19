"""verify_witness.py — независимая проверка свидетеля A280537: перебор ВСЕХ четвёрок в целочисленной
арифметике. Намеренно не использует ни списка плоскостей, ни какой-либо структуры перечислителя:
единственный вход — координаты точек, единственный критерий — определитель.
usage: python3 verify_witness.py n "(x,y,z) (x,y,z) ..."   |   python3 verify_witness.py --file f.txt"""
import re, sys
from itertools import combinations
def det3(a,b,c,d):
    u=[b[i]-a[i] for i in range(3)];v=[c[i]-a[i] for i in range(3)];w=[d[i]-a[i] for i in range(3)]
    return u[0]*(v[1]*w[2]-v[2]*w[1])-u[1]*(v[0]*w[2]-v[2]*w[0])+u[2]*(v[0]*w[1]-v[1]*w[0])
def check(n, pts):
    assert len(set(pts))==len(pts), "точки не различны"
    assert all(0<=c<n for p in pts for c in p), "точка вне куба"
    bad=[q for q in combinations(pts,4) if det3(*q)==0]
    print(f"n={n}: точек {len(pts)}, компланарных четвёрок {len(bad)}"
          + (f"  ПЕРВАЯ: {bad[0]}  — СВИДЕТЕЛЬ НЕВЕРЕН" if bad else "  — свидетель ЧИСТ"))
    return not bad
if __name__=="__main__":
    if sys.argv[1]=="--file":
        txt=open(sys.argv[2]).read()
    else:
        n=int(sys.argv[1]); txt=sys.argv[2]
        pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',txt)]
        sys.exit(0 if check(n,pts) else 1)
    ok=True
    for line in txt.splitlines():
        pts=[tuple(map(int,m)) for m in re.findall(r'\((\d+),(\d+),(\d+)\)',line)]
        if len(pts)>=4:
            n=max(c for p in pts for c in p)+1
            ok &= check(n,pts)
    sys.exit(0 if ok else 1)
