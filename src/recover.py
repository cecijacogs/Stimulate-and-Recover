import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import numpy as np
import csv
import os
import argparse

from scipy.optimize import minimize
from src.simulate import simulate_data

# passes --N arugment for testing
parser = argparse.ArgumentParser()
parser.add_argument('--N', type=int, required=True, help="Number of trials")
args = parser.parse_args()

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
        simulated_rt, _ = simulate_data(a, v, t, len(rt))
        error = np.sum((rt - simulated_rt) ** 2)  # squared error
        return error
    
    initial_guess = [1.0, 1.0, 0.3]  # [a, v, t]
    result = minimize(loss_function, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])
    
    return result.x  # returns recovered [a, v, t] values

# reads the last row from summary.csv to get simulated parameters
summary_path = os.path.join(os.getcwd(), 'results', 'summary.csv')

# reads the last simulated row
with open(summary_path, mode='r') as file:
    reader = list(csv.reader(file))
    if len(reader) <= 1:
        raise ValueError("summary.csv has no data to process.")
    last_row = reader[-1]  # retrieves last row of simulated parameters
    N, a, v, t = map(float, last_row)  # converts to float

# if the N is different, this will update it
if args.N != N:
    N = args.N  # updates N with the one passed via command line

# simulates the response times / accuracy using the parameters
rt, acc = simulate_data(a, v, t, int(N))

# recovers parameters from simulated data
recovered_a, recovered_v, recovered_t = recover_parameters(rt, acc)

# adds recovered parameters back to summary.csv
with open(summary_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([N, a, v, t, recovered_a, recovered_v, recovered_t])
