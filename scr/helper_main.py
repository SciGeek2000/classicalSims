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

def plot_circuit_class(circuit):
    plt.scatter(circuit.phi_T, circuit.E, s=0.5, c=circuit.stability_colormap)
    plt.vlines(-np.pi/2, min(circuit.E), max(circuit.E))
    plt.vlines(np.pi/2, min(circuit.E), max(circuit.E))
    plt.grid()
    plt.show()
