/* plain_count.c — счёт максимумов БЕЗ единого отсечения, кроме самого запрета.
 *
 * Второй способ для тех n, где полный перебор подмножеств уже невозможен (при n=4 их 1.5e11).
 * От моего обхода отличается тем, что НЕ содержит ни ёмкостной оценки, ни ограничения «в слое
 * не более трёх», ни оценки по остатку — только «добавляемая точка не создаёт нарушения»
 * и порядок по возрастанию индекса. То есть не разделяет с ним ни одной догадки об устройстве
 * задачи, кроме определения запрета.
 *
 * Аргументы: n M [секунды]
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
static int n,N,M; typedef struct{signed char x,y,z;} P;
static P cell[1400]; static P S[40]; static int k;
static long long found=0, nodes=0; static double T; static clock_t st; static int to=0;
static int ok(P q){
    for(int a=0;a<k;a++)for(int b=a+1;b<k;b++){
        long long ux=S[b].x-S[a].x,uy=S[b].y-S[a].y,uz=S[b].z-S[a].z;
        long long vx=q.x-S[a].x,vy=q.y-S[a].y,vz=q.z-S[a].z;
        if((uy*vz-uz*vy)==0&&(uz*vx-ux*vz)==0&&(ux*vy-uy*vx)==0) return 0;
        for(int c=b+1;c<k;c++){
            long long wx=S[c].x-S[a].x,wy=S[c].y-S[a].y,wz=S[c].z-S[a].z;
            if(ux*(vy*wz-vz*wy)-uy*(vx*wz-vz*wx)+uz*(vx*wy-vy*wx)==0) return 0;
        }
    }
    return 1;
}
static void dfs(int start){
    if(to) return;
    if(((++nodes)&0xFFFFF)==0 && T>0 && (double)(clock()-st)/CLOCKS_PER_SEC>T){to=1;return;}
    if(k==M){ found++; return; }
    for(int i=start;i<N;i++){
        if(k+(N-i)<M) return;              /* единственное отсечение: точек уже не хватит */
        if(!ok(cell[i])) continue;
        S[k++]=cell[i]; dfs(i+1); k--;
        if(to) return;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); M=atoi(argv[2]); T=argc>3?atof(argv[3]):0;
    N=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){cell[N].x=x;cell[N].y=y;cell[N].z=z;N++;}
    st=clock(); dfs(0);
    if(to) printf("n=%d M=%d ВРЕМЯ ВЫШЛО — счёт неполон (насчитано %lld, узлов %lld)\n",n,M,found,nodes);
    else   printf("n=%d M=%d: ПРАВИЛЬНЫХ %lld (узлов %lld, без отсечений кроме запрета)\n",n,M,found,nodes);
    return 0;
}
