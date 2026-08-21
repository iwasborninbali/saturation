/* knuth2d.c — НЕСМЕЩЁННАЯ оценка числа правильных m-подмножеств методом Кнута.
 *
 * ЗАЧЕМ. Точный счёт у порога (r = m/2n ~ 0.9) кончается на n=10: дальше дерево растёт
 * на порядки. А вопрос о гипотезе Гая–Келли решается именно поведением промаха при больших n.
 * Оценка Кнута (1975) даёт НЕСМЕЩЁННУЮ оценку числа листьев дерева поиска по случайным
 * спускам: на каждом шаге считаем число ветвей c, выбираем одну наугад, копим произведение.
 * Среднее произведений по многим спускам равно числу листьев ТОЧНО в математическом ожидании.
 *
 * ПОЧЕМУ ПО УПОРЯДОЧЕННЫМ, А НЕ ПО ВОЗРАСТАЮЩИМ. Первая редакция спускалась по дереву
 * возрастающих номеров и НИ РАЗУ не долетела до нужной глубины за два миллиона спусков:
 * выбирая клетку только с бо́льшим номером, спуск сразу прыгает в хвост и упирается в конец
 * диапазона. Считаем УПОРЯДОЧЕННЫЕ последовательности (клетка берётся из всех живых)
 * и делим на m!: каждое подмножество даёт ровно m! последовательностей.
 *
 * ЧЕГО ОНА НЕ ДАЁТ. Разброс может быть огромен, и среднее по выборке — не то же, что
 * ожидание. Поэтому: (1) сверка на точно известных n=6..9 обязательна; (2) приводится
 * разброс, а не только среднее; (3) без сверки числа не используются.
 *
 * СБОРКА: cc -O3 -march=native -o knuth2d knuth2d.c -lm
 * ЗАПУСК: ./knuth2d <n> <m> <спусков> [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define MAXW 16                   /* 1024 клеток: n <= 32 */
typedef struct { unsigned long long w[MAXW]; } BS;
static int N,NN,NW;
static BS *LINE;
static inline int bget(const BS*a,int i){return (a->w[i>>6]>>(i&63))&1ULL;}
static inline void bset(BS*a,int i){a->w[i>>6]|=1ULL<<(i&63);}
static unsigned long long rs;
static inline unsigned long long rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int argc,char**argv){
    if(argc<4){ fprintf(stderr,"usage: knuth2d <n> <m> <спусков> [семя]\n"); return 2; }
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
    long double сумма=0.0L, сумма2=0.0L; long long дошло=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    for(long long s=0;s<S;s++){
        BS alive; memset(&alive,0,sizeof alive);
        for(int i=0;i<NN;i++) bset(&alive,i);
        long double вес=1.0L; int k=0, жив=1;
        while(k<m){
            int c=0;
            for(int i=0;i<NN;i++) if(bget(&alive,i)) cand[c++]=i;
            if(c==0){ жив=0; break; }
            вес*= (long double)c;
            int p=cand[rnd()%(unsigned long long)c];
            for(int t=0;t<k;t++){ BS*L=&LINE[(size_t)p*NN+chosen[t]];
                for(int w=0;w<NW;w++) alive.w[w] &= ~L->w[w]; }
            alive.w[p>>6] &= ~(1ULL<<(p&63));
            chosen[k++]=p;
        }
        if(жив){ сумма+=вес; сумма2+=вес*вес; дошло++; }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    long double факт=1.0L; for(int i=2;i<=m;i++) факт*=(long double)i;
    long double ср=сумма/(long double)S/факт;
    long double ср2=сумма/(long double)S;
    long double дисп=сумма2/(long double)S - ср2*ср2;
    long double ош=sqrtl(дисп>0?дисп:0)/sqrtl((long double)S)/факт;
    printf("n=%d m=%d спусков=%lld: оценка %.6Le, отн.ошибка %.1Lf%%, дошло %lld (%.1f%%), %.1fс\n",
           n,m,S,ср, (ср>0? ош/ср*100:0.0L), дошло, 100.0*дошло/S, el);
    return 0;
}
