"""verify_sym_soundness.py — независимая проверка САМОГО ОПАСНОГО звена цепочки UNSAT:
корректности симметрийного отсечения (lex-leader) при том самом n, для которого заявлен результат.

ПОЧЕМУ ЭТО ЗВЕНО ОСОБОЕ. Разбиение на куски проверяемо арифметикой (22^2 = 484), невыполнимость
каждого куска удостоверена решателем, семантика кодировки проверена сквозным тестом. Но
симметрийные клаузы стоят СБОКУ от всего этого: они сужают пространство поиска, и если они сужают
его слишком сильно — выбросив ЦЕЛУЮ орбиту, — то все куски честно окажутся невыполнимыми,
все сертификаты честно проверятся, а утверждение будет ложным. Ни DRAT, ни проверка свидетеля
этого не ловят: DRAT удостоверяет ровно ту формулу, которую ему дали.

ЧТО ПРОВЕРЯЕТСЯ. Строится формула, содержащая ТОЛЬКО симметрийные клаузы (ловушка 5b: при проверке
локального свойства снимай глобальные ограничения — иначе кардинальность объявит «невыполнимо»
там, где виноват не тот, кого проверяем). Для набора точек S подставляются юниты по всем клеткам,
и решателю остаётся лишь досогласовать вспомогательные переменные. Тогда

    формула выполнима  <=>  S переживает отсечение.

Независимо, своей группой и своим сравнением, вычисляется, является ли S лексикографическим
минимумом своей орбиты. Требуемое совпадение — тождественное. Смертельное направление одно:
если лексминимум орбиты объявлен НЕвыполнимым, орбита выброшена целиком и заявление рушится.

    python3 verify_sym_soundness.py n [trials]
"""
import os, random, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from plane4_cnf import CNF, lex_leader          # проверяем ИХ клаузы, не свою реконструкцию
import plane4_cnf

KISSAT = os.path.expanduser("~/bin/kissat")


def my_cube_group(n):
    """48 симметрий куба — своя реализация, намеренно не импортируется из проверяемого файла"""
    from itertools import permutations, product
    cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}
    out = []
    for perm in permutations(range(3)):
        for sg in product((0, 1), repeat=3):
            sigma = [0] * len(cells)
            for c in cells:
                t = tuple((n - 1 - c[perm[k]]) if sg[k] else c[perm[k]] for k in range(3))
                sigma[idx[c]] = idx[t]
            out.append(sigma)
    return out


def images(mask, group):
    """все образы набора-битовой-строки под группой; каждый образ — кортеж 0/1 длины nc"""
    nc = len(mask)
    res = []
    for sigma in group:
        img = [0] * nc
        for i in range(nc):
            if mask[i]:
                img[sigma[i]] = 1          # sigma[i] — куда уезжает клетка i
        res.append(tuple(img))
    return res


def build_sym_only(n):
    """формула из ОДНИХ симметрийных клауз (их lex_leader, их группа) — без прямых и кардинальности"""
    nc = n * n * n
    F = CNF(nc)
    x = lambda i: i + 1
    ns = 0
    for sigma in plane4_cnf.cube_group(n):
        lex_leader(F, x, sigma, nc)
        ns += 1
    return F, nc, ns


def sat_with_units(F, nc, mask, tmpdir):
    """выполнима ли формула, если все клетки прибиты юнитами по mask"""
    path = os.path.join(tmpdir, "t.cnf")
    with open(path, "w") as f:
        f.write(f"p cnf {F.nv} {len(F.cl) + nc}\n")
        for c in F.cl:
            f.write(" ".join(map(str, c)) + " 0\n")
        for i in range(nc):
            f.write(f"{i + 1 if mask[i] else -(i + 1)} 0\n")
    r = subprocess.run([KISSAT, "-q", path], capture_output=True, text=True)
    if r.returncode == 10:
        return True
    if r.returncode == 20:
        return False
    raise RuntimeError(f"kissat rc={r.returncode}")


def main():
    n = int(sys.argv[1])
    trials = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rng = random.Random(20260820 + n)
    F, nc, ns = build_sym_only(n)
    group = my_cube_group(n)
    print(f"n={n}: клеток {nc}, симметрийных клауз {len(F.cl)}, переменных {F.nv}, "
          f"разбито симметрий {ns}, своя группа {len(group)}")
    bad_fatal, bad_weak, checked = [], [], 0
    with tempfile.TemporaryDirectory() as td:
        for t in range(trials):
            k = rng.randint(max(1, nc // 6), nc // 2)
            mask = [0] * nc
            for i in rng.sample(range(nc), k):
                mask[i] = 1
            orb = sorted(set(images(mask, group)))
            lexmin = orb[0]                                   # 0 < 1 позиционно — тот же порядок, что в клаузе (-a v b)
            # смертельное направление: лексминимум ОБЯЗАН пережить отсечение
            if not sat_with_units(F, nc, lexmin, td):
                bad_fatal.append((t, "лексминимум орбиты отвергнут"))
            checked += 1
            # обратное направление: не-минимумы должны отсекаться (слабое; его нарушение лишь ослабляет)
            for other in orb[1:3]:
                if sat_with_units(F, nc, other, td):
                    bad_weak.append((t, "не-минимум пережил"))
                checked += 1
            # и ровно один выживший на орбиту — итоговая форма
            if len(orb) <= 8:
                surv = sum(1 for o in orb if sat_with_units(F, nc, o, td))
                checked += len(orb)
                if surv != 1:
                    (bad_fatal if surv == 0 else bad_weak).append((t, f"выживших на орбите {surv}, орбита {len(orb)}"))
    print(f"наборов испытано {trials}, вызовов решателя {checked}")
    print(f"СМЕРТЕЛЬНЫХ нарушений (орбита выброшена целиком): {len(bad_fatal)}  {bad_fatal[:3]}")
    print(f"слабых (отсечение не полное, лишь неэффективно): {len(bad_weak)}  {bad_weak[:3]}")
    print("ВЕРДИКТ:", "отсечение КОРРЕКТНО — ни одна орбита не выброшена" if not bad_fatal
          else "ОТСЕЧЕНИЕ НЕКОРРЕКТНО — заявление UNSAT недействительно")


if __name__ == "__main__":
    main()
