#!/bin/bash

export LC_ALL=C

# 'src' directory to the Python path
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

#ensures 'bc' is installed
if ! command -v bc &> /dev/null; then
    echo "Installing bc..."
    apt-get update && apt-get install -y bc
fi

# results directory
results_dir="results"
mkdir -p $results_dir

# results file for summary
results_file="$results_dir/summary.csv"

# checks if summary.csv exists and will create it with headers if it doesn't
if [ ! -f "$results_file" ] || [ ! -s "$results_file" ]; then
    echo "N,iteration,simulated_a,simulated_v,simulated_t,recovered_a,recovered_v,recovered_t,bias_a,bias_v,bias_t,squared_error_a,squared_error_v,squared_error_t" > $results_file
fi

# the 3000 iterations
for N in 10 40 4000; do
    for i in {1..1000}; do
        # prints progress for each simulation
        echo "Running simulation for N=$N, Iteration=$i"
        
        # runs the simulation script
        python3 src/simulate.py --N $N
        
        # reads the simulated parameters from the temporary file
        sim_file="$results_dir/simulated_params.csv"
        if [ -f "$sim_file" ]; then
            simulated_a=$(tail -1 "$sim_file" | cut -d',' -f2 | tr -d '\r')
            simulated_v=$(tail -1 "$sim_file" | cut -d',' -f3 | tr -d '\r')
            simulated_t=$(tail -1 "$sim_file" | cut -d',' -f4 | tr -d '\r')
        else
            echo "Error: Simulated parameters file not found!"
            continue
        fi
        
        python3 src/recover.py --N $N --a $simulated_a --v $simulated_v --t $simulated_t
        
        # reads the recovered parameters from the temporary file
        rec_file="$results_dir/recovered_params.csv"
        if [ -f "$rec_file" ]; then
            recovered_a=$(tail -1 "$rec_file" | cut -d',' -f1 | tr -d '\r')
            recovered_v=$(tail -1 "$rec_file" | cut -d',' -f2 | tr -d '\r')
            recovered_t=$(tail -1 "$rec_file" | cut -d',' -f3 | tr -d '\r')
        else
            echo "Error: Recovered parameters file not found!"
            continue
        fi
        
        # calculates bias and squared error
        bias_a=$(echo "$recovered_a - $simulated_a" | bc -l)
        bias_v=$(echo "$recovered_v - $simulated_v" | bc -l)
        bias_t=$(echo "$recovered_t - $simulated_t" | bc -l)
        
        squared_error_a=$(echo "$bias_a * $bias_a" | bc -l)
        squared_error_v=$(echo "$bias_v * $bias_v" | bc -l)
        squared_error_t=$(echo "$bias_t * $bias_t" | bc -l)
        
        # adds formatted row to summary.csv
        echo "$N,$i,$simulated_a,$simulated_v,$simulated_t,$recovered_a,$recovered_v,$recovered_t,$bias_a,$bias_v,$bias_t,$squared_error_a,$squared_error_v,$squared_error_t" >> $results_file
    done
done

# generates aggregated statistics for the report
echo "Calculating summary statistics..."
echo "N,mean_bias_a,mean_bias_v,mean_bias_t,mean_squared_error_a,mean_squared_error_v,mean_squared_error_t" > "$results_dir/aggregated_stats.csv"

for N in 10 40 4000; do
    # uses awk to calculate means for each N value
    mean_bias_a=$(awk -F, -v n="$N" '$1==n {sum+=$9; count++} END {print sum/count}' "$results_file")
    mean_bias_v=$(awk -F, -v n="$N" '$1==n {sum+=$10; count++} END {print sum/count}' "$results_file")
    mean_bias_t=$(awk -F, -v n="$N" '$1==n {sum+=$11; count++} END {print sum/count}' "$results_file")
    mean_squared_error_a=$(awk -F, -v n="$N" '$1==n {sum+=$12; count++} END {print sum/count}' "$results_file")
    mean_squared_error_v=$(awk -F, -v n="$N" '$1==n {sum+=$13; count++} END {print sum/count}' "$results_file")
    mean_squared_error_t=$(awk -F, -v n="$N" '$1==n {sum+=$14; count++} END {print sum/count}' "$results_file")
    
    echo "$N,$mean_bias_a,$mean_bias_v,$mean_bias_t,$mean_squared_error_a,$mean_squared_error_v,$mean_squared_error_t" >> "$results_dir/aggregated_stats.csv"
done

echo "Simulation completed! Results stored in $results_file and $results_dir/aggregated_stats.csv"
