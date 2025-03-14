#!/bin/bash

export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# runs 1000 times for each (10, 40, and 1000 for 3000 iterations)
for N in 10 40 4000; do
    for i in {1..1000}; do
        python3 src/simulate.py --N $N
        python3 src/recover.py
    done
done
