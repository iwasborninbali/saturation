/* no4_count_prof.c — исчерпывающий перебор конфигураций без четырёх компланарных
 * с ТОЧНЫМ профилем слоёв по двум осям. Никакого SAT: компланарность считается определителем.
 *
 * Зачем. Второй солвер закрывает a(6) <= 16 через SAT-разбиение по парам профилей. Тот же вопрос,
 * решённый перебором, не разделяет с ним ни одной строчки кода: ни кодировки, ни решателя, ни
 * сертификата. Если оба пути дадут «ноль конфигураций на 17 точек», значение, доказанное до нас
 * исчерпывающим перебором, будет воспроизведено двумя несвязанными способами.
 *
 * Полнота разбиения по парам профилей: у всякой конфигурации есть определённый профиль вдоль
 * КАЖДОЙ оси, поэтому перебор всех пар (профиль по x, профиль по y) исчерпывает пространство.
 * Пропуск даже одной пары обесценивает всё.
 *
 * Отсечения: точный профиль по x и по y (превышение — сразу отбой; слой по x, пройденный
 * недобором, — тоже), ёмкость слоя 3, запрет трёх коллинеарных (любая четвёртая с ними
 * компланарна), нехватка оставшихся клеток.
 *
 *   cc -O2 -o no4_count_prof no4_count_prof.c && ./no4_count_prof n M "p0,..,p0" "p1,..,p1"
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, NC, M;
static int px[512],py[512],pz[512];
static int S[64], sz;
static long long found=0, nodes=0;
static int lay[3][16], P0[16], P1[16];

static inline int det3(int ax,int ay,int az,int bx,int by,int bz,int cx,int cy,int cz){
    return ax*(by*cz-bz*cy)-ay*(bx*cz-bz*cx)+az*(bx*cy-by*cx);
}
static int ok_add(int q){
    for(int i=0;i<sz;i++){int a=S[i];
        int vx=px[q]-px[a],vy=py[q]-py[a],vz=pz[q]-pz[a];
        for(int j=i+1;j<sz;j++){int b=S[j];
            int ux=px[b]-px[a],uy=py[b]-py[a],uz=pz[b]-pz[a];
            if(uy*vz-uz*vy==0&&uz*vx-ux*vz==0&&ux*vy-uy*vx==0) return 0;
            for(int k=j+1;k<sz;k++){int c=S[k];
                int wx=px[c]-px[a],wy=py[c]-py[a],wz=pz[c]-pz[a];
                if(det3(ux,uy,uz,wx,wy,wz,vx,vy,vz)==0) return 0;}}}
    return 1;
}
static void rec(int start){
    nodes++;
    if(sz==M){ found++;
        printf("НАЙДЕНО:"); for(int i=0;i<sz;i++) printf(" %d%d%d",px[S[i]],py[S[i]],pz[S[i]]);
        printf("\n"); fflush(stdout); return; }
    if(sz + (NC-start) < M) return;
    for(int q=start;q<NC;q++){
        if(sz + (NC-q) < M) return;
        /* слой по x закрывается, когда индекс уходит дальше: проверяем недобор */
        if(px[q]>0 && lay[0][px[q]-1] != P0[px[q]-1]) return;   /* предыдущий x-слой уже не добрать */
        if(lay[0][px[q]]>=P0[px[q]] || lay[1][py[q]]>=P1[py[q]] || lay[2][pz[q]]>=3) continue;
        if(!ok_add(q)) continue;
        S[sz++]=q; lay[0][px[q]]++; lay[1][py[q]]++; lay[2][pz[q]]++;
        rec(q+1);
        sz--; lay[0][px[q]]--; lay[1][py[q]]--; lay[2][pz[q]]--;
    }
}
int main(int argc,char**argv){
    n=atoi(argv[1]); M=atoi(argv[2]);
    {char*t=strtok(argv[3],","); for(int i=0;i<n;i++){P0[i]=atoi(t); t=strtok(NULL,",");}}
    {char*t=strtok(argv[4],","); for(int i=0;i<n;i++){P1[i]=atoi(t); t=strtok(NULL,",");}}
    int s0=0,s1=0; for(int i=0;i<n;i++){s0+=P0[i]; s1+=P1[i];}
    if(s0!=M||s1!=M){printf("ОТКАЗ: профили не дают M (%d, %d против %d)\n",s0,s1,M); return 2;}
    NC=0; for(int x=0;x<n;x++)for(int y=0;y<n;y++)for(int z=0;z<n;z++){px[NC]=x;py[NC]=y;pz[NC]=z;NC++;}
    rec(0);
    {char b0[64],b1[64]; int o=0; for(int i=0;i<n;i++) o+=sprintf(b0+o,i?",%d":"%d",P0[i]); o=0; for(int i=0;i<n;i++) o+=sprintf(b1+o,i?",%d":"%d",P1[i]); printf("n=%d M=%d P0=%s P1=%s: конфигураций %lld (узлов %lld)\n",n,M,b0,b1,found,nodes);}
    return 0;
}
