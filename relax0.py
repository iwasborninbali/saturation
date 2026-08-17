"""relax0.py — drop k individual points of a known book, keep the rest fixed, enumerate ALL lawful completions
without any symmetry (sym 0); report new books and their exact class.  usage: relax0.py FILE n k tries [seed] [secs]"""
import sys, os, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/web'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import decode
from stab import classify, encode
import saturation as S
path, n, k, tries = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1; secs = sys.argv[6] if len(sys.argv) > 6 else "120"
rng = random.Random(seed)
lines = [l for l in open(path) if l.strip()]
binary = './there' if n <= 64 else './there128'
seen = {}; tot = 0
for t in range(tries):
    line = rng.choice(lines); cls, nn, book = decode(line)
    pts = sorted(book)
    drop = set(rng.sample(pts, k))
    keep = [x for x in pts if x not in drop]
    open('relax_fix.txt', 'w').write(' '.join(map(str, keep)))
    out = subprocess.run([binary, str(n), '0', '1', secs], capture_output=True, text=True, env=dict(os.environ, FIX='relax_fix.txt', ALL='1', PRINTALL='1')).stdout
    sols = [frozenset(int(x) for x in l.split()[1:]) for l in out.split('\n') if l.startswith('sol')]
    news = [s for s in sols if s != book]; tot += len(sols)
    for s in news:
        S.certify(s, n); c = classify(s, n); e = encode(s, n)
        if e not in seen:
            seen[e] = c; print(f"try {t}: NEW class={c}: {e[:50]}...", flush=True)
print(f"tries {tries}, k={k}: completions {tot}, distinct new books {len(seen)} classes {sorted(set(seen.values()))}")
