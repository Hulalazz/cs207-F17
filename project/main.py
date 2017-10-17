import numpy as np
import chemkin

concs = np.array([2.0, 1.0, 0.5, 1.0, 1.0])
T = 1500.0

A1, b1, E1 = 1.0e+08, 0.5, 5.0e+04
k2 = 1.0e+04
A3, E3 = 1.0e+07, 1.0e+04

rxns = chemkin.reactions('rxns.xml')
rxns.read()

k = np.zeros(rxns.M)

k[0] = rxns.k_mod_arr(A1, b1, E1, T)
k[1] = rxns.k_const(k2)
k[2] = rxns.k_arr(A3, E3, T)

omega = rxns.progress_rate(concs, k)

f = rxns.reaction_rate(omega)

print(f)
