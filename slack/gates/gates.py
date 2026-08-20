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
