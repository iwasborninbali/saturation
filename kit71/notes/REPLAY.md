# Как воспроизвести (всё в трёх файлах мира + мой код в этой папке)

Сборка быстрых инструментов (только предлагают; решает `saturation.the_law` через `solve.py`):

    gcc -O2 -march=native -o fast/sa     fast/sa.c     -lm   # отжиг, случайные ходы орбит
    gcc -O2 -march=native -o fast/mc     fast/mc.c     -lm   # min-conflict с полем пар F
    gcc -O2 -march=native -o fast/mc2    fast/mc2.c    -lm   # то же + корзины по F (быстрее), табу, RELOAD
    gcc -O2 -march=native -o fast/mc3    fast/mc3.c    -lm   # + ходы по 3 орбиты (P3)
    gcc -O2 -march=native -o fast/mcw    fast/mcw.c    -lm   # + веса прямых (breakout)
    gcc -O2 -march=native -o fast/ils    fast/ils.c    -lm   # ILS по законным книгам, (1,k)-обмены
    gcc -O2 -march=native -o fast/lns    fast/lns.c    -lm   # LNS: кластерное разрушение + точный ремонт
    gcc -O2 -march=native -o fast/polish fast/polish.c       # точные (r,r+1)-обмены, r<=3
    gcc -O2 -march=native -o fast/bt     fast/bt.c            # полный перебор класса симметрии

Сертификация любого списка токенов (через закон, с записью в реестр при n=71):

    python3 solve.py verify 71 out/<file>.txt
    python3 report.py            # итоговый отчёт: лучший Foothold, canon key, токены, журнал гипотез

## Фундаменты (лучшее 134)
Лучший прогон: `TABU=20 RELOAD=20000 DRIFT=6 ./fast/mc 71 100 rot2 63 900 0.4 0.1 out/r4_3 1`
(семя 63 = 60+3 в раунде 4; итог `out/r4_3_lawful_134.txt`, найден на 424 с). Второй 134:
`TABU=20 RELOAD=20000 DRIFT=6 ./fast/mc 71 100 rot2 93 900 0.4 0.1 out/r5_11 1`.
Замечание: гонки потоков нет (один процесс на прогон), но время-зависимые проверки (`now()`) влияют только
на печать; траектория детерминирована семенем при том же бинарнике/флагах.

## Алгебраические семена
    python3 h1_conics.py 29 31 37 41 43 47 53 59 61 67 71 73     # коники mod q + ремонт + жадное дозаполнение
    python3 h1b_hyper.py                                          # чистые гиперболы; лучшая (x+18)(y+18)=35 mod 53 → 88

## Фланг: исчерпание классов
    ./fast/bt <n> <group> [maxseconds] [maxsolutions] [order]   # group ∈ id rot2 diag adiag v2 h v hv c4 d4
    for n in 2 3 4 5 6 7 8 9 10; do for g in id rot2 diag adiag h v c4 d4 v2 hv; do ./fast/bt $n $g 600 -1 0 | grep TRACE; done; done
    for n in 11 13 15 17 19 21 23 25 27; do ./fast/bt $n v2 900 -1 1 | grep TRACE; done
Печатает `TRACE n=… group=… nodes=… solutions=… seconds=… complete=1` — это и есть трасса; решения печатаются строками `SOL …`.

## Калибровка метода на n, где насыщение достижимо
    TABU=20 RELOAD=20000 DRIFT=6 ./fast/mc2 <n> 10 rot2 7 300 0.4 0.1 out/cal_<n> 1     # n=20,30,40,52
