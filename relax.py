"""relax.py — same-size large-neighbourhood search on a known rot2-symmetric book: drop k half-turn pairs,
keep the rest fixed, enumerate ALL lawful completions in the rot2 class (there.c, FIX=), and report the
completions that differ from the original, with their exact class.
usage: python3 relax.py FILE n k tries [seed] [secs]"""
import sys, os, random, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/web'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import decode
from stab import classify, encode
import saturation as S
path, n, k, tries = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
seed = int(sys.argv[5]) if len(sys.argv) > 5 else 1; secs = sys.argv[6] if len(sys.argv) > 6 else "120"
rng = random.Random(seed); m = n - 1
lines = [l for l in open(path) if l.strip()]
binary = './there' if n <= 64 else './there128'
seen = {}
for t in range(tries):
    line = rng.choice(lines); cls, nn, book = decode(line)
    pts = sorted(divmod(x, n) for x in book)
    pairs = sorted({tuple(sorted([(u, v), (m - u, m - v)])) for (u, v) in pts})
    drop = rng.sample(pairs, k)
    dropped = {c for pr in drop for c in pr}
    keep = [u * n + v for (u, v) in pts if (u, v) not in dropped]
    open('relax_fix.txt', 'w').write(' '.join(map(str, keep)))
    out = subprocess.run([binary, str(n), '1', '1', secs], capture_output=True, text=True, env=dict(os.environ, FIX='relax_fix.txt', ALL='1', PRINTALL='1')).stdout
    sols = [frozenset(int(x) for x in l.split()[1:]) for l in out.split('\n') if l.startswith('sol')]
    status = out.strip().split('\n')[-1][:60] if out.strip() else 'no output'
    news = [s for s in sols if s != book]
    print(f"try {t}: dropped {k} pairs -> completions {len(sols)} (new {len(news)}) [{status}]", flush=True)
    for s in news:
        S.certify(s, n); c = classify(s, n); e = encode(s, n)
        if e not in seen:
            seen[e] = c; print(f"   NEW class={c}: {e}", flush=True)
print("distinct new books:", len(seen), sorted(set(seen.values())))
