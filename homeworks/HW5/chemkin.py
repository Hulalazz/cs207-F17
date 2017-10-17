import numpy as np
import copy
def progress_rate(nu_react, concs, k):
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
    >>> progress_rate_2(np.array([[2.0, 1.0], [1.0, 0.0], [0.0, 1.0]]), np.array([2.0, 1.0, 1.0]), 10.0)
    array([ 40.,  20.])
    """
    progress = copy.copy(k) # Initialize progress rates with reaction rate coefficients
    for jdx, rj in enumerate(progress):
        if rj < 0:
            raise ValueError("k = {0:18.16e}:  Negative reaction rate coefficients are prohibited!".format(rj))
        for idx, xi in enumerate(concs):
            nu_ij = nu_react[idx,jdx]
            if xi  < 0.0:
                raise ValueError("x{0} = {1:18.16e}:  Negative concentrations are prohibited!".format(idx, xi))
            if nu_ij < 0:
                raise ValueError("nu_{0}{1} = {2}:  Negative stoichiometric coefficients are prohibited!".format(idx, jdx, nu_ij))
            
            progress[jdx] *= xi**nu_ij
    return progress

def reaction_rate(nu_react, nu_prod, rj):
    """Returns the reaction rate of a system of irreversible, elementary reactions
    
    INPUTS:
    =======
    nu_react: numpy array of floats, 
              size: num_species X num_reactions
              stoichiometric coefficients for the reactants
    nu_prod:  numpy array of floats, 
              size: num_species X num_reactions
              stoichiometric coefficients for the products
    k:        float, default value is 10, 
              Reaction rate coefficient for the reaction
    concs:    numpy array of floats 
              concentration of species

    RETURNS:
    ========
    f: numpy array of floats
       size: num_species
       reaction rate of each specie
    
    EXAMPLES:
    =========
    >>> nu_react = np.array([[1.0, 0.0], [2.0, 0.0], [0.0, 2.0]])
    >>> nu_prod = np.array([[0.0, 1.0], [0.0, 2.0], [1.0, 0.0]])
    >>> r = np.array([ 40.,  20.])
    >>> reaction_rate(nu_react, nu_prod, r)
    array([-20., -40.,   0.])
    """
    nu = nu_prod - nu_react
    return np.dot(nu, rj)
