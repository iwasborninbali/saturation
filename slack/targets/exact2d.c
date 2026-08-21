/* exact2d.c — ИСЧЕРПЫВАЮЩИЙ поиск максимума без трёх на прямой, с отсечением по ёмкости.
 *
 * ЗАЧЕМ ЗДЕСЬ, А НЕ В ЖАДНОМ. Отсечение «k + ёмкость < цель» измерено на полном материале
 * при n=6: убивает до 97% тупиковых ветвей, НЕ ГУБЯ НИ ОДНОЙ ведущей к максимуму. В жадном
 * вероятностном поиске это дало ноль — там цена вычисления съедает выигрыш. Место законного
 * отсечения — исчерпывающее дерево, где срезанная ветка не обходится вовсе.
 *
 * ЁМКОСТЬ. В строке не более двух точек. Значит из живых клеток строки возьмёшь не больше
 * min(2 - уже_в_строке, живых_в_строке). Сумма по строкам — граница сверху на добавимое.
 * То же по столбцам; берём меньшую. Граница ЗАКОННАЯ: ни одна достижимая ветка не срезается.
 *
 * СБОРКА: cc -O3 -march=native -o exact2d exact2d.c
 * ЗАПУСК: ./exact2d <n> <цель> <отсечение 0|1> [секунд] [dump]
 *
 * РАСШИРЕНО ДО 128 КЛЕТОК (n<=11). Прежняя редакция держала маску в одном 64-битном слове
 * и потому обрывалась на n=8. Все выводы о структуре стояли на n=6 и n=7 — на двух точках,
 * и это ровно та узость, против которой мы же и предостерегали.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static int n,N,TARGET,PRUNE,DUMP;
static double LIMIT; static struct timespec T0; static int stopped=0;
typedef struct { unsigned long long a,b; } M2;      /* маска на 128 клеток */
static M2 *LINE;
static inline M2 m2_and_not(M2 x,M2 y){ M2 r={x.a&~y.a, x.b&~y.b}; return r; }
static inline int m2_get(M2 x,int i){ return i<64 ? (int)((x.a>>i)&1ULL) : (int)((x.b>>(i-64))&1ULL); }
static inline void m2_clr(M2*x,int i){ if(i<64) x->a&=~(1ULL<<i); else x->b&=~(1ULL<<(i-64)); }
static inline void m2_set(M2*x,int i){ if(i<64) x->a|=1ULL<<i; else x->b|=1ULL<<(i-64); }
static inline int m2_pop(M2 x){ return __builtin_popcountll(x.a)+__builtin_popcountll(x.b); }
static int chosen[128], rowc[64], colc[64];
static long long nodes=0; static int best=0;

static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return (t.tv_sec-T0.tv_sec)+1e-9*(t.tv_nsec-T0.tv_nsec); }
static int capacity(M2 alive,int k){
    int жст[64],жсб[64];
    for(int t=0;t<n;t++){жст[t]=0;жсб[t]=0;}
    for(int i=0;i<N;i++) if(m2_get(alive,i)){ жст[i/n]++; жсб[i%n]++; }
    int s1=0,s2=0;
    for(int r=0;r<n;r++){ int м=2-rowc[r]; if(м<0)м=0; s1 += жст[r]<м?жст[r]:м; }
    for(int c=0;c<n;c++){ int м=2-colc[c]; if(м<0)м=0; s2 += жсб[c]<м?жсб[c]:м; }
    (void)k; return s1<s2?s1:s2;
}
static void dfs(int start,int k,M2 alive){
    nodes++;
    if((nodes&0xFFFFF)==0 && elapsed()>LIMIT) stopped=1;
    if(stopped) return;
    if(k>best) best=k;
    if(k>=TARGET){
        if(DUMP){ printf("%d",k); for(int t=0;t<k;t++) printf(" %d",chosen[t]); printf("\n"); }
        return;
    }
    int запас = PRUNE ? capacity(alive,k) : m2_pop(alive);
    if(k+запас < TARGET) return;
    for(int c=start;c<N;c++){
        if(!m2_get(alive,c)) continue;
        M2 na=alive;
        for(int t=0;t<=c;t++) m2_clr(&na,t);
        for(int t=0;t<k;t++) na = m2_and_not(na, LINE[(size_t)c*N+chosen[t]]);
        chosen[k]=c; rowc[c/n]++; colc[c%n]++;
        dfs(c+1,k+1,na);
        rowc[c/n]--; colc[c%n]--;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); TARGET=atoi(argv[2]); PRUNE=atoi(argv[3]);
    LIMIT=(argc>4)?atof(argv[4]):1e18; DUMP=(argc>5)?atoi(argv[5]):0;
    N=n*n; if(N>128){fprintf(stderr,"n>11 не помещается\n");return 2;}
    LINE=malloc((size_t)N*N*sizeof(M2));
    for(int i=0;i<N;i++)for(int j=0;j<N;j++){
        M2 m={0,0};
        if(i!=j){int xi=i%n,yi=i/n,xj=j%n,yj=j/n;
            for(int k2=0;k2<N;k2++){int xk=k2%n,yk=k2/n;
                if((long long)(xj-xi)*(yk-yi)-(long long)(yj-yi)*(xk-xi)==0) m2_set(&m,k2);}}
        LINE[(size_t)i*N+j]=m;
    }
    for(int t=0;t<n;t++){rowc[t]=0;colc[t]=0;}
    clock_gettime(CLOCK_MONOTONIC,&T0);
    M2 all={0,0}; for(int i=0;i<N;i++) m2_set(&all,i);
    dfs(0,0,all);
    fprintf(stderr,"n=%d цель=%d отсечение=%s: %s достигнуто %d, узлов %lld, %.2fс\n",
           n,TARGET,PRUNE?"ЁМКОСТЬ":"живые",stopped?"ОБОРВАНО —":"ИСЧЕРПАНО —",best,nodes,elapsed());
    return 0;
}
