/* planesizes3d.c — распределение плоскостей куба [n]^3 по числу узлов решётки.
 *
 * ЗАЧЕМ. В двумерии я заменил оценку «тройки независимы» на «прямые независимы» и получил
 * оценку СВЕРХУ вместо оценки СНИЗУ: связь внутри прямой делает избегание легче. Здесь то же
 * самое одной ступенью выше — вместо «четвёрки независимы» взять «ПЛОСКОСТИ независимы».
 * Тогда множитель 1.103, который сейчас ОДОЛЖЕН из двумерия, заменяется ВЫВЕДЕННОЙ скобкой:
 *      порог по четвёркам  <=  истина  <=  порог по плоскостям
 * Разница между заимствованным числом и выведенной границей — это разница между тем,
 * что мы предполагаем, и тем, что мы знаем.
 *
 * КАК СЧИТАЕТСЯ. Плоскость с примитивной нормалью m и сдвигом d несёт k узлов; площадь сечения
 * куба не превышает sqrt(3) n^2, а плотность узлов на плоскости есть 1/|m|, поэтому
 * k >= 4 требует |m| <= sqrt(3) n^2 / 4. Перебираем нормали в этих пределах и считаем узлы.
 *
 * СВЕРКА ОБЯЗАТЕЛЬНА: сумма C(k,4) по плоскостям должна ПРЕВЫШАТЬ точное число компланарных
 * четвёрок ровно на величину переучёта четвёрок, лежащих на одной ПРЯМОЙ (такая четвёрка
 * лежит во многих плоскостях). При n=3 прямых из четырёх узлов нет, поэтому там сумма обязана
 * совпасть с точным 2918 — это и есть проверка перечисления.
 *
 * СБОРКА: cc -O3 -march=native -o planesizes3d planesizes3d.c -lm
 * ЗАПУСК: ./planesizes3d <n>
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

static int gcd3(int a,int b,int c){
    while(b){int t=a%b;a=b;b=t;} a=a<0?-a:a;
    while(c){int t=a%c;a=c;c=t;} return a<0?-a:a;
}

int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: planesizes3d <n>\n"); return 2; }
    int n=atoi(argv[1]);
    int RMAX=n*n; if(getenv("RMAX")) RMAX=atoi(getenv("RMAX"));  /* граница на компоненты нормали. Выведенная sqrt(3)n^2/4 ОКАЗАЛАСЬ ЗАНИЖЕННОЙ: при n=7 она дала 22 и потеряла 8064 плоскости из 346743. Верно найдено СТАБИЛИЗАЦИЕЙ: 30, 45, 60 дают одно и то же. Урок: выведенную границу проверяют стабилизацией, а не доверием к выводу. */      /* граница на компоненты нормали */
    if (RMAX> 400) RMAX=400;
    long long *hist=calloc((size_t)(n*n*n+2),sizeof(long long));
    long long planes=0, rich=0;
    struct timespec t0,t1; clock_gettime(CLOCK_MONOTONIC,&t0);

    for(int a=0;a<=RMAX;a++)
    for(int b=(a==0?0:-RMAX);b<=RMAX;b++)
    for(int c=((a==0&&b==0)?1:-RMAX);c<=RMAX;c++){
        if(a==0&&b==0&&c==0) continue;
        if(gcd3(a,b,c)!=1) continue;
        /* нормаль с точностью до знака: берём лексикографически большую из (m,-m) */
        if (a==0 && (b<0 || (b==0 && c<0))) continue;
        long long lo=0, hi=0;
        lo += (a<0? (long long)a*(n-1):0); hi += (a>0? (long long)a*(n-1):0);
        lo += (b<0? (long long)b*(n-1):0); hi += (b>0? (long long)b*(n-1):0);
        lo += (c<0? (long long)c*(n-1):0); hi += (c>0? (long long)c*(n-1):0);
        long long span = hi-lo+1;
        if (span > 40000000LL) continue;               /* защита: нормаль слишком велика */
        int *cnt=calloc((size_t)span,sizeof(int));
        if(!cnt){ fprintf(stderr,"нет памяти\n"); return 2; }
        for(int x=0;x<n;x++){
            long long ax=(long long)a*x;
            for(int y=0;y<n;y++){
                long long axy=ax+(long long)b*y;
                for(int z=0;z<n;z++) cnt[axy+(long long)c*z-lo]++;
            }
        }
        for(long long d=0; d<span; d++){
            int k=cnt[d];
            if(k>=1) planes++;
            if(k<4) continue;
            /* ПЛОСКОСТИ БЕЗ СОБСТВЕННОЙ ТОЛЩИНЫ ОТБРАСЫВАЮТСЯ. Плоскость может резать куб
             * тонким ломтем и содержать ровно одну прямую: все её узлы коллинеарны. Такая
             * даёт только КОЛЛИНЕАРНЫЕ четвёрки, а те лежат во множестве плоскостей сразу,
             * и учитывать их по каждой значит считать одно и то же многократно.
             * Без этого отбрасывания счёт давал 784395 плоскостей при n=7 против нашего
             * проверенного 346743, и сумма C(k,4) завышала точное число на 28.5% вместо 1.75%. */
            {
                int f1=-1,f2=-1, collinear=1;
                long long dd=d+lo;
                for(int x=0;x<n && collinear;x++){
                    long long ax=(long long)a*x;
                    for(int y=0;y<n && collinear;y++){
                        long long axy=ax+(long long)b*y;
                        for(int z=0;z<n;z++){
                            if(axy+(long long)c*z!=dd) continue;
                            int idx=(x*n+y)*n+z;
                            if(f1<0){ f1=idx; continue; }
                            if(f2<0){ f2=idx; continue; }
                            int x1=f1/(n*n), y1=(f1/n)%n, z1=f1%n;
                            int x2=f2/(n*n), y2=(f2/n)%n, z2=f2%n;
                            long long ux=x2-x1, uy=y2-y1, uz=z2-z1;
                            long long vx=x-x1, vy=y-y1, vz=z-z1;
                            if(uy*vz-uz*vy || uz*vx-ux*vz || ux*vy-uy*vx){ collinear=0; break; }
                        }
                    }
                }
                if(collinear) continue;
            }
            rich++; hist[k]++;
        }
        free(cnt);
    }
    clock_gettime(CLOCK_MONOTONIC,&t1);
    double el=(t1.tv_sec-t0.tv_sec)+1e-9*(t1.tv_nsec-t0.tv_nsec);
    /* сумма C(k,4) — для сверки с точным числом компланарных четвёрок */
    long double s4=0;
    for(int k=4;k<=n*n*n;k++) if(hist[k]) s4 += (long double)hist[k]*k*(k-1)*(k-2)*(k-3)/24.0L;
    printf("n=%d RMAX=%d: богатых плоскостей %lld, сумма C(k,4)=%.0Lf, %.1fс\n", n, RMAX, rich, s4, el);
    printf("распределение (k: сколько):");
    for(int k=4;k<=n*n*n;k++) if(hist[k]) printf(" %d:%lld",k,hist[k]);
    printf("\n");
    free(hist);
    return 0;
}
