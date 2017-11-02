import numpy as np

class thermochem:

    def __init__(self, rxnset):
        self.rxnset = rxnset

    def Cp_over_R:

    def H_over_RT:

    def S_over_R:

    def backward_coeffs(self, kf, T):
        dH_RT = np.dot(self.rxnset.nuij.T, H_over_RT(T))
        dS_R = np.dot(self.rxnset.nuij.T, S_over_R(T))

        gamma = np.sum(self.rxnset.nuij, axis=0)
        fact = p0 / R / T
        kb = fact**gamma * np.exp(dS_R - dH_RT)
        return kb
