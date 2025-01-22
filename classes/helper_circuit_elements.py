'''Module for all the functions to be used'''

from matplotlib import pyplot as plt
import numpy as np
import time
import sys
from scipy.optimize import root_scalar



class JJ: ...
class Inductor: ...
class Leg: ...
class LinRhombus: ...
class Cos2Phi: ...


### for circuit_elements.py ###
def precise_sol(leg, chi_min, chi_max, phi_T_val, points = 100):
    chi_range = np.linspace(chi_min, chi_max, points)
    # phi_T, chi = np.meshgrid()
    phi_ind = phi_T - chi
    diff_row = leg.junction.current(chi) - leg.ind.current(phi_ind)
    valid_chi, _ = sign_switch(diff_row)
    return valid_chi


def invert_phase_relation(leg: Leg) -> Leg:
    '''
    Within a given phi_T range, this will find all the permissible current values that satisfy
    the phase/current condition.
    '''
    
    def calculate_inverted_phase(mod_2pi):
        '''
        Inverts the phase relation of phase across leg and phase of defining variable chi
        - Creates mesh grid of chi and phi_T (where phi_T has already been mod 2pied)
        - Finds where in each row there are solutions (the difference changes sign)
        - Returns a data array
        '''
        phi_T, chi = np.meshgrid(leg.phase, leg.phase)
        phi_ind = phi_T - chi + mod_2pi
        current_diff = leg.junction.current(chi) - leg.ind.current(phi_ind)
        chi_index, phi_T_index = sign_switch(current_diff)
        # TODO: ADD MORE PRECISE VALUES TO CHI USING THE ROOT SCALAR FUNCTION
        valid_phi_T = phi_T[0, phi_T_index]
        # valid_chi = precise_sol(leg, chi[chi_index, 0], chi[chi_index-1, 0], valid_phi_T)
        valid_chi = chi[chi_index, 0]
        valid_current = leg.junction.current(valid_chi)
        valid_phi_ind = valid_chi + mod_2pi # NOTE: This is non-compact
        data = np.array((
            valid_phi_T,
            valid_current,
            valid_chi,
            valid_phi_ind)).T # VERY IMPORTANT AS THIS DEFINES THE DATA STRUCTURE'S ORDER
        return data


    def mod_2pi_shifter(direction):
        '''
        Shifts inductor's phase by 2pi forward/backwards until no valid solutions are found
        - This is identical to taking any other variable mod 2pi. The single relation has
          the singular degree of freedom being the modulo 2pi that the relation take on.
        '''
        if direction == 'forward':
            sign = 1
        elif direction == 'backward':
            sign = -1
        else:
            raise Exception('Invalid argument for forward_back function')
        mod_2pi = 0
        contains_data = True 
        while(contains_data == True):
            data = calculate_inverted_phase(mod_2pi)
            if data.shape[1] != leg.current_data.shape[1]: raise Exception('Data.shape incorrect')
            leg.current_data = np.append(leg.current_data, data, axis=0)
            mod_2pi += sign*2*np.pi
            contains_data = True if data.shape[0] != 0 else False
    
    mod_2pi_shifter('forward')
    mod_2pi_shifter('backward')
    return leg

def average_contiguous_columns(arr): # Unneeded if each phi_T is given a precise chi and current value
    """
    Avgs the values in all columns except the first for each contiguous unique entry in column 0
    Parameters: arr (numpy.ndarray): Input 2D array with shape (n, m).
    Returns: numpy.ndarray: Output array with each row = [unique_value, avg_col1, avg_col2, ...].
    """
    first_col = arr[:, 0]
    other_cols = arr[:, 1:]

    result = []
    start_idx = 0

    for i in range(1, len(first_col)):
        if first_col[i] != first_col[start_idx]:
            # Compute average for the contiguous block in all other columns
            avg_values = np.mean(other_cols[start_idx:i], axis=0)
            result.append([first_col[start_idx], *avg_values])
            start_idx = i

    # Handle the last block
    avg_values = np.mean(other_cols[start_idx:], axis=0)
    result.append([first_col[start_idx], *avg_values])

    return np.array(result)

def add_interpolated_rows(arr, delta: int = 20):
    """
    Adds rows to an n x 2 array if the second column increases by more than 1
    between consecutive rows. The new rows consist of linearly interpolated values.

    Parameters: arr (numpy.ndarray): Input n x 2 array of integers.
    Returns: numpy.ndarray: New array with interpolated rows added where necessary.
    """
    result = []

    for i in range(len(arr) - 1):
        # Append the current row to the result
        result.append(arr[i])

        # Check if the second column increases by more than 1
        diff = arr[i + 1, 1] - arr[i, 1]
        if abs(diff) > 1 and abs(diff) < delta:
            # Linearly interpolate values for the second column
            x_start, x_end = arr[i, 0], arr[i + 1, 0]
            y_start, y_end = arr[i, 1], arr[i + 1, 1]

            for y in range(y_start + 1, y_end):
                # Interpolate x values linearly
                x_interp = x_start + (y - y_start) * (x_end - x_start) / (y_end - y_start)
                result.append([round(x_interp), y])

    # Append the last row
    result.append(arr[-1])

    return np.array(result, dtype=int)

def sum_matching_rows(arr1, arr2):
    """
    Sums all possible combinations of rows from two matrices where the first column values are =.
    Parameters:
        arr1 (numpy.ndarray): First array of shape (n, k).
        arr2 (numpy.ndarray): Second array of shape (m, k).
    Returns: numpy.ndarray: Array containing the summed rows where the first column matches.
    """
    # Ensure both arrays have the same number of columns
    if arr1.shape[1] != arr2.shape[1]:
        raise ValueError("Both arrays must have the same number of columns.")

    result = []
    
    # Iterate over unique values in the first column of arr1
    unique_values = np.intersect1d(arr1[:, 0], arr2[:, 0])
    
    for value in unique_values:
        # Select rows from both arrays where the first column matches the current value
        rows1 = arr1[arr1[:, 0] == value]
        rows2 = arr2[arr2[:, 0] == value]

        # Compute all possible sums of rows
        for row1 in rows1:
            for row2 in rows2:
                result.append(row1 + row2)

    return np.array(result)

def sign_switch(sign_change_mat):
    '''
    - Checks for a sign change in a sign_change matrix
    - Makes every value of phi_T present on the grid'''
    signs = np.sign(sign_change_mat)
    sign_change_bools = signs[:, :-1] * signs[:, 1:] < 0
    valid_chi, valid_phi_T = np.nonzero(sign_change_bools)
    if valid_chi.size == 0:
        return valid_chi, valid_phi_T
    valid_phases = np.stack((valid_chi, valid_phi_T)).T
    valid_gridded = add_interpolated_rows(valid_phases) 
    valid_chi, valid_gridded_phi_T = valid_gridded[:, 0], valid_gridded[:, 1]
    return (valid_chi, valid_gridded_phi_T)



### Misc Functions ###

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Record the start time
        result = func(*args, **kwargs)  # Call the function
        end_time = time.time()  # Record the end time
        print(f"{func.__name__} executed in {end_time - start_time:.6f} seconds")
        return result  # Return the function's result
    return wrapper



### Unused Functions ###

def rolling_average(array, window_size):
    """
    Computes the rolling average of a 1D NumPy array.
    Parameters:
        array (numpy.ndarray): Input 1D array.
        window_size (int): Size of the rolling window.
    Returns: numpy.ndarray: Array of rolling averages.
    """
    # Use np.convolve to compute rolling average
    kernel = np.ones(window_size) / window_size
    rolling_avg = np.convolve(array, kernel, mode='valid')
    return rolling_avg

def find_all_solutions(b, x_min, x_max, num_points=1000):
    """
    Finds all solutions to sin(x) = b * x within a specified interval [x_min, x_max].
    Parameters:
        b (float): Coefficient in the equation sin(x) = b * x.
        x_min (float): Minimum value of the interval.
        x_max (float): Maximum value of the interval.
        num_points (int): Number of points to scan for initial guesses.
    Returns: solutions (list): List of solutions (roots) in the interval.
    """
    # Define the function f(x) = sin(x) - b * x
    def f(x):
        return np.sin(x) - b * x

    # Generate initial guesses using a linspace
    x_values = np.linspace(x_min, x_max, num_points)
    solutions = []

    # Check sign changes between consecutive points for root existence
    for i in range(len(x_values) - 1):
        x_left, x_right = x_values[i], x_values[i + 1]
        if f(x_left) * f(x_right) < 0:  # Sign change indicates a root
            # Use root_scalar to find the root in the interval
            sol = root_scalar(f, bracket=[x_left, x_right], method='brentq')
            if sol.converged:
                solutions.append(sol.root)

    return solutions
