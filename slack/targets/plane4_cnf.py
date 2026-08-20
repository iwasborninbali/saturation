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
    def totalizer(s, lits, cap):
        """унарный счётчик с обрезкой: o[j] <-> «истинных не менее j+1», обе импликации.
           Нужен потому, что at-least-M через счётчик Синца по отрицаниям стоит |lits|*(nc-M)
           переменных (111 тысяч при n=7) — больше всей остальной формулы. Из ограничения «в каждом
           слое не более трёх» сразу следует, что всего точек не более 3n, поэтому счётчик обрезается
           на 3n+1 и стоит O(|lits| * 3n)."""
        if len(lits) == 1: return [lits[0]]
        mid = len(lits)//2
        A = s.totalizer(lits[:mid], cap); B = s.totalizer(lits[mid:], cap)
        k = min(len(A)+len(B), cap)
        O = [s.new() for _ in range(k)]
        for a in range(len(A)+1):
            for b in range(len(B)+1):
                c = a+b
                if 0 < c <= k:                       # A_a & B_b -> O_{a+b}
                    cl = [O[c-1]]
                    if a: cl.append(-A[a-1])
                    if b: cl.append(-B[b-1])
                    s.add(*cl)
                if a < len(A) and b < len(B) or (c < k):   # ~A_{a+1} & ~B_{b+1} -> ~O_{a+b+1}
                    if c+1 <= k:
                        cl = [-O[c]]
                        if a < len(A): cl.append(A[a])
                        if b < len(B): cl.append(B[b])
                        s.add(*cl)
        return O

    def atleast(s, lits, m, cap):
        O = s.totalizer(lits, cap)
        assert m <= len(O), f"обрезка счётчика {len(O)} меньше требуемого {m}"
        s.add(O[m-1])

    def write(s, path, comment=""):
        with open(path, "w") as f:
            if comment: f.write(f"c {comment}\n")
            f.write(f"p cnf {s.nv} {len(s.cl)}\n")
            f.write("".join(" ".join(map(str, c)) + " 0\n" for c in s.cl))

def cube_group(n):
    """48 симметрий куба как перестановки индексов клеток: 6 перестановок осей x 8 отражений"""
    from itertools import permutations, product
    cells=[(x,y,z) for x in range(n) for y in range(n) for z in range(n)]
    idx={c:i for i,c in enumerate(cells)}
    G=[]
    for perm in permutations(range(3)):
        for sg in product((1,-1),repeat=3):
            sigma=[0]*len(cells)
            for c in cells:
                t=tuple(c[perm[k]] if sg[k]==1 else n-1-c[perm[k]] for k in range(3))
                sigma[idx[c]]=idx[t]
            if sigma!=list(range(len(cells))): G.append(sigma)
    return G

def lex_leader(F, x, sigma, nc):
    """x <=_lex sigma(x): оставляет в каждой орбите лексикографически минимальный элемент.
       Корректно, потому что свойство 'нет четырёх компланарных' инвариантно относительно группы,
       и значит вместе с любым решением лекс-минимальный представитель его орбиты тоже решение."""
    eq = None                                   # eq_i: префиксы совпали до позиции i включительно
    for i in range(nc):
        a, b = x(i), x(sigma[i])
        if a == b:                              # клетка неподвижна — сравнение тривиально
            continue
        if eq is None: F.add(-a, b)             # x_0 <= sigma(x)_0
        else:          F.add(-eq, -a, b)
        ne = F.new()                            # ne <-> eq & (a <-> b)
        if eq is None:
            F.add(-ne, -a, b); F.add(-ne, a, -b); F.add(ne, a, b); F.add(ne, -a, -b)
        else:
            F.add(-ne, eq); F.add(-ne, -a, b); F.add(-ne, a, -b)
            F.add(ne, -eq, a, b); F.add(ne, -eq, -a, -b)
        eq = ne

def build(n, M, path, sym=False, invariant=None, profiles=None):
    nc, pl = planes(n)
    F = CNF(nc)
    x = lambda i: i + 1
    for m in pl: F.atmost([x(i) for i in m], 3)
    if profiles:
        # ПРОФИЛЬ ПО НЕСКОЛЬКИМ ОСЯМ (предложение первого солвера).
        # У конфигурации есть определённый профиль вдоль КАЖДОЙ оси, поэтому разбиение по ПАРЕ
        # (профиль по x, профиль по y) исчерпывающе, если перечислены ВСЕ пары. Куски при этом
        # несут вдвое больше равенств и потому несравнимо жёстче.
        # Совместимо с симметрийным отсечением ровно потому, что перечисляются все пары:
        # лексминимальный представитель имеет какие-то профили, и кусок с ними в списке есть.
        # ПРОПУСК ХОТЯ БЫ ОДНОЙ ПАРЫ ОБЕСЦЕНИВАЕТ ВСЁ.
        for axis, prof in profiles.items():
            assert len(prof) == n and sum(prof) == M, f"профиль по оси {axis} не согласован с M"
            for t in range(n):
                cs = [x(i) for i in range(nc)
                      if (i//(n*n) if axis==0 else (i//n)%n if axis==1 else i%n) == t]
                F.atmost(cs, prof[t])
                F.atmost([-c for c in cs], len(cs)-prof[t])
    F.atleast([x(i) for i in range(nc)], M, 3*n + 1)    # обрезка законна: a(n) <= 3n (слой есть плоскость)
    if invariant:
        # поиск среди ИНВАРИАНТНЫХ конфигураций: законно только для нижних границ
        for sigma in invariant:
            for i in range(nc):
                if i != sigma[i]:
                    F.add(-x(i), x(sigma[i])); F.add(x(i), -x(sigma[i]))
    ns = 0
    if sym:
        for sigma in cube_group(n): lex_leader(F, x, sigma, nc); ns += 1
    F.write(path, f"A280537 n={n} M={M}: {nc} cells, {len(pl)} rich planes, {ns} symmetries broken; SAT <=> a({n}) >= {M}")
    print(f"n={n} M={M}{' +сим' if sym else ''}: клеток {nc}, плоскостей {len(pl)}, симметрий {ns}, переменных {F.nv}, клауз {len(F.cl)} -> {path}")

if __name__ == "__main__":
    inv = None
    if "--inv" in sys.argv:
        n0 = int(sys.argv[1]); name = sys.argv[sys.argv.index("--inv")+1]
        def enc(x,y,z): return (x*n0+y)*n0+z
        def dec(i): return (i//(n0*n0), (i//n0)%n0, i%n0)
        MAPS = {
            "cyc3":  lambda x,y,z: (y,z,x),                    # порядок 3
            "swapxy":lambda x,y,z: (y,x,z),                    # порядок 2
            "refx":  lambda x,y,z: (n0-1-x,y,z),               # порядок 2
            "point": lambda x,y,z: (n0-1-x,n0-1-y,n0-1-z),     # порядок 2, центральная
            "rot4z": lambda x,y,z: (y,n0-1-x,z),               # порядок 4
            "diag":  lambda x,y,z: (n0-1-y,n0-1-x,z),          # порядок 2
        }
        f = MAPS[name]
        inv = [[ enc(*f(*dec(i))) for i in range(n0**3) ]]
    elif "--cyc3" in sys.argv:
        n0 = int(sys.argv[1])
        inv = [[ ((i//n0)%n0)*n0*n0 + (i%n0)*n0 + (i//(n0*n0)) for i in range(n0**3) ]]
    profs = None
    if "--profiles" in sys.argv:      # формат: "0=3,3,3,3,3,2;1=3,3,3,3,2,3"
        profs = {}
        for part in sys.argv[sys.argv.index("--profiles")+1].split(";"):
            a, p = part.split("=")
            profs[int(a)] = [int(t) for t in p.split(",")]
    build(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sym=("--sym" in sys.argv),
          invariant=inv, profiles=profs)
