"""Замкнутая нуль-модель для доли дважды занятых диагоналей + спектр направлений."""
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

# ---- конечное n: max-entropy по диагоналям (<=2 на диагональ, всего 2n точек) ----
def kappa_null_finite(n):
    c = np.array([n-abs(j) for j in range(-(n-1), n)], dtype=float)
    def total(z):
        w1 = c*z; w2 = c*(c-1)/2*z*z
        return ((w1 + 2*w2)/(1+w1+w2)).sum() - 2*n
    z = brentq(total, 1e-12, 10.0)
    w1 = c*z; w2 = c*(c-1)/2*z*z
    return (w2/(1+w1+w2)).sum()/n

# ---- предел n->infty ----
def kappa_null_limit():
    def tot(y):
        f = lambda s: (y*s + (y*s)**2)/(1 + y*s + (y*s)**2/2)
        return 2*quad(f, 0, 1)[0] - 2
    y = brentq(tot, 1e-9, 100)
    g = lambda s: ((y*s)**2/2)/(1 + y*s + (y*s)**2/2)
    return y, 2*quad(g, 0, 1)[0]

print("нуль-модель «случайные 2n точек, <=2 на диагональ» (строки/столбцы НЕ навязаны):")
for n in (12, 16, 20, 40, 100, 1000, 10000):
    print(f"   n={n:>6}: kappa_null = {kappa_null_finite(n):.5f}")
y, kl = kappa_null_limit()
print(f"   предел n->oo: y = {y:.6f},  kappa_null = {kl:.6f}")
print()
print("измерено на настоящих решениях: kappa(20) = 0.73036,  kappa(18..19) ~ 0.7310..0.7314")
for name, v in [("pi/sqrt3", np.pi/3**0.5), ("4/pi", 4/np.pi), ("2-4/pi", 2-4/np.pi),
                ("sqrt3-1", 3**0.5-1), ("pi^2/12-", np.pi**2/12-0.09), ("ln2+", np.log(2)+0.037),
                ("3/4", 0.75), ("2-pi/sqrt3+...", 2-np.pi/3**0.5+0.544)]:
    print(f"   {name:>15} = {v:.5f}")
