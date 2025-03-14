import numpy as np

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

    rt = [] #response times (simulated)
    acc = [] # simulated accuracies (where 1 is correct; 0 is incorrect)
    
    for _ in range(N):
        # simulates the EZ diffusion model process
        decision_time = a / v  # simulating decision time based on a and v
        non_decision_time = t  # non-decision time
        total_rt = decision_time + non_decision_time
        
        # Accuracy to be randomly simulated
        accuracy = np.random.choice([0, 1], p=[0.2, 0.8])  # in this code, we set it to 80% correct accuracy
        
        rt.append(total_rt)
        acc.append(accuracy)
    
    return np.array(rt), np.array(acc)

def generate_random_parameters():
    a = np.random.uniform(0.5, 2)  # Random boundary separation
    v = np.random.uniform(0.5, 2)  # Random drift rate
    t = np.random.uniform(0.1, 0.5)  # Random non-decision time
    return a, v, t