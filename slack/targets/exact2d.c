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
 * ЗАПУСК: ./exact2d <n> <цель> <отсечение 0|1>
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static int n,N,TARGET,PRUNE;
static unsigned long long *LINE;
static int chosen[128], rowc[64], colc[64];
static long long nodes=0; static int best=0;

static int capacity(unsigned long long alive,int k){
    int жст[64],жсб[64];
    for(int t=0;t<n;t++){жст[t]=0;жсб[t]=0;}
    unsigned long long a=alive;
    while(a){ int i=__builtin_ctzll(a); a&=a-1; жст[i/n]++; жсб[i%n]++; }
    int s1=0,s2=0;
    for(int r=0;r<n;r++){ int м=2-rowc[r]; if(м<0)м=0; s1 += жст[r]<м?жст[r]:м; }
    for(int c=0;c<n;c++){ int м=2-colc[c]; if(м<0)м=0; s2 += жсб[c]<м?жсб[c]:м; }
    (void)k; return s1<s2?s1:s2;
}
static void dfs(int start,int k,unsigned long long alive){
    nodes++;
    if(k>best) best=k;
    if(k>=TARGET) return;
    int запас = PRUNE ? capacity(alive,k) : __builtin_popcountll(alive);
    if(k+запас < TARGET) return;
    unsigned long long a = alive & ~((start? ((1ULL<<start)-1) : 0ULL));
    while(a){
        int c=__builtin_ctzll(a); a&=a-1;
        unsigned long long na=alive & ~((1ULL<<(c+1))-1);
        for(int t=0;t<k;t++) na &= ~LINE[(size_t)c*N+chosen[t]];
        chosen[k]=c; rowc[c/n]++; colc[c%n]++;
        dfs(c+1,k+1,na);
        rowc[c/n]--; colc[c%n]--;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); TARGET=atoi(argv[2]); PRUNE=atoi(argv[3]);
    N=n*n; if(N>64){fprintf(stderr,"n>8\n");return 2;}
    LINE=malloc((size_t)N*N*sizeof(unsigned long long));
    for(int i=0;i<N;i++)for(int j=0;j<N;j++){
        unsigned long long m=0;
        if(i!=j){int xi=i%n,yi=i/n,xj=j%n,yj=j/n;
            for(int k2=0;k2<N;k2++){int xk=k2%n,yk=k2/n;
                if((long long)(xj-xi)*(yk-yi)-(long long)(yj-yi)*(xk-xi)==0) m|=1ULL<<k2;}}
        LINE[(size_t)i*N+j]=m;
    }
    for(int t=0;t<n;t++){rowc[t]=0;colc[t]=0;}
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    dfs(0,0,(N==64)?~0ULL:((1ULL<<N)-1));
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("n=%d цель=%d отсечение=%s: достигнуто %d, узлов %lld, %.2fс\n",
           n,TARGET,PRUNE?"ЁМКОСТЬ":"живые",best,nodes,el);
    return 0;
}
