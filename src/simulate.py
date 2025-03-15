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
    rt = []
    acc = []
    
    for _ in range(N):
        # calculates decision time with EZ diffusion formulas
        if np.random.random() < (1 / (1 + np.exp(-v * a))):  # find prob for correct repsonses
            # decision time for correct responses
            decision_time = (a / (2 * v)) * (1 - np.exp(-(v * a)))/(1 + np.exp(-(v * a)))
            accuracy = 1
        else:
            # decision time for incorrect responses
            decision_time = (a / (2 * v)) * (1 + np.exp(-(v * a)))/(1 - np.exp(-(v * a)))
            accuracy = 0
            
        # variability
        decision_time += np.random.normal(0, 0.1)
        total_rt = max(0.1, decision_time + t)  # ensures stimulated response times are positive
        
        rt.append(total_rt)
        acc.append(accuracy)
    
    return np.array(rt), np.array(acc)

def generate_random_parameters():
    """ Generate random values for a, v, and t """
    a = np.random.uniform(0.5, 2)  #random boundary separation
    v = np.random.uniform(0.5, 2)  #random drift rate
    t = np.random.uniform(0.1, 0.5)  #random non-decision time
    return a, v, t

# command-line arguments for N
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, required=True, help="Number of trials")
    args = parser.parse_args()

# random parameters
a, v, t = generate_random_parameters()

# simulates data
rt, acc = simulate_data(a, v, t, args.N)

# directory for saving results
results_dir = os.path.join(os.getcwd(), 'results')
os.makedirs(results_dir, exist_ok=True)

# file path for temporary storage of simulated parameters
file_path = os.path.join(results_dir, 'simulated_params.csv')

# makes sure that headers are made -- only if the file is empty
write_header = not os.path.exists(file_path) or os.stat(file_path).st_size == 0

# writes parameters to the temporary CSV file
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    if write_header:
        writer.writerow(['N', 'a', 'v', 't'])
    writer.writerow([args.N, a, v, t])

# saves the simulated data to a file for recovery
data_file_path = os.path.join(results_dir, f'simulated_data_N{args.N}.csv')
with open(data_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['rt', 'acc'])
    for i in range(len(rt)):
        writer.writerow([rt[i], acc[i]])
