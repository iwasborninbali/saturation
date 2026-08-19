"""gaps.py — реестр ДЫР В СПЕЦИФИКАЦИИ (не в коде).

Тесты здесь делятся на три сорта:
  A. инварианты, которые ДЕРЖАТСЯ            — обычные тесты (зелёные);
  B. дефекты кода, которые ЛОВЯТСЯ           — обычные тесты, утверждающие поломку (зелёные);
  C. ДЫРЫ спецификации                        — @gap(...): тест утверждает то, что ДОЛЖНО было бы
     выполняться по докстрингам phenomenon.py / holes.py, и падает, потому что этого НЕТ.

Сорт C помечен unittest.expectedFailure: пока дыра открыта — прогон зелёный, дыра
зафиксирована машинно.  Если дыру закрыть, тест даст "unexpected success", и прогон станет
КРАСНЫМ — это заставит убрать маркер и переписать спецификацию.  Так список xfail = список
«чего нет», и он не может незаметно устареть.

`python3 tests/gaps_report.py` печатает этот список в markdown (вход для дип-ресёрча).
"""
from __future__ import annotations

import unittest
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class Gap:
    id: str
    module: str
    title: str
    expected: str      # что обязано выполняться по тексту спецификации
    actual: str        # что на самом деле
    consequence: str   # чем это грозит выводам, которые на спецификацию опираются


REGISTRY: Dict[str, Gap] = {}


def gap(gid: str, *, module: str, title: str, expected: str, actual: str, consequence: str):
    """Пометить тест как фиксацию дыры спецификации; регистрирует метаданные и вешает xfail."""
    def deco(fn):
        if gid in REGISTRY:
            raise RuntimeError(f"duplicate gap id {gid}")
        REGISTRY[gid] = Gap(gid, module, title, expected, actual, consequence)
        fn.__gap_id__ = gid
        fn.__doc__ = f"[{gid}] {title}"
        return unittest.expectedFailure(fn)
    return deco
