/* no4_mixed.c — наращивание по СМЕШАННЫМ ходам: орбита цикла ИЛИ одна свободная клетка.
 *
 * Что здесь сохранено и что изменено. Измерено, что наращиватель выигрывает не качеством спуска
 * (локальное улучшение здесь невозможно: максимумы рассеяны), а ОТБОРОМ ОБЛАСТИ — симметрия
 * даёт обогащение от x25 при n=3 до x12843 при n=5. Значит менять надо не способ хода, а границы
 * области. Здесь область расширена ровно на один шаг: набор больше не обязан быть инвариантным,
 * но орбита остаётся доступной как ОДИН ход, то есть отбор сохраняется как склонность, а не как
 * запрет.
 *
 * Отжиг (no4_anneal.c) провалил калибровку именно потому, что менял способ хода, не меняя области.
 *
 * Аргументы: n цель секунды семя выход [доля_орбитных_ходов]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
static int n; typedef struct{int x,y,z;} P;
#define MAXC 28000
static P cell[MAXC]; static int ncell;
static P orb[MAXC][3]; static int orbsz[MAXC], norb;
static P S[256]; static int k;
static P best[256]; static int bk=0;
static long long det4(P a,P b,P c,P d){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z,wx=d.x-a.x,wy=d.y-a.y,wz=d.z-a.z;return ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx);}
static int col3(P a,P b,P c){long long ux=b.x-a.x,uy=b.y-a.y,uz=b.z-a.z,vx=c.x-a.x,vy=c.y-a.y,vz=c.z-a.z;return (uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0;}
/* можно ли добавить группу из g точек */
static int fits(P*np,int g){
    P all[256]; memcpy(all,S,k*sizeof(P));
    for(int i=0;i<g;i++){
        for(int j=0;j<k;j++) if(S[j].x==np[i].x&&S[j].y==np[i].y&&S[j].z==np[i].z) return 0;
        for(int j=0;j<i;j++) if(np[j].x==np[i].x&&np[j].y==np[i].y&&np[j].z==np[i].z) return 0;
        all[k+i]=np[i];
    }
    int tot=k+g;
    for(int a=0;a<tot;a++)for(int b=a+1;b<tot;b++)for(int c=b+1;c<tot;c++){
        int t3=(c>=k); if(t3&&col3(all[a],all[b],all[c])) return 0;
        for(int d=c+1;d<tot;d++){ if(!(t3||d>=k)) continue;
            if(det4(all[a],all[b],all[c],all[d])==0) return 0; }
    }
    return 1;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); int target=atoi(argv[2]); double T=atof(argv[3]);
    unsigned sd=(unsigned)atoi(argv[4]); const char*out=argv[5];
    int orbpct = argc>6? atoi(argv[6]) : 70;
    if((long)n*n*n>MAXC){fprintf(stderr,"ОТКАЗ: n=%d не помещается\n",n);return 2;}
    srand(sd);
    ncell=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){cell[ncell].x=x;cell[ncell].y=y;cell[ncell].z=z;ncell++;}
    static int seen[MAXC]; memset(seen,0,sizeof seen); norb=0;
    for(int i=0;i<ncell;i++){
        int id=(cell[i].x*n+cell[i].y)*n+cell[i].z; if(seen[id])continue;
        P p=cell[i],cur=p; int g=0;
        do{ int c=(cur.x*n+cur.y)*n+cur.z; if(!seen[c]){seen[c]=1; orb[norb][g++]=cur;}
            P q={cur.y,cur.z,cur.x}; cur=q; }while(!(cur.x==p.x&&cur.y==p.y&&cur.z==p.z)&&g<3);
        orbsz[norb]=g; norb++;
    }
    fprintf(stderr,"n=%d клеток %d орбит %d, орбитных ходов %d%%\n",n,ncell,norb,orbpct);
    clock_t st=clock(); long rs=0;
    int ord[MAXC];
    while((double)(clock()-st)/CLOCKS_PER_SEC<T && bk<target){
        rs++; k=0;
        for(int pass=0; pass<2; pass++){
            /* первый проход — орбитами (отбор области), второй — свободными клетками (расширение) */
            int cnt = pass==0? norb : ncell;
            for(int i=0;i<cnt;i++) ord[i]=i;
            for(int i=cnt-1;i>0;i--){int j=rand()%(i+1);int t=ord[i];ord[i]=ord[j];ord[j]=t;}
            for(int i=0;i<cnt;i++){
                if(pass==0){ if(rand()%100>=orbpct) continue;
                    if(fits(orb[ord[i]],orbsz[ord[i]])) for(int t=0;t<orbsz[ord[i]];t++) S[k++]=orb[ord[i]][t]; }
                else { P q=cell[ord[i]]; if(fits(&q,1)) S[k++]=q; }
            }
        }
        if(k>bk){ bk=k; memcpy(best,S,k*sizeof(P));
            fprintf(stderr,"  %d точек (перезапуск %ld)\n",bk,rs); fflush(stderr);
            if(out){FILE*f=fopen(out,"w"); if(f){fprintf(f,"# n=%d смешанные ходы, точек %d\n",n,bk);
                for(int i=0;i<bk;i++)fprintf(f,"%d %d %d\n",best[i].x,best[i].y,best[i].z); fclose(f);}} }
    }
    fprintf(stderr,"итог %d точек, перезапусков %ld\n",bk,rs);
    return bk>=target?0:1;
}
