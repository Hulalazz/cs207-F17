import numpy as np
import copy

class chemkin:

    def __init__(self, fname):
        self.name = fname

    def read(self):
        # Parse .xml input file
        self.nuij_p  = np.array([[2.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        self.nuij_pp = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])
        self.nuij = self.nuij_pp - self.nuij_p
        self.M = 3
        self.N = 5


class reactions(chemkin):

    def __init__(self, fname):
        self.name = fname

    def k_const(self, k=1.0):
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
    
    def k_arr(self, A, E, T, R=8.314):
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
    
    def k_mod_arr(self, A, b, E, T, R=8.314):
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

    def progress_rate(self, concs, k):
        """Returns the progress rate of a system of irreversible, elementary reactions
        
        INPUTS:
        =======
        nu_react: numpy array of floats, 
                  size: num_species X num_reactions
                  stoichiometric coefficients for the reaction
        k:        array of floats
                  Reaction rate coefficient for the reaction
        concs:    numpy array of floats 
                  concentration of species
    
        RETURNS:
        ========
        omega: numpy array of floats
               size: num_reactions
               progress rate of each reaction
        
        EXAMPLES:
        =========
        >>> progress_rate(np.array([2.0, 1.0, 1.0]), 10.0)
        array([ 40.,  20.])
        """
        progress = copy.copy(k) # Initialize progress rates with reaction rate coefficients
        for jdx, rj in enumerate(progress):
            if rj < 0:
                raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(rj))
            for idx, xi in enumerate(concs):
                nu_ij = self.nuij_p[idx,jdx]
                if xi  < 0.0:
                    raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
                if nu_ij < 0:
                    raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))
                
                progress[jdx] *= xi**nu_ij
        return progress

    def reaction_rate(self, rj):
        return np.dot(self.nuij, rj)
