import unittest
from classes.helper_circuit_elements import *
from classes.circuit_elements import *
from scr.helper_main import *

class LegTests(unittest.TestCase):
    def setUp(self):
        '''Run before all tests automatically'''
        self.leg = Leg(JJ(1), Inductor(1))

    def test_range(self):
        self.assertEqual(self.leg.junction.EJ, self.leg.junction.EJ)
    
    def test_other(self):
        self.assertEqual(1,1)

class my_second_test(unittest.TestCase):
    def test_anotherone(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()