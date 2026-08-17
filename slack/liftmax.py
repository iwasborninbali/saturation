"""liftmax.py — exact maximum lawful subset of a lifted arc.  usage: liftmax.py mode p N k s_from secs"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
mode, p, N, k, s, secs = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
here = os.path.dirname(os.path.abspath(__file__)); best = None
while True:
    cnf = os.path.join(tempfile.gettempdir(), f"lift_{mode}{p}_{N}_{k}_{s}.cnf")
    with open(cnf, "w") as f:
        r0 = subprocess.run([os.path.join(here, "liftmax"), mode, str(p), str(N), str(k), str(s)], stdout=f, stderr=subprocess.PIPE, text=True)
    cands = [tuple(map(int, l.split()[2:4])) for l in r0.stderr.split("\n") if l.startswith("cand")]
    r = subprocess.run(["kissat", "-q", f"--time={secs}", cnf], capture_output=True, text=True).stdout
    if "s SATISFIABLE" in r:
        pts = set()
        for tok in r.split():
            if tok.lstrip("-").isdigit():
                v = int(tok)
                if 0 < v <= len(cands): pts.add(cands[v - 1])
        S.the_law(frozenset(x * N + y for (x, y) in pts), N)
        best = s; print(f"{mode} p={p} N={N} k={k}: |cand|={len(cands)} SAT at s={s} (ratio {s/N:.3f})", flush=True); s += 1
    elif "s UNSATISFIABLE" in r:
        print(f"{mode} p={p} N={N} k={k}: UNSAT at s={s} => max = {s-1} (ratio {(s-1)/N:.3f})", flush=True); break
    else:
        print(f"{mode} p={p} N={N} k={k}: unknown at s={s} within {secs}s (best {best})", flush=True); break
    os.remove(cnf)
