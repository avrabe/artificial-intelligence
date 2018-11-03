#!/bin/sh
killall -9 python3
for i in 1 2 3 4 5 6 7 8 9 10
do
for j in 1 2 3 4 5 6 7 8 9 10  
do
python3 ./create_openbook.py -p 100 -r 1 -w match_"$i"_"$j".log &
done
wait
done
