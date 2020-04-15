#!/bin/bash

# rm data/choice-5fns.out

python3 increment.py increment >> data/choice-5fns.out &
inc_pid=$!
python3 square.py square >> data/choice-5fns.out &
squ_pid=$!
python3 double.py double >> data/choice-5fns.out &
dou_pid=$!
python3 half.py half >> data/choice-5fns.out &
hal_pid=$!
python3 divideby2.py divideby2 >> data/choice-5fns.out &
div_pid=$!
python3 divideby5.py input increment square double half divideby2 &
dec_pid=$!

sleep 5
python3 input.py input

sleep 2
kill -9 $inc_pid
kill -9 $squ_pid
kill -9 $dou_pid
kill -9 $hal_pid
kill -9 $div_pid
kill -9 $dec_pid
