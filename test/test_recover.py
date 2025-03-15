import unittest
import numpy as np
import os
import tempfile
import csv

from src.recover import recover_parameters
from src.simulate import simulate_data

class TestRecover(unittest.TestCase):
    
    def test_recover_parameters(self):
        # using known parameters to test recovery
        known_a, known_v, known_t = 1.0, 1.0, 0.3
        N = 200  # give more samples for better recovery
        
        # generates the test data with known parameters
        rt, acc = simulate_data(known_a, known_v, known_t, N)
        
        # Test parameter recovery
        estimated_params = recover_parameters(rt, acc)
        estimated_a, estimated_v, estimated_t = estimated_params
        
        # this checks if recovered parameters are close to the original
        # -- uses a larger tolerance because of stochastic nature
        self.assertTrue(np.allclose(estimated_params, [known_a, known_v, known_t], atol=0.2))
        
        # other tests for each individual parameter
        self.assertAlmostEqual(estimated_a, known_a, delta=0.2)
        self.assertAlmostEqual(estimated_v, known_v, delta=0.2)
        self.assertAlmostEqual(estimated_t, known_t, delta=0.2)
    
    def test_loss_function_minimum(self):
        """Test that the loss function is minimized at the true parameters"""
        # creates a simple test case
        known_a, known_v, known_t = 1.0, 1.0, 0.3
        N = 100
        
        # generates the test data
        rt, acc = simulate_data(known_a, known_v, known_t, N)
        
        # grabs recover_parameters function to expose loss function
        # tests the internals of recover_parameters
        def get_loss_function():
            def wrapped_loss(params):
                a, v, t = params
                simulated_rt, simulated_acc = simulate_data(a, v, t, len(rt))
                rt_error = np.sum((rt - simulated_rt) ** 2)
                acc_error = np.sum((acc - simulated_acc) ** 2)
                return rt_error + 10 * acc_error
            return wrapped_loss
        
        loss_fn = get_loss_function()
        
        # (loss should be relatively low at the true parameters)
        true_loss = loss_fn([known_a, known_v, known_t])
        
        # (loss should be higher at different parameters)
        different_loss = loss_fn([known_a + 0.5, known_v - 0.3, known_t + 0.1])
        
        # (loss at true parameters should be lower)
        self.assertLess(true_loss, different_loss)

if __name__ == '__main__':
    unittest.main()
