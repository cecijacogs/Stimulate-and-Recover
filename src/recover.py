import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.simulate import simulate_data

import numpy as np
import csv
import os
import argparse

from scipy.optimize import minimize

def recover_parameters(rt, acc):
    """
    Recover the parameters (a, v, t) from the simulated data.
    
    Parameters:
    - rt: Response times
    - acc: Accuracy data
    
    Returns:
    - recovered_a, recovered_v, recovered_t: Estimated parameters
    
    """

    def loss_function(params):
        a, v, t = params
        # generates simulated data
        simulated_rt, simulated_acc = simulate_data(a, v, t, len(rt))
        
        # error calc for RT and accuracy
        rt_error = np.sum((rt - simulated_rt) ** 2)
        acc_error = np.sum((acc - simulated_acc) ** 2)
        
        # combined error with accuracy
        error = rt_error + 10 * acc_error
        return error
    
    initial_guess = [1.0, 1.0, 0.3]  # [a, v, t]
    result = minimize(loss_function, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])
    
    return result.x  # returns recovered [a, v, t] values

def main():
    # argument parser to accept simulation parameters in recover.py
    parser = argparse.ArgumentParser()
    parser.add_argument('--N', type=int, required=True, help="Number of trials")
    parser.add_argument('--a', type=float, required=True, help="Simulated boundary separation")
    parser.add_argument('--v', type=float, required=True, help="Simulated drift rate")
    parser.add_argument('--t', type=float, required=True, help="Simulated non-decision time")
    args = parser.parse_args()

    # loads the simulated data
    data_file_path = os.path.join(os.getcwd(), 'results', f'simulated_data_N{args.N}.csv')
    try:
        with open(data_file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # skips header
            data = list(reader)
            rt = np.array([float(row[0]) for row in data])
            acc = np.array([int(row[1]) for row in data])
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # uses the parameters passed directly via command line
    a, v, t = args.a, args.v, args.t

    # recovers parameters from simulated data
    recovered_a, recovered_v, recovered_t = recover_parameters(rt, acc)

    # saves recovered parameters to a temporary file
    results_dir = os.path.join(os.getcwd(), 'results')
    rec_file_path = os.path.join(results_dir, 'recovered_params.csv')
    with open(rec_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([recovered_a, recovered_v, recovered_t])

    print(f"Original parameters: a={args.a}, v={args.v}, t={args.t}")
    print(f"Recovered parameters: a={recovered_a}, v={recovered_v}, t={recovered_t}")

if __name__ == '__main__':
    main()
    