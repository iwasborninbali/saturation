"""count_books.py — count pairwise D4-inequivalent configurations among the BOOK lines of sweep journals.
usage: python3 bench/count_books.py n journal1 [journal2 ...]"""
import sys
sys.path.insert(0, 'web')
import stab
n = int(sys.argv[1])
def canon(cells):
    pts = [divmod(t, n) for t in cells]; best = None
    for f in stab.images(n):
        img = tuple(sorted(f(u, v) for u, v in pts))
        if best is None or img < best: best = img
    return best
for path in sys.argv[2:]:
    classes = {}; labelled = 0
    for l in open(path):
        if l.startswith('BOOK'):
            labelled += 1
            toks = l.split(' sol ')[1].split(); cells = frozenset(int(t) for t in toks)
            key = canon(cells)
            classes.setdefault(key, []).append(l.split()[1])
    stabs = [stab.classify(frozenset(u * n + v for u, v in c), n) for c in classes]
    print(f"{path}: labelled solutions {labelled}, inequivalent configurations {len(classes)}; classes: {stabs}; sub-classes: {[v[0] for v in classes.values()]}")
