# OEIS — копипаст во «внутренний формат» (3.09.2026)

Как вставлять: на oeis.org → «Contribute new sequence» (для новых) или «Edit» на A399138 → внизу формы ссылка/переключатель
«internal format» (редактирование %-строками) → вставить блок целиком, поля %A/%D/%K автор/дата подставит система (проверь %O и %K).
Числа для n = 7 — ПОДТВЕРЖДЕНЫ двумя независимыми программами (коллега, 115 с на Маке; opus, 1688 с на ВМ): 101612896 и 2445518;
f-вектор n=7: 1, 49, 1176, 17600, 175952, 1189868, 5367308, 15657764, 28228158, 29554396, 16533504, 4399596, 471860, 15532, 132 (132 = A000755(7) ✓);
максимальные по размерам n=7: {8: 4136, 9: 97712, 10: 864918, 11: 1158976, 12: 305960, 13: 13684, 14: 132}.

---------------------------------------------------------------- НОВАЯ 1
%N Number of subsets of the n X n grid with no three collinear points (the empty set is counted).
%S 2,16,230,4812,109536,3599697
%C a(n) is the number of faces (including the empty face) of the independence complex of the 3-uniform hypergraph whose edges are the collinear triples of the n X n grid (A000938(n) triples); the number of faces of size 2n is A000755(n), and 2n is the maximum size.
%C f-vectors (number of subsets by size): n=3: 1, 9, 36, 76, 78, 28, 2; n=4: 1, 16, 120, 516, 1278, 1668, 998, 204, 11; n=5: 1, 25, 300, 2148, 9498, 25052, 36698, 26700, 8242, 840, 32; n=6: 1, 36, 630, 6768, 47331, 215448, 620210, 1073076, 1035097, 496436, 98950, 5664, 50.
%C Computed by two independent programs (exhaustive depth-first enumeration).
%e For n = 2 every subset of the 2 X 2 grid is admissible, so a(2) = 2^4 = 16. For n = 3 the 512 subsets minus those containing one of the 8 collinear triples leave a(3) = 230.
%o (Python)
%o from itertools import combinations
%o def a(n):
%o     cells=[(r,c) for r in range(n) for c in range(n)]; N=len(cells); ix={c:i for i,c in enumerate(cells)}
%o     coll=[[] for _ in range(N)]
%o     for p,q,r in combinations(cells,3):
%o         if (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])==0:
%o             i,j,k=ix[p],ix[q],ix[r]; coll[i].append((j,k)); coll[j].append((i,k)); coll[k].append((i,j))
%o     inS=[False]*N
%o     def rec(k):
%o         if k==N: return 1
%o         t=rec(k+1)
%o         if not any(inS[i] and inS[j] for i,j in coll[k]):
%o             inS[k]=True; t+=rec(k+1); inS[k]=False
%o         return t
%o     return rec(0)
%Y Cf. A000755, A000769, A000938, A277433, A219760.
%K nonn,hard,more
%O 1,1
%A Aleksei Kudriashov, Sep 03 2026
СЕДЬМОЙ ЧЛЕН ПОДТВЕРЖДЁН — правка A398172 (когда есть слот; edit → internal format → заменить строку %S):
%S 2,16,230,4812,109536,3599697,101612896
и в Discussion: a(7) confirmed by the second independent program (1688 s, Python DFS on a 32-core VM).

---------------------------------------------------------------- НОВАЯ 2
%N Number of maximal subsets of the n X n grid with no three collinear points (subsets to which no further grid point can be added).
%S 1,1,23,347,5646,116411
%C These are the facets of the independence complex of the collinear-triples hypergraph of the n X n grid. Their sizes range from A277433(n) (Martin Gardner's minimum no-3-in-a-line problem, all slopes) to 2n; exactly A000755(n) of them have the maximum size 2n. The complex is not pure for n >= 3.
%C Numbers of maximal subsets by size: n=3: sizes 4, 5, 6 occur 5, 16, 2 times; n=4: sizes 4..8 occur 2, 8, 210, 116, 11 times; n=5: sizes 6..10 occur 152, 1468, 3474, 520, 32 times; n=6: sizes 6..12 occur 8, 172, 11955, 49332, 49830, 5064, 50 times.
%C Computed by two independent programs (exhaustive depth-first enumeration with a maximality check).
%e For n = 3 there are 23 maximal subsets: 5 of size 4, 16 of size 5 and 2 of size 6 (the two 6-point no-three-in-line solutions of the 3 X 3 grid).
%o (Python) see the program for the total count; count only those complete subsets S for which every cell outside S is collinear with two cells of S.
%Y Cf. A000755, A000769, A000938, A277433, A219760.
%K nonn,hard,more
%O 1,2
%A Aleksei Kudriashov, Sep 03 2026
СЕДЬМОЙ ЧЛЕН ПОДТВЕРЖДЁН — правка A398184 (когда есть слот): заменить строку %S и добавить строку %C:
%S 1,1,23,347,5646,116411,2445518
%C n=7: sizes 8..14 occur 4136, 97712, 864918, 1158976, 305960, 13684, 132 times.
и в Discussion: a(7) confirmed by the second independent program.

---------------------------------------------------------------- ПРАВКА A399138 (Edit → internal format)
Заменить строку %C:
%C Lower bounds for the next terms, with witness configurations in the attached file: a(7) >= 73, a(8) >= 94, a(9) >= 116, a(10) >= 138, a(11) >= 164. The configurations for n = 8..11 were found by exact optimization (CP-SAT) restricted to configurations invariant under a subgroup of the symmetry group of the cube; those for n = 9 and n = 10 are optimal within their symmetry class (a subgroup of order 12); the bound at n = 11 is not closed. - _Aleksei Kudriashov_, Sep 03 2026
Заменить строку %H a-файла:
%H Aleksei Kudriashov, <a href="/A399138/a399138.txt">Witness configurations for a(1)-a(6) and for the bounds a(7) >= 73, a(8) >= 94, a(9) >= 116, a(10) >= 138, a(11) >= 164</a>.
Файл для загрузки: docs/oeis/a399138.txt (этот репозиторий).

---------------------------------------------------------------- ВТОРОЙ %o (коллега) — добавить в ОБЕ записи при правке седьмых членов
%o (Python) # second, independent program (bitmask search; returns (A398172(n), A398184(n)))
%o # A398172 (subsets of the n X n grid with no three collinear points) and A398184 (maximal such subsets):
%o # second, independent program (bitmask DFS). a(n) = total, b(n) = maximal. Python 3.
%o from math import gcd
%o def A398172_A398184(n):
%o     N = n*n; P = [(i//n, i%n) for i in range(N)]; L = [[0]*N for _ in range(N)]
%o     for i in range(N):
%o         for j in range(i+1, N):
%o             dx, dy = P[j][0]-P[i][0], P[j][1]-P[i][1]; g = gcd(dx, dy); dx //= g; dy //= g
%o             L[i][j] = L[j][i] = sum(1 << k for k in range(N) if k != i and k != j and (P[k][0]-P[i][0])*dy == (P[k][1]-P[i][1])*dx)
%o     full = (1 << N) - 1; cnt = [0, 0]
%o     def dfs(start, S, chosen, F):        # F = cells lying on a line through two chosen points (forbidden)
%o         cnt[0] += 1
%o         if S | F == full: cnt[1] += 1    # maximal: every free cell is forbidden
%o         for c in range(start, N):
%o             if not F >> c & 1:
%o                 G = F
%o                 for s in chosen: G |= L[s][c]
%o                 dfs(c+1, S | 1 << c, chosen + [c], G)
%o     dfs(0, 0, [], 0); return cnt[0], cnt[1]
%o     print([A398172_A398184(n) for n in range(1, 7)])   # [(2, 1), (16, 1), (230, 23), (4812, 347), (109536, 5646), (3599697, 116411)]
