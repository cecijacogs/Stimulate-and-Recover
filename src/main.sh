#!/bin/bash

# Add the 'src' directory to the Python path
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Set up results file for summary
results_file="results/summary.csv"
echo "N,iteration,bias_a,bias_v,bias_t,squared_error_a,squared_error_v,squared_error_t" > $results_file

# 3000 iterations
for N in 10 40 4000; do
    for i in {1..1000}; do
        # Print progress for each simulation
        echo "Running simulation for N=$N, Iteration=$i"
        
        # Run the simulation and recovery scripts
        python3 src/simulate.py --N $N
        python3 src/recover.py
        
        # Capture the simulated and recovered parameters (modify these paths as needed)
        simulated_a=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $2}' results/summary.csv)  # Simulated a value
        simulated_v=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $3}' results/summary.csv)  # Simulated v value
        simulated_t=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $4}' results/summary.csv)  # Simulated t value
        
        recovered_a=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $5}' results/summary.csv)  # Recovered a value
        recovered_v=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $6}' results/summary.csv)  # Recovered v value
        recovered_t=$(awk -F',' -v N=$N 'NR==1 && $1==N {print $7}' results/summary.csv)  # Recovered t value
        
        # Calculate bias and squared error
        bias_a=$(echo "$recovered_a - $simulated_a" | bc)
        bias_v=$(echo "$recovered_v - $simulated_v" | bc)
        bias_t=$(echo "$recovered_t - $simulated_t" | bc)
        
        squared_error_a=$(echo "($bias_a)^2" | bc)
        squared_error_v=$(echo "($bias_v)^2" | bc)
        squared_error_t=$(echo "($bias_t)^2" | bc)
        
        # Append the results to the summary CSV
        echo "$N,$i,$bias_a,$bias_v,$bias_t,$squared_error_a,$squared_error_v,$squared_error_t" >> $results_file
    done
done
