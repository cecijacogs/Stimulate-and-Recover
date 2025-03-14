import unittest
import numpy as np

from src.recover import recover_parameters
from src.simulate import simulate_data

class TestRecover(unittest.TestCase):
    
    def test_recover_parameters(self):
        # Use known parameters to test recovery
        rt, acc = simulate_data(1.0, 1.0, 0.3, 100)
        estimated_params = recover_parameters(rt, acc)
        self.assertTrue(np.allclose(estimated_params, [1.0, 1.0, 0.3], atol=0.1))

if __name__ == '__main__':
    unittest.main()