"""This module contains functions that return reaction rate coefficients
   
   MEMBERS:
   ========
   k_const:   Returns a constant reaction rate coefficient
   k_arr:     Returns the Arrhenius reaction rate coefficient
   k_mod_arr: Returns the modified Arrhenius reaction rate coefficient
"""

import numpy as np

def k_const(k=1.0):
    """Simply returns a constant reaction rate coefficient
    
    INPUTS:
    =======
    k: float, default value = 1.0
       Constant reaction rate coefficient
    
    RETURNS:
    ========
    k: float
       Constant reaction rate coefficient
    
    EXAMPLES:
    =========
    >>> k_const(5.0)
    5.0
    """
    if k < 0:
        raise ValueError("Negative reaction rate coefficients are prohibited.")

    return k

def k_arr(A, E, T, R=8.314):
    """Calculates the Arrhenius reaction rate coefficient
    
    INPUTS:
    =======
    A: float
       Arrhenius prefactor
       Must be positive
    E: float
       Activation energy
    T: float
       Temperature
       Must be positive
    R: float, default value = 8.314
       Ideal gas constant
       Must be positive
    
    RETURNS:
    ========
    k: float
       Arrhenius reaction rate coefficient
    
    EXAMPLES:
    =========
    >>> k_arr(2.0, 3.0, 100.0)
    1.9927962618542914
    """
    
    if A < 0.0:
        raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

    if T < 0.0:
        raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

    if R < 0.0:
        raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

    return A * np.exp(-E / R / T)

def k_mod_arr(A, b, E, T, R=8.314):
    """Calculates the modified Arrhenius reaction rate coefficient
    
    INPUTS:
    =======
    A: float
       Arrhenius prefactor
       Must be positive
    b: float
       Modified Arrhenius parameter
    E: float
       Activation energy
    T: float
       Temperature
       Must be positive
    R: float, default value = 8.314
       Ideal gas constant
       Must be positive
    
    RETURNS:
    ========
    k: float
       Modified Arrhenius reaction rate coefficient
    
    EXAMPLES:
    =========
    >>> k_mod_arr(2.0, -0.5, 3.0, 100.0)
    0.19927962618542916
    """
    if A < 0.0:
        raise ValueError("A = {0:18.16e}:  Negative Arrhenius prefactor is prohibited!".format(A))

    if T < 0.0:
        raise ValueError("T = {0:18.16e}:  Negative temperatures are prohibited!".format(T))

    if R < 0.0:
        raise ValueError("R = {0:18.16e}:  Negative ideal gas constant is prohibited!".format(R))

    return A * T**b * np.exp(-E / R / T)