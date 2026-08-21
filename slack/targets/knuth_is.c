/* knuth_is.c — оценка числа правильных m-подмножеств с ВЫБОРОМ ПО ВАЖНОСТИ.
 *
 * ЗАЧЕМ. Равномерный спуск (knuth2d.c) перестаёт долетать при n=25: ноль попаданий из двух
 * миллионов. Причина не в задаче, а в предложении: равномерный выбор ведёт в клетки, которые
 * убивают много, и ветка гибнет задолго до глубины m.
 *
 * ЧТО ИЗМЕНЕНО. Клетка c берётся с вероятностью p(c), пропорциональной ЧИСЛУ ЖИВЫХ,
 * ОСТАЮЩИХСЯ ПОСЛЕ ЕЁ ПОСТАНОВКИ, а вес делится на p(c). Оценка остаётся НЕСМЕЩЁННОЙ:
 * математическое ожидание произведения 1/p по пути равно числу путей. Меняется только
 * дисперсия — и хвост, из-за которого спуски не долетали.
 *
 * ЦЕНА. На каждом шаге вычисляется place() для КАЖДОГО живого кандидата, а не для одного.
 * Дороже на порядок-два за спуск; окупается тем, что спуски долетают.
 *
 * СБОРКА: cc -O3 -march=native -o knuth_is knuth_is.c -lm
 * ЗАПУСК: ./knuth_is <n> <m> <спусков> [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXW 26   /* n<=40: NN=1600, NW=25. Запас в 64 слова замедлял вдвое — структура копируется. */
typedef struct { unsigned long long w[MAXW]; } BS;
static int N,NN,NW;
static BS *LINE;
static inline int bget(const BS*a,int i){return (a->w[i>>6]>>(i&63))&1ULL;}
static inline void bset(BS*a,int i){a->w[i>>6]|=1ULL<<(i&63);}
static inline int bpop(const BS*a){int s=0;for(int t=0;t<NW;t++)s+=__builtin_popcountll(a->w[t]);return s;}
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
static inline double rnd01(void){ return (double)(rnd()>>11)/9007199254740992.0; }
int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: knuth_is <n> <m> <спусков> [семя]\n"); return 2; }
    int n=atoi(argv[1]), m=atoi(argv[2]); long long S=atoll(argv[3]);
    rs=(argc>4)?(unsigned long long)atoll(argv[4]):88172645463325252ULL; if(!rs) rs=1;
    N=n; NN=n*n; NW=(NN+63)/64;
    if(NW>MAXW){ fprintf(stderr,"n слишком велик\n"); return 2; }
    LINE=calloc((size_t)NN*NN,sizeof(BS));
    for(int i=0;i<NN;i++)for(int j=0;j<NN;j++){
        if(i==j) continue;
        int xi=i%n,yi=i/n,xj=j%n,yj=j/n;
        BS b; memset(&b,0,sizeof b);
        for(int k=0;k<NN;k++){int xk=k%n,yk=k/n;
            if((long long)(xj-xi)*(yk-yi)-(long long)(yj-yi)*(xk-xi)==0) bset(&b,k);}
        LINE[(size_t)i*NN+j]=b;
    }
    int *chosen=malloc(sizeof(int)*NN), *cand=malloc(sizeof(int)*NN);
    double *вес=malloc(sizeof(double)*NN);
    BS *после=malloc(sizeof(BS)*NN);
    long double сумма=0.0L, сумма2=0.0L; long long дошло=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    for(long long s=0;s<S;s++){
        BS alive; memset(&alive,0,sizeof alive);
        for(int i=0;i<NN;i++) bset(&alive,i);
        long double w=1.0L; int k=0, жив=1;
        while(k<m){
            int c=0; double сум=0.0;
            for(int i=0;i<NN;i++){
                if(!bget(&alive,i)) continue;
                BS na=alive; na.w[i>>6] &= ~(1ULL<<(i&63));
                for(int t=0;t<k;t++){ BS*L=&LINE[(size_t)i*NN+chosen[t]];
                    for(int q=0;q<NW;q++) na.w[q] &= ~L->w[q]; }
                int ост=bpop(&na);
                double v=(double)ост+1.0;      /* +1: клетка, оставляющая ноль живых, тоже допустима на последнем шаге */
                cand[c]=i; вес[c]=v; после[c]=na; сум+=v; c++;
            }
            if(c==0){ жив=0; break; }
            double r=rnd01()*сум, acc=0.0; int pick=c-1;
            for(int q=0;q<c;q++){ acc+=вес[q]; if(r<=acc){ pick=q; break; } }
            w *= (long double)(сум/вес[pick]);
            alive=после[pick]; chosen[k++]=cand[pick];
        }
        if(жив){ сумма+=w; сумма2+=w*w; дошло++; }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    long double факт=1.0L; for(int i=2;i<=m;i++) факт*=(long double)i;
    long double ср=сумма/(long double)S/факт;
    long double ср2=сумма/(long double)S;
    long double д=сумма2/(long double)S-ср2*ср2;
    long double ош=sqrtl(д>0?д:0)/sqrtl((long double)S)/факт;
    printf("n=%d m=%d спусков=%lld: оценка %.6Le, отн.ошибка %.1Lf%%, дошло %lld (%.1f%%), %.1fс\n",
           n,m,S,ср,(ср>0?ош/ср*100:0.0L),дошло,100.0*дошло/S,el);
    return 0;
}
