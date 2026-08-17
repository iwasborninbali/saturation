"""pair_kissat.py — decide 'lawful subset of size >= s exists?' for a hyperbola-pair candidate set with kissat
(per-line at-most-2 sequential counters + totalizer at-least-s, DIMACS via python-sat, witness through the law).
usage: pair_kissat.py M p N k1,k2 s secs   |   pair_kissat.py PH p k N s secs"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
from maxlawful_pysat import cands_M, cands_PH, lines
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool, CNF
mode = sys.argv[1]
if mode == "M":
    p, N = int(sys.argv[2]), int(sys.argv[3]); ks = {int(k) % p for k in sys.argv[4].split(",")}; s, secs = int(sys.argv[5]), int(sys.argv[6])
    cands = cands_M(p, ks, N); tag = f"M p={p} ks={sorted(ks)} N={N}"
else:
    p, k, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); s, secs = int(sys.argv[5]), int(sys.argv[6])
    cands = cands_PH(p, k, N); tag = f"PH p={p} k={k} N={N}"
n = len(cands); L = lines(cands); pool = IDPool(start_from=n + 1); cnf = CNF()
for mem in L:
    cnf.extend(CardEnc.atmost(lits=[i + 1 for i in mem], bound=2, vpool=pool, encoding=EncType.seqcounter).clauses)
cnf.extend(CardEnc.atleast(lits=list(range(1, n + 1)), bound=s, vpool=pool, encoding=EncType.totalizer).clauses)
path = os.path.join(tempfile.gettempdir(), f"pair_{mode}_{p}_{s}_{os.getpid()}.cnf"); cnf.to_file(path)
r = subprocess.run([os.path.expanduser("~/bin/kissat"), "-q", f"--time={secs}", path], capture_output=True, text=True).stdout
if "s SATISFIABLE" in r:
    model = set(int(t) for t in r.split() if t.lstrip("-").isdigit() and 0 < int(t) <= n)
    pts = [cands[v - 1] for v in model]; S.the_law(frozenset(x * N + y for (x, y) in pts), N)
    print(f"{tag} s={s}: SAT (ratio {s/N:.3f}) witness={sorted(pts)}", flush=True)
elif "s UNSATISFIABLE" in r: print(f"{tag} s={s}: UNSAT", flush=True)
else: print(f"{tag} s={s}: unknown within {secs}s", flush=True)
os.remove(path)
