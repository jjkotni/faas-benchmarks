#!/bin/bash

#rm data/sequence-2fns.out

python3 square.py input >> data/sequence-2fns.out &
squ_pid=$!

sleep 5
python3 input.py input

sleep 3
kill -9 $squ_pid
