/* no4_all.c — ВСЕ максимумы в [n]^3, а не найденные.
 *
 * Зачем. Всякий структурный замер на найденных объектах измеряет отбор, а не предмет: мой
 * симметричный поиск работает в области, где плотность максимумов на порядки выше средней.
 * Несмещённый источник — только полное перечисление. В двумерии оно у второго солвера есть;
 * в трёхмерии не было ни у кого.
 *
 * Считает: сколько всего максимумов, сколько из них имеют хоть одну нетривиальную симметрию куба
 * (48 движений), и сколько классов с точностью до этих движений.
 *
 * Отсечения: ёмкость по трём осям (в слое не более трёх точек) и порядок по индексу.
 * Аргументы: n M [секунды]
 */
/* Фильтр по направлениям здесь ПРОИГРЫВАЕТ и потому выключен по умолчанию: замерено на n=4,
 * 16.8 с против 13.2 с. Он стоит O(k) НОДов против O(k^3) арифметики полной проверки и окупается
 * лишь при k порядка тридцати, как в поиске по орбитам. При k=10 полная проверка дешевле. */
#ifndef USE_DIRFILTER
#define USE_DIRFILTER 0
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n, M;
typedef struct { signed char x,y,z; } P;
static P cell[1400]; static int ncell;
static P S[40]; static int k;
static long long found=0, sym=0, nodes=0;
static FILE *dump=NULL;   /* DUMPFILE: выгрузка самих максимумов для замеров рассеянности */
static int occ[3][20];
static double T; static clock_t st; static int timedout=0;
static int shard=-1,nshard=1,d0=0;
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
/* фильтр по направлениям: два параллельных отрезка компланарны, пересекающиеся дают
   коллинеарную тройку. Значит у любых двух пар направления различны. Это не НОВОЕ отсечение —
   ровно то же отвергает и полная проверка, — но стоит O(k) вместо O(k^3). */
static unsigned char *dseen; static int DM,DSPAN;
static int dtmp[64], dtn;
static int dircode(int dx,int dy,int dz){
    int a=dx<0?-dx:dx,b=dy<0?-dy:dy,c=dz<0?-dz:dz,g;
    while(b){int t=a%b;a=b;b=t;} g=a; while(c){int t=g%c;g=c;c=t;}
    if(g){dx/=g;dy/=g;dz/=g;}
    if(dx<0||(dx==0&&(dy<0||(dy==0&&dz<0)))){dx=-dx;dy=-dy;dz=-dz;}
    return (dx+DM)*DSPAN*DSPAN+(dy+DM)*DSPAN+(dz+DM);
}
static int fits(P q){
    if(occ[0][(int)q.x]>=3||occ[1][(int)q.y]>=3||occ[2][(int)q.z]>=3) return 0;
#if USE_DIRFILTER
    dtn=0;
    for(int i=0;i<k;i++){ int c=dircode(q.x-S[i].x,q.y-S[i].y,q.z-S[i].z);
        if(dseen[c]){ for(int t=0;t<dtn;t++) dseen[dtmp[t]]=0; return 0; }
        dseen[c]=1; dtmp[dtn++]=c; }
    for(int t=0;t<dtn;t++) dseen[dtmp[t]]=0;
#endif
    for(int a=0;a<k;a++)for(int b=a+1;b<k;b++) if(col3(S[a],S[b],q)) return 0;
    for(int a=0;a<k;a++)for(int b=a+1;b<k;b++)for(int c=b+1;c<k;c++) if(det4(S[a],S[b],S[c],q)==0) return 0;
    return 1;
}
/* 48 движений куба: перестановка координат и отражения */
static int perm[6][3]={{0,1,2},{0,2,1},{1,0,2},{1,2,0},{2,0,1},{2,1,0}};
static int has_symmetry(void){
    int m=n-1;
    for(int p=0;p<6;p++) for(int s=0;s<8;s++){
        if(p==0&&s==0) continue;                       /* тождественное не считается */
        int ok=1;
        for(int i=0;i<k&&ok;i++){
            int c[3]={S[i].x,S[i].y,S[i].z};
            int q[3]={c[perm[p][0]],c[perm[p][1]],c[perm[p][2]]};
            if(s&1)q[0]=m-q[0]; if(s&2)q[1]=m-q[1]; if(s&4)q[2]=m-q[2];
            int f=0;
            for(int j=0;j<k;j++) if(S[j].x==q[0]&&S[j].y==q[1]&&S[j].z==q[2]){f=1;break;}
            if(!f) ok=0;
        }
        if(ok) return 1;
    }
    return 0;
}
static int capacity(int start){
    int cap=1<<30;
    for(int a=0;a<3;a++){ int c=0;
        int liv[20]; memset(liv,0,sizeof liv);
        for(int i=start;i<ncell;i++){ int L = a==0?cell[i].x : a==1?cell[i].y : cell[i].z; liv[L]++; }
        for(int L=0;L<n;L++){ int room=3-occ[a][L]; if(room<0)room=0; c += room<liv[L]?room:liv[L]; }
        if(c<cap) cap=c; }
    return cap;
}
static void dfs(int start){
    if(timedout) return;
    if(((++nodes)&0xFFFF)==0 && T>0 && (double)(clock()-st)/CLOCKS_PER_SEC>T){timedout=1;return;}
    if(k==M){ found++; if(has_symmetry()) sym++;
        if(dump){ for(int i=0;i<k;i++) fprintf(dump,"%d %d %d%s",S[i].x,S[i].y,S[i].z,i+1<k?" ":"\n"); }
        return; }
    if(k+(ncell-start)<M) return;
    if(k+capacity(start)<M) return;
    for(int i=start;i<ncell;i++){
        if(d0==0 && shard>=0 && (i%nshard)!=shard) continue;
        if(k+(ncell-i)<M) return;
        if(!fits(cell[i])) continue;
#if USE_DIRFILTER
        for(int j=0;j<k;j++) dseen[dircode(cell[i].x-S[j].x,cell[i].y-S[j].y,cell[i].z-S[j].z)]=1;
#endif
        S[k++]=cell[i]; occ[0][(int)cell[i].x]++; occ[1][(int)cell[i].y]++; occ[2][(int)cell[i].z]++;
        d0++; dfs(i+1); d0--;
        k--; occ[0][(int)cell[i].x]--; occ[1][(int)cell[i].y]--; occ[2][(int)cell[i].z]--;
#if USE_DIRFILTER
        for(int j=0;j<k;j++) dseen[dircode(cell[i].x-S[j].x,cell[i].y-S[j].y,cell[i].z-S[j].z)]=0;
#endif
        if(timedout) return;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); M=atoi(argv[2]); T=argc>3?atof(argv[3]):0;
    if(argc>5){shard=atoi(argv[4]); nshard=atoi(argv[5]);}
    if(n>19||(long)n*n*n>1400){fprintf(stderr,"ОТКАЗ: n=%d не помещается\n",n);return 2;}
    if(M>40){fprintf(stderr,"ОТКАЗ: M=%d больше буфера\n",M);return 2;}
    ncell=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){cell[ncell].x=x;cell[ncell].y=y;cell[ncell].z=z;ncell++;}
    DM=n-1; DSPAN=2*DM+1; dseen=calloc((size_t)DSPAN*DSPAN*DSPAN,1);
    if(!dseen){fprintf(stderr,"ОТКАЗ: нет памяти под направления\n");return 2;}
    { const char*d=getenv("DUMPFILE"); if(d) dump=fopen(d,"w"); }
    memset(occ,0,sizeof occ); st=clock(); dfs(0);
    if(dump) fclose(dump);
    if(timedout) printf("n=%d M=%d ВРЕМЯ ВЫШЛО (узлов %lld, насчитано %lld)\n",n,M,nodes,found);
    else printf("n=%d M=%d доля %d/%d: ВСЕГО %lld, с симметрией %lld (%.1f%%), узлов %lld\n",
                n,M,shard,nshard,found,sym,found?100.0*sym/found:0.0,nodes);
    return 0;
}
