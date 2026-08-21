/* no4_anneal.c — ВТОРАЯ реализация поиска, устроенная иначе: не наращивание, а починка.
 *
 * Зачем вторая. Измерено (второй солвер, столбец r=0.50): разброс между семенами занижает истинную
 * погрешность до 5.5 раз, потому что семена меряют дисперсию ОДНОГО алгоритма при ОДНОМ способе
 * обхода. Всё, чем реализации различаются, изнутри невидимо. Десять семян моего наращивателя,
 * дружно дающих 35 при n=15, — это одно наблюдение, а не десять.
 *
 * Устройство. Берётся СРАЗУ M точек (k орбит цикла), считается число нарушений — компланарных
 * четвёрок и коллинеарных троек, — и отжигом обменивается орбита на орбиту, пока нарушения не
 * обнулятся. Наращиватель никогда не проходит через неправильные наборы; этот только через них
 * и ходит. Способы промахиваться у них разные, и в этом весь смысл.
 *
 * Аргументы: n орбит секунды семя выход
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
static int n,m_;
typedef struct{int x,y,z;} P;
#define MAXO 9000
static P orb[MAXO][3]; static int norb=0;
static int sel[64], nsel;            /* выбранные орбиты */
static P pts[192]; static int npts;
static unsigned long long rs;
static double rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return (rs>>11)*0x1.0p-53;}
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
static void rebuild(void){ npts=0; for(int i=0;i<nsel;i++) for(int t=0;t<3;t++) pts[npts++]=orb[sel[i]][t]; }
    /* нарушения, задевающие слот [lo,hi). Перебираются ТОЛЬКО тупли, где слот участвует:
   раньше сканировались все C(npts,4), теперь только те, где хоть одна точка из слота. */
static long long viol_of(int lo,int hi){
    int sl[8], ns=0, ot[192], no=0;
    for(int i=0;i<npts;i++){ if(i>=lo&&i<hi) sl[ns++]=i; else ot[no++]=i; }
    long long v=0;
    /* тройки */
    for(int i=0;i<ns;i++){
        for(int a=0;a<no;a++) for(int b=a+1;b<no;b++)
            if(col3(pts[sl[i]],pts[ot[a]],pts[ot[b]])) v++;
        for(int j=i+1;j<ns;j++){
            for(int a=0;a<no;a++) if(col3(pts[sl[i]],pts[sl[j]],pts[ot[a]])) v++;
            for(int k=j+1;k<ns;k++) if(col3(pts[sl[i]],pts[sl[j]],pts[sl[k]])) v++;
        }
    }
    /* четвёрки */
    for(int i=0;i<ns;i++){
        for(int a=0;a<no;a++) for(int b=a+1;b<no;b++) for(int c=b+1;c<no;c++)
            if(det4(pts[sl[i]],pts[ot[a]],pts[ot[b]],pts[ot[c]])==0) v++;
        for(int j=i+1;j<ns;j++){
            for(int a=0;a<no;a++) for(int b=a+1;b<no;b++)
                if(det4(pts[sl[i]],pts[sl[j]],pts[ot[a]],pts[ot[b]])==0) v++;
            for(int k=j+1;k<ns;k++)
                for(int a=0;a<no;a++) if(det4(pts[sl[i]],pts[sl[j]],pts[sl[k]],pts[ot[a]])==0) v++;
        }
    }
    return v;
}
static long long viol_all(void){
    long long v=0;
    for(int a=0;a<npts;a++)for(int b=a+1;b<npts;b++)for(int c=b+1;c<npts;c++){
        if(col3(pts[a],pts[b],pts[c])) v++;
        for(int d=c+1;d<npts;d++) if(det4(pts[a],pts[b],pts[c],pts[d])==0) v++; }
    return v;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int K=atoi(argv[2]); double T=atof(argv[3]);
    rs=strtoull(argv[4],0,10)|1ULL; const char*out=argv[5];
    if((long)n*n*n>27000){fprintf(stderr,"ОТКАЗ: n=%d велико\n",n);return 2;}
    static int seen[27000]; memset(seen,0,sizeof seen);
    for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){
        int id=(x*n+y)*n+z; if(seen[id])continue;
        P p={x,y,z},cur=p; int k=0;
        do{int c=(cur.x*n+cur.y)*n+cur.z; if(!seen[c]){seen[c]=1; if(k<3) orb[norb][k]=cur; k++;}
           P q={cur.y,cur.z,cur.x}; cur=q;}while(!(cur.x==p.x&&cur.y==p.y&&cur.z==p.z)&&k<3);
        if(k==3) norb++;                      /* только орбиты размера 3 */
    }
    if(K>60||3*K>192){fprintf(stderr,"ОТКАЗ: K=%d велико\n",K);return 2;}
    fprintf(stderr,"n=%d орбит размера 3: %d, ищем %d орбит = %d точек\n",n,norb,K,3*K);
    clock_t st=clock(); long long best=1LL<<60; long tries=0;
    while((double)(clock()-st)/CLOCKS_PER_SEC<T){
        tries++;
        nsel=0; { int used[MAXO]; memset(used,0,sizeof used);
            while(nsel<K){ int o=(int)(rnd()*norb); if(!used[o]){used[o]=1; sel[nsel++]=o;} } }
        rebuild(); long long cur=viol_all(); long acc=0;
        double temp=cur>0? (double)cur/4.0 : 1.0;
        for(long it=0; it<30000 && cur>0; it++){
            if((it&1023)==0 && (double)(clock()-st)/CLOCKS_PER_SEC>T) break;
            temp*=0.9996; if(temp<0.02) temp=0.02;
            int i=(int)(rnd()*nsel);
            int o=(int)(rnd()*norb); int dup=0;
            for(int j=0;j<nsel;j++) if(sel[j]==o) dup=1;
            if(dup) continue;
            int old=sel[i];
            long long before=viol_of(3*i,3*i+3);
            sel[i]=o; rebuild();
            long long after=viol_of(3*i,3*i+3);
            long long d=after-before;
            if(d<=0 || rnd()<exp(-(double)d/temp)){ cur+=d;
                if((++acc%2000)==0){ long long ex=viol_all();
                    if(ex!=cur){ fprintf(stderr,"ОТКАЗ: приращения разошлись с полным счётом (%lld против %lld)\n",cur,ex); return 3; } } }
            else { sel[i]=old; rebuild(); }
        }
        if(cur<best){ best=cur;
            fprintf(stderr,"  нарушений %lld (попытка %ld)\n",best,tries); fflush(stderr);
            if(best==0 && out){ FILE*f=fopen(out,"w");
                if(f){for(int i=0;i<npts;i++)fprintf(f,"%d %d %d\n",pts[i].x,pts[i].y,pts[i].z);fclose(f);} } }
        if(best==0) break;
    }
    fprintf(stderr,"итог: нарушений %lld, попыток %ld\n",best,tries);
    return best==0?0:1;
}
