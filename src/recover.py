from src.simulate import simulate_data
import numpy as np
from scipy.optimize import minimize

def recover_parameters(rt, acc):

    """
    Recover the parameters (a, v, t) from the simulated data.

    Parameters:
    - rt: Response times
    - acc: Accuracy data

    Returns:
    - a, v, t: Estimated parameters
    """
    
    def loss_function(params):
        a, v, t = params
        simulated_rt, simulated_acc = simulate_data(a, v, t, len(rt))
        error = np.sum((rt - simulated_rt) ** 2)  # Squared error
        return error
    
    initial_guess = [1.0, 1.0, 0.3]  # Initial guess for [a, v, t]
    result = minimize(loss_function, initial_guess, bounds=[(0.5, 2), (0.5, 2), (0.1, 0.5)])
    
    return result.x  # Estimated [a, v, t]