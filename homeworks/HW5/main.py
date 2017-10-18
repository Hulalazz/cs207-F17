import numpy as np
import chemkin
import reaction_coeffs as rrc

np.set_printoptions(precision=3)

M = 3 # Number of reaction
N = 5 # Number of species

concs = np.array([2.0, 1.0, 0.5, 1.0, 1.0])

Temps = [750.0, 1500.0, 2500.0]

A1, b1, E1 = 1.0e+08, 0.5, 5.0e+04
A2, E2 = 1.0e+07, 1.0e+04

nu_react = np.array([[2.0, 0.0, 0.0], [1.0, 0.0, 1.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
nu_prod = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [2.0, 0.0, 1.0], [0.0, 0.0, 1.0], [0.0, 1.0, 0.0]])    

print(nu_react)
print()
print(nu_prod)
print()

k = np.zeros(M)
for T in Temps:
    # Get the reaction rate coefficients
    k[0] = rrc.k_mod_arr(A1, b1, E1, T)
    k[1] = rrc.k_const(1.0e+04)
    k[2] = rrc.k_arr(A2, E2, T)
    
    # Get progress rates for reactions
    omega = chemkin.progress_rate(nu_react, concs, k)
    
    # Get reaction rates for species
    f = chemkin.reaction_rate(nu_react, nu_prod, omega)
    
    # Print reaction rates to screen
    print('T = {0:9.3f}'.format(T))
    print('k = {}'.format(k))
    print('f = {}\n\n'.format(f))
