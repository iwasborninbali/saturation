import sys
sys.path.insert(0, '/Users/iwasborninbali/saturation')
import saturation as S
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
CLASSES = {'.': 'iden', ':': 'rot2', '/': 'dia1', '-': 'ort1', 'o': 'rot4', 'c': 'rct4', 'x': 'dia2', '+': 'ort2', '*': 'full'}
def decode(line):
    line = line.strip()
    cls, body = line[0], line[1:]
    n = len(body) // 2
    cols = [IDX[c] for c in body]
    book = frozenset(r * n + cols[2 * r + k] for r in range(n) for k in range(2))
    return CLASSES[cls], n, book
if __name__ == "__main__":
    for path in sys.argv[1:]:
        for i, line in enumerate(open(path)):
            if not line.strip(): continue
            cls, n, book = decode(line)
            print(path, cls, S.certify(book, n))
            if i >= 1: break
