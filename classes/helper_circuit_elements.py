from classes.circuit_elements import *

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