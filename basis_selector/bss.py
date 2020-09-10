"""
Author: Amanda Dewyer
Date: September 7th 2020

Main class to run basis set property program.
Program will create and run nwchem quantum chemistry
calculations with various basis sets and identify which
basis sets produce a property type within a given threshold
of a reference value supplied by the user.
"""

import sys
import os
import logging
import time
from basis_selector import basis_sets as b
from basis_selector import molecule
from basis_selector import nwchem
from basis_selector import parameters
from basis_selector import basis_library_nwchem as nwlib
from basis_selector import compare_values

def main():
   
    try:
        input_file = sys.argv[1]
    except IndexError:
        print("Invalid input file, please try again.")
        sys.exit(-1)

    if not os.path.exists('singlePoints'):
        os.makedirs('singlePoints')

    # Gather parameters from user input .json file.
    param = parameters.Parameters(input_file)
    
    # Create output file to track calculation progress.
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logging.info("############################")
    logging.info("Starting basis set selection.")
    logging.info("{} file supplied as input.".format(input_file))
    logging.info("\t{} value for comparison is {} within a {} threshold.".format(param.par['reference_type'],
                                                                                 param.par['reference_value'],
                                                                                 param.par['property_threshold']))
    # List of all available NWChem basis sets.
    allNwchemBasis = nwlib.get_all_nwchem_basis()
    # Create list of possible pople & dunning basis sets for testing.
    basisSets = b.create_basis_list()
    # Check to see if basis sets are available in NWChem software.
    for bas in basisSets:
        if bas not in allNwchemBasis:
            basisSets.remove(bas)

    # Create NWChem object for use in quantum chemical calculations.
    nw = nwchem.Nwchem(param)
    allCalcs = []
    energies = {}  # [calc name : energy]
    for basisSet in basisSets:
        calcName = nw.write_nwchem_input(basisSet)
        allCalcs.append(calcName)

    # Run all basis set calculations and check whether job status 0 (running) or 1 (finished).
    status = 1  # No Calculations Running
    print("Starting basis set calculations")
    for calcName in allCalcs:
        if status != 0:
            logging.info("submitting {}.inp".format(calcName))
            nw.nwchem_submit(calcName)
            status = 0
            time.sleep(3) 
        while status == 0:
            status = nw.check_nwchem(calcName)
        energy = nw.get_nwchem_energy(calcName)
        energies[calcName] = energy

    acceptableBasisSets = compare_values.check_property(param.par['molecule_name'], param.par['reference_type'], param.par['property_threshold'], energies, param.par['reference_value'])
    logging.info("The following basis sets produce energies within {} of {}".format(param.par['property_threshold'], param.par['reference_value']))
    for basis in acceptableBasisSets:
        logging.info("\t{}".format(basis))
