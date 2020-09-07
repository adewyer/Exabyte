"""
Author: Amanda Dewyer
Date: September 7th 2020

Basis sets available for selection
by the automated basis set selector package
"""

# Pople Basis Sets (X-YZg type basis)
# X = primitive gaussians defining core electrons
# Y & Z = primitive gaussians defining valence electons

polarization = '*'
popleDiffuse = '+'
popleBasis = {}
pople = 'G'

popleBasis['3-21G'] = '3-21'
popleBasis['6-31G'] = '6-31'
popleBasis['6-211G'] = '6-311'

# Dunning Basis Sets (cc-pVNZ type basis)
# cc-p = correlation consistent polarized
# V = valence only functionals
# NZ = number of functions used to describe valence electrons
# core electron functions can be added

dunningDiffuse = 'aug-'
dunningBasis = {}

dunningBasis['cc-pVDZ'] = 'cc-pVDZ' 
dunningBasis['cc-pVTZ'] = 'cc-pVTZ' 
dunningBasis['cc-pVQZ'] = 'cc-pVQZ' 
dunningBasis['cc-pV5Z'] = 'cc-pV5Z' 
dunningBasis['cc-pV6Z'] = 'cc-pV6Z'

# Other basis set types to add:
# Karlsruhe (def2-NVP type basis)
# CBS (complete basis set type)
# STO (minimal basis sets)
