/* knuth_count2d.c — НЕЗАВИСИМАЯ оценка числа расстановок без трёх на прямой в решётке n x n.
 *
 * Зачем. Точный счёт известен до n=20; отделить форму промаха эвристики (ln n от sqrt n) могло бы
 * одно количество при n=21, но точный счёт там стоит порядка пятисот ядро-лет. Нужна ОЦЕНКА.
 *
 * Способ (Кнут, 1975). Спускаемся от пустого множества, на каждом шаге выбирая равновероятно
 * одну из d допустимых клеток, и перемножаем d по пути. Матожидание произведения равно числу
 * УПОРЯДОЧЕННЫХ последовательностей длины m; делим на m!, получаем число множеств.
 * Спуск, умерший раньше m, даёт ноль — это не брак, а честное слагаемое.
 *
 * Допустимость держится счётчиком: клетка запрещена, если она коллинеарна с какой-то уже
 * выбранной ПАРОЙ. Добавляя P, для каждой прежней Q проходим прямую PQ примитивным шагом и
 * поднимаем счётчик у всех её узлов, кроме P и Q. Стоимость шага O(k*n), всего O(m^2 * n).
 *
 * Погрешность НЕ берётся из собственной оценки метода — она заведомо занижена (замерено вторым
 * солвером: разброс втрое при заявленных 12-54%). Берётся из разброса независимых партий.
 *
 * Аргументы: n m спусков партий семя
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int n, N;
static int blocked[1024];      /* сколько пар делают клетку запрещённой */
static int chosen[128], nch;
static int used[1024];
static unsigned long long rng_s;
static double rnd(void){ rng_s ^= rng_s<<13; rng_s ^= rng_s>>7; rng_s ^= rng_s<<17; return (rng_s>>11)*0x1.0p-53; }

/* поднять (delta=+1) или снять (delta=-1) запрет вдоль прямой через ячейки a и b */
static void mark_line(int a, int b, int delta){
    int ax=a%n, ay=a/n, bx=b%n, by=b/n;
    int dx=bx-ax, dy=by-ay, g=abs(dx); int h=abs(dy);
    while(h){ int t=g%h; g=h; h=t; }
    dx/=g; dy/=g;
    for(int s=-1;s<=1;s+=2){
        int x=ax, y=ay;
        for(;;){
            x+=s*dx; y+=s*dy;
            if(x<0||x>=n||y<0||y>=n) break;
            int c=y*n+x;
            if(c!=a && c!=b) blocked[c]+=delta;
        }
    }
    /* середина отрезка тоже покрыта проходом от a в сторону b */
}

int main(int argc,char**argv){
    n=atoi(argv[1]); int m=atoi(argv[2]);
    long long D=atoll(argv[3]); int B=atoi(argv[4]);
    rng_s=strtoull(argv[5],0,10)|1ULL; N=n*n;
    if(N>1024||m>128){fprintf(stderr,"ОТКАЗ: n=%d m=%d не помещается\n",n,m);return 2;}
    double bl[64]; int nb=0;
    for(int b=0;b<B;b++){
        double sum=0;                       /* среднее произведений по партии */
        for(long long it=0; it<D; it++){
            for(int i=0;i<N;i++){blocked[i]=0;used[i]=0;}
            nch=0;
            double lp=0; int dead=0;
            for(int step=0; step<m; step++){
                int cand[1024], d=0;
                for(int c=0;c<N;c++) if(!used[c] && blocked[c]==0) cand[d++]=c;
                if(d==0){dead=1;break;}
                lp += log((double)d);
                int p = cand[(int)(rnd()*d)];
                for(int i=0;i<nch;i++) mark_line(p, chosen[i], +1);
                chosen[nch++]=p; used[p]=1;
            }
            if(!dead) sum += exp(lp - lgamma(m+1.0));   /* делим на m! сразу, в логах */
        }
        bl[nb++] = sum/D;
    }
    double s=0; for(int i=0;i<nb;i++) s+=bl[i];
    double mean=s/nb, var=0;
    for(int i=0;i<nb;i++) var+=(bl[i]-mean)*(bl[i]-mean);
    var/= (nb>1? nb-1:1);
    printf("n=%d m=%d спусков %lld x %d партий\n", n, m, D, B);
    for(int i=0;i<nb;i++) printf("  партия %d: %.4g\n", i, bl[i]);
    printf("СРЕДНЕЕ %.5g, разброс партий +-%.3g (%.0f%%)\n", mean, sqrt(var), sqrt(var)/mean*100);
    return 0;
}
