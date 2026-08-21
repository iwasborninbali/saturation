"""first_moment_indep.py — НЕЗАВИСИМОЕ построение порога первого момента для задачи о трёх на прямой.

Написано по собственному выводу, без чтения кода второго солвера: у нас уже измерено, что
независимые реализации дают вчетверо разные деревья при совпадающих ответах, и здесь проверяется
то же самое на ЧИСЛЕ.

Вывод. Коллинеарная тройка однозначно определяется своей СРЕДНЕЙ точкой, поэтому число троек
равно сумме по неупорядоченным парам числа целых точек строго между ними, а между (0,0) и (a,b)
их ровно gcd(a,b)-1.

    T(n) = 2 * SUM_{a,b>=1} (n-a)(n-b)(gcd(a,b)-1)  +  2n * SUM_{a>=1} (n-a)(a-1)

Прямая сумма стоит O(n^2). Свёртка Дирихле её убирает: gcd(a,b) = SUM_{d | gcd} phi(d), откуда

    SUM_{a,b} (n-a)(n-b) gcd(a,b) = SUM_d phi(d) * ( SUM_{a: d|a} (n-a) )^2      — O(n log n)

Порог: наименьшее m, при котором ожидание числа правильных m-множеств падает ниже единицы,
то есть ln C(n^2, m) = T(n) * C(m,3) / C(n^2,3).
"""
import sys
from math import lgamma, log, gcd, pi, sqrt

def totients(N):
    ph = list(range(N + 1))
    for p in range(2, N + 1):
        if ph[p] == p:                      # p простое
            for q in range(p, N + 1, p):
                ph[q] -= ph[q] // p
    return ph

def T_collinear(n, ph):
    m = n - 1
    # S(d) = сумма (n-a) по a, кратным d, a<=m
    tot = 0
    for d in range(1, m + 1):
        k = m // d                          # a = d, 2d, ..., kd
        # SUM_{j=1..k} (n - j*d) = k*n - d*k(k+1)/2
        S = k * n - d * k * (k + 1) // 2
        tot += ph[d] * S * S
    # SUM_{a,b>=1}(n-a)(n-b)gcd = tot ; вычитаем SUM (n-a)(n-b)*1
    U = sum(n - a for a in range(1, m + 1))
    body = tot - U * U
    axis = sum((n - a) * (a - 1) for a in range(1, m + 1))
    return 2 * body + 2 * n * axis

def lnC(N, k):
    if k < 0 or k > N: return float('-inf')
    return lgamma(N + 1) - lgamma(k + 1) - lgamma(N - k + 1)

def threshold(n, ph):
    N = n * n
    T = T_collinear(n, ph)
    lnC3 = lnC(N, 3)
    def gap(m):
        return lnC(N, m) - T * __import__('math').exp(lnC(m, 3) - lnC3)
    lo, hi = 2, min(N, 8 * n)
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if gap(mid) > 0: lo = mid
        else: hi = mid
    return lo, T

ph = totients(70000)
print(f"{'n':>7} {'порог m*':>10} {'m*/n':>10}")
prev = None
for n in [1000, 2000, 4000, 8000, 16000, 32000, 64000]:
    m, T = threshold(n, ph)
    print(f"{n:>7} {m:>10} {m/n:>10.5f}")
    prev = (n, m / n)
print()
print(f"pi/sqrt(3)     = {pi/sqrt(3):.6f}")
print(f"(2pi^2/3)^(1/3)= {(2*pi*pi/3)**(1/3):.6f}")
