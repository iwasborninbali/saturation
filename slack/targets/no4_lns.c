/* no4_lns.c — большая окрестность с ТОЧНЫМ доращиванием.
 *
 * Симметричный обход даёт максимум внутри подпространства, но при n=6 он равен 15 при истинных 16 —
 * значит потолок симметрии реален и пробивается только выходом из неё. Стохастическое доращивание
 * ничего не доказывает; здесь оно ЗАМЕНЕНО полным перебором: выбиваем j точек и обходим ВСЕ способы
 * доложить остаток. Если ни одно выбивание j точек не даёт прироста — это утверждение об окрестности,
 * а не отчёт о неудаче.
 *
 * Аргументы: n свидетель j
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { int x,y,z; } P;
static int n; static P W[64]; static int nw=0;
static P cur[64]; static int nc=0; static int bestadd=0; static P bestset[64]; static int bestn=0;
static P cand[2200]; static int ncand;
static long long nodes=0;
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
static int fits(P q){
    for(int i=0;i<nc;i++) if(cur[i].x==q.x&&cur[i].y==q.y&&cur[i].z==q.z) return 0;
    for(int a=0;a<nc;a++) for(int b=a+1;b<nc;b++) if(col3(cur[a],cur[b],q)) return 0;
    for(int a=0;a<nc;a++) for(int b=a+1;b<nc;b++) for(int c=b+1;c<nc;c++) if(det4(cur[a],cur[b],cur[c],q)==0) return 0;
    return 1;
}
/* полный обход доращиваний: список кандидатов пересчитывается на каждом уровне */
static void complete(int start){
    nodes++;
    if(nc>bestn){bestn=nc;memcpy(bestset,cur,nc*sizeof(P));}
    for(int i=start;i<ncand;i++){
        if(!fits(cand[i])) continue;
        cur[nc++]=cand[i];
        complete(i+1);
        nc--;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); const char*wf=argv[2]; int j=atoi(argv[3]);
    FILE*f=fopen(wf,"r"); char ln[256];
    if(!f){fprintf(stderr,"ОТКАЗ: свидетель %s не читается. Инструмент без входа не считает по остатку.\n",wf);return 2;}
    while(fgets(ln,sizeof ln,f)){if(ln[0]=='#')continue;int a,b,c;if(sscanf(ln,"%d %d %d",&a,&b,&c)==3){W[nw].x=a;W[nw].y=b;W[nw].z=c;nw++;}}
    fclose(f);
    if(nw<4){fprintf(stderr,"ОТКАЗ: во входе %d точек, считать нечего.\n",nw);return 2;}
    setvbuf(stdout,NULL,_IOLBF,0);
    ncand=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){cand[ncand].x=x;cand[ncand].y=y;cand[ncand].z=z;ncand++;}
    printf("свидетель %d точек, выбиваем по %d, кандидатов %d\n",nw,j,ncand);
    int globalbest=nw; long long tried=0;
    /* рекурсивный обход ВСЕХ подмножеств размера j — прежний тройной цикл держал только j<=3 */
    int drop[16];
    void run_neighbourhood(void){
        nc=0;
        for(int i=0;i<nw;i++){int d=0;for(int t=0;t<j;t++) if(drop[t]==i) d=1; if(!d) cur[nc++]=W[i];}
        bestn=nc; memcpy(bestset,cur,nc*sizeof(P)); tried++;
        complete(0);
        if(bestn>globalbest){
            globalbest=bestn;
            printf("ПРИРОСТ: %d точек после выбивания %d\n",bestn,j);
            char o[256]; snprintf(o,sizeof o,"%s.lns%d",wf,bestn);
            FILE*g=fopen(o,"w"); if(g){for(int i=0;i<bestn;i++)fprintf(g,"%d %d %d\n",bestset[i].x,bestset[i].y,bestset[i].z);fclose(g);}
        }
    }
    void pick(int at,int start){
        if(at==j){ run_neighbourhood(); return; }
        for(int i=start;i<nw;i++){ drop[at]=i; pick(at+1,i+1); }
    }
    pick(0,0);
    printf("окрестностей пройдено %lld, узлов %lld, максимум по всей окрестности %d %s\n",
           tried,nodes,globalbest, globalbest>nw?"— ПРИРОСТ":"— прироста нет, окрестность исчерпана");
    return 0;
}
