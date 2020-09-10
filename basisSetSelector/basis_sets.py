"""
Author: Amanda Dewyer
Date: September 7th 2020

Basis sets available for selection
by the automated basis set selector package
"""

# Pople Basis Sets (X-YZg type basis)
# X = primitive gaussians defining core electrons
# Y & Z = primitive gaussians defining valence electons

polarization = 's'
popleDiffuse = '+'
popleBasis = {}

popleBasis['3-21g'] = '3-21'
popleBasis['6-31g'] = '6-31'
popleBasis['6-211g'] = '6-311'

# Dunning Basis Sets (cc-pVNZ type basis)
# cc-p = correlation consistent polarized
# V = valence only functionals
# NZ = number of functions used to describe valence electrons
# core electron functions can be added

dunningDiffuse = 'aug-'
dunningBasis = {}

dunningBasis['cc-pvdz'] = 'cc-pvdz' 
dunningBasis['cc-pvtz'] = 'cc-pvtz' 
dunningBasis['cc-pvqz'] = 'cc-pvqz' 
# commented out 5z and 6z for demo due to time for calculations to run w/ aug-
# dunningBasis['cc-pv5z'] = 'cc-pv5z'  
# dunningBasis['cc-pv6z'] = 'cc-pv6z'

# Other basis set types to add:
# Karlsruhe (def2-NVP type basis)
# CBS (complete basis set type)
# STO (minimal basis sets)

def generate_single_basis(basisType, basis, polarization='', diffuse=''):
    if basisType == 'pople':
        basis = basis
        basisSet = popleBasis[basis] + diffuse + 'g' + polarization
    elif basisType == 'dunning':
        basis = basis
        basisSet = diffuse + dunningBasis[basis]
    else:
        print('Invalid basis set parameters for basis set generation')
        return None

    return basisSet

def create_basis_list():
    basisSets = []
    # Pople basis sets
    polarizationOptions = ['', polarization, 2 * polarization]
    diffuseOptions = ['', popleDiffuse, 2 * popleDiffuse]
    dunningOptions = ['', dunningDiffuse]
    for key, value in popleBasis.items():
        for pol in polarizationOptions:
            for dif in diffuseOptions:
                basis = value + dif + 'g' + pol
                basisSets.append(basis)

    for key, value in dunningBasis.items():
        for option in dunningOptions:
            basis = option + value
            basisSets.append(basis)

    return basisSets

"""
def main():
    # testing
    polar = polarization * 2
    generate_basis('pople', '3-21G', polar)
    generate_basis('dunning', 'cc-pVDZ', '', dunningDiffuse)
    basis = create_basis_list()
    print(basis)
main()
"""
