"""arcmod.py — A(m): max |S|, S in Z_m^2 with no triple det = 0 (mod m); via kissat.  usage: arcmod.py m [s_from] [secs]"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
m = int(sys.argv[1]); s = int(sys.argv[2]) if len(sys.argv) > 2 else (3 * m) // 2; secs = int(sys.argv[3]) if len(sys.argv) > 3 else 300
here = os.path.dirname(os.path.abspath(__file__))
best = None
while True:
    cnf = os.path.join(tempfile.gettempdir(), f"arcmod_{m}_{s}.cnf")
    with open(cnf, "w") as f:
        subprocess.run([os.path.join(here, "arcmod"), str(m), str(s)], stdout=f, check=True)
    r = subprocess.run(["kissat", "-q", f"--time={secs}", cnf], capture_output=True, text=True).stdout
    if "s SATISFIABLE" in r:
        pts = set()
        for tok in r.split():
            if tok.lstrip("-").isdigit():
                v = int(tok)
                if 0 < v <= m * m: pts.add(v - 1)
        # verify: no det=0 mod m triple, and lawful in Z^2 via the law
        book = frozenset(pts)
        S.the_law(book, m)
        best = (s, sorted(pts))
        print(f"m={m}: SAT at s={s} (ratio {s/m:.3f}); points={sorted(divmod(p, m) for p in pts)}", flush=True)
        s += 1
    elif "s UNSATISFIABLE" in r:
        if best is None:                                # no witness below yet: search downwards before claiming
            print(f"m={m}: UNSAT at s={s}; no witness yet — stepping down", flush=True); s -= 1
            if s <= 2: print(f"m={m}: degenerate", flush=True); break
            continue
        print(f"m={m}: UNSAT at s={s}  => A({m}) = {s-1} (ratio {(s-1)/m:.3f}) [witness at {best[0]}]", flush=True); break
    else:
        print(f"m={m}: unknown at s={s} within {secs}s (best so far {best[0] if best else None})", flush=True); break
    os.remove(cnf)
