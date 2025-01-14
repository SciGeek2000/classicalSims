'''Main .py for running classical simulations'''

import sys
import numpy as np
import matplotlib as mpl
import matplotlib.style as mplstyle
import datetime
import pickle
from pathlib import Path
from matplotlib import pyplot as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.ticker import MultipleLocator
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from tqdm import tqdm
from classes.helper_circuit_elements import *
from classes.circuit_elements import *
from helper_main import *


if __name__ == "__main__":
    '''Input here either a YAML file recieved from the command line, command line arguments, or directly set params'''

    grid_spacing = 0.005
    brillouin_zone = 1
    phi_T = np.arange(-brillouin_zone*np.pi, brillouin_zone*np.pi, grid_spacing)

    set_units('Ones')

    @timing_decorator
    def run_leg(EJ, EL):
        '''Creates a run of a single leg'''
        leg = make_phi_leg(EJ=EJ, EL=EL)
        leg.current(phi_T)
        leg.energy()
        return leg

    @timing_decorator
    def run_sym_linrhombus(sym_EJ, sym_EL):
        '''Creates a run of a symmetric linear rhombus'''
        linrhombus = make_symmetric_linrhombus(sym_EJ=sym_EJ, sym_EL=sym_EL)
        linrhombus.current(phi_T)
        linrhombus.energy()
        linrhombus.stability()
        return linrhombus

    @timing_decorator
    def run_asym_linrhombus(EJ1, EL1, EJ2, EL2):
        '''Creates a run of a assymetric linear rhombus'''
        linrhombus = make_assymmetric_linrhombus(EJ1, EL1, EJ2, EL2)
        linrhombus.current(phi_T)
        linrhombus.energy()
        linrhombus.stability()
        return linrhombus

    ### Run Circuit ###

    for i in range(1, 40, 10):
        circuit = run_sym_linrhombus(i,1)
        print(i)
        plot_circuit_class(circuit)
    

    # params = command_line_arg_setting()
    # run_leg(*params)
    # for i in range(1, 2, 1):
        # run_asym_linrhombus(20, 1, i, 1)
