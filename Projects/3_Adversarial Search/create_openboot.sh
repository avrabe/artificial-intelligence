#!/bin/sh
killall -9 python3
for i in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
do
for j in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 
do
python3 ./create_openbook.py -p 100 -r 10000 -w match_"$i"_"$j".log &
done
wait
done
