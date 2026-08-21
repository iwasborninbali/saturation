/* level_profile2d.c — СКОЛЬКО правильных расстановок существует на КАЖДОМ размере.
 *
 * ЗАЧЕМ. Предложен послойный подъём: взять все расстановки размера k, добавить по точке,
 * получить все размера k+1. Логика полна — условие «нет трёх на прямой» наследуется вниз,
 * значит всякая (k+1)-расстановка содержит k-расстановку, и надстройка ничего не теряет.
 * Вопрос ТОЛЬКО в числе: сколько объектов придётся держать на худшем слое.
 *
 * КАК. Обход по формуле смерти: две точки убивают прямую навсегда. Клетка жива, пока через
 * неё не прошла мёртвая прямая. Идём по клеткам в порядке номера, на каждом шаге берём
 * очередную живую — так каждое подмножество посещается ровно один раз, без повторов.
 *
 * СБОРКА: cc -O3 -march=native -o level_profile2d level_profile2d.c
 * ЗАПУСК: ./level_profile2d <n> [предел_секунд]
 *
 * РАСШИРЕНО ДО 128 КЛЕТОК (n<=11). Прежняя редакция держала маску в одном 64-битном слове.
 * Повод: вывод «шаг промаха эвристики затухает» был снят ПРИ m=2n, то есть ровно на жёстком
 * потолке, и мог быть свойством близости к потолку, а не показателя. Различить можно только
 * на других m, а для этого нужен полный профиль при n>8.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef struct { unsigned long long a,b; } M2;   /* маска на 128 клеток: n <= 11 */
static inline int  m2_get(M2 x,int i){ return i<64 ? (int)((x.a>>i)&1ULL) : (int)((x.b>>(i-64))&1ULL); }
static inline void m2_set(M2*x,int i){ if(i<64) x->a|=1ULL<<i; else x->b|=1ULL<<(i-64); }
static int n, N;
static M2 *LINE;                      /* LINE[i*N+j] — маска всех клеток на прямой через i и j */
static unsigned long long CNT[80];    /* сколько правильных расстановок каждого размера */
static int chosen[80];
static double LIMIT; static struct timespec T0; static int stopped=0;

static double elapsed(void){
    struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return (t.tv_sec-T0.tv_sec)+1e-9*(t.tv_nsec-T0.tv_nsec);
}

static void dfs(int start, int k, M2 dead){
    if(stopped) return;
    if((k&3)==0 && elapsed()>LIMIT){ stopped=1; return; }
    for(int c=start;c<N;c++){
        if(m2_get(dead,c)) continue;
        M2 nd=dead; m2_set(&nd,c);
        for(int t=0;t<k;t++){ M2*m=&LINE[(size_t)c*N+chosen[t]]; nd.a|=m->a; nd.b|=m->b; }
        chosen[k]=c; CNT[k+1]++;
        dfs(c+1,k+1,nd);
        if(stopped) return;
    }
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: level_profile2d <n> [предел_секунд]\n"); return 2; }
    n=atoi(argv[1]); N=n*n;
    if(N>128){ fprintf(stderr,"n>11 не помещается\n"); return 2; }
    LIMIT=(argc>2)?atof(argv[2]):1e18;
    LINE=malloc((size_t)N*N*sizeof(M2));
    for(int i=0;i<N;i++) for(int j=0;j<N;j++){
        M2 m={0,0};
        if(i!=j){
            int xi=i%n, yi=i/n, xj=j%n, yj=j/n;
            for(int k=0;k<N;k++){
                int xk=k%n, yk=k/n;
                if((long long)(xj-xi)*(yk-yi)-(long long)(yj-yi)*(xk-xi)==0) m2_set(&m,k);
            }
        }
        LINE[(size_t)i*N+j]=m;
    }
    clock_gettime(CLOCK_MONOTONIC,&T0);
    CNT[0]=1;
    { M2 z={0,0}; dfs(0,0,z); }
    printf("n=%d %s (%.1fс)\n", n, stopped?"ОБОРВАНО ПО ВРЕМЕНИ — числа НЕПОЛНЫ":"полностью", elapsed());
    unsigned long long peak=0; int pk=0, top=0;
    for(int k=0;k<=N && k<80;k++) if(CNT[k]){ top=k; if(CNT[k]>peak){peak=CNT[k];pk=k;} }
    for(int k=0;k<=top;k++) if(CNT[k]) printf("  размер %2d: %llu\n", k, CNT[k]);
    if(!stopped) printf("  ПИК на размере %d: %llu штук;  на максимуме (%d): %llu;  пик/максимум = %.0f\n",
                        pk, peak, top, CNT[top], (double)peak/(double)CNT[top]);
    return 0;
}
