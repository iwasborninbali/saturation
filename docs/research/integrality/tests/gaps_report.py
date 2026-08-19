"""gaps_report.py — печатает реестр дыр спецификации (gaps.REGISTRY) в markdown.

Импортирует все шесть тестовых модулей — при импорте срабатывают декораторы @gap и
наполняют gaps.REGISTRY, — после чего печатает:

  * сводку по линзам (сколько дыр нашла каждая) и по объекту (phenomenon.py / holes.py);
  * указатель: id / линза / место в спецификации / заголовок;
  * подробные таблицы id / title / expected / actual / consequence,
    СГРУППИРОВАННЫЕ по объекту спецификации и ОТСОРТИРОВАННЫЕ по id.

Запуск:
    python3 tests/gaps_report.py            # печатает markdown в stdout
    python3 tests/gaps_report.py --write    # перегенерирует хвост tests/GAPS.md

`--write` заменяет в GAPS.md только то, что МЕЖДУ маркерами MARK_BEG и MARK_END,
оставляя написанные руками предисловие (сверху) и русское резюме (снизу) нетронутыми, —
так отчёт не может разойтись с реестром, а руками написанное не может быть затёрто.

Ничего не импортирует, кроме stdlib, gaps.py и тестовых модулей; phenomenon.py и
holes.py не трогает.
"""
from __future__ import annotations

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)                       # gaps.py, test_*.py
sys.path.insert(0, os.path.dirname(_HERE))      # phenomenon.py, holes.py

import gaps  # noqa: E402

# Порядок = порядок линз в отчёте; он же порядок импорта.
LENSES = [
    ("test_contracts.py",      "contracts",      "GAP-C"),
    ("test_numbers.py",        "numbers",        "GAP-N"),
    ("test_toys.py",           "toys",           "GAP-T"),
    ("test_principles.py",     "principles",     "GAP-P"),
    ("test_holes.py",          "holes",          "GAP-H"),
    ("test_falsifiability.py", "falsifiability", "GAP-F"),
]

MARK_BEG = "<!-- НАЧАЛО СГЕНЕРИРОВАННОГО gaps_report.py; НЕ ПРАВИТЬ РУКАМИ -->"
MARK_END = "<!-- КОНЕЦ СГЕНЕРИРОВАННОГО -->"

# Порядок групп в подробной части.
TARGET_ORDER = ["phenomenon.py", "phenomenon.py + holes.py", "holes.py"]


def load_registry() -> dict[str, str]:
    """Импортировать тестовые модули по одному и запомнить, какая линза какие id внесла.

    Возвращает {gap_id: "test_xxx.py"}.  gaps.gap() падает на повторном id, поэтому
    сам факт успешного импорта шести модулей — это проверка уникальности id.
    """
    origin: dict[str, str] = {}
    for filename, _lens, _prefix in LENSES:
        modname = filename[:-3]
        before = set(gaps.REGISTRY)
        __import__(modname)
        for gid in sorted(set(gaps.REGISTRY) - before):
            origin[gid] = filename
    return origin


def target_of(module_field: str) -> str:
    """Свести свободный текст Gap.module к объекту спецификации, за который отвечает дыра."""
    has_p = "phenomenon.py" in module_field
    has_h = "holes.py" in module_field
    if has_p and has_h:
        return "phenomenon.py + holes.py"
    if has_h:
        return "holes.py"
    return "phenomenon.py"


def locus_of(module_field: str) -> str:
    """Уточнение внутри объекта: то, что линза дописала к имени файла ('P3', '§0', ...)."""
    locus = module_field
    for name in ("phenomenon.py", "holes.py"):
        locus = locus.replace(name, "")
    locus = " ".join(locus.split())     # схлопнуть пробелы, оставшиеся от имён файлов
    locus = locus.strip(" +()")         # убрать связки, повисшие по краям
    return locus or "—"


def holes_word(n: int) -> str:
    """Русское склонение слова «дыра» при числительном: 1 дыра, 3 дыры, 7 дыр, 14 дыр."""
    if 11 <= n % 100 <= 14:
        return "дыр"
    last = n % 10
    if last == 1:
        return "дыра"
    if 2 <= last <= 4:
        return "дыры"
    return "дыр"


def cell(text: str) -> str:
    r"""Обезвредить текст для ячейки markdown-таблицы.

    В полях 92 символа '|' (|S|, |V|, λ_min/√m₂ …) — без экранирования таблица
    рассыпается на 19 дырах из 36.  Переводов строки в полях нет, но схлопываем на
    случай будущих правок: ячейка обязана остаться однострочной.
    """
    return " ".join(text.replace("|", r"\|").split())


def table(rows: list[list[str]], header: list[str]) -> list[str]:
    out = ["| " + " | ".join(header) + " |",
           "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def render(origin: dict[str, str]) -> str:
    reg = gaps.REGISTRY
    ids = sorted(reg)
    lines: list[str] = []
    W = lines.append

    # ---------- сводка ----------
    W("## Сводка")
    W("")
    W(f"Дыр в реестре: **{len(ids)}**. Каждая — тест с маркером `@gap`, то есть "
      "`unittest.expectedFailure`: пока дыра открыта, прогон зелёный; как только дыру "
      "закроют, тест даст *unexpected success* и прогон станет КРАСНЫМ.")
    W("")
    by_lens = [[lens, f"`{fn}`", prefix,
                str(sum(1 for g in ids if origin.get(g) == fn))]
               for fn, lens, prefix in LENSES]
    by_lens.append(["**итого**", "", "", f"**{len(ids)}**"])
    lines += table(by_lens, ["линза", "файл", "префикс", "дыр"])
    W("")
    counts: dict[str, int] = {}
    for g in ids:
        counts[target_of(reg[g].module)] = counts.get(target_of(reg[g].module), 0) + 1
    rows = [[f"`{t}`", str(counts[t])] for t in TARGET_ORDER if t in counts]
    lines += table(rows, ["объект спецификации", "дыр"])
    W("")
    W("Пропуски в нумерации (`GAP-H-05`, `GAP-P-04`) — не потерянные дыры: обе отвергнуты "
      "на проверке как педантичные (претензии к набору полей dataclass и к пунктуации), "
      "их содержательный остаток переведён в обычные тесты. Номера не переиспользуются.")
    W("")

    # ---------- указатель ----------
    W("## Указатель")
    W("")
    rows = [[f"`{g}`", origin.get(g, "?").replace("test_", "").replace(".py", ""),
             cell(locus_of(reg[g].module)), cell(reg[g].title)] for g in ids]
    lines += table(rows, ["id", "линза", "место в спецификации", "заголовок"])
    W("")

    # ---------- подробно ----------
    W("## Дыры подробно")
    W("")
    for tgt in TARGET_ORDER:
        group = [g for g in ids if target_of(reg[g].module) == tgt]
        if not group:
            continue
        W(f"### {tgt} — {len(group)} {holes_word(len(group))}")
        W("")
        rows = [[f"`{g}`", cell(reg[g].title), cell(reg[g].expected),
                 cell(reg[g].actual), cell(reg[g].consequence)] for g in group]
        lines += table(rows, ["id", "title", "expected (что обязано быть по тексту)",
                              "actual (что есть)", "consequence (чем грозит выводам)"])
        W("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    origin = load_registry()
    body = render(origin)
    if "--write" in sys.argv[1:]:
        path = os.path.join(_HERE, "GAPS.md")
        if not os.path.exists(path):
            print(f"нет файла {path}: сначала создайте его с предисловием и маркером",
                  file=sys.stderr)
            return 2
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        if MARK_BEG not in old or MARK_END not in old:
            print(f"в {path} нет пары маркеров:\n{MARK_BEG}\n{MARK_END}", file=sys.stderr)
            return 2
        head = old.split(MARK_BEG)[0]
        tail = old.split(MARK_END, 1)[1]
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(head + MARK_BEG + "\n\n" + body + "\n" + MARK_END + tail)
        print(f"перезаписана середина {path} ({len(gaps.REGISTRY)} дыр); "
              "предисловие и русское резюме сохранены", file=sys.stderr)
        return 0
    sys.stdout.write(body)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
