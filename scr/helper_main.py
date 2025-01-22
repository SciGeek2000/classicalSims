import sys
from classes.circuit_elements import *

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

def make_phi_leg(EJ, EL) -> Leg:
    ind = Inductor(EL=EL)
    jj = JJ(EJ=EJ)
    leg = Leg(jj, ind)
    return leg

def make_2phi_leg(E2J, EL) -> Leg:
    ind = Inductor(EL=EL)
    cos2phi = Cos2Phi(E2J=E2J)
    twophi_leg = Leg(cos2phi, ind)
    return twophi_leg

def make_symmetric_linrhombus(sym_EJ, sym_EL) -> LinRhombus:
    leg1 = make_phi_leg(EJ=sym_EJ, EL=sym_EL)
    leg2 = make_phi_leg(EJ=sym_EJ, EL=sym_EL)
    linrhombus = LinRhombus(leg1, leg2) 
    return linrhombus

def make_assymmetric_linrhombus(EJ1, EL1, EJ2, EL2) -> LinRhombus:
    leg1 = make_phi_leg(EJ=EJ1, EL=EL1)
    leg2 = make_phi_leg(EJ=EJ2, EL=EL2)
    linrhombus = LinRhombus(leg1, leg2)
    return linrhombus

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
    if show and save is False:
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
    ax[1].set_ylabel(r'I')
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