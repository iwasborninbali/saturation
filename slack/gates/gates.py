"""gates.py — ворота, через которые обязано проходить любое утверждение и любой запуск.

Каждая функция здесь существует потому, что БЕЗ НЕЁ МЫ УЖЕ ОДИН РАЗ ОШИБЛИСЬ. Рядом с каждой
указан случай. Ворота не советуют — они ОТКАЗЫВАЮТ: возвращают False или бросают Refusal,
и вызывающий код обязан остановиться.

Общий принцип, выведенный за сутки: почти все наши ошибки были не в вычислениях, а в том, что
УТВЕРЖДЕНИЕ ОКАЗЫВАЛОСЬ СИЛЬНЕЕ ТОГО, ЧТО РЕАЛЬНО ПРОИЗОШЛО. Ворота проверяют именно это.
"""
from __future__ import annotations
import os, re, shutil, subprocess, sys
from itertools import combinations


class Refusal(Exception):
    """Ворота отказали. Это не ошибка программы — это её правильная работа."""


class ClaimRefusal(Refusal):
    """ВОРОТА НА УТВЕРЖДЕНИЕ. Обходить нельзя никогда: обход здесь есть ложь.
    Сюда относится всё, что отвечает на вопрос «что мы установили»: «не знаю» не есть «нет»,
    кусок закрывает только явный UNSAT, число без артефакта, невозможность при сужении."""


class RunRefusal(Refusal):
    """ВОРОТА НА ЗАПУСК. Это ОЦЕНКА, и она бывает неверна — у первого солвера ворота отказали,
    показав «занято 12 из 12», хотя шесть ядер были чужие и его шесть задач машину не перегружали.
    Обход допустим, но обязан быть ЯВНЫМ и записанным: override=«причина».
    Различение предложено первым солвером; без него ворота либо игнорируют, либо ломают работу."""


def _allow(msg: str, override: str | None) -> None:
    """Обход ворот на запуск: только с названной причиной, и она попадает в журнал."""
    if not override:
        raise RunRefusal(msg)
    import datetime, os as _os
    line = f"{datetime.datetime.now():%F %H:%M} ОБХОД ВОРОТ: {msg} || причина: {override}\n"
    with open(_os.environ.get("GATE_LOG", "/tmp/gate_overrides.log"), "a") as f:
        f.write(line)
    print("  " + line.strip())


def _refuse(msg: str) -> None:
    """по умолчанию — ворота на утверждение: обход невозможен"""
    raise ClaimRefusal(msg)


# ─────────────────────────── 1. ворота на УТВЕРЖДЕНИЯ ───────────────────────────

def gate_three_valued(status: str) -> str:
    """Ловушка 6. Инструмент, способный сказать «не знаю», обязан различать ТРИ исхода.
    Случай: CP-SAT вернул UNKNOWN по таймауту, а код напечатал «оптимум единственен».
    Ещё: pkill оставил 150 строк «выполнено» с пустым выводом; таймаут; rc=137."""
    s = status.strip().upper()
    if s == "UNSAT":
        return "CLOSED"          # закрывает кусок
    if s == "SAT":
        return "REFUTES"         # рушит утверждение о невыполнимости
    return "NO_INFORMATION"      # всё прочее НЕ закрывает и НЕ опровергает


def gate_coverage(expected: list[str], results: dict[str, str]) -> None:
    """Полнота покрытия. Кусок закрыт только явным UNSAT; «не знаю» не закрывает.
    Случай: 11 строк rc=137 в журнале n=6; монитор считал строки и объявил «128 из 128»."""
    closed = {k for k, v in results.items() if gate_three_valued(v) == "CLOSED"}
    fatal  = {k for k, v in results.items() if gate_three_valued(v) == "REFUTES"}
    if fatal:
        _refuse(f"есть ВЫПОЛНИМЫЕ куски ({len(fatal)}): утверждение о невыполнимости ложно. Например {sorted(fatal)[:3]}")
    missing = [e for e in expected if e not in closed]
    if missing:
        _refuse(f"покрытие НЕПОЛНО: не закрыто {len(missing)} из {len(expected)}. Например {missing[:3]}")


def gate_witness(points: list[tuple], n: int, expect_size: int, kind: str) -> None:
    """Свидетель. Проверяется ПО СВОИМ КООРДИНАТАМ; провенанс файла значения не имеет.
    Случай: пустой свидетель объявлялся «чистым»; 72 и 90 не имели артефакта вовсе;
    отчёт называл 16 при файле с 15 и 93 при отсутствующем файле."""
    if len(points) < 3:
        _refuse(f"свидетель пуст или слишком мал ({len(points)} точек): проверять нечего — это НЕ подтверждение")
    if expect_size is not None and len(points) != expect_size:
        _refuse(f"точек {len(points)}, а заявлено {expect_size}")
    if len(set(points)) != len(points):
        _refuse("точки не различны")
    if not all(0 <= c < n for p in points for c in p):
        _refuse("точка вне куба")
    if kind == "no3":
        def cr(a, b, c):
            u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]
            return (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
        bad = [t for t in combinations(points, 3) if cr(*t) == (0, 0, 0)]
        if bad: _refuse(f"коллинеарных троек {len(bad)}, первая {bad[0]}")
    elif kind == "no4":
        def d3(a, b, c, d):
            u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]; w = [d[i]-a[i] for i in range(3)]
            return u[0]*(v[1]*w[2]-v[2]*w[1]) - u[1]*(v[0]*w[2]-v[2]*w[0]) + u[2]*(v[0]*w[1]-v[1]*w[0])
        bad = [q for q in combinations(points, 4) if d3(*q) == 0]
        if bad: _refuse(f"компланарных четвёрок {len(bad)}, первая {bad[0]}")
    else:
        _refuse(f"неизвестный вид задачи: {kind}")


def gate_verifier_selftest(verifier_path: str) -> None:
    """Ловушка 11 (2026-08-20). Проверяльщик, ни разу не показавший ОТКАЗ, НЕ ПРОВЕРЕН:
    слепой проверяльщик и честный дают одинаковое «свидетель ЧИСТ», и по выходу их не различить.
    Случай: оба наших проверяльщика свидетелей молча разбирали ПУТЬ как данные, а в одном из них
    ветка --file была мёртвым кодом, который ни разу не исполнялся. Ни один результат от этого
    не пострадал — но посторонний, запустивший проверяльщик естественным способом, получал отказ
    на ВЕРНОМ свидетеле, а это разрушает доверие ко всему остальному.

    Ворота на УТВЕРЖДЕНИЕ: перед тем как сослаться на свидетеля, проверяльщик обязан показать,
    что он умеет отвергать — на подсаженной коллинеарной тройке (или компланарной четвёрке)."""
    if not os.path.exists(verifier_path):
        _refuse(f"проверяльщика нет по пути {verifier_path} — сослаться на него нельзя")
    try:
        r = subprocess.run([sys.executable, verifier_path, "--selftest"],
                           capture_output=True, text=True, timeout=600)
    except subprocess.TimeoutExpired:
        _refuse(f"самопроверка {verifier_path} не завершилась за 600 с — считаем непройденной")
    if r.returncode != 0:
        _refuse(f"самопроверка {verifier_path} ПРОВАЛЕНА:\n{r.stdout.strip()}\n{r.stderr.strip()}")
    if "ПРОЙДЕНА" not in r.stdout:
        _refuse(f"самопроверка {verifier_path} не сказала «ПРОЙДЕНА» — молчание не есть успех:\n{r.stdout.strip()}")


def gate_watcher_blind(sources: list[tuple[str, float]], solvers_running: int,
                       max_silence_s: int = 1800, override: str | None = None) -> None:
    """Ловушка 12 (2026-08-20). «Движения нет» и «я смотрю не туда, куда пишут» ВЫГЛЯДЯТ ОДИНАКОВО.
    Случай: verdict19.sh три часа показывал «402, без движения», потому что имена файлов
    результатов были зашиты, а живой счёт писал в другие. Сорок пять решателей работали
    и писали в файлы, которых инструмент не читал. Занижение было систематическим и в одну
    сторону — наблюдатель НИКОГДА не завышает, он всегда пропускает.

    Отсюда правило: пока решатели работают, ТИШИНА ИСТОЧНИКОВ ЕСТЬ ПОДОЗРЕНИЕ НА СЛЕПОТУ
    ИНСТРУМЕНТА, а не наблюдение об отсутствии прогресса. Заявлять «прогресса нет» в таком
    состоянии запрещено, пока не показано, что читаются именно те файлы, в которые пишут.

    sources: [(имя, mtime_unix)]; solvers_running: сколько решателей живо."""
    import time
    if solvers_running <= 0:
        return                      # никто не работает — тишина законна
    if not sources:
        _refuse(f"решателей работает {solvers_running}, а источников не найдено НИ ОДНОГО — "
                f"это слепота инструмента, а не отсутствие результатов")
    newest_name, newest_t = max(sources, key=lambda x: x[1])
    silence = time.time() - newest_t
    if silence > max_silence_s:
        _allow(f"решателей работает {solvers_running}, но свежайший источник ({newest_name}) молчит "
               f"{silence/60:.0f} мин при пороге {max_silence_s/60:.0f}. Пока не показано, что "
               f"инструмент читает ТЕ ЖЕ файлы, в которые пишут решатели, вывод «прогресса нет» "
               f"недопустим — он неотличим от слепоты", override)


def gate_cnf_intact(path: str, sample_only: bool = False) -> int:
    """Ловушка 13 (2026-08-20). Мы проверяли ЧИСЛО порождённых файлов и ни разу — их ЦЕЛОСТНОСТЬ.
    Случай: 162 куска решающего вопроса вернули rc=1 — kissat выходил с ошибкой за ноль секунд,
    потому что файл был оборван (почти наверняка кончился диск). Число файлов при этом сходилось,
    `gate_generated` был доволен, а 162 узла остались нерешёнными И НЕЗАМЕЧЕННЫМИ: в журнале
    они выглядели как строки результата, наравне с UNSAT.

    Обрыв записи даёт ПРАВИЛЬНОЕ число файлов и неправильное содержимое. Поэтому кроме счёта
    обязана проверяться заявленная в шапке длина. Возвращает число клауз; бросает при расхождении.

    Ворота на УТВЕРЖДЕНИЕ: испорченный кусок не решён, что бы ни говорил журнал."""
    if not os.path.exists(path):
        _refuse(f"кусок {path} отсутствует — он НЕ решён")
    size = os.path.getsize(path)
    if size == 0:
        _refuse(f"кусок {path} ПУСТ — он не решён")
    nv = ncl = None
    seen = 0
    with open(path, "rb") as f:
        for line in f:
            if not line or line[:1] in (b"c", b"\n"):
                continue
            if line[:5] == b"p cnf":
                parts = line.split()
                nv, ncl = int(parts[2]), int(parts[3])
                continue
            seen += 1
            if sample_only and seen > 1000:
                break
    if nv is None:
        _refuse(f"в {path} нет строки 'p cnf' — файл не является CNF")
    if sample_only:
        return ncl
    if seen != ncl:
        _refuse(f"кусок {path} ОБОРВАН: шапка обещает {ncl} клауз, в файле {seen} "
                f"(разница {ncl - seen}). Такой кусок не решается — решатель вернёт ошибку, "
                f"и в журнале она будет неотличима от результата")
    return seen


def gate_sibling_columns(parent_cols: set, children_cols: list) -> int:
    """Ловушка 14 (2026-08-20, найдена первым солвером). Схема имён `{родитель}_s{индекс}` НЕ
    записывает СТОЛБЕЦ, по которому дробили. Поэтому два разбиения одного узла по разным столбцам
    дают файлы с ОДИНАКОВЫМИ именами и разным содержимым.

    Два вида беды, и они НЕ равны:
      (а) столбец зафиксирован повторно — расточительно, но БЕЗОПАСНО: ребёнок с другим
          подмножеством противоречит родительским клаузам и невыполним по-настоящему;
      (б) под одним узлом СМЕШАНЫ дети от РАЗНЫХ столбцов — НЕСОСТОЯТЕЛЬНО: каждое разбиение
          исчерпывающе по отдельности, смесь — нет, а правило «все 64 потомка закрыты» её примет,
          потому что имён ровно столько, сколько надо, и все они на месте.

    Опасна (б). Эти ворота её и ловят: у всех братьев новый столбец обязан быть ОДИН.
    Возвращает номер нового столбца."""
    new_cols = set()
    for cc in children_cols:
        extra = set(cc) - set(parent_cols)
        if not extra:
            continue                    # повторная фиксация — случай (а), не ошибка
        new_cols |= extra
    if len(new_cols) > 1:
        _refuse(f"дети одного узла дробились по РАЗНЫМ столбцам {sorted(new_cols)}. "
                f"Каждое разбиение исчерпывающе по отдельности, их СМЕСЬ — нет; "
                f"правило «все потомки закрыты» приняло бы её, потому что имён ровно столько, "
                f"сколько нужно. Это ложное закрытие, и по именам оно не видно")
    return next(iter(new_cols)) if new_cols else -1


def gate_density_threshold(problem: str, n: int, M: int, kind: str = "дробить_сразу") -> float:
    """Ловушка 15 (2026-08-21). Порог плотности остатка ИЗМЕРЕН для одной задачи и одних n, M.
    Перенести его на другие — ровно та ошибка, которую мы ловили весь предыдущий день:
    свойство, проверенное в одном контексте, не переносится в другой само собой.

    Эти ворота делают перенос НЕВОЗМОЖНЫМ: порог берётся только из файла замеров, и если
    для данной задачи замера нет, ворота ОТКАЗЫВАЮТ, а не возвращают правдоподобное число.
    Порог, взятый на глаз, опаснее отсутствующего: он выглядит как измеренная величина.

    kind: 'трудности' (что считать трудным) либо 'дробить_сразу' (когда пропускать решателя).
    Это РАЗНЫЕ величины, и путать их дорого — см. density_calibration.json."""
    import json
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "density_calibration.json")
    if not os.path.exists(path):
        _refuse(f"файла замеров {path} нет — порог взять неоткуда")
    tab = json.load(open(path, encoding="utf-8"))
    key = f"{problem}:n={n}:M={M}"
    if key not in tab:
        have = [k for k in tab if not k.startswith("_")]
        _refuse(f"порог плотности для «{key}» НЕ ИЗМЕРЕН. Замеренные: {have}. "
                f"Применять чужой порог нельзя: он откалиброван под другую задачу и другие n, M, "
                f"а выглядит как измеренная величина. Сначала замер, потом применение")
    rec = tab[key]
    fld = f"порог_{kind}"
    if fld not in rec:
        _refuse(f"в замере «{key}» нет поля {fld}; есть {list(rec)}")
    return float(rec[fld])


def gate_restriction(kind: str, axes_used: int, verdict: str) -> str:
    """Ловушка про избыточные ограничения. Невозможность, полученная при СУЖЕНИИ,
    относится только к суженному классу. Случай: «профиль 88 при n=7 невозможен» было
    получено по трём осям, то есть лишь для симметричных конфигураций."""
    if verdict.upper() != "UNSAT":
        return verdict
    if kind == "profile" and axes_used > 1:
        return "UNSAT_ONLY_FOR_SYMMETRIC_PROFILES"
    if kind == "invariant":
        return "UNSAT_ONLY_WITHIN_THE_SYMMETRIC_STRATUM"
    return "UNSAT"


def gate_pattern(values: dict[int, int], formula, predictions=None) -> str:
    """Ловушка подгонки — в формулировке первого солвера, и она лучше моей исходной.

    Мой первый вариант считал ТОЧКИ и отказывал меньше чем на шести. Это неверно по устройству:
    число наблюдений не различает подгонку и знание. Закономерность на шести согласных точках может
    быть совпадением (наша 2n^2-2n+4 держалась на n=2,3,4 и потом ещё на 6), а верная закономерность
    на трёх точках может быть настоящей.

    Различает одно: **сделала ли закономерность предсказание о случае, который в неё НЕ закладывали,
    и был ли этот случай затем посчитан.**

      законом можно назвать, только если
        (а) выведено утверждение о случае, не использованном при формулировке, И
        (б) этот случай посчитан, И
        (в) результат совпал.
      иначе — только «наблюдение с данными», и данные обязаны быть приведены.

    predictions: список пар (n, измеренное) для случаев ВНЕ values; допускается одна пара.
    ЛЮБОЕ провалившееся предсказание отменяет все пережившие — иначе достаточно было бы найти
    один удачный случай и умолчать о неудачных. Наша формула 2n^2-2n+4 ровно такова: построенная
    на n=2,3,4, она угадала 64 при n=6 и провалилась при n=5 и n=7.

    Проверка на наших двух провалах:
      2n^2-2n+4 по n=2,3,4 предсказала a(7)=88; посчитано — профиль невозможен. Отказ верный.
      «большая группа лучше» не предсказывала ничего, только перечисляла измеренное. Отказ на (а).
    """
    bad = {n: (v, formula(n)) for n, v in values.items() if formula(n) != v}
    if bad:
        _refuse(f"формула расходится с данными, на которых построена, в точках {sorted(bad)}: {bad}")
    if not predictions:
        _refuse("закономерность не сделала ни одного предсказания о случае вне своих данных: "
                "это НАБЛЮДЕНИЕ, а не закон. Назови случай, который она обязана предсказать, и посчитай его")
    if isinstance(predictions, tuple): predictions = [predictions]
    survived, failed = [], []
    for n_pred, measured in predictions:
        if n_pred in values:
            _refuse(f"случай n={n_pred} использован при формулировке — это не предсказание, а подгонка. "
                    f"Взять случай ВНЕ {sorted(values)}")
        exp = formula(n_pred)
        (survived if exp == measured else failed).append((n_pred, exp, measured))
    if failed:
        _refuse(f"предсказания ПРОВАЛИЛИСЬ в {[f[0] for f in failed]}: {failed}. "
                f"Пережившие ({[s0[0] for s0 in survived]}) этого не отменяют — иначе достаточно было бы "
                f"найти удачный случай и умолчать о неудачных. Закономерность опровергнута")
    return f"предсказания пережиты во всех проверенных случаях: {survived}"


def gate_text_vs_artifacts(text: str, repo_root: str) -> list[str]:
    """Ловушка 8. Текст умеет утверждать больше, чем его артефакты.
    Случай: в заметке стояли a(7)>=72 и a(8)>=90, а свидетелей под ними не было.
    Возвращает список чисел, под которыми не нашлось файла (эвристика, не доказательство)."""
    claims = re.findall(r'a\((\d+)\)\s*(?:>=|\\ge|=)\s*(\d+)', text)
    missing = []
    for n, v in claims:
        found = subprocess.run(['grep', '-rl', f'points={v}', os.path.join(repo_root, 'certs')],
                               capture_output=True, text=True).stdout.strip()
        if not found:
            found = subprocess.run(['bash', '-c',
                f'grep -rl "" {repo_root}/certs 2>/dev/null | while read f; do '
                f'c=$(grep -cE "^\\(?[0-9]+" "$f"); [ "$c" = "{v}" ] && echo "$f"; done'],
                capture_output=True, text=True).stdout.strip()
        if not found:
            missing.append(f"a({n})={v}")
    return missing


# ─────────────────────────── 2. ворота на ЗАПУСКИ ───────────────────────────

def gate_disk(path: str = "/tmp", need_gb: float = 5.0, override: str | None = None) -> None:
    """Случай: диск на ВМ забился, subsplit записал 38 файлов вместо 192 и напечатал «192»."""
    free = shutil.disk_usage(path).free / 2**30
    if free < need_gb:
        _allow(f"на {path} свободно {free:.1f} ГБ, требуется {need_gb}: генерация даст НЕПОЛНОЕ разбиение", override)


def gate_generated(outdir: str, prefix: str, expected: int) -> None:
    """Ловушка 9. Печатать план вместо факта нельзя: пересчитать созданное на диске."""
    got = len([f for f in os.listdir(outdir) if f.startswith(prefix) and f.endswith('.cnf')])
    if got != expected:
        _refuse(f"просили {expected} файлов, записалось {got}: разбиение НЕПОЛНО, пользоваться нельзя")


def gate_load(host: str | None = None, max_ratio: float = 0.9, override: str | None = None) -> int:
    """Сколько ядер РЕАЛЬНО свободно. Случай: 21 решатель на 8 ядрах; и обратный —
    ВМ-3 простаивала с нулевой загрузкой, пока я считал, что она занята.
    Возвращает число свободных ядер; отказывает, если их нет."""
    if host:
        out = subprocess.run(['bash', '-c', host], capture_output=True, text=True).stdout
        cpus, load = (int(x) for x in out.split()[:1]), None
        try:
            cpus, load = int(out.split()[0]), float(out.split()[1])
        except Exception:
            _refuse(f"не удалось снять загрузку с {host}: {out[:80]}")
    else:
        cpus = os.cpu_count() or 1
        load = os.getloadavg()[0]
    free = int(cpus - load)
    if free <= 0:
        _allow(f"свободных ядер нет: {cpus} ядер, занято {load:.1f}. Запуск только вытеснит текущее", override)
    return free


def gate_log_is_stale(log_path: str, writer_pid: int | None = None, max_silence_s: int = 900) -> None:
    """Журнал живого процесса, который давно не менялся, — НЕ картина работы.

    Наблюдение хозяина, и оно верное: всё, что мы видим через журналы, врёт систематически
    В ОДНУ СТОРОНУ — занижает. Причина в том, что все механизмы обрыва действуют одинаково:
    git заменил файл и дескриптор повис; вывод буферизован; писатель убит; результаты отдаются
    по порядку и ждут медленный первый. Ни один из них не может показать БОЛЬШЕ сделанного,
    только меньше. Поэтому «журнал стоит» никогда не значит «работа стоит».

    За сутки трижды: поиск нашёл 18 точек при журнале с 17; семя, названное застрявшим, дошло
    до 18; потоковый прогон держал готовые результаты, ожидая первый.
    """
    import time as _t
    if not os.path.exists(log_path):
        _refuse(f"журнала {log_path} нет вовсе — судить о работе по нему нельзя")
    silence = _t.time() - os.path.getmtime(log_path)
    alive = False
    if writer_pid:
        try: os.kill(writer_pid, 0); alive = True
        except OSError: alive = False
    if alive and silence > max_silence_s:
        _refuse(f"процесс {writer_pid} ЖИВ, а журнал {log_path} молчит {int(silence)} с. "
                f"Журнал не отражает работу: смотреть на артефакт (файл-свидетель, файл результатов), "
                f"а не на вывод. Занижение — обычный исход, завышение невозможно")


def gate_report_from_artifact(claimed: int, artifact_dir: str, kind: str, n: int) -> None:
    """Отчитываться числом из ЖУРНАЛА, когда рядом лежит артефакт, нельзя.

    Проверяет: нет ли в artifact_dir свидетеля ЛУЧШЕ заявленного. Если есть — заявленное число
    занижено, и отчёт надо строить по файлу.  Обратная ситуация (артефакт хуже заявленного)
    ещё опаснее: значит числа, которое называют, вообще нет на диске."""
    import re as _re, glob as _glob
    best, where = -1, None
    for f in _glob.glob(os.path.join(artifact_dir, "*.txt")):
        txt = "\n".join(l for l in open(f) if not l.strip().startswith("#"))
        pts = [tuple(map(int, m)) for m in _re.findall(r'\((\d+),(\d+),(\d+)\)', txt)]
        if not pts:
            pts = [tuple(int(t) for t in l.split()) for l in txt.splitlines()
                   if len(l.split()) == 3 and all(t.lstrip('-').isdigit() for t in l.split())]
        if len(pts) > best: best, where = len(pts), f
    if best < 0:
        _refuse(f"в {artifact_dir} нет ни одного свидетеля: число {claimed} предъявить нечем")
    if best > claimed:
        _refuse(f"заявлено {claimed}, а на диске лежит свидетель на {best} точек ({os.path.basename(where)}): "
                f"отчёт занижен — журнал отстал от артефакта")
    if best < claimed:
        _refuse(f"заявлено {claimed}, а лучший свидетель на диске — {best} ({os.path.basename(where)}): "
                f"числа {claimed} нет ни в одном артефакте")


def gate_orphaned_solvers(names=("kissat", "cadical", "glucose")) -> list:
    """Решатели, работающие на УДАЛЁННЫХ файлах. Возвращает список PID; пустой — всё в порядке.

    Случай (трижды за сутки): я удалял каталог с кусками, считая работу снятой, а процессы
    держали дескрипторы и продолжали считать осиротевшие inode — ядра заняты, результат никому
    не нужен, и по списку процессов это выглядит как нормальная работа.

    Родственно ловушке 10: там git оставлял живой процесс писать в никуда, здесь я оставлял его
    читать из ниоткуда. Общее — файл исчез, а процесс об этом не знает."""
    import subprocess as _sp
    out = []
    for nm in names:
        pids = _sp.run(["pgrep", "-x", nm], capture_output=True, text=True).stdout.split()
        for pid in pids:
            args = _sp.run(["ps", "-o", "args=", "-p", pid], capture_output=True, text=True).stdout.strip()
            f = args.split()[-1] if args else ""
            if f.endswith(".cnf") and not os.path.exists(f):
                out.append((int(pid), f))
    return out


def gate_log_location(path: str, repo_root: str) -> None:
    """Ловушка 10. git заменяет файл целиком, и вывод ЖИВОГО процесса обрывается молча.
    Журнал работающего прогона не должен лежать внутри рабочего дерева."""
    if os.path.abspath(path).startswith(os.path.abspath(repo_root)):
        _refuse(f"журнал {path} внутри рабочего дерева git: любой коммит во время счёта оборвёт его. "
                f"Писать вне дерева и копировать по завершении")


def gate_kill_pattern(pattern: str) -> None:
    """Случай (трижды за сутки): pkill -f по образцу убивал собственную ssh-сессию,
    потому что образец попадал в её командную строку."""
    own = ' '.join(sys.argv) + os.environ.get('SSH_ORIGINAL_COMMAND', '')
    if pattern in own:
        _refuse(f"образец «{pattern}» встречается в командной строке текущего процесса: "
                f"pkill убьёт и его. Снимать по списку PID")


def gate_background(cmd: str, expect_seconds: int, override: str | None = None) -> None:
    """Случай: генерация запущена не в фоне, оборвалась вместе с командой на середине;
    четыре ядра десять минут «считали» несуществующие файлы."""
    if expect_seconds > 100 and '&' not in cmd and 'nohup' not in cmd and 'setsid' not in cmd:
        _allow(f"прогон на ~{expect_seconds} с запускается на переднем плане: он оборвётся вместе с командой", override)


if __name__ == "__main__":
    print(__doc__)
    print("Ворота:", ", ".join(k for k in globals() if k.startswith("gate_")))
