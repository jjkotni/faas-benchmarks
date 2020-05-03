#!/bin/bash

# rm data/sequence-5fns.out

python3 divideby2.py half >> data/sequence-5fns.out &
div_pid=$!
python3 half.py increment half &
hal_pid=$!
python3 increment.py square increment &
inc_pid=$!
python3 square.py input square &
squ_pid=$!

sleep 5
python3 input.py input

sleep 3
kill -9 $inc_pid
kill -9 $squ_pid
kill -9 $hal_pid
kill -9 $div_pid
