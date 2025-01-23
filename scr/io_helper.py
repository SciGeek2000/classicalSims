import sys
import pickle
import re
import os
import datetime
from classes.circuit_elements import *


### Loading parameters in #########################################################################

def command_line_arg_setting() -> list:
    script_name = sys.argv[0]
    arg_strs = sys.argv[1:]
    arg_floats = [float(arg_str) for arg_str in arg_strs]
    return arg_floats

def YAML_arg_setting() -> list:
    script_name = sys.argv[0]
    filename = sys.argv[1]
    try:
        with open(filename, 'r') as file:
            content = file.read()
            args = parse_YAML(content)
            return args
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

def parse_YAML() -> list:
    pass


### Pickling Sims #################################################################################

def pickle_circuit(circuit, directory):
    '''Create formatting for common circuit types and then add a default catch-all which may not 
    look pretty, but will convert the unique properties of the circuit into a filename'''
    
    def sanitize_filename(filename, replacement_char="_"):
        """
        Sanitize a string to make it a valid filename by replacing invalid characters.
        Parameters:
            filename (str): The original string to sanitize.
            replacement_char (str): The character to replace invalid chars with. Default is "_".
        Returns:
            str: A sanitized, valid filename.
        """

        invalid_chars = r'[<>:"/\\|?*\0]'
        sanitized = re.sub(invalid_chars, replacement_char, filename)
        sanitized = sanitized.strip()
        return sanitized[:255]

    if circuit.name is 'Asymmetric Rhombus':
        fname = f'{circuit.name}_EJ1{circuit.EJ1:0.3f}_EL1{circuit.EL1:0.3f}_EJ2{circuit.EJ2:0.3f}_EL2{circuit.EL2}'
    elif circuit.name is 'Symmetric Rhombus':
        fname = f'{circuit.name}_EJ{circuit.EJ:0.3f}_EL{circuit.EL}'
    elif circuit.name is Leg.name:
        fname = f'{circuit.name}_EJ{circuit.EJ:0.3f}_EL{circuit.EJ:0.3f}'
    else:
        fname = sanitize_filename(circuit.dir())

    fname = directory + fname
    if os.path.exists(fname) is True: raise(Exception('File name already exists'))

    with open(fname, 'wb') as f:
        pickle.dump(circuit, f)

def load_pickled_circuit(circuit_name, directory):
    '''Load from a directory a pickled circuit'''
    pass


### Plotting Data #################################################################################
def plot_circuit_class(circuit, show=True, save=False):
    def sym_legend(ax, circuit):
        '''For use in legs and symmetric linear rhombuses'''
        ax.text(0.025, 0.96,
          rf'$E_J = {circuit.EJ:0.3f}$'
          '\n'
          rf'$E_L = {circuit.EL:0.3f}$'
          '\n'
          rf'$E_J/E_L = {(circuit.EJ/circuit.EL):0.3f}$',
          transform=ax.transAxes, fontsize=10, va='top', 
          bbox={'boxstyle':'round', 'alpha':0.2, 'color':'black'})

    def asym_legend(ax, circuit):
        '''For use in assymetric linear rhombuses'''
        ax.text(0.025, 0.96,
          rf'$E_{{J1}} = {circuit.EJ1:0.3f}$'
          '\n'
          rf'$E_{{J2}} = {circuit.EJ2:0.3f}$'
          '\n'
          rf'$E_{{L1}} = {circuit.EL1:0.3f}$'
          '\n'
          rf'$E_{{L2}} = {circuit.EL2:0.3f}$',
          transform=ax.transAxes, fontsize=10, va='top', 
          bbox={'boxstyle':'round', 'alpha':0.2, 'color':'black'})
        
    # Early return if we actually don't even use it
    if show is False and save is False:
        return
    
    size = 0.5
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(15,6))
    
    ### Current Phase Relation Plot ###
    ax[0].scatter(circuit.phi_T/(np.pi), circuit.I, s=size, c=circuit.stability_colormap)
    ax[0].set_xlabel(r'$\phi_T/\pi$')
    ax[0].set_ylabel(r'I')
    ax[0].set_title(f'Current Phase Relation of {circuit.name}')
    ax[0].grid()
    if circuit.name in ('Symmetric Rhombus', 'JJ + Inductor'): sym_legend(ax[0], circuit)
    elif circuit.name == 'Asymmetric Rhombus': asym_legend(ax[0], circuit)

    ### Energy Plot ###
    ax[1].scatter(circuit.phi_T/(np.pi), circuit.E, s=size, c=circuit.stability_colormap)
    ax[1].set_xlabel(r'$\phi_T/\pi$')
    ax[1].set_ylabel(r'E')
    ax[1].set_title(f'Energy Phase Relation of {circuit.name}')
    ax[1].grid()
    if circuit.name in ('Symmetric Rhombus', 'JJ + Inductor'): sym_legend(ax[1], circuit)
    elif circuit.name == 'Asymmetric Rhombus': asym_legend(ax[1], circuit)
    fig.tight_layout()

    if show is True:
        plt.show()
    if save is True:
        fig.savefig('./resources/data/figures/' + circuit.name.replace(' ', '_'))
    
    # for lh in leg.legend_handles:
    #     lh.set_alpha(1)
    #     lh.set_sizes([100])