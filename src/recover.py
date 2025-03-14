import numpy as np
import csv
import os

from scipy.optimize import minimize
from src.simulate import simulate_data

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
        error = np.sum((rt - simulated_rt) ** 2)  # Squared error
        return error
    
    initial_guess = [1.0, 1.0, 0.3]  # Initial guess for [a, v, t]
    result = minimize(loss_function, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])
    
    return result.x  # Returns recovered [a, v, t]

# Read the last row from summary.csv to get simulated parameters
summary_path = os.path.join(os.getcwd(), 'results', 'summary.csv')

# Read the last simulated row
with open(summary_path, mode='r') as file:
    reader = list(csv.reader(file))
    if len(reader) <= 1:
        raise ValueError("summary.csv has no data to process.")
    last_row = reader[-1]  # Get last row of simulated parameters
    N, a, v, t = map(float, last_row)  # Convert to float

# Simulate response times and accuracy using the extracted parameters
rt, acc = simulate_data(a, v, t, int(N))

# Recover parameters from simulated data
recovered_a, recovered_v, recovered_t = recover_parameters(rt, acc)

# Append recovered parameters back to summary.csv
with open(summary_path, mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([N, a, v, t, recovered_a, recovered_v, recovered_t])
