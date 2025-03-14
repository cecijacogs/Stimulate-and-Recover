#!/bin/bash

# Add the 'src' directory to the Python path
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Ensure 'bc' is installed
if ! command -v bc &> /dev/null; then
    echo "Installing bc..."
    apt-get update && apt-get install -y bc
fi

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
        python3 src/recover.py --N $N  

        # Capture the latest simulated and recovered parameters
        last_row=$(tail -1 results/summary.csv)

        # Extract values from the last row safely
        simulated_a=$(echo "$last_row" | awk -F',' '{print $2}')
        simulated_v=$(echo "$last_row" | awk -F',' '{print $3}')
        simulated_t=$(echo "$last_row" | awk -F',' '{print $4}')
        recovered_a=$(echo "$last_row" | awk -F',' '{print $5}')
        recovered_v=$(echo "$last_row" | awk -F',' '{print $6}')
        recovered_t=$(echo "$last_row" | awk -F',' '{print $7}')

        # Handle missing values
        simulated_a=${simulated_a:-"NA"}
        simulated_v=${simulated_v:-"NA"}
        simulated_t=${simulated_t:-"NA"}
        recovered_a=${recovered_a:-"NA"}
        recovered_v=${recovered_v:-"NA"}
        recovered_t=${recovered_t:-"NA"}

        # Calculate bias and squared error
        if [[ "$simulated_a" != "NA" && "$recovered_a" != "NA" ]]; then
            bias_a=$(echo "$recovered_a - $simulated_a" | bc 2>/dev/null || echo "NA")
            squared_error_a=$(echo "$bias_a^2" | bc 2>/dev/null || echo "NA")
        else
            bias_a="NA"
            squared_error_a="NA"
        fi

        if [[ "$simulated_v" != "NA" && "$recovered_v" != "NA" ]]; then
            bias_v=$(echo "$recovered_v - $simulated_v" | bc 2>/dev/null || echo "NA")
            squared_error_v=$(echo "$bias_v^2" | bc 2>/dev/null || echo "NA")
        else
            bias_v="NA"
            squared_error_v="NA"
        fi

        if [[ "$simulated_t" != "NA" && "$recovered_t" != "NA" ]]; then
            bias_t=$(echo "$recovered_t - $simulated_t" | bc 2>/dev/null || echo "NA")
            squared_error_t=$(echo "$bias_t^2" | bc 2>/dev/null || echo "NA")
        else
            bias_t="NA"
            squared_error_t="NA"
        fi

        # Append formatted row to summary.csv
        echo "$N,$i,$bias_a,$bias_v,$bias_t,$squared_error_a,$squared_error_v,$squared_error_t" >> $results_file
    done
done
