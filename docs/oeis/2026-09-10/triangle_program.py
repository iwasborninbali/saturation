from math import gcd
def row(n): # T(n,0..2n): k-subsets of the n X n grid with no three collinear points
    N = n*n; P = [divmod(i, n) for i in range(N)]
    L = [[sum(1 << k for k in range(N) if k != i and k != j and (P[k][0]-P[i][0])*(P[j][1]-P[i][1]) == (P[k][1]-P[i][1])*(P[j][0]-P[i][0])) for j in range(N)] for i in range(N)]
    T = [0]*(2*n+1)
    def dfs(start, chosen, F): # F = cells collinear with two chosen cells (blocked)
        T[len(chosen)] += 1
        for c in range(start, N):
            if not F >> c & 1:
                G = F
                for s in chosen: G |= L[s][c]
                dfs(c+1, chosen + [c], G)
    dfs(0, [], 0); return T
if __name__ == "__main__":
    import sys
    for n in range(1, int(sys.argv[1]) + 1): print(n, row(n))
