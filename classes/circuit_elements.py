'''A module which defines the classes used for the classical simulation'''
import numpy as np
from lib.circuit_calcs import *

hbar = 1
e = 1
phi_naught = 1

def set_units(unit_name: str) -> None:
    global hbar
    global e
    global phi_naught
    if unit_name == 'Ones':
        hbar = 1
        e = 1
        phi_naught = 1
    elif unit_name == 'SI':
        pass
    elif unit_name == 'eV':
        pass
    elif unit_name == 'GHz':
        pass
    else:
        raise Exception('Not a valid unit yet')


class JJ:
    '''A class definining a JJ'''
    def __init__(self, EJ):
        self.EJ = EJ
        self.Ic = self.EJ*2*e/hbar #VERIFY

    def current(self, phase):
        self.I = self.Ic*np.sin(phase)
        return self.I

    def energy(self, phase):
        self.E = -self.EJ*np.cos(phase)
        return self.E

    def stability(self, phase):
        self.stability_vals = self.EJ*np.cos(phase)
        return self.stability_vals


class Cos2Phi:
    '''A class defining a Cos2Phi ideal element'''
    def __init__(self, E2J):
        self.E2J = E2J
        self.Ic = self.E2J*2*e/hbar #VERIFY 

    def current(self, phase):
        self.phase = phase
        self.I = self.Ic*np.sin(2*self.phase)
        try: del self.E
        except: pass
        return self.I

    def energy(self, phase):
        self.phase = phase
        self.E = -self.E2J*np.cos(self.phase)
        try: del self.I
        except: pass
        return self.E

    def stability(self, phase):
        self.stability_vals = self.E2J*np.cos(phase)
        return self.stability_vals

    def __call__(self):
        try: return self.E
        except:
            print('The energies for this class have not been calculated yet')
            raise


class Inductor:
    def __init__(self, EL):
        self.EL = EL
        self.L = (phi_naught/2/np.pi)**2/self.EL #VERIFY

    def current(self, phase):
        self.I = (1/self.L)*phase #VERIFY
        return self.I

    def invert_current(self, I):
        inductor_phase = I*self.L
        return inductor_phase

    def energy(self, phase):
        self.E = self.EL/2*phase**2
        return self.E

    def stability(self, phase):
        self.stability_vals = 2*self.EL*np.ones(phase.shape)
        return self.stability_vals


class Leg:
    def __init__(self, junction, ind):
        Leg.name = 'JJ + Inductor'
        self.junction = junction
        self.ind = ind
        self.EJ = self.junction.EJ
        self.EL = self.ind.EL
    def calculate_circuit(self, phase, threaded_flux=0) -> np.ndarray:
        self.phase = phase
        self.current(phase, threaded_flux)
        self.energy()
        self.stability()
        self.data = np.concatenate((self.current_data, self.E.reshape(-1,1), self.stability_bool.reshape(-1,1)), axis=1)
        return self.data #[[current_data], [E], [stability_bool]]

    def current(self, phase, threaded_flux=0) -> np.ndarray:
        self.phase = phase + threaded_flux
        self.current_data = np.empty((0,4)) # [[phi_T], [I], [chi], [phi_ind]]
        self = invert_phase_relation(self)
        self.current_data = average_contiguous_columns(self.current_data)
        self._assign_current_vars(closure_phase=threaded_flux)
        return self.current_data #[[phi_T], [I], [chi], [phi_ind]]

    def energy(self) -> np.ndarray:
        if not hasattr(self, 'current_data'): raise Exception('Need to run current method first')
        junc_e = self.junction.energy(self.chi)
        ind_e = self.ind.energy(self.phi_ind)
        self.E = junc_e + ind_e
        return self.E

    def stability(self) -> np.ndarray:
        if not hasattr(self, 'current_data'): raise Exception('Need to run a calculation first')
        junction_stability_vals = self.junction.stability(self.chi)
        ind_stability_vals = self.ind.stability(self.phi_ind)
        self.stability_vals = junction_stability_vals + ind_stability_vals
        self.stability_bool = np.where(self.stability_vals>0, 1, 0)
        self.stability_colormap = np.where(self.stability_bool==1, 'b', 'r')
        return self.stability_vals

    def _assign_current_vars(self, closure_component='JJ', closure_phase=0) -> None:
        if closure_component == 'JJ':
            self.phi_T   = self.current_data[:,0] - closure_phase
            self.I       = self.current_data[:,1]
            self.chi     = self.current_data[:,2]
            self.phi_ind = self.current_data[:,3] - closure_phase
        elif closure_component == 'Inductor':
            self.phi_T   = self.current_data[:,0] - closure_phase
            self.I       = self.current_data[:,1]
            self.chi     = self.current_data[:,2] - closure_phase
            self.phi_ind = self.current_data[:,3]
        else:
            raise Exception('Name a valid closure component')
        self.current_data = np.concatenate([
          self.phi_T.reshape(-1,1),
          self.I.reshape(-1,1),
          self.chi.reshape(-1,1),
          self.phi_ind.reshape(-1,1)],
          axis=1)
        return self

    def __call__(self):
        pass


class LinRhombus:
    def __init__(self, leg1: Leg, leg2: Leg):
        self.leg1 = leg1
        self.leg2 = leg2
        if leg1.junction.EJ == leg2.junction.EJ and leg1.ind.EL == leg2.ind.EL: 
            self.name = 'Symmetric Rhombus'
            self.EJ = leg1.junction.EJ
            self.EL = leg1.ind.EL
        else:
            self.name = 'Asymmetric Rhombus'
            self.EJ1 = leg1.junction.EJ
            self.EL1 = leg1.ind.EL
            self.EJ2 = leg2.junction.EJ
            self.EL2 = leg2.ind.EL

    def calculate_circuit(self, phase, threaded_flux=np.pi):
        self.phase = phase
        self.threaded_flux = threaded_flux
        self.leg1.calculate_circuit(phase, threaded_flux=0)
        self.leg2.calculate_circuit(phase, threaded_flux=threaded_flux) # VERIFY SIGN TREATMENT
        self.data = sum_matching_rows(self.leg1.data, self.leg2.data) # Only chi column will not make sense
        self.phi_T = self.data[:,0]/2
        self.I = self.data[:,1]
        self.E = self.data[:,-2]
        self.data[:,-1] = np.where(self.data[:,-1]==2, 1, 0) # Only output 'stable' if both chi1 and chi2 have stable phases
        self.stability_bool = self.data[:,-1]
        self.stability_colormap = np.where(self.stability_bool==1, 'b', 'r')

    def current(self, phase, threaded_flux=np.pi):
        self.phase = phase
        self.threaded_flux = threaded_flux
        self.leg1.current(phase)
        self.leg2.current(phase + threaded_flux, threaded_flux) #VERFIY SIGN TREATMENT
        self.current_data = sum_matching_rows(self.leg1.current_data, self.leg2.current_data) # Only sensical for getting I
        self._assign_current_vars()

    def stability(self):
        if not hasattr(self, 'current_data'): raise Exception('Need to run a calculation first')
        return self.stability_bool

    def energy(self):
        if not hasattr(self, 'current_data'): raise Exception('Need to run a calculation first')
        return self.E

    def _assign_current_vars(self):
        self.phi_T = self.current_data[:,0]
        self.I = self.current_data[:,1]
        self.chi1 = self.leg1.chi
        self.chi2 = self.leg2.chi 
        self.phi_ind1 = self.leg1.phi_ind
        self.phi_ind2 = self.leg2.phi_ind

    def __call__(self):
        pass