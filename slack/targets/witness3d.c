/* witness3d.c — поиск больших конфигураций без четырёх компланарных в кубе [n]^3.
 *
 * ЗАЧЕМ. У A280537 данные обрываются на a(8)=20; девятого члена нет ни у кого.
 * Энтропийный порог предсказывает a(9) ~ 22. Предсказание проверяется тем, что 22 точки
 * при n=9 либо находятся, либо нет — и найденная конфигурация даёт ПЕРВУЮ нижнюю границу.
 *
 * УСТРОЙСТВО — ПО СМЕРТИ. Клетка жива, пока через неё не прошла ни одна мёртвая прямая
 * (две точки) и ни одна мёртвая плоскость (три точки). Растим жадно из пустоты, выбирая
 * среди живых, пока живых не останется. Конфигурация максимальна не достижением,
 * а исчерпанием.
 *
 * ДВА ПРАВИЛА ВЫБОРА, оба меряются:
 *   0 — случайное среди живых;
 *   1 — «наименьший урон»: та клетка, что убивает меньше всего остальных.
 * Второе — естественная эвристика смерти: беречь место для рождения.
 *
 * ПОЧЕМУ ПЕРЕЗАПУСКИ, А НЕ УЛУЧШЕНИЕ. Измерено сегодня: у конфигурации вблизи максимума
 * СОСЕДЕЙ НЕТ — удаление любой точки оживляет ровно одну клетку, ту же самую. Локальный
 * поиск двигаться не может в принципе, только далёкие прыжки. Отсюда: расти от пустоты
 * и перезапускаться, а не чинить почти готовое.
 *
 * СБОРКА: cc -O3 -march=native -o witness3d witness3d.c
 * ЗАПУСК: ./witness3d <n> <цель> <перезапусков> [правило 0|1] [семя]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXW 16                         /* 16*64 = 1024 клетки, то есть n <= 10 */
typedef struct { unsigned long long w[MAXW]; } BS;

static int N, NN, NW;
static signed char *PX,*PY,*PZ;
static BS *killp;                       /* маска прямой через пару */

static inline void bs_zero(BS*a){ for(int t=0;t<NW;t++) a->w[t]=0ULL; }
static inline void bs_set(BS*a,int i){ a->w[i>>6]|=1ULL<<(i&63); }
static inline int  bs_get(const BS*a,int i){ return (a->w[i>>6]>>(i&63))&1ULL; }
static inline void bs_andnot(BS*a,const BS*b){ for(int t=0;t<NW;t++) a->w[t]&=~b->w[t]; }
static inline int  bs_pop(const BS*a){ int s=0; for(int t=0;t<NW;t++) s+=__builtin_popcountll(a->w[t]); return s; }

static unsigned long long rs;
static inline unsigned long long rnd(void){
    rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs;
}

/* маска плоскости через три точки, без них самих */
static void plane_mask(int i,int j,int k,BS*out){
    long long ux=PX[j]-PX[i], uy=PY[j]-PY[i], uz=PZ[j]-PZ[i];
    long long vx=PX[k]-PX[i], vy=PY[k]-PY[i], vz=PZ[k]-PZ[i];
    long long a=uy*vz-uz*vy, b=uz*vx-ux*vz, c=ux*vy-uy*vx;
    long long d=a*PX[i]+b*PY[i]+c*PZ[i];
    bs_zero(out);
    if (a==0&&b==0&&c==0) return;
    for(int t=0;t<NN;t++)
        if (a*PX[t]+b*PY[t]+c*PZ[t]==d) bs_set(out,t);
    out->w[i>>6]&=~(1ULL<<(i&63));
    out->w[j>>6]&=~(1ULL<<(j&63));
    out->w[k>>6]&=~(1ULL<<(k&63));
}

int main(int argc,char**argv){
    if (argc<4){ fprintf(stderr,"usage: witness3d <n> <цель> <перезапусков> [правило] [семя]\n"); return 2; }
    int n=atoi(argv[1]), target=atoi(argv[2]);
    long long tries=atoll(argv[3]);
    int rule = (argc>4)? atoi(argv[4]) : 1;
    rs = (argc>5)? (unsigned long long)atoll(argv[5]) : 88172645463325252ULL;
    N=n; NN=n*n*n; NW=(NN+63)/64;
    if (NW>MAXW){ fprintf(stderr,"n слишком велико\n"); return 2; }

    PX=malloc(NN); PY=malloc(NN); PZ=malloc(NN);
    { int t=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){PX[t]=x;PY[t]=y;PZ[t]=z;t++;} }
    killp=malloc((size_t)NN*NN*sizeof(BS));
    if(!killp){ fprintf(stderr,"нет памяти под маски пар\n"); return 2; }
    for(int i=0;i<NN;i++)
        for(int j=i+1;j<NN;j++){
            BS m; bs_zero(&m);
            long long ux=PX[j]-PX[i], uy=PY[j]-PY[i], uz=PZ[j]-PZ[i];
            for(int k=0;k<NN;k++){
                if(k==i||k==j) continue;
                long long vx=PX[k]-PX[i], vy=PY[k]-PY[i], vz=PZ[k]-PZ[i];
                if (uy*vz-uz*vy==0 && uz*vx-ux*vz==0 && ux*vy-uy*vx==0) bs_set(&m,k);
            }
            killp[(size_t)i*NN+j]=m; killp[(size_t)j*NN+i]=m;
        }

    int *chosen=malloc(sizeof(int)*NN), *best=malloc(sizeof(int)*NN);
    int bestk=0; long long hits=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);
    for(long long tr=0; tr<tries; tr++){
        BS alive; bs_zero(&alive);
        for(int i=0;i<NN;i++) bs_set(&alive,i);
        int k=0;
        while(1){
            int cnt=bs_pop(&alive);
            if(!cnt) break;
            int pick=-1;
            if (rule==0 || k<2){
                int r=(int)(rnd()%(unsigned long long)cnt), seen=0;
                for(int i=0;i<NN;i++) if(bs_get(&alive,i)){ if(seen++==r){pick=i;break;} }
            } else {
                /* НАИМЕНЬШИЙ УРОН: беречь место для рождения */
                int bestdmg=1<<30;
                for(int i=0;i<NN;i++){
                    if(!bs_get(&alive,i)) continue;
                    BS na=alive; na.w[i>>6]&=~(1ULL<<(i&63));
                    for(int t=0;t<k;t++) bs_andnot(&na,&killp[(size_t)i*NN+chosen[t]]);
                    for(int a=0;a<k;a++) for(int b=a+1;b<k;b++){
                        BS pm; plane_mask(chosen[a],chosen[b],i,&pm); bs_andnot(&na,&pm);
                    }
                    int dmg=cnt-1-bs_pop(&na);
                    if(dmg<bestdmg || (dmg==bestdmg && (rnd()&1))){ bestdmg=dmg; pick=i; }
                }
            }
            if(pick<0) break;
            alive.w[pick>>6]&=~(1ULL<<(pick&63));
            for(int t=0;t<k;t++) bs_andnot(&alive,&killp[(size_t)pick*NN+chosen[t]]);
            for(int a=0;a<k;a++) for(int b=a+1;b<k;b++){
                BS pm; plane_mask(chosen[a],chosen[b],pick,&pm); bs_andnot(&alive,&pm);
            }
            chosen[k++]=pick;
        }
        if(k>bestk){
            bestk=k; memcpy(best,chosen,sizeof(int)*k);
            clock_gettime(CLOCK_MONOTONIC,&t1);
            double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
            printf("НАЙДЕНО %d точек (перезапуск %lld, %.1fс):", k, tr, el);
            for(int t=0;t<k;t++) printf(" (%d,%d,%d)",PX[best[t]],PY[best[t]],PZ[best[t]]);
            printf("\n"); fflush(stdout);
        }
        if(k>=target){ hits++; break; }
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    printf("ИТОГ n=%d: лучшее %d (цель %d), %.1fс\n", n, bestk, target, el);
    return 0;
}
