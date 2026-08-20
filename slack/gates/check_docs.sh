#!/bin/bash
# check_docs.sh — ДОКУМЕНТАЦИЯ ИСПОЛНЯЕТСЯ, А НЕ ЧИТАЕТСЯ.
#
# Существует потому, что 2026-08-20 обнаружилось: команды воспроизведения в docs/VERIFICATION.md
# ни разу не запускались как написаны. Путь к свидетелю разбирался как данные, ветка --file была
# мёртвым кодом, ссылка вела на несуществующий файл. Для нас это ничего не изменило — для
# постороннего это означало отказ на ВЕРНОМ свидетеле, то есть худший из возможных первых опытов.
#
# Здесь проверяется: (1) каждый путь, упомянутый в документах, существует; (2) каждый проверяльщик
# умеет ОТВЕРГАТЬ; (3) каждый свидетель проходит проверку с ожидаемым числом точек.
set -u
R="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$R"
fail=0

echo "== 1. ссылки на файлы в документах"
# Один проход: печатаем и считаем ИЗ ОДНИХ И ТЕХ ЖЕ данных. Два прохода уже однажды дали нам
# «план вместо факта»; здесь та же ловушка была заложена, пока сканирование шло дважды.
python3 - <<'PYEOF' || fail=1
import re, os, sys
DOCS = ["docs/VERIFICATION.md", "docs/HANDOVER.md", "docs/research/ADVERSARIAL_REVIEW_BRIEF.md"]
# фигурные скобки в путях вида logs/sweeps/f41A_sym{9,10}_n41.txt — это ДВЕ ссылки, а не одна
# Класс символов ДОЛЖЕН забирать токен целиком. Узкий класс молча обрезал путь до
# существующего родительского каталога и объявлял битую ссылку целой — подсаженная
# ссылка с кириллицей прошла ворота. Берём всё до пробела и разметки, потом чистим хвост.
PAT = re.compile(r"(?:certs|slack|logs|paper|docs)/[^\s`\"'()\[\]|<>*]+")
def expand(p):
    m = re.search(r"\{([^{}]*)\}", p)
    if not m: return [p]
    out = []
    for alt in m.group(1).split(","):
        out += expand(p[:m.start()] + alt + p[m.end():])
    return out
broken = []
for d in DOCS:
    if not os.path.exists(d):
        broken.append((d, "<нет самого документа>")); continue
    for raw in sorted(set(PAT.findall(open(d, encoding="utf-8").read()))):
        for f in expand(raw):
            f = f.rstrip(".,:;)")
            if not os.path.exists(f): broken.append((d, f))
for d, f in broken: print(f"  БИТАЯ ССЫЛКА в {d}: {f}")
print(f"  все ссылки на месте" if not broken else f"  битых ссылок: {len(broken)}")
sys.exit(1 if broken else 0)
PYEOF

echo "== 2. проверяльщики умеют отвергать"
for v in certs/no3_3d/verify_witness_lines.py certs/a280537/verify_witness.py; do
  if python3 "$v" --selftest 2>&1 | grep -q "ПРОЙДЕНА"; then echo "  ок: $v"
  else echo "  САМОПРОВЕРКА ПРОВАЛЕНА: $v"; fail=1; fi
done

echo "== 3. свидетели"
check () { # проверяльщик n файл сколько
  out=$(python3 "$1" "$2" "$3" "$4" 2>&1)
  if echo "$out" | grep -q "ЧИСТ"; then echo "  ок: $3 ($4 точек)"
  else echo "  ОТКАЗ на $3: $out"; fail=1; fi
}
L=certs/no3_3d/verify_witness_lines.py; P=certs/a280537/verify_witness.py
check $L 5 certs/no3_3d/sat_witness_n5_40.txt 40
check $L 6 certs/no3_3d/sat_witness_n6_64.txt 64
check $L 7 certs/no3_3d/n7_warm_first_solver.txt 73
check $L 8 certs/no3_3d/n8_warm93_first_solver.txt 93
check $P 5 certs/a280537/witness_n5.txt 13
check $P 6 certs/a280537/witness_n6_16.txt 16
check $P 7 certs/a280537/witness_n7_18_first_solver.txt 18

echo
[ "$fail" -eq 0 ] && echo "ИТОГ: документация исполняется как написана." \
                  || { echo "ИТОГ: ОТКАЗ — документация расходится с репозиторием."; exit 1; }
