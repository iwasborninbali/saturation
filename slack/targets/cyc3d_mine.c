/* cyc3d_mine.c — НЕЗАВИСИМЫЙ исчерпывающий обход циклически-инвариантных конфигураций
 * в кубе [n]^3 без четырёх компланарных.
 *
 * ЗАЧЕМ. У напарника два утверждения выше n=8: симметричный максимум равен ровно 23 при n=9
 * и ровно 26 при n=10, деревья исчерпаны. Свидетель проверяется за секунды кем угодно;
 * ИСЧЕРПАНИЕ проверяется только ПОВТОРЕНИЕМ. Написано с нуля, без чтения их кода, чтобы
 * проверка не унаследовала их слепых пятен.
 *
 * УСТРОЙСТВО. Циклическая перестановка (x,y,z) -> (y,z,x). Клетки с x=y=z неподвижны
 * (орбита размера 1), прочие лежат в орбитах размера 3. Инвариантное множество есть
 * ОБЪЕДИНЕНИЕ ОРБИТ, поэтому обход идёт по орбитам, а не по клеткам.
 *
 * ОТСЕЧЕНИЯ: (1) орбита мертва, если её добавление даёт четыре компланарных с уже взятыми;
 * (2) ёмкость: в каждой осевой плоскости не более 3 точек, значит k + сумма по слоям
 *     min(3-занято, доступно) <= ЛУЧШЕМУ НАЙДЕННОМУ отсекает ветку доказуемо.
 *     Резать по ЦЕЛИ здесь нельзя: цель 3n недостижима, и такое отсечение срезает максимум.
 *
 * СБОРКА: cc -O3 -march=native -o cyc3d_mine cyc3d_mine.c
 * ЗАПУСК: ./cyc3d_mine <n> <секунд>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, NN, NORB;
static signed char *PX,*PY,*PZ;
static int (*ORB)[3];          /* клетки орбиты */
static int *OSZ;               /* размер орбиты: 1 или 3 */
static int *chosen;            /* выбранные КЛЕТКИ */
static int *orbsel;            /* выбранные орбиты */
static long long nodes=0; static int best=0;
static double LIMIT; static struct timespec T0; static int stopped=0;
static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
    return (t.tv_sec-T0.tv_sec)+1e-9*(t.tv_nsec-T0.tv_nsec); }
static inline int idx(int x,int y,int z){ return (x*n+y)*n+z; }

/* четыре точки компланарны? */
static inline int coplanar(int a,int b,int c,int d){
    long long ux=PX[b]-PX[a],uy=PY[b]-PY[a],uz=PZ[b]-PZ[a];
    long long vx=PX[c]-PX[a],vy=PY[c]-PY[a],vz=PZ[c]-PZ[a];
    long long wx=PX[d]-PX[a],wy=PY[d]-PY[a],wz=PZ[d]-PZ[a];
    return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)==0;
}
/* законно ли добавить орбиту o к выбранным k клеткам */
static int lawful(int o,int k){
    int m=OSZ[o];
    int t[3]; for(int i=0;i<m;i++) t[i]=ORB[o][i];
    /* внутри самой орбиты: если m=3, три её точки не должны быть коллинеарны,
     * иначе с любой четвёртой дадут компланарную четвёрку */
    if(m==3){
        long long ux=PX[t[1]]-PX[t[0]],uy=PY[t[1]]-PY[t[0]],uz=PZ[t[1]]-PZ[t[0]];
        long long vx=PX[t[2]]-PX[t[0]],vy=PY[t[2]]-PY[t[0]],vz=PZ[t[2]]-PZ[t[0]];
        if(uy*vz-uz*vy==0 && uz*vx-ux*vz==0 && ux*vy-uy*vx==0) return 0;
    }
    /* четвёрки: сколько новых точек участвует — 1,2,3 */
    for(int i=0;i<m;i++){
        /* 1 новая + 3 старых */
        for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++)
            if(coplanar(chosen[a],chosen[b],chosen[c],t[i])) return 0;
        /* 2 новых + 2 старых */
        for(int j=i+1;j<m;j++){
            for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)
                if(coplanar(chosen[a],chosen[b],t[i],t[j])) return 0;
            /* 3 новых + 1 старая */
            for(int l=j+1;l<m;l++)
                for(int a=0;a<k;a++)
                    if(coplanar(chosen[a],t[i],t[j],t[l])) return 0;
        }
    }
    return 1;
}
static int TARGET;
/* ДОЛИ по индексу ПЕРВОЙ взятой орбиты: у всякой конфигурации она одна, доли не пересекаются
 * и в сумме дают всё. Проверяется тем, что сумма долей воспроизводит цельный ответ. */
static int SHARD=-1, NSHARD=1;
/* НАЧАЛЬНОЕ ЛУЧШЕЕ. Если нижняя граница уже известна свидетелем (например 26 при n=10),
 * можно начать с best = граница-1 и резать всё, что её не превосходит. Ответ не меняется:
 * мы ищем максимум, а он заведомо не ниже известного. Дерево сжимается сильно.
 * ОГОВОРКА: при таком запуске «МАКСИМУМ = best0» означает «ничего выше не найдено»,
 * а не «максимум равен best0» — читать надо как проверку превосходства. */
static int BEST0=0;
static int slab[3][64];
static int capacity(int start){
    int c[3][64];
    for(int o=0;o<3;o++) for(int t=0;t<n;t++) c[o][t]=0;
    for(int o=start;o<NORB;o++)
        for(int i=0;i<OSZ[o];i++){ int p=ORB[o][i]; c[0][PX[p]]++; c[1][PY[p]]++; c[2][PZ[p]]++; }
    int m=1<<30;
    for(int o=0;o<3;o++){ int s=0;
        for(int t=0;t<n;t++){ int мест=3-slab[o][t]; if(мест<0)мест=0;
            s += c[o][t]<мест?c[o][t]:мест; }
        if(s<m) m=s; }
    return m;
}
static void dfs(int start,int k,int no){
    if(stopped) return;
    nodes++;
    if((nodes&0xFFFFF)==0 && elapsed()>LIMIT) stopped=1;
    if(k>best) best=k;
    /* ОШИБКА ПЕРВОЙ РЕДАКЦИИ: резал по цели 3n, которая НЕДОСТИЖИМА, и тем самым срезал
     * всё, что не дотягивается до неё — включая настоящий максимум. При n=7 дало 17 против
     * верных 18; при n=5 и n=6 совпало случайно. Для ПОИСКА МАКСИМУМА резать надо по
     * текущему лучшему: ветка мертва, если не может ПРЕВЗОЙТИ уже найденное. */
    if(k+capacity(start) <= best) return;
    for(int o=start;o<NORB;o++){
        if(k==0 && SHARD>=0 && (o % NSHARD)!=SHARD) continue;
        if(!lawful(o,k)) continue;
        int m=OSZ[o];
        for(int i=0;i<m;i++){ int p=ORB[o][i]; chosen[k+i]=p;
            slab[0][PX[p]]++; slab[1][PY[p]]++; slab[2][PZ[p]]++; }
        orbsel[no]=o;
        dfs(o+1,k+m,no+1);
        for(int i=0;i<m;i++){ int p=ORB[o][i];
            slab[0][PX[p]]--; slab[1][PY[p]]--; slab[2][PZ[p]]--; }
        if(stopped) return;
    }
}
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: cyc3d_mine <n> <секунд> [цель]\n"); return 2; }
    n=atoi(argv[1]); LIMIT=atof(argv[2]); NN=n*n*n;
    TARGET=(argc>3)?atoi(argv[3]):3*n;
    if(argc>5){ SHARD=atoi(argv[4]); NSHARD=atoi(argv[5]); }
    if(argc>6){ BEST0=atoi(argv[6]); best=BEST0; }
    if(n>60){ fprintf(stderr,"n слишком велик\n"); return 2; }
    PX=malloc(NN);PY=malloc(NN);PZ=malloc(NN);
    { int t=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){PX[t]=x;PY[t]=y;PZ[t]=z;t++;} }
    ORB=malloc(sizeof(int)*3*NN); OSZ=malloc(sizeof(int)*NN);
    char *seen=calloc(NN,1);
    NORB=0;
    for(int p=0;p<NN;p++){
        if(seen[p]) continue;
        int x=PX[p],y=PY[p],z=PZ[p];
        int a=idx(x,y,z), b=idx(y,z,x), c=idx(z,x,y);
        if(a==b && b==c){ ORB[NORB][0]=a; OSZ[NORB]=1; seen[a]=1; }
        else { ORB[NORB][0]=a; ORB[NORB][1]=b; ORB[NORB][2]=c; OSZ[NORB]=3;
               seen[a]=seen[b]=seen[c]=1; }
        NORB++;
    }
    chosen=malloc(sizeof(int)*NN); orbsel=malloc(sizeof(int)*NN);
    for(int o=0;o<3;o++) for(int t=0;t<n;t++) slab[o][t]=0;
    clock_gettime(CLOCK_MONOTONIC,&T0);
    dfs(0,0,0);
    printf("n=%d орбит=%d доля=%d/%d нач.лучшее=%d: %s МАКСИМУМ %d, узлов %lld, %.1fс\n",
           n,NORB,SHARD,NSHARD,BEST0, stopped?"ОБОРВАНО —":"ИСЧЕРПАНО —", best, nodes, elapsed());
    return 0;
}
