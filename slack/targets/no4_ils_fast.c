/* no4_ils.c — асимметричный итерированный локальный поиск, умеющий СТАРТОВАТЬ С ЗАДАННОГО ЯДРА.
 * Смысл: симметричный обход при n=6 упёрся в 15 при истинных 16, значит симметрия недобирает.
 * Пробить её потолок можно только выйдя из подпространства — но не с нуля, а с найденного ядра:
 * выбить из него несколько точек и доращивать уже без всякой симметрии.
 * Аргументы: n цель секунды семя выход [файл_ядра]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n; typedef struct { int x,y,z; } P;
static P cell[2200]; static int ncell;
static P S[64]; static int k;
static P best[64]; static int bk=0;
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}

/* фильтр по направлениям: у любых двух пар примитивные направления обязаны различаться.
   Необходимое условие, поэтому полная проверка идёт следом. O(k) против O(k^3). */
static unsigned char *dseen; static int DM,DSPAN;
static int dtmp[256], dtn;
static int dircode(int dx,int dy,int dz){
    int a=dx<0?-dx:dx,b=dy<0?-dy:dy,c=dz<0?-dz:dz,g;
    while(b){int t=a%b;a=b;b=t;} g=a; while(c){int t=g%c;g=c;c=t;}
    if(g){dx/=g;dy/=g;dz/=g;}
    if(dx<0||(dx==0&&(dy<0||(dy==0&&dz<0)))){dx=-dx;dy=-dy;dz=-dz;}
    return (dx+DM)*DSPAN*DSPAN+(dy+DM)*DSPAN+(dz+DM);
}
static void dir_rebuild(void){
    memset(dseen,0,(size_t)DSPAN*DSPAN*DSPAN);
    for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)
        dseen[dircode(S[j].x-S[i].x,S[j].y-S[i].y,S[j].z-S[i].z)]=1;
}

static int ok(P q){
    for(int i=0;i<k;i++) if(S[i].x==q.x&&S[i].y==q.y&&S[i].z==q.z) return 0;
    dtn=0;
    for(int i=0;i<k;i++){ int c=dircode(q.x-S[i].x,q.y-S[i].y,q.z-S[i].z);
        if(dseen[c]){ for(int t=0;t<dtn;t++) dseen[dtmp[t]]=0; return 0; }
        dseen[c]=1; dtmp[dtn++]=c; }
    for(int t=0;t<dtn;t++) dseen[dtmp[t]]=0;
    for(int a=0;a<k;a++) for(int b=a+1;b<k;b++) if(col3(S[a],S[b],q)) return 0;
    for(int a=0;a<k;a++) for(int b=a+1;b<k;b++) for(int c=b+1;c<k;c++) if(det4(S[a],S[b],S[c],q)==0) return 0;
    return 1;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int target=atoi(argv[2]); double T=atof(argv[3]);
    unsigned sd=(unsigned)atoi(argv[4]); const char*out=argv[5]; const char*core=argc>6?argv[6]:NULL;
    DM=n-1; DSPAN=2*DM+1; dseen=calloc((size_t)DSPAN*DSPAN*DSPAN,1);
    if(!dseen){fprintf(stderr,"ОТКАЗ: нет памяти под таблицу направлений\n");return 2;}
    srand(sd); ncell=0;
    for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){cell[ncell].x=x;cell[ncell].y=y;cell[ncell].z=z;ncell++;}
    P seedset[64]; int ns=0;
    if(core){FILE*f=fopen(core,"r");char ln[256];
        while(f&&fgets(ln,sizeof ln,f)){if(ln[0]=='#')continue;int a,b,c;if(sscanf(ln,"%d %d %d",&a,&b,&c)==3){seedset[ns].x=a;seedset[ns].y=b;seedset[ns].z=c;ns++;}}
        if(f)fclose(f); fprintf(stderr,"ядро %d точек из %s\n",ns,core);}
    int ord[2200]; clock_t st=clock(); long rs=0;
    while((double)(clock()-st)/CLOCKS_PER_SEC<T&&bk<target){
        rs++;
        k=0;
        if(ns){ int drop=1+rand()%4; int use=ns-drop;
            for(int i=0;i<ns;i++)ord[i]=i;
            for(int i=ns-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
            for(int i=0;i<use;i++) S[k++]=seedset[ord[i]]; }
        dir_rebuild();
        for(int i=0;i<ncell;i++)ord[i]=i;
        for(int i=ncell-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
        for(int i=0;i<ncell;i++) if(ok(cell[ord[i]])) { for(int j=0;j<k;j++) dseen[dircode(cell[ord[i]].x-S[j].x,cell[ord[i]].y-S[j].y,cell[ord[i]].z-S[j].z)]=1; S[k++]=cell[ord[i]]; }
        for(int it=0;it<3000&&k<target;it++){
            if((double)(clock()-st)/CLOCKS_PER_SEC>T) break;
            if(k>bk){bk=k;memcpy(best,S,k*sizeof(P));fprintf(stderr,"  %d точек (перезапуск %ld)\n",bk,rs);}
            int kick=1+rand()%3;
            for(int q=0;q<kick&&k>0;q++){int i=rand()%k;S[i]=S[--k];} dir_rebuild();
            for(int i=ncell-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
            for(int i=0;i<ncell;i++) if(ok(cell[ord[i]])) { for(int j=0;j<k;j++) dseen[dircode(cell[ord[i]].x-S[j].x,cell[ord[i]].y-S[j].y,cell[ord[i]].z-S[j].z)]=1; S[k++]=cell[ord[i]]; }
        }
        if(k>bk){bk=k;memcpy(best,S,k*sizeof(P));fprintf(stderr,"  %d точек (перезапуск %ld)\n",bk,rs);}
    }
    fprintf(stderr,"итог %d точек, перезапусков %ld\n",bk,rs);
    FILE*g=fopen(out,"w"); if(g){for(int i=0;i<bk;i++)fprintf(g,"%d %d %d\n",best[i].x,best[i].y,best[i].z);fclose(g);}
    return bk>=target?0:1;
}
