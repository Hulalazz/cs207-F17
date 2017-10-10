import numpy as np
import xml.etree.ElementTree as ET

tree = ET.parse('rxns.xml')
rxns = tree.getroot()

R = 8.314
T = 1500.0
RT = R * T

for reactions in rxns.findall('reactionData'):
    for rxn in reactions.findall('reaction'):
        for ratecoeff in rxn.findall('rateCoeff'):
            for model in ratecoeff.findall('Arrhenius'):
                A = float(model.find('A').text)
                b = float(model.find('b').text)
                E = float(model.find('E').text)

                k = A * T**b * np.exp(-E / RT)

                print('k for {0} = {1:20.16e}'.format(rxn.attrib['id'], k))

for p in rxns.findall('phase'):
    species = p.find('speciesArray').text.split()

print(species)
