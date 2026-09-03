# A398172 (subsets of the n X n grid with no three collinear points) and A398184 (maximal such subsets):
# second, independent program (bitmask DFS). a(n) = total, b(n) = maximal. Python 3.
from math import gcd
def A398172_A398184(n):
    N = n*n; P = [(i//n, i%n) for i in range(N)]; L = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i+1, N):
            dx, dy = P[j][0]-P[i][0], P[j][1]-P[i][1]; g = gcd(dx, dy); dx //= g; dy //= g
            L[i][j] = L[j][i] = sum(1 << k for k in range(N) if k != i and k != j and (P[k][0]-P[i][0])*dy == (P[k][1]-P[i][1])*dx)
    full = (1 << N) - 1; cnt = [0, 0]
    def dfs(start, S, chosen, F):        # F = cells lying on a line through two chosen points (forbidden)
        cnt[0] += 1
        if S | F == full: cnt[1] += 1    # maximal: every free cell is forbidden
        for c in range(start, N):
            if not F >> c & 1:
                G = F
                for s in chosen: G |= L[s][c]
                dfs(c+1, S | 1 << c, chosen + [c], G)
    dfs(0, 0, [], 0); return cnt[0], cnt[1]
if __name__ == "__main__":
    print([A398172_A398184(n) for n in range(1, 7)])   # [(2, 1), (16, 1), (230, 23), (4812, 347), (109536, 5646), (3599697, 116411)]
