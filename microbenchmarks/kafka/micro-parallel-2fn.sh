#!/bin/bash

# rm data/parallel-2fns.out

python3 increment.py input aggregate &
inc_pid=$!
python3 square.py input aggregate &
squ_pid=$!
python3 aggregate.py 2 aggregate >> data/parallel-2fns.out &
agg_pid=$!

sleep 5
python3 input.py input

sleep 3
kill -9 $inc_pid
kill -9 $squ_pid
kill -9 $agg_pid
