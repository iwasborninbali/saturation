"""oeis_scan.py — МЕХАНИЧЕСКИЙ генератор кандидатов жанра 1: «величины, которые никто не считал,
хотя объект известен и определён».  Признак из нашего регламента: в литературе есть асимптотика,
а таблицы малых значений нет.

Зачем машиной, а не агентом.  Ресёрчи 10 и 11 вернули по большей части РАСШИРЕНИЯ ФРОНТИРОВ, и те
умерли от стоимости структурно: фронтир стоит ровно там, где остановилась группа с ресурсами больше
нашего.  Жанр 1 устроен иначе — там счёт мал, потому что его просто никто не вёл.  Такой отбор
формализуется фильтром и потому воспроизводим: любой может перезапустить его и получить тот же список.

ЧТО ЭТО НЕ ДЕЛАЕТ.  Сканер не устанавливает границ и не выносит вердиктов.  Он даёт ЛИДЫ, каждый из
которых обязан пройти C0 (подтверждение по первоисточнику) и аудит стоимости.  Запись OEIS — по
классификации ресёрча 11 — supporting source, не frontier authority.

ФИЛЬТР (каждое условие — из уже пойманной ошибки или из профиля группы):
  + keyword:more            последовательность заведомо неполна (иначе считать нечего)
  + мало известных членов   короткая таблица малых значений — это и есть «никто не считал»
  + объект комбинаторный    в названии максимум/минимум/число способов над параметром размера
  + есть асимптотика        в комментариях/формулах/ссылках говорят о росте, но не дают членов
  − не охота за простыми    «Numbers k such that … is prime» — это жанр 2, он у нас всегда умирает
  − не гигантские члены     если известные члены уже астрономические, следующий недостижим

usage: python3 oeis_scan.py [--pages N] [--out FILE]
"""
from __future__ import annotations
import json, re, subprocess, sys, time

UA = "Mozilla/5.0"          # oeis.org отдаёт 403 стандартным клиентам; проверенный обходной путь
QUERIES = [
    # ключевые слова: полнота охвата важнее точности — отсев делает ранжирование
    "keyword:more keyword:hard keyword:nonn", "keyword:more keyword:nice keyword:nonn",
    "keyword:more keyword:hard keyword:tabl", "keyword:hard keyword:nice keyword:nonn",
    # формулировки комбинаторных экстремумов
    "keyword:more maximum number of points", "keyword:more maximal number",
    "keyword:more minimum number of", "keyword:more largest subset",
    "keyword:more smallest number of", "keyword:more greatest number of",
    "keyword:more maximum size of", "keyword:more largest set of",
    # геометрия на решётках и в кубах — наш профиль
    "keyword:more no three", "keyword:more no four", "keyword:more general position",
    "keyword:more grid points", "keyword:more lattice points no",
    "keyword:more n X n X n grid", "keyword:more points in the plane",
    "keyword:more collinear", "keyword:more coplanar", "keyword:more convex position",
    # графы, гиперкубы, коды
    "keyword:more induced subgraph maximum", "keyword:more hypercube subset",
    "keyword:more binary code maximum", "keyword:more cap set", "keyword:more sidon set",
    "keyword:more nonattacking", "keyword:more packing in", "keyword:more covering code",
    # прямые маркеры жанра 1
    "keyword:more exhaustive search", "keyword:more found by exhaustive",
    "keyword:more conjectured value", "keyword:more based on numerical evidence",
    "keyword:more asymptotically", "keyword:more upper bound is known",
]
ASYMPTOTIC = re.compile(r"asymptot|Theta\(|O\(n|grows (?:like|as)|~\s*[cC]?\s*n|conjectur|upper bound|lower bound|order of magnitude", re.I)
COMBINATORIAL = re.compile(r"maxim(?:um|al)|minim(?:um|al)|largest|smallest number of|number of ways|greatest number", re.I)
PRIMEHUNT = re.compile(r"Numbers k such that|is prime|primes? p such that|semiprime|repunit|palindrom", re.I)

def fetch(q: str, start: int) -> list:
    r = subprocess.run(["curl", "-s", "-A", UA, f"https://oeis.org/search?q={q.replace(' ','+')}&fmt=json&start={start}"],
                       capture_output=True, text=True, timeout=60)
    try:
        d = json.loads(r.stdout)
    except Exception:
        return []
    return d if isinstance(d, list) else d.get("results") or []

def terms(e: dict) -> list:
    return [t for t in (e.get("data") or "").split(",") if t.strip()]

def blob(e: dict) -> str:
    parts = []
    for k in ("comment", "formula", "link", "example", "ext"):
        v = e.get(k)
        if isinstance(v, list): parts += v
        elif isinstance(v, str): parts.append(v)
    return " ".join(parts)

def score(e: dict) -> tuple[int, list[str]]:
    """баллы и причины; фильтры-минусы возвращают -1 (кандидат вычёркивается)"""
    name, ts, txt = e.get("name", ""), terms(e), blob(e)
    why = []
    if PRIMEHUNT.search(name): return -1, ["охота за простыми/паттернами цифр — наш всегдашний kill"]
    if not ts: return -1, ["нет членов"]
    big = max((len(t.strip().lstrip("-")) for t in ts), default=0)
    if big > 12: return -1, [f"известные члены уже {big}-значные — следующий недостижим"]
    s = 0
    if len(ts) <= 8:  s += 3; why.append(f"известно всего {len(ts)} членов")
    elif len(ts) <= 12: s += 2; why.append(f"известно {len(ts)} членов")
    else: why.append(f"членов {len(ts)} — таблица уже длинная")
    kw = e.get("keyword", "")
    if "hard" in kw: s += 2; why.append("keyword:hard")
    if "nice" in kw: s += 1; why.append("keyword:nice")
    if COMBINATORIAL.search(name): s += 3; why.append("комбинаторный экстремум/счёт над параметром")
    if ASYMPTOTIC.search(txt): s += 3; why.append("в тексте есть асимптотика/оценка, но нет членов")
    if re.search(r"\bgrid\b|lattice|graph|hypercube|simplex|polytope|permutation|matrix|geometry|point set", name + " " + txt, re.I):
        s += 1; why.append("объект дискретно-геометрический (наш профиль)")
    if int(e.get("references", 0) or 0) >= 30: s -= 1; why.append("много ссылок — вероятна активная работа")
    return s, why

def main() -> None:
    pages = 3; out = "docs/research/targets/oeis_scan_results.md"
    a = sys.argv[1:]
    if "--pages" in a: pages = int(a[a.index("--pages") + 1])
    if "--out" in a: out = a[a.index("--out") + 1]
    seen: dict[str, dict] = {}
    for q in QUERIES:
        for pg in range(pages):
            res = fetch(q, pg * 10)
            if not res: break
            for e in res: seen.setdefault(f"A{int(e['number']):06d}", e)
            time.sleep(0.4)          # вежливость к oeis.org
        print(f"  «{q}» → всего уникальных {len(seen)}", file=sys.stderr, flush=True)
    ranked = []
    for aid, e in seen.items():
        s, why = score(e)
        if s >= 0: ranked.append((s, aid, e, why))
    ranked.sort(key=lambda r: (-r[0], r[1]))
    with open(out, "w") as f:
        f.write("# Механический скан OEIS: лиды жанра 1\n\n")
        f.write("Сгенерировано `slack/targets/oeis_scan.py`. **Это лиды, а не кандидаты**: каждая строка обязана\n"
                "пройти C0 (подтверждение по первоисточнику) и аудит стоимости, прежде чем стать кандидатом.\n"
                "OEIS по классификации ресёрча 11 — supporting source, не frontier authority.\n\n")
        f.write(f"Просмотрено записей: {len(seen)}; прошло фильтр: {len(ranked)}.\n\n")
        f.write("| балл | A-номер | название | членов | почему |\n|---:|---|---|---:|---|\n")
        for s, aid, e, why in ranked[:60]:
            nm = e.get("name", "").replace("|", "\\|")[:110]
            f.write(f"| {s} | [{aid}](https://oeis.org/{aid}) | {nm} | {len(terms(e))} | {'; '.join(why)} |\n")
    print(f"\nпросмотрено {len(seen)}, прошло фильтр {len(ranked)}, записано в {out}")
    for s, aid, e, why in ranked[:12]:
        print(f"  {s:2d}  {aid}  {e.get('name','')[:88]}")

if __name__ == "__main__":
    main()
