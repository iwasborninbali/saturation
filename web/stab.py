"""stab.py — exact symmetry class of a book (Flammenkamp's names) and his encoding.

    python3 web/stab.py N t1 t2 ...          # tokens
    python3 web/stab.py N @file              # whitespace-separated tokens in a file
Prints: class name, stabilizer, and the encoded configuration line (class char + columns).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from decode import ALPHA

MOTIONS = ["iden", "rot90", "rot180", "rot270", "flipu", "flipv", "swap", "antiswap"]

def images(n):
    m = n - 1
    return [lambda u, v: (u, v), lambda u, v: (v, m - u), lambda u, v: (m - u, m - v), lambda u, v: (m - v, u),
            lambda u, v: (m - u, v), lambda u, v: (u, m - v), lambda u, v: (v, u), lambda u, v: (m - v, m - u)]

def stabilizer(book, n):
    pts = {divmod(t, n) for t in book}
    return [MOTIONS[i] for i, f in enumerate(images(n)) if {f(u, v) for (u, v) in pts} == pts]

def classify(book, n):
    """exact class: iden rot2 dia1 ort1 rot4 dia2 ort2 full, or 'rct4' pseudo-class inside rot2"""
    st = set(stabilizer(book, n))
    if st == {"iden"}:
        return "iden"
    if st == {"iden", "rot180"}:
        # rct4 = rot4 symmetry except on the long axes (Flammenkamp's pseudo-class, kept for ODD n only; its true stabilizer
        # is {1, rot180}, i.e. rot2): check off-axis cells are closed under rot90
        m = n - 1
        pts = {divmod(t, n) for t in book}
        off = {(u, v) for (u, v) in pts if u != v and u + v != m}
        if (n & 1) and {(v, m - u) for (u, v) in off} == off:
            return "rct4"
        return "rot2"
    if st == {"iden", "swap"} or st == {"iden", "antiswap"}:
        return "dia1"
    if st == {"iden", "flipu"} or st == {"iden", "flipv"}:
        return "ort1"
    if st == {"iden", "rot90", "rot180", "rot270"}:
        return "rot4"
    if st == {"iden", "swap", "antiswap", "rot180"}:
        return "dia2"
    if st == {"iden", "flipu", "flipv", "rot180"}:
        return "ort2"
    if len(st) == 8:
        return "full"
    return "?" + ",".join(sorted(st))

CHAR = {"iden": ".", "rot2": ":", "dia1": "/", "ort1": "-", "rot4": "o", "rct4": "c", "dia2": "x", "ort2": "+", "full": "*"}

def encode(book, n):
    cls = classify(book, n)
    rows = {}
    for t in sorted(book):
        rows.setdefault(t // n, []).append(t % n)
    assert all(len(v) == 2 for v in rows.values()) and len(rows) == n, "encoding needs exactly two tokens per row"
    return CHAR.get(cls, "?") + "".join(ALPHA[c] for u in range(n) for c in sorted(rows[u]))

if __name__ == "__main__":
    n = int(sys.argv[1])
    if sys.argv[2].startswith("@"):
        toks = [int(x) for x in open(sys.argv[2][1:]).read().replace(",", " ").split()]
    else:
        toks = [int(x) for x in sys.argv[2:]]
    book = frozenset(toks)
    print("class:", classify(book, n), "stabilizer:", stabilizer(book, n))
    print("encoded:", encode(book, n))
