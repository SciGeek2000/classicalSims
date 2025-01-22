import unittest
from classes.helper_circuit_elements import *
from classes.circuit_elements import *
from scr.helper_main import *

# File names must start unless a new pattern is defined with the -p flag
# Class names can be arbitrary, but must be derived from the baseclass unittest.TestCase
# The setUp method is run before every test
# All methods for testing need to match the pattern "test*"

class LegTests(unittest.TestCase):
    def setUp(self):
        '''Run before all tests automatically'''
        grid_spacing = 0.005
        brillouin_zone = 1 # Should always be set to one, given all mod 2pi solutions are accounted for
        self.phi_T = np.arange(-brillouin_zone*np.pi, brillouin_zone*np.pi, grid_spacing)
        set_units('Ones')
        self.nonhyst_leg = Leg(JJ(1), Inductor(1))
        self.hyst_leg = Leg(JJ(40), Inductor(1))
        self.nonhyst_leg.calculate_circuit(self.phi_T)
        self.hyst_leg.calculate_circuit(self.phi_T)

    def test_range(self):
        '''Ensures output phi_T range does not exceed input phi_T range'''
        self.assertGreaterEqual(np.max(self.phi_T), np.max(self.hyst_leg.phi_T),
          'Maximum bound of input phi_T violated by output in hysteretic case')
        self.assertLessEqual(np.min(self.phi_T), np.min(self.hyst_leg.phi_T),
          'Minimum bound of input phi_T violated by output in hysteretic case')
        self.assertGreaterEqual(np.max(self.phi_T), np.max(self.nonhyst_leg.phi_T),
          'Maximum bound of input phi_T violated by output in non-hysteretic case')
        self.assertLessEqual(np.min(self.phi_T), np.min(self.nonhyst_leg.phi_T),
          'Minimum bound of input phi_T violated by output in non-hysteretic case')
        
    def test_gridded_values(self):
        '''Ensures that all input phi_T lie on the grid after doing calculations'''        
        pass

    def test_test(self):
        pass
        # self.assertTrue(LegTests.hi=='his', 'Hi is not "hi"')

class LinRhombusTests(unittest.TestCase): 
    def setUp(self):
        '''Run before all tests automatically'''
        grid_spacing = 0.005
        brillouin_zone = 1 # Should always be set to one, given all mod 2pi solutions are accounted for
        self.phi_T = np.arange(-brillouin_zone*np.pi, brillouin_zone*np.pi, grid_spacing)
        set_units('Ones')
        leg1 = Leg(JJ(EJ=1), Inductor(EL=1))
        leg2 = Leg(JJ(EJ=1), Inductor(EL=1))
        self.linrhombus = LinRhombus(leg1, leg2)
        
    def test_unknown(self):
        pass

if __name__ == '__main__':
    unittest.main()