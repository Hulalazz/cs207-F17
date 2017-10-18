import numpy as np
import xml.etree.ElementTree as ET

tree = ET.parse('rxns.xml')
rxns = tree.getroot()

R = 8.314
T = 1500.0
RT = R * T

for p in rxns.findall('phase'):
    species = p.find('speciesArray').text.split()

N = len(species)

#species_dict = dict(zip(species, list(range(len(species)))))
species_dict = dict(zip(list(range(len(species))), species))

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

                # k = A * T**b * np.exp(-E / RT)
                # print('k for {0} = {1:20.16e}'.format(rxn.attrib['id'], k))

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
        reactant_list = [0]*N
        for i in reactants:
            s_nuij = i.split(':')
            sr = s_nuij[0]
            for idx, s in enumerate(species):
                if sr == s:
                    reactant_list[idx] = int(s_nuij[1])
                    break

        products = rxn.find('products').text.split()
        product_list = [0]*N
        for i in products:
            s_nuij = i.split(':')
            sp = s_nuij[0]
            for idx, s in enumerate(species):
                if sp == s:
                    product_list[idx] = int(s_nuij[1])
                    break

        stoich_info[rxn.attrib['id']] = {"reactants":reactant_list, "products":product_list}
            
      
        M += 1

print(rxn_info)
print(stoich_info)

#for r, kd in rxn_info.items():
#    for ktype, params in kd.items():
#        if (ktype == "Constant"):
#           print(params)
#        elif (ktype == "Arrhenius"):
#           print(params)
#        elif (ktype == "modifiedArrhenius"):
#           print(params)
#        else:
#            print("Nope")

print(N, M)
nuij_p = np.zeros([N,M])
nuij_pp = np.zeros([N,M])
j = 0
for r, st_info in stoich_info.items():
    col_r = st_info["reactants"]
    col_p = st_info["products"]
    nuij_p[:,j] = col_r
    nuij_pp[:,j] = col_p
    j += 1

print("\n\n\n")
print(nuij_pp)


