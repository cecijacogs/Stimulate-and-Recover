import numpy as np
import csv
import os
import argparse

def simulate_data(a, v, t, N):

    """
    Simulate response times and accuracies based on EZ diffusion model parameters.

    Parameters:
    - a: Boundary separation (0.5 to 2)
    - v: Drift rate (0.5 to 2)
    - t: Non-decision time (0.1 to 0.5)
    - N: Number of trials

    Returns:
    - rt: Simulated response times
    - acc: Simulated accuracies (1 = correct, 0 = incorrect)
    """

    rt = []  # response times (simulated)
    acc = []  # simulated accuracies (where 1 is correct; 0 is incorrect)
    
    for _ in range(N):
        #EZ diffusion model process
        decision_time = a / v  # simulating decision time based on a and v
        non_decision_time = t  # non-decision time
        total_rt = decision_time + non_decision_time
        
        # randomly simulated (80% correct)
        accuracy = np.random.choice([0, 1], p=[0.2, 0.8])
        
        rt.append(total_rt)
        acc.append(accuracy)
    
    return np.array(rt), np.array(acc)

def generate_random_parameters():
    """ Generate random values for a, v, and t """
    a = np.random.uniform(0.5, 2)  # Random boundary separation
    v = np.random.uniform(0.5, 2)  # Random drift rate
    t = np.random.uniform(0.1, 0.5)  # Random non-decision time
    return a, v, t

# Parse command-line arguments for N
parser = argparse.ArgumentParser()
parser.add_argument('--N', type=int, required=True, help="Number of trials")
args = parser.parse_args()

# Generate random parameters
a, v, t = generate_random_parameters()

# Simulate data
rt, acc = simulate_data(a, v, t, args.N)

# Prepare directory for saving results
results_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(results_dir, exist_ok=True)

# Define file path
file_path = os.path.join(results_dir, 'summary.csv')

# Ensure that headers are written only if the file is empty
write_header = not os.path.exists(file_path) or os.stat(file_path).st_size == 0

# Write results to summary.csv
with open(file_path, mode='a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['N', 'a', 'v', 't'])
    if write_header:
        writer.writeheader()  # Write headers only once
    writer.writerow({'N': args.N, 'a': a, 'v': v, 't': t})
