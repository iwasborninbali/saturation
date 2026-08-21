/* knuth_imp2d.c — оценка числа расстановок без трёх на прямой ВЫБОРОМ ПО ВАЖНОСТИ.
 *
 * Наивный равновероятный спуск (knuth_count2d.c) измеренно проваливается уже при n=10:
 * 134 против точных 1135 при разбросе 162%. Причина — у самого потолка m=2n дерево узко,
 * успешные спуски редки и несут огромный вес, так что среднее определяется хвостом.
 *
 * Починка. Выбираем кандидата c с вероятностью p(c), пропорциональной тому, СКОЛЬКО кандидатов
 * останется после него (просмотр на один шаг вперёд), и домножаем на 1/p(c) вместо d.
 * Оценка остаётся несмещённой при любых положительных p; смещается только дисперсия, а она нам
 * и мешала. Вес берём (останется + 1), чтобы ни один путь не получил нулевой вероятности.
 *
 * Погрешность — из разброса независимых партий, а не из собственной оценки метода.
 *
 * Аргументы: n m спусков партий семя
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
static int n, N;
static int blocked[1024], used[1024], chosen[128], nch;
static int tmpmark[1024];
static unsigned long long rs;
static double rnd(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*0x1.0p-53; }

static void line_apply(int a,int b,int delta,int *arr){
    int ax=a%n, ay=a/n, bx=b%n, by=b/n;
    int dx=bx-ax, dy=by-ay, g=abs(dx), h=abs(dy);
    while(h){int t=g%h; g=h; h=t;}
    dx/=g; dy/=g;
    for(int s=-1;s<=1;s+=2){
        int x=ax,y=ay;
        for(;;){ x+=s*dx; y+=s*dy;
            if(x<0||x>=n||y<0||y>=n) break;
            int c=y*n+x; if(c!=a&&c!=b) arr[c]+=delta; }
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int m=atoi(argv[2]);
    long long D=atoll(argv[3]); int B=atoi(argv[4]); rs=strtoull(argv[5],0,10)|1ULL;
    N=n*n; if(N>1024||m>128){fprintf(stderr,"ОТКАЗ: не помещается\n");return 2;}
    double bl[64]; int nb=0;
    for(int b=0;b<B;b++){
        double sum=0;
        for(long long it=0; it<D; it++){
            for(int i=0;i<N;i++){blocked[i]=0;used[i]=0;}
            nch=0; double lw=0; int dead=0;
            for(int step=0; step<m; step++){
                int cand[1024], d=0;
                for(int c=0;c<N;c++) if(!used[c]&&blocked[c]==0) cand[d++]=c;
                if(d==0){dead=1;break;}
                double w[1024], tot=0;
                if(step+1<m){
                    for(int i=0;i<d;i++){
                        int c=cand[i];
                        for(int t=0;t<N;t++) tmpmark[t]=0;
                        for(int j=0;j<nch;j++) line_apply(c,chosen[j],1,tmpmark);
                        int rem=0;
                        for(int t=0;t<d;t++){ int u=cand[t]; if(u!=c && tmpmark[u]==0) rem++; }
                        w[i]=rem+1.0; tot+=w[i];
                    }
                } else { for(int i=0;i<d;i++){w[i]=1.0;} tot=d; }
                double r=rnd()*tot, acc=0; int pick=d-1;
                for(int i=0;i<d;i++){ acc+=w[i]; if(r<=acc){pick=i;break;} }
                lw += log(tot/w[pick]);
                int p=cand[pick];
                for(int j=0;j<nch;j++) line_apply(p,chosen[j],1,blocked);
                chosen[nch++]=p; used[p]=1;
            }
            if(!dead) sum += exp(lw - lgamma(m+1.0));
        }
        bl[nb++]=sum/D;
    }
    double s=0; for(int i=0;i<nb;i++) s+=bl[i];
    double mean=s/nb, var=0;
    for(int i=0;i<nb;i++) var+=(bl[i]-mean)*(bl[i]-mean);
    var/=(nb>1?nb-1:1);
    printf("n=%d m=%d: СРЕДНЕЕ %.5g, разброс партий +-%.3g (%.0f%%)\n", n,m,mean,sqrt(var),sqrt(var)/mean*100);
    return 0;
}
