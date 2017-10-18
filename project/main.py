import numpy as np
import chemkin

concs = np.array([2.0, 1.0, 0.5, 1.0, 1.0])
T = 1500.0

rxns = chemkin.reactions('rxnset_long.xml')
rxns.read()

k = np.zeros(rxns.M)

j = 0
for r, kd in rxns.rxn_info.items():
    for ktype, params in kd.items():
        if (ktype == "Constant"):
           k[j] = rxns.k_const(params)
        elif (ktype == "Arrhenius"):
           k[j] = rxns.k_arr(params[0], params[1], T)
        elif (ktype == "modifiedArrhenius"):
           k[j] = rxns.k_mod_arr(params[0], params[1], params[2], T)
        else:
            print("Nope")
    j += 1

print("Reaction Rate Coefficients:")
print("===========================")
for rxn, rrc in enumerate(k):
    print("k{0} = {1:18.16e}".format(rxn+1, rrc))
print("\n\n")

omega = rxns.progress_rate(concs, k)

f = rxns.reaction_rate(omega)

print("Reaction Rates:")
print("===============")
sdict = dict(enumerate(rxns.species))
for i, fs in enumerate(f):
    print("{0} = {1:18.16e}".format(sdict[i], fs))
print("\n\n")
