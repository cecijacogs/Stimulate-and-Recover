#!/bin/bash

# Add the 'src' directory to the Python path
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# 3000 iterations
for N in 10 40 4000; do
    for i in {1..1000}; do
        # Print progress for each simulation
        echo "Running simulation for N=$N, Iteration=$i"
        
        # Run the simulation and recovery scripts
        python3 src/simulate.py --N $N
        python3 src/recover.py
    done
done
