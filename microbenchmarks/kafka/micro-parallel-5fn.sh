#!/bin/bash

rm data/parallel-5fns.out

python3 increment.py input aggregate &
inc_pid=$!
python3 square.py input aggregate &
squ_pid=$!
python3 double.py input aggregate &
dou_pid=$!
python3 half.py input aggregate &
hal_pid=$!
python3 divideby2.py input aggregate &
div_pid=$!
python3 aggregate.py 5 aggregate >> data/parallel-5fns.out &
agg_pid=$!

sleep 5
python3 input.py input

sleep 3
kill -9 $inc_pid
kill -9 $squ_pid
kill -9 $dou_pid
kill -9 $hal_pid
kill -9 $div_pid
kill -9 $agg_pid
