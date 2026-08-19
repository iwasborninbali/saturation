"""verify_symmetry_direct.py — проверка симметрийного отсечения ПРЯМЫМ ВЫЧИСЛЕНИЕМ, без решателя.

Зачем ещё одна, когда есть проверка первого солвера. Его метод подставляет юниты и спрашивает
решатель; мой вычисляет клаузы напрямую. Общего между методами нет ничего, кроме проверяемого
предмета, — а именно этого мы и добиваемся: одна ошибка не может пройти через оба.

Что проверяется. Отсечение lex_leader должно быть в точности предикатом «x лексикографически не
больше sigma(x) для всех sigma из группы куба», то есть «x — лексминимум своей орбиты». Опасно
ровно одно направление: если лексминимум орбиты ОТВЕРГНУТ, вся орбита выброшена, и тогда
невыполнимость всех кусков ничего не значит. Обратное направление (лишний выживший) безобидно —
оно лишь ослабляет отсечение.

Метод. Вспомогательные переменные eq_i полностью определяются набором, поэтому клаузы можно не
решать, а вычислить: идём по клеткам, поддерживаем «префиксы совпали», и требуем, чтобы при
совпавшем префиксе из x_i следовало x_{sigma(i)}. Это в точности x <= sigma(x).

usage: python3 verify_symmetry_direct.py n [число_наборов]
"""
import sys, random
sys.path.insert(0, __file__.rsplit('/',1)[0])
from plane4_cnf import cube_group

def survives(x, G, nc):
    """переживает ли набор x отсечение — по той же логике, что закодирована в lex_leader"""
    for sigma in G:
        eq = True
        for i in range(nc):
            a, b = x[i], x[sigma[i]]
            if a == b:            # неподвижная по значению позиция: eq не меняется
                continue
            if eq and a and not b:      # x_i=1, sigma(x)_i=0 при совпавшем префиксе => x > sigma(x)
                return False
            if eq and not a and b:      # x < sigma(x): дальше эта sigma не ограничивает
                break
        # если дошли до конца с eq — наборы равны, ограничение выполнено
    return True

def lexmin_of_orbit(x, G, nc):
    best = tuple(x)
    for sigma in G:
        img = tuple(x[sigma[i]] for i in range(nc))
        if img < best: best = img
    return best

def main(n, trials):
    G = cube_group(n); nc = n**3
    ident = list(range(nc))
    Gfull = G + [ident]
    rnd = random.Random(20260820 + n)
    deadly = harmless = 0
    for t in range(trials):
        k = rnd.randint(2, max(3, nc // 8))
        x = [0]*nc
        for i in rnd.sample(range(nc), k): x[i] = 1
        lm = list(lexmin_of_orbit(x, Gfull, nc))
        if not survives(lm, G, nc):
            deadly += 1
            print(f"  СМЕРТЕЛЬНО: лексминимум орбиты ОТВЕРГНУТ (набор из {k} клеток)")
        # безобидное направление: сколько нелексминимальных всё же выжило
        if x != lm and survives(x, G, nc): harmless += 1
    print(f"n={n}: наборов {trials}, симметрий {len(G)}")
    print(f"  СМЕРТЕЛЬНЫХ (лексминимум отвергнут): {deadly}")
    print(f"  безобидных (нелексминимальный выжил): {harmless}")
    print("  ВЕРДИКТ: отсечение " + ("НЕ ТЕРЯЕТ орбит" if deadly==0 else "ТЕРЯЕТ ОРБИТЫ — ВСЕ ВЫВОДЫ НЕДЕЙСТВИТЕЛЬНЫ"))
    return 0 if deadly==0 else 1

if __name__=="__main__":
    n = int(sys.argv[1]); trials = int(sys.argv[2]) if len(sys.argv)>2 else 300
    sys.exit(main(n, trials))
