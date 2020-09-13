"""
Author: Amanda Dewyer
Date: September 7th 2020

Script is meant to act as a dictionary of
Basis sets available for use with the 
automated basis set selector package

Other basis set types to add in the future:
  Karlsruhe (def2-NVP type basis)
  CBS (complete basis set type)
  STO (minimal basis sets)
  cc-pV5Z, cc-pV6Z, aug-cc-pV5Z, aug-cc-pV6Z
  Any basis sets available in nwchem

"""

# Dictionary for Pople Basis Sets (X-YZg type basis)
# X = primitive gaussians defining core electrons
# Y & Z = primitive gaussians defining valence electons
# Polarization and diffuse functions can be added onto basis set

polarization = 's'
popleDiffuse = '+'

popleBasis = {}
popleBasis['3-21g'] = '3-21'
popleBasis['6-31g'] = '6-31'
popleBasis['6-211g'] = '6-311'

# Dictionary for Dunning Basis Sets (cc-pVNZ type basis)
# cc-p = correlation consistent polarized basis sets
# V = valence only functionals
# NZ = number of functions used to describe valence electrons
# core electron functions can be added

dunningDiffuse = 'aug-'

dunningBasis = {}
dunningBasis['cc-pvdz'] = 'cc-pvdz' 
dunningBasis['cc-pvtz'] = 'cc-pvtz' 
dunningBasis['cc-pvqz'] = 'cc-pvqz' 


def generate_single_basis(basisType, basis, polarization='', diffuse=''):
    """
    Generation of a single basis set for use in an NWChem calculation
    This function would be used in a later code version where individual
    basis sets were tested based on molecule properties. Rather than broad
    testing across any available basis sets.
    """
  
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
    """
    Generation of a list of pople and dunning basis sets based on
    dictionaries listed above, and additional functionality that can be applied.
    (i.e. polarization (s) and diffuse (+) functiions.)
    Basis sets are generated to match NWChem formatting.

    For example:

    Pople basis sets ranging from:
    3-21G (simplest based on dictionary and additional functions)
    3-21gs
    3-21+g
    3-21+g*
    ...
    ...
    ...
    6-311+gs
    6-311++gs
    6-31++Gss (most complex based on dictionary and additional functions)
    """

    basisSets = []

    # keywords to add additional functions for pople basis sets
    polarizationOptions = ['', polarization, 2 * polarization]
    diffuseOptions = ['', popleDiffuse, 2 * popleDiffuse]

    # keyword to add diffuse functions to dunning basis sets 
    dunningOptions = ['', dunningDiffuse]

    # create list of all possible pople basis set combos from popleBasis dict.
    for key, value in popleBasis.items():
        for pol in polarizationOptions:
            for dif in diffuseOptions:
                basis = value + dif + 'g' + pol
                basisSets.append(basis)

    # create list of all possible dunning basis set combos from dunningBasis dict.
    for key, value in dunningBasis.items():
        for option in dunningOptions:
            basis = option + value
            basisSets.append(basis)

    return basisSets
