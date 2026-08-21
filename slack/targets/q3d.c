/* q3d.c — точное число КОМПЛАНАРНЫХ ЧЕТВЁРОК в кубе [n]^3.
 *
 * ЗАЧЕМ. Энтропийный порог для A280537 стоит на Q(n): порог m* решает
 *      log C(N,m) = C(m,4)/C(N,4) * Q(n),   N = n^3.
 * В двумерии аналогичная величина выведена точно: T(n) ~ (3/pi^2) n^4 ln n, и численный ряд
 * идёт туда же. В трёхмерии константа пока стоит на ПЯТИ точках и догадке — значит её надо
 * прижать численно, прежде чем что-то утверждать.
 *
 * КАК СЧИТАЕТСЯ. Четвёрка компланарна тогда и только тогда, когда три разностных вектора
 * от одной из её точек линейно зависимы. Считаем УПОРЯДОЧЕННЫЕ четвёрки (A,B,C,D) различных
 * точек с det(B-A, C-A, D-A) = 0 и делим на 24: каждое 4-подмножество даёт ровно 24 таких
 * упорядочения, и условие симметрично.
 *
 * Это ЧЕСТНЫЙ счёт нулевых определителей, а не сумма C(k,4) по плоскостям: та завышает,
 * потому что четвёрка на одной прямой лежит во МНОГИХ плоскостях и считается многократно
 * (при n=3 совпало, при n=4 разошлось на 1.16% — прямых из четырёх узлов там уже хватает).
 *
 * СВЕРКА ОБЯЗАТЕЛЬНА: при n=3 ответ обязан быть 2918, при n=4 — 64576.
 * Оба числа у нас проверены независимо ранее.
 *
 * СБОРКА: cc -O3 -march=native -o q3d q3d.c
 * ЗАПУСК: ./q3d <n>
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(int argc, char **argv){
    if (argc < 2){ fprintf(stderr, "usage: q3d <n>\n"); return 2; }
    int n = atoi(argv[1]);
    int N = n*n*n;
    signed char *X = malloc(N), *Y = malloc(N), *Z = malloc(N);
    int t = 0;
    for (int x=0;x<n;x++) for (int y=0;y<n;y++) for (int z=0;z<n;z++){
        X[t]=x; Y[t]=y; Z[t]=z; t++;
    }
    unsigned long long ord = 0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    /* A < B < C < D по индексу: считаем сразу 4-ПОДМНОЖЕСТВА, деление на 24 не нужно */
    for (int a=0;a<N;a++){
        int ax=X[a], ay=Y[a], az=Z[a];
        for (int b=a+1;b<N;b++){
            int ux=X[b]-ax, uy=Y[b]-ay, uz=Z[b]-az;
            for (int c=b+1;c<N;c++){
                int vx=X[c]-ax, vy=Y[c]-ay, vz=Z[c]-az;
                /* нормаль плоскости через A,B,C */
                long long nx = (long long)uy*vz - (long long)uz*vy;
                long long ny = (long long)uz*vx - (long long)ux*vz;
                long long nz = (long long)ux*vy - (long long)uy*vx;
                if (nx==0 && ny==0 && nz==0){
                    /* A,B,C коллинеарны: ЛЮБАЯ четвёртая точка компланарна с ними */
                    ord += (unsigned long long)(N - c - 1);
                    continue;
                }
                for (int d=c+1;d<N;d++){
                    long long wx=X[d]-ax, wy=Y[d]-ay, wz=Z[d]-az;
                    if (nx*wx + ny*wy + nz*wz == 0) ord++;
                }
            }
        }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d: компланарных четвёрок %llu, точек %d, %.1fс\n", n, ord, N, el);
    free(X); free(Y); free(Z);
    return 0;
}
