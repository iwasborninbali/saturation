/* rows2.c — точный счёт расстановок 2n точек на сетке n x n без трёх на прямой (A000755).
 *
 * ЗАЧЕМ. Родовой счётчик (level_profile2d) обходит ВСЕ подмножества и умирает на n=12:
 * до n=20 по замеру порядка 500 ядро-лет. Чаффин взял n=17 и n=18 ещё в 2006 году, значит
 * дело не в железе, а в алгоритме. Запись A000755_calibration.txt так и кончается:
 * «нам нужен алгоритм, а не ядра». Вот он.
 *
 * ИДЕЯ. При m=2n потолок берётся ровно: в каждой строке НЕ БОЛЬШЕ двух точек (иначе три
 * на прямой), а всего точек 2n при n строках — значит в каждой строке РОВНО две. То же для
 * столбцов. Поэтому перебирать надо не подмножества, а пары столбцов построчно.
 *
 * СМЕРТЬ. Две поставленные точки убивают всю прямую через них навсегда. Держим на каждой
 * клетке счётчик «сколькими мёртвыми прямыми накрыта»; клетка жива при нуле.
 *
 * СБОРКА: cc -O3 -march=native -o rows2 rows2.c
 * ЗАПУСК: ./rows2 <n> [предел_секунд]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, NC;
static int *dead;                 /* счётчик мёртвых прямых на клетке */
static int colcnt[64];
static int px[64], py[64], nsel;  /* поставленные точки */
static long long total, nodes;
static double LIMIT; static int stopped;
static struct timespec T0;
static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
  return (t.tv_sec-T0.tv_sec)+(t.tv_nsec-T0.tv_nsec)/1e9; }

static int gcdi(int a,int b){ if(a<0)a=-a; if(b<0)b=-b; while(b){int t=a%b;a=b;b=t;} return a; }

/* пройти прямую через (x1,y1) и (x2,y2), изменив счётчики всех прочих её клеток на delta */
static void mark_line(int x1,int y1,int x2,int y2,int delta){
    int dx=x2-x1, dy=y2-y1, g=gcdi(dx,dy); dx/=g; dy/=g;
    /* отойти к началу прямой внутри сетки */
    int sx=x1, sy=y1;
    while(sx-dx>=0 && sx-dx<n && sy-dy>=0 && sy-dy<n){ sx-=dx; sy-=dy; }
    for(int x=sx,y=sy; x>=0&&x<n&&y>=0&&y<n; x+=dx,y+=dy){
        if((x==x1&&y==y1)||(x==x2&&y==y2)) continue;
        dead[y*n+x]+=delta;
    }
}
static void place(int x,int y){
    for(int i=0;i<nsel;i++) mark_line(px[i],py[i],x,y,+1);
    px[nsel]=x; py[nsel]=y; nsel++; colcnt[x]++;
}
static void unplace(void){
    nsel--; int x=px[nsel], y=py[nsel]; colcnt[x]--;
    for(int i=0;i<nsel;i++) mark_line(px[i],py[i],x,y,-1);
}
/* ПЕРВАЯ РЕДАКЦИЯ ПРОИГРАЛА РОДОВОМУ СЧЁТЧИКУ: n=10 за 41.06с против 6.98с у него.
 * Правильная идея (в строке ровно две) со слабым отсечением хуже неправильной с сильным.
 * Две правки: (а) отсекать и по СТРОКАМ — всякой незаполненной нужно >=2 живых клетки;
 * (б) заполнять не по порядку, а САМУЮ СТЕСНЁННУЮ строку. Выбор её однозначен по
 * состоянию, поэтому каждая расстановка по-прежнему рождается ровно один раз. */
static int filled[64];
static int pick_row(int depth){
    int rem=n-depth, colalive[64];
    for(int x=0;x<n;x++) colalive[x]=0;
    int bestr=-1, bestc=1<<30;
    for(int y=0;y<n;y++){
        if(filled[y]) continue;
        int r=0;
        for(int x=0;x<n;x++)
            if(dead[y*n+x]==0 && colcnt[x]<2){ r++; colalive[x]++; }
        if(r<2) return -1;                  /* строке нечем заполниться */
        if(r<bestc){ bestc=r; bestr=y; }
    }
    for(int x=0;x<n;x++){
        int need=2-colcnt[x];
        if(need>rem) return -1;             /* столбцу не хватит строк */
        if(colalive[x]<need) return -1;     /* столбцу не хватит живых клеток */
    }
    return bestr;
}
static void rec(int depth){
    if(stopped) return;
    nodes++;
    if((nodes&0xFFFFF)==0 && elapsed()>LIMIT) stopped=1;
    if(depth==n){ total++; return; }
    int y=pick_row(depth);
    if(y<0) return;
    filled[y]=1;
    for(int a=0;a<n;a++){
        if(dead[y*n+a] || colcnt[a]>=2) continue;
        place(a,y);
        for(int b=a+1;b<n;b++){
            if(dead[y*n+b] || colcnt[b]>=2) continue;
            place(b,y);
            rec(depth+1);
            unplace();
            if(stopped){ unplace(); filled[y]=0; return; }
        }
        unplace();
    }
    filled[y]=0;
}
int main(int argc,char**argv){
    if(argc<2){ fprintf(stderr,"usage: rows2 <n> [секунд]\n"); return 2; }
    n=atoi(argv[1]); LIMIT=(argc>2)?atof(argv[2]):1e9;
    if(n<2||n>40){ fprintf(stderr,"n вне диапазона\n"); return 2; }
    NC=n*n; dead=calloc(NC,sizeof(int));
    clock_gettime(CLOCK_MONOTONIC,&T0);
    rec(0);
    printf("n=%d: %s A000755 = %lld, узлов %lld, %.2fс\n",
           n, stopped?"ОБОРВАНО, НЕПОЛНО —":"", total, nodes, elapsed());
    return 0;
}

/* ИТОГ ЗАМЕРА, чтобы не переписывали заново.
 * Улучшенная редакция (отсечение по строкам + самая стеснённая строка):
 *      n= 8   216 823 узла   0.27с
 *      n= 9 1 800 321 узел   2.68с
 *      n=10 15 514 075 узлов 28.54с      рост ~8.6 на шаг
 * Родовой счётчик (level_profile2d, ALL=1) на том же n=10: 5 531 521 узел, 6.98с.
 * ПОСТРОЧНАЯ ПЕРЕФОРМУЛИРОВКА ПРОИГРЫВАЕТ ВТРОЕ. Показатель тот же (~9 на шаг),
 * выиграна только константа, и та в минус. Экстраполяция от n=10 при 8.6 на шаг:
 *      n=15  15 суток      n=20  ~3800 лет      n=21  ~32000 лет
 * Значит узкое место НЕ в формулировке. Чаффин взял n=17,18 на железе 2006 года —
 * его метод примерно втрое-тысячекратно лучше обоих наших, и за двадцать минут он
 * не воспроизводится. Отказ с числом: новый член A000755 этим путём недостижим. */
