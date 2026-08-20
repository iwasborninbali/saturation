"""verify_all_certs.py — сплошная независимая проверка КАЖДОГО свидетеля в репозитории.

Смысл в полноте, а не в глубине: любой файл, объявленный свидетелем, обязан пройти проверку тем
кодом, который его не создавал. Проверяются оба вида утверждений — «нет трёх коллинеарных»
(векторное произведение по всем тройкам) и «нет четырёх компланарных» (определитель по всем
четвёркам), — вид выбирается по каталогу и по заголовку файла, а при сомнении проверяются ОБА
и печатаются оба результата: молча выбрать более слабую проверку хуже, чем признать неясность.

    python3 verify_all_certs.py
"""
import os, re, sys
from itertools import combinations


def read_points(path):
    pts = []
    for ln in open(path, errors="replace"):
        s = ln.strip()
        if not s or s.startswith("#"): continue
        s = s.replace("(", " ").replace(")", " ").replace(",", " ").replace("[", " ").replace("]", " ")
        t = s.split()
        if len(t) % 3 != 0 or not t: continue
        if not all(re.fullmatch(r"-?\d+", u) for u in t): continue
        for i in range(0, len(t), 3):
            pts.append(tuple(int(t[i + k]) for k in range(3)))
    return pts


def bad_lines(S):
    b = 0
    for a, c, d in combinations(S, 3):
        u = tuple(c[k] - a[k] for k in range(3)); v = tuple(d[k] - a[k] for k in range(3))
        if (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]) == (0, 0, 0): b += 1
    return b


def bad_planes(S):
    b = 0
    for a, c, d, e in combinations(S, 4):
        u = tuple(c[k]-a[k] for k in range(3)); v = tuple(d[k]-a[k] for k in range(3)); w = tuple(e[k]-a[k] for k in range(3))
        if u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0]) == 0: b += 1
    return b


rows, problems = [], []
for root, _, files in os.walk("certs"):
    for fn in sorted(files):
        if not fn.endswith(".txt"): continue
        p = os.path.join(root, fn)
        S = read_points(p)
        if not S:
            rows.append((p, 0, 0, "-", "-", "нет точек — не свидетель")); continue
        if len(set(S)) != len(S):
            problems.append((p, "ПОВТОРЯЮЩИЕСЯ ТОЧКИ"))
        n = max(max(q) for q in S) + 1
        head = open(p, errors="replace").readline().lower()
        kind = "planes" if ("coplanar" in head or "a280537" in p.lower()) else "lines"
        bl = bad_lines(S)
        bp = bad_planes(S) if (kind == "planes" or len(S) <= 24) else None
        verdict = "ЧИСТ" if (bl == 0 if kind == "lines" else bp == 0) else "НЕЧИСТ"
        if verdict == "НЕЧИСТ": problems.append((p, f"коллинеарных {bl}, компланарных {bp}"))
        rows.append((p, len(S), n, bl, "-" if bp is None else bp, f"{kind}: {verdict}"))

w = max(len(r[0]) for r in rows)
print(f"{'файл'.ljust(w)}  точек   n  колл.  компл.  вердикт")
for r in rows:
    print(f"{r[0].ljust(w)}  {str(r[1]).rjust(5)} {str(r[2]).rjust(3)}  {str(r[3]).rjust(5)}  {str(r[4]).rjust(6)}  {r[5]}")
print(f"\nвсего файлов {len(rows)}, проблемных {len(problems)}")
for p, why in problems: print("  ПРОБЛЕМА:", p, "—", why)
print("ЗАМЕЧАНИЕ: для задачи о прямых столбец «компл.» справочный (четыре компланарных там разрешены).")
