import unittest
import sys
import os
import numpy as np

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # adds parent directory to sys.path

from src.simulate import simulate_data, generate_random_parameters

class TestSimulate(unittest.TestCase):
    
    def test_generate_random_parameters(self):

        """Test that generated parameters are within the expected ranges"""

        a, v, t = generate_random_parameters()
        self.assertTrue(0.5 <= a <= 2)
        self.assertTrue(0.5 <= v <= 2)
        self.assertTrue(0.1 <= t <= 0.5)
    
    def test_simulate_data(self):

        """Test that simulate_data returns arrays of the expected length"""

        rt, acc = simulate_data(1.0, 1.0, 0.3, 100)
        self.assertEqual(len(rt), 100)
        self.assertEqual(len(acc), 100)
        
        # tests all response times to be positive
        self.assertTrue(all(rt > 0))
        
        # tests to see if accuracy values are binary (0 or 1)
        self.assertTrue(all((acc == 0) | (acc == 1)))
    
    def test_simulate_data_parameters(self):

        """Test that different parameters produce different data patterns"""

        # generates data with fast drift rate (should have lower RTs)
        rt_fast, acc_fast = simulate_data(1.0, 2.0, 0.3, 200)
        
        # generates data with slow drift rate (should have higher RTs)
        rt_slow, acc_slow = simulate_data(1.0, 0.5, 0.3, 200)
        
        # fast drift should have faster responses on average
        self.assertLess(np.mean(rt_fast), np.mean(rt_slow))
        
        # generates data with higher boundary (should be more accurate)
        _, acc_high_boundary = simulate_data(2.0, 1.0, 0.3, 200)
        
        # generates data with lower boundary (should be less accurate)
        _, acc_low_boundary = simulate_data(0.5, 1.0, 0.3, 200)
        
        # higher boundary should lead to higher accuracy on average
        self.assertGreaterEqual(np.mean(acc_high_boundary), np.mean(acc_low_boundary))

if __name__ == '__main__':
    unittest.main()
