"""
Author: Amanda Dewyer
Date: September 7th 2020

Main class to run basis set selector program.
Functionality includes:
1. Reading in user input from .json file.
2. Running basis set selector method designated by user.
3. Returns optimal basis set for user, based on input.
"""

import time
import sys
import os
import logging
from basisSetSelector import basis_sets as basis
from basisSetSelector import molecule
from basisSetSelector import nwchem
from basisSetSelector import parameters
from basisSetSelector import basis_library_nwchem as nwlib
from basisSetSelector import propertyCheck

def main():
   
    try:
        input_file = sys.argv[1]
    except IndexError:
        print("Invalid input file, please try again.")
        sys.exit(-1)

    if not os.path.exists('singlePoints'):
        os.makedirs('singlePoints')

    param = parameters.Parameters(input_file)
    
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logging.info("Starting basis set selection.")
    logging.info("{} file supplied as input.".format(input_file))
    logging.info("Method for basis set selection set to {}".format(param.par['basis_set_selector']))

    if param.par['basis_set_selector'] == 'General':
        logging.info("\tModel phase selected: {}".format(param.par['model_phase']))
    elif param.par['basis_set_selector'] == 'Specific':
        logging.info("\t{} value for comparison is {} within a threshold of {} units.".format(param.par['reference_type'],
                                                                                              param.par['reference_value'],
                                                                                              param.par['selector_threshold']))
    else:
        logging.info("Method for basis set selection is invalid, method should be either 'General' or 'Specific'")
        print("Invalid parameter input for method selection, please try again.")
        sys.exit(-1)

    basisSets = basis.create_basis_list()
    allNwchemBasis = nwlib.get_all_nwchem_basis()
    for bas in basisSets:
        if bas not in allNwchemBasis:
            basisSets.remove(bas)
    nw = nwchem.Nwchem(param)
    jobs = []
    energies = {}
    for basisSet in basisSets:
        print(basisSet)
        job = nw.write_nwchem_input(basisSet)
        jobs.append(job)

    status = 1
    for i, job in enumerate(jobs):
        if status == 1:
            print("submitting {}.inp".format(job))
            nw.nwchem_submit(job)
            status = 0
            time.sleep(3) 
        while status == 0:
            status = nw.check_nwchem(job)
        energy = nw.get_nwchem_energy(job) 
        energies[job] = energy
    print(energies)
    print(type(energies))
    #need to get code to send dictionary
    acceptableBasisSets = propertyCheck.compare_property(param.par['selector_threshold'], energies, param.par['reference_value'])
    print("The following basis sets produce energies within {} of {}".format(param.par['selector_threshold'], param.par['reference_value']))
    for b in acceptableBasisSets:
        print("\t{}".format(b))
       
main()
"""
    # test works to connect to basis sets module
    basisSet = basis.generate_basis('pople', '3-21G', '+', '*')
    print(basis)
    # test molecule
    mol = molecule.Molecule(param.par['charge'], param.par['multiplicity'], param.par['structure'])
    print(mol.get_atoms()) 
    print(mol.get_coords()) 
    print(mol.get_charge())
    print(mol.get_mult())
"""
