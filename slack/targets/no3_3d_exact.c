/* no3_3d_exact.c — ПОЛНЫЙ исчерпывающий перебор: максимум точек в кубе n^3 без трёх
 * на одной прямой (OEIS A399138). Не по орбитам, а по всем подмножествам.
 *
 * ЗАЧЕМ. В черновике A399138 стоят ТОЧНЫЕ значения 1, 8, 16, 28, 40, 64. Точное значение
 * содержит ВЕРХНЮЮ границу, а свидетель даёт только нижнюю. Верхние стоят на SAT с
 * сертификатами DRAT; здесь они берутся независимо, полным перебором, без SAT вообще.
 *
 * ФОРМУЛА СМЕРТИ. Две выбранные точки убивают всю прямую через них: любая третья на ней
 * запрещена навсегда. Держим на каждой клетке счётчик накрывших её мёртвых прямых.
 *
 * ПЛАНКА. Задаётся отдельно и НЕ является источником ответа при ИСЧЕРПАНИИ: отсечение
 * срезает лишь ветви, не способные её превзойти. При обрыве по времени — является,
 * и тогда отчёт говорит об этом словами.
 *
 * СБОРКА: cc -O3 -march=native -o no3_3d_exact no3_3d_exact.c
 * ЗАПУСК: ./no3_3d_exact <n> <секунд> <планка>
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

static int n, NN;
static int *dead;                 /* сколько мёртвых прямых накрыло клетку */
static int px[512], py[512], pz[512], nsel;
static int best, BEST0;
static long long nodes;
static double LIMIT; static int stopped;
static struct timespec T0;
static double elapsed(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t);
  return (t.tv_sec-T0.tv_sec)+(t.tv_nsec-T0.tv_nsec)/1e9; }
static int g3(int a,int b){ if(a<0)a=-a; if(b<0)b=-b; while(b){int t=a%b;a=b;b=t;} return a; }

/* пройти прямую через две точки, изменив счётчики всех прочих её клеток на delta */
static void mark(int x1,int y1,int z1,int x2,int y2,int z2,int delta){
    int dx=x2-x1, dy=y2-y1, dz=z2-z1;
    int g=g3(g3(dx,dy),dz); dx/=g; dy/=g; dz/=g;
    int sx=x1, sy=y1, sz=z1;
    while(sx-dx>=0&&sx-dx<n&&sy-dy>=0&&sy-dy<n&&sz-dz>=0&&sz-dz<n){ sx-=dx; sy-=dy; sz-=dz; }
    for(int x=sx,y=sy,z=sz; x>=0&&x<n&&y>=0&&y<n&&z>=0&&z<n; x+=dx,y+=dy,z+=dz){
        if((x==x1&&y==y1&&z==z1)||(x==x2&&y==y2&&z==z2)) continue;
        dead[(x*n+y)*n+z]+=delta;
    }
}
static void place(int x,int y,int z){
    for(int i=0;i<nsel;i++) mark(px[i],py[i],pz[i],x,y,z,+1);
    px[nsel]=x; py[nsel]=y; pz[nsel]=z; nsel++;
}
static void unplace(void){
    nsel--; int x=px[nsel],y=py[nsel],z=pz[nsel];
    for(int i=0;i<nsel;i++) mark(px[i],py[i],pz[i],x,y,z,-1);
}
static void rec(int start){
    if(stopped) return;
    nodes++;
    if((nodes&0xFFFFF)==0 && elapsed()>LIMIT) stopped=1;
    if(nsel>best) best=nsel;
    int alive=0;
    for(int c=start;c<NN;c++) if(!dead[c]) alive++;
    if(nsel+alive<=best) return;                    /* не сможет превзойти найденное */
    for(int c=start;c<NN;c++){
        if(dead[c]) continue;
        int x=c/(n*n), y=(c/n)%n, z=c%n;
        place(x,y,z);
        rec(c+1);
        unplace();
        if(stopped) return;
    }
}
int main(int argc,char**argv){
    if(argc<3){ fprintf(stderr,"usage: no3_3d_exact <n> <секунд> [планка]\n"); return 2; }
    n=atoi(argv[1]); LIMIT=atof(argv[2]); BEST0=(argc>3)?atoi(argv[3]):0;
    if(n<1||n>8){ fprintf(stderr,"n вне диапазона 1..8\n"); return 2; }
    NN=n*n*n; dead=calloc(NN,sizeof(int)); best=BEST0;
    clock_gettime(CLOCK_MONOTONIC,&T0);
    rec(0);
    if(BEST0>0 && best==BEST0)
        printf("n=%d планка=%d: %s НЕ ПРЕВЗОШЁЛ ПЛАНКИ (о достижимости самой %d ничего не сказано), узлов %lld, %.1fс\n",
               n,BEST0, stopped?"ОБОРВАНО —":"ИСЧЕРПАНО —", BEST0, nodes, elapsed());
    else
        printf("n=%d планка=%d: %s МАКСИМУМ %d, узлов %lld, %.1fс\n",
               n,BEST0, stopped?"ОБОРВАНО —":"ИСЧЕРПАНО —", best, nodes, elapsed());
    return 0;
}
