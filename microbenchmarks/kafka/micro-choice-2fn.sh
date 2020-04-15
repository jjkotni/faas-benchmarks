#!/bin/bash

rm data/choice-2fns.out

python3 increment.py increment >> data/choice-2fns.out &
inc_pid=$!
python3 double.py double >> data/choice-2fns.out &
dou_pid=$!
python3 divideby2.py input increment double &
div_pid=$!

sleep 5
python3 input.py input

sleep 5
kill -9 $inc_pid
kill -9 $dou_pid
kill -9 $div_pid
