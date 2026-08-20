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


def _refuse(msg: str) -> None:
    raise Refusal(msg)


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


def gate_pattern(values: dict[int, int], formula) -> None:
    """Ловушка подгонки. Закономерность, снятая с нескольких точек, — не закон.
    Случаи: 2n^2-2n+4 совпала при n=2,3,4 и провалилась при 5; «бо́льшая группа лучше»
    держалась на четырёх точках и рухнула на следующих четырёх."""
    if len(values) < 6:
        _refuse(f"закономерность построена на {len(values)} точках: этого мало, чтобы называть её законом. "
                f"Приводить как НАБЛЮДЕНИЕ С ДАННЫМИ, добрать точек прежде чем обобщать")
    bad = {n: (v, formula(n)) for n, v in values.items() if formula(n) != v}
    if bad: _refuse(f"формула расходится с данными в точках {sorted(bad)}: {bad}")


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

def gate_disk(path: str = "/tmp", need_gb: float = 5.0) -> None:
    """Случай: диск на ВМ забился, subsplit записал 38 файлов вместо 192 и напечатал «192»."""
    free = shutil.disk_usage(path).free / 2**30
    if free < need_gb:
        _refuse(f"на {path} свободно {free:.1f} ГБ, требуется {need_gb}: генерация даст НЕПОЛНОЕ разбиение")


def gate_generated(outdir: str, prefix: str, expected: int) -> None:
    """Ловушка 9. Печатать план вместо факта нельзя: пересчитать созданное на диске."""
    got = len([f for f in os.listdir(outdir) if f.startswith(prefix) and f.endswith('.cnf')])
    if got != expected:
        _refuse(f"просили {expected} файлов, записалось {got}: разбиение НЕПОЛНО, пользоваться нельзя")


def gate_load(host: str | None = None, max_ratio: float = 0.9) -> int:
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
        _refuse(f"свободных ядер нет: {cpus} ядер, загрузка {load:.1f}. Запуск только вытеснит текущее")
    return free


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


def gate_background(cmd: str, expect_seconds: int) -> None:
    """Случай: генерация запущена не в фоне, оборвалась вместе с командой на середине;
    четыре ядра десять минут «считали» несуществующие файлы."""
    if expect_seconds > 100 and '&' not in cmd and 'nohup' not in cmd and 'setsid' not in cmd:
        _refuse(f"прогон на ~{expect_seconds} с запускается на переднем плане: он оборвётся вместе с командой")


if __name__ == "__main__":
    print(__doc__)
    print("Ворота:", ", ".join(k for k in globals() if k.startswith("gate_")))
