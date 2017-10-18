import numpy as np
import copy
import xml.etree.ElementTree as ET

class chemkin:

    def __init__(self, fname):
        self.name = fname

    def read(self):
        tree = ET.parse(self.name)
        rxns = tree.getroot()

        for p in rxns.findall('phase'):
            species = p.find('speciesArray').text.split()
        
        self.N = len(species)

        rxn_info = {}
        stoich_info = {}
        for reactions in rxns.findall('reactionData'):
            M = 0
            for rxn in reactions.findall('reaction'):
                d = {}
                for ratecoeff in rxn.findall('rateCoeff'):
                    for model in ratecoeff.findall('modifiedArrhenius'):
                        A = float(model.find('A').text)
                        b = float(model.find('b').text)
                        E = float(model.find('E').text)
        
                        d['modifiedArrhenius'] = [A, b, E]
                        rxn_info[rxn.attrib['id']] = d
        
                    for model in ratecoeff.findall('Arrhenius'):
                        A = float(model.find('A').text)
                        E = float(model.find('E').text)
        
                        d['Arrhenius'] = [A, E]
                        rxn_info[rxn.attrib['id']] = d
        
                    for model in ratecoeff.findall('Constant'):
                        k = float(model.find('k').text)
        
                        d['Constant'] = k
                        rxn_info[rxn.attrib['id']] = d
        
                reactants = rxn.find('reactants').text.split()
                reactant_list = [0]*self.N
                for i in reactants:
                    s_nuij = i.split(':')
                    sr = s_nuij[0]
                    for idx, s in enumerate(species):
                        if sr == s:
                            reactant_list[idx] = int(s_nuij[1])
                            break
        
                products = rxn.find('products').text.split()
                product_list = [0]*self.N
                for i in products:
                    s_nuij = i.split(':')
                    sp = s_nuij[0]
                    for idx, s in enumerate(species):
                        if sp == s:
                            product_list[idx] = int(s_nuij[1])
                            break
        
                stoich_info[rxn.attrib['id']] = {"reactants":reactant_list, "products":product_list}
                    
              
                M += 1
        
        self.M = M

        self.rxn_info = rxn_info
        self.stoich_info = stoich_info
        
        nuij_p = np.zeros([self.N,self.M])
        nuij_pp = np.zeros([self.N,self.M])
        j = 0
        for r, st_info in stoich_info.items():
            col_r = st_info["reactants"]
            col_p = st_info["products"]
            nuij_p[:,j] = col_r
            nuij_pp[:,j] = col_p
            j += 1

        self.nuij_p = nuij_p
        self.nuij_pp = nuij_pp
        self.nuij = nuij_pp - nuij_p


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
