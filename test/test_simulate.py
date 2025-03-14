import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # adds parent directory to sys.path

from src.simulate import simulate_data, generate_random_parameters

class TestSimulate(unittest.TestCase):
    
    def test_generate_random_parameters(self):
        a, v, t = generate_random_parameters()
        self.assertTrue(0.5 <= a <= 2)
        self.assertTrue(0.5 <= v <= 2)
        self.assertTrue(0.1 <= t <= 0.5)
    
    def test_simulate_data(self):
        rt, acc = simulate_data(1.0, 1.0, 0.3, 100)
        self.assertEqual(len(rt), 100)
        self.assertEqual(len(acc), 100)

if __name__ == '__main__':
    unittest.main()