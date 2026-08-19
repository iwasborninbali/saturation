"""plane4_cnf.py — кодировка A280537 в SAT: есть ли в [n]^3 множество из M точек без четырёх компланарных?

Зачем SAT, а не перебор. Дерево перебора растёт примерно в 5 раз быстрее на каждом шаге по n
(точные размеры решающих деревьев: 35, 3406, 1 769 732 при n = 2,3,4), и экстраполяция на n = 7
даёт порядок 10^18 узлов — недостижимо ни числом машин, ни настройкой отсечений, ни симметрией
куба (она даёт всего x48). Но в форме «в каждой плоскости не более трёх точек» задача имеет всего
n^3 булевых переменных (343 при n = 7) и кардинальные ограничения — это образцовый вход для SAT,
а UNSAT даёт проверяемый третьей стороной сертификат.

Кодировка:
  x_i          — клетка i выбрана;
  для каждой плоскости с k >= 4 узлами: at-most-3 (прямые клаузы при k <= 8, счётчик Синца иначе);
  глобально: at-least-M.

Реализация НАМЕРЕННО на другом языке и по другой логике, чем перечислители, — это третья
независимая точка зрения на ту же задачу.

usage: python3 plane4_cnf.py n M out.cnf
"""
import sys
from itertools import combinations
from math import gcd

def planes(n):
    """все плоскости с >= 4 узлами решётки [n]^3, перечисленные ПО ТРОЙКАМ УЗЛОВ (потерять нельзя)"""
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}
    seen = set()
    for a, b, c in combinations(cells, 3):
        u = (b[0]-a[0], b[1]-a[1], b[2]-a[2]); v = (c[0]-a[0], c[1]-a[1], c[2]-a[2])
        nx = u[1]*v[2]-u[2]*v[1]; ny = u[2]*v[0]-u[0]*v[2]; nz = u[0]*v[1]-u[1]*v[0]
        if (nx, ny, nz) == (0, 0, 0): continue          # три точки коллинеарны — плоскости нет
        d = nx*a[0]+ny*a[1]+nz*a[2]
        g = gcd(gcd(abs(nx), abs(ny)), abs(nz))
        nx, ny, nz, d = nx//g, ny//g, nz//g, d//g
        if (nx, ny, nz) < (0, 0, 0) or (nx < 0 or (nx == 0 and (ny < 0 or (ny == 0 and nz < 0)))):
            nx, ny, nz, d = -nx, -ny, -nz, -d
        seen.add((nx, ny, nz, d))
    out = []
    for (nx, ny, nz, d) in seen:
        m = [idx[c] for c in cells if nx*c[0]+ny*c[1]+nz*c[2] == d]
        if len(m) >= 4: out.append(m)
    return len(cells), out

class CNF:
    def __init__(s, nv): s.nv = nv; s.cl = []
    def new(s): s.nv += 1; return s.nv
    def add(s, *lits): s.cl.append(list(lits))
    def atmost(s, lits, k):
        """счётчик Синца (2005): at-most-k над lits, O(k*|lits|) клауз и переменных"""
        n = len(lits)
        if n <= k: return
        if k == 3 and n <= 8:                       # при малых плоскостях прямая кодировка дешевле
            for q in combinations(lits, k + 1):
                s.add(*[-x for x in q])
            return
        sv = [[s.new() for _ in range(k)] for _ in range(n-1)]
        s.add(-lits[0], sv[0][0])
        for j in range(1, k): s.add(-sv[0][j])
        for i in range(1, n-1):
            s.add(-lits[i], sv[i][0]); s.add(-sv[i-1][0], sv[i][0])
            for j in range(1, k):
                s.add(-lits[i], -sv[i-1][j-1], sv[i][j]); s.add(-sv[i-1][j], sv[i][j])
            s.add(-lits[i], -sv[i-1][k-1])
        s.add(-lits[n-1], -sv[n-2][k-1])
    def write(s, path, comment=""):
        with open(path, "w") as f:
            if comment: f.write(f"c {comment}\n")
            f.write(f"p cnf {s.nv} {len(s.cl)}\n")
            f.write("".join(" ".join(map(str, c)) + " 0\n" for c in s.cl))

def build(n, M, path):
    nc, pl = planes(n)
    F = CNF(nc)
    x = lambda i: i + 1
    for m in pl: F.atmost([x(i) for i in m], 3)
    F.atmost([-x(i) for i in range(nc)], nc - M)        # at-least-M = at-most-(nc-M) отрицаний
    F.write(path, f"A280537 n={n} M={M}: {nc} cells, {len(pl)} rich planes; SAT <=> a({n}) >= {M}")
    print(f"n={n} M={M}: клеток {nc}, богатых плоскостей {len(pl)}, переменных {F.nv}, клауз {len(F.cl)} -> {path}")

if __name__ == "__main__":
    build(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])
