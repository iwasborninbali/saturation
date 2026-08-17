"""arcmod2.py — A(m) with kissat, one s per call: prints SAT/UNSAT/unknown; verifies SAT witnesses with the law and the det condition.
usage: arcmod2.py m s secs [FIX1]"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
m, s, secs = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
fix1 = len(sys.argv) > 4 and sys.argv[4] == "FIX1"
here = os.path.dirname(os.path.abspath(__file__))
KISSAT = os.path.expanduser("~/bin/kissat")
cnf = os.path.join(tempfile.gettempdir(), f"arcmod2_{m}_{s}_{int(fix1)}.cnf")
env = dict(os.environ); 
if fix1: env["FIX1"] = "1"
with open(cnf, "w") as f:
    subprocess.run([os.path.join(here, "arcmod2"), str(m), str(s)], stdout=f, check=True, env=env)
r = subprocess.run([KISSAT, "-q", f"--time={secs}", cnf], capture_output=True, text=True).stdout
if "s SATISFIABLE" in r:
    pts = set()
    for tok in r.split():
        if tok.lstrip("-").isdigit():
            v = int(tok)
            if 0 < v <= m * m: pts.add(v - 1)
    S.the_law(frozenset(pts), m)                                # lawful in the m x m grid
    P = sorted(divmod(p, m) for p in pts)
    for i in range(len(P)):                                     # det condition mod m, exact
        for j in range(i + 1, len(P)):
            for k in range(j + 1, len(P)):
                (ua, va), (ub, vb), (uc, vc) = P[i], P[j], P[k]
                assert ((ub - ua) * (vc - va) - (vb - va) * (uc - ua)) % m != 0
    print(f"m={m} s={s}: SAT (ratio {s/m:.3f}) fix1={int(fix1)} points={P}", flush=True)
elif "s UNSATISFIABLE" in r:
    print(f"m={m} s={s}: UNSAT fix1={int(fix1)}", flush=True)
else:
    print(f"m={m} s={s}: unknown within {secs}s fix1={int(fix1)}", flush=True)
os.remove(cnf)
