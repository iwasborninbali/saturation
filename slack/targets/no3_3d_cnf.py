"""no3_3d_cnf.py — SAT-кодировка трёхмерного no-three-in-line: есть ли в [n]^3 множество из M точек,
никакие три из которых не коллинеарны?

Перенос приёма, сработавшего на A280537. Прямая, содержащая <= 2 узла решётки, запретить ничего не
может, поэтому

    S допустимо  <=>  для КАЖДОЙ прямой L с >= 3 узлами:  |S ∩ L| <= 2.

Ограничение по осям (n^2 прямых, параллельных оси, по <= 2 точки) даёт a(n) <= 2n^2 и законную
обрезку счётчика.

Зачем это, когда перебор уже идёт: перебор доказывает полноту СОБСТВЕННЫМ аргументом о покрытии
префиксов, который проверяет только наша же программа. UNSAT даёт сертификат DRAT, проверяемый
чужой программой. Второе строго сильнее, и если оно ещё и быстрее — перебор становится независимой
сверкой, а не основным доказательством.

usage: python3 no3_3d_cnf.py n M out.cnf [--sym]
"""
import sys
from itertools import combinations
from math import gcd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from plane4_cnf import CNF, cube_group, lex_leader

def lines(n):
    """все прямые с >= 3 узлами решётки [n]^3, перечисленные ПО ПАРАМ узлов (потерять нельзя)"""
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}
    seen = {}
    for a, b in combinations(cells, 2):
        d = (b[0]-a[0], b[1]-a[1], b[2]-a[2])
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2]))
        d = (d[0]//g, d[1]//g, d[2]//g)
        if d < (0, 0, 0) or (d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0)))):
            d = (-d[0], -d[1], -d[2])
        # канонический представитель прямой: самая «ранняя» точка на ней внутри куба
        p = a
        while True:
            q = (p[0]-d[0], p[1]-d[1], p[2]-d[2])
            if all(0 <= t < n for t in q): p = q
            else: break
        seen.setdefault((p, d), None)
    out = []
    for (p, d) in seen:
        m, q = [], p
        while all(0 <= t < n for t in q):
            m.append(idx[q]); q = (q[0]+d[0], q[1]+d[1], q[2]+d[2])
        if len(m) >= 3: out.append(m)
    return len(cells), out

def build(n, M, path, sym=False, profile=None, axes=(0,1,2), invariant=None):
    """profile: список из n чисел — сколько точек в каждом слое, перпендикулярном ВСЕМ трём осям.
       Структурная форма задачи: она несравненно легче общей, потому что кардинальность
       распадается на n маленьких ограничений вместо одного большого. Именно так первый солвер
       нашёл конфигурацию на 64 точки при n=6 за восемь секунд.

       axes: по каким осям навязывать профиль. ЭТО СУЩЕСТВЕННО ДЛЯ ТОЛКОВАНИЯ ОТВЕТА.
         * SAT при любом наборе осей -> конфигурация существует -> законная НИЖНЯЯ граница.
         * UNSAT при ОДНОЙ оси -> ни одна конфигурация с таким распределением по этой оси
           не существует. Сильное утверждение.
         * UNSAT при трёх осях -> не существует конфигурации с таким СИММЕТРИЧНЫМ профилем.
           Это НЕ означает, что нет конфигурации с тем же числом точек: профиль по разным осям
           может различаться. Слабое утверждение, и путать их нельзя."""
    nc, ln = lines(n)
    F = CNF(nc); x = lambda i: i + 1
    for m in ln: F.atmost([x(i) for i in m], 2)
    if profile:
        assert len(profile) == n and sum(profile) == M, "профиль не согласован с M"
        for axis in axes:
            for t in range(n):
                cells = [x(i) for i in range(nc)
                         if (i//(n*n) if axis==0 else (i//n)%n if axis==1 else i%n) == t]
                F.atmost(cells, profile[t])                       # не больше
                F.atmost([-c for c in cells], len(cells)-profile[t])  # и не меньше
    F.atleast([x(i) for i in range(nc)], M, 2*n*n + 1)   # обрезка законна: a(n) <= 2n^2
    if invariant:
        # ПОИСК СРЕДИ ИНВАРИАНТНЫХ конфигураций (приём первого солвера).
        # Клетки склеиваются в орбиты выбранной подгруппы, переменных в |G| раз меньше,
        # и поиск резко ускоряется. ЗАКОННО ТОЛЬКО ДЛЯ НИЖНИХ ГРАНИЦ: что найдено — существует;
        # ненайденное здесь НЕ означает несуществующего, потому что несимметричные конфигурации
        # из рассмотрения исключены.
        for sigma in invariant:
            for i in range(nc):
                if i != sigma[i]:
                    F.add(-x(i), x(sigma[i])); F.add(x(i), -x(sigma[i]))
    ns = 0
    if sym:
        for sigma in cube_group(n): lex_leader(F, x, sigma, nc); ns += 1
    F.write(path, f"no-three-in-line 3D n={n} M={M}: {nc} cells, {len(ln)} rich lines, {ns} symmetries")
    print(f"n={n} M={M}{' +сим' if sym else ''}: клеток {nc}, богатых прямых {len(ln)}, переменных {F.nv}, клауз {len(F.cl)} -> {path}")

if __name__ == "__main__":
    prof = None
    if "--profile" in sys.argv:
        prof = [int(t) for t in sys.argv[sys.argv.index("--profile")+1].split(",")]
    ax = (0,1,2)
    if "--axes" in sys.argv: ax = tuple(int(t) for t in sys.argv[sys.argv.index("--axes")+1].split(","))
    inv = None
    if "--cyc3" in sys.argv:            # (x,y,z) -> (y,z,x): циклическая перестановка осей, порядок 3
        n0 = int(sys.argv[1])
        inv = [[ ((i//n0)%n0)*n0*n0 + (i%n0)*n0 + (i//(n0*n0)) for i in range(n0**3) ]]
    build(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sym=("--sym" in sys.argv), profile=prof, axes=ax, invariant=inv)
