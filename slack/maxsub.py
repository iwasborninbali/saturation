"""maxsub.py — exact maximum lawful subset of a candidate set (list of (x,y)), via kissat; witnesses verified by the law.
usage as module: maxsub(cands, N, s_from, secs) -> (best, witness) ; CLI: maxsub.py rule2h p [s_from] [secs]"""
import sys, os, subprocess, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
HERE = os.path.dirname(os.path.abspath(__file__))
def maxsub(cands, N, s, secs=600, verbose=True):
    cands = sorted(cands); best = None; wit = None
    while True:
        cnf = os.path.join(tempfile.gettempdir(), f"maxsub_{os.getpid()}_{s}.cnf")
        with open(cnf, 'w') as f:
            subprocess.run([HERE + '/maxsub', str(s)], input="\n".join(f"{x} {y}" for x, y in cands) + "\n", stdout=f, text=True)
        r = subprocess.run(['kissat', '-q', f'--time={secs}', cnf], capture_output=True, text=True).stdout
        os.remove(cnf)
        if 's SATISFIABLE' in r:
            pts = set()
            for tok in r.split():
                if tok.lstrip('-').isdigit():
                    v = int(tok)
                    if 0 < v <= len(cands): pts.add(cands[v - 1])
            S.the_law(frozenset(x * N + y for (x, y) in pts), N)
            best, wit = s, pts
            if verbose: print(f"  SAT at s={s} ({s/N:.3f} N)", flush=True)
            s += 1
        elif 's UNSATISFIABLE' in r:
            if verbose: print(f"  UNSAT at s={s} => max = {s-1} ({(s-1)/N:.3f} N)", flush=True)
            return best, wit, True
        else:
            if verbose: print(f"  unknown at s={s} within {secs}s (best {best})", flush=True)
            return best, wit, False
if __name__ == "__main__":
    sys.path.insert(0, HERE)
    from rule2h import rule
    p = int(sys.argv[2]); N = 2 * p
    s0 = int(sys.argv[3]) if len(sys.argv) > 3 else 3 * (p - 1) - 2
    secs = int(sys.argv[4]) if len(sys.argv) > 4 else 900
    R = rule(p)
    print(f"p={p} N={N} |R|={len(R)} HJSW={3*(p-1)}")
    best, wit, exact = maxsub(R, N, s0, secs)
    print(f"RESULT p={p}: max lawful subset of R(p) = {best}{'' if exact else '+ (not exact)'}  ratio {best/N:.3f}  HJSW ratio {3*(p-1)/N:.3f}")
