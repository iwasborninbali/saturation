"""cross_solver.py — снятие последней общей зависимости: перерешение той же формулы ДРУГИМ решателем.

Оба солвера получали UNSAT от kissat. Кодировки, проверки и агрегаторы у нас независимы, но сама
программа, произносящая слово «невыполнимо», была одна. Для кусков, чьи DRAT-сертификаты мы
воспроизводим по требованию, а не храним, эта зависимость остаётся неснятой.

Здесь та же формула предъявляется решателям ИНОЙ родословной: Glucose и MiniSat идут от совсем
другой линии, CaDiCaL — другой код (хотя и тот же автор, что у kissat, поэтому он считается
слабейшим из трёх свидетельств).

    python3 cross_solver.py file.cnf solver [seconds]
"""
import sys, time
from pysat.formula import CNF
from pysat.solvers import Solver

path, name = sys.argv[1], sys.argv[2]
budget = float(sys.argv[3]) if len(sys.argv) > 3 else 0
f = CNF(from_file=path)
t0 = time.time()
with Solver(name=name, bootstrap_with=f.clauses) as S:
    r = S.solve()
    st = "SAT" if r else "UNSAT"
    print(f"{path.split('/')[-1]} {name}: {st} за {time.time()-t0:.0f}с "
          f"(конфликтов {S.accum_stats().get('conflicts','?')})", flush=True)
