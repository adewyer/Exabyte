"""
Author: Amanda Dewyer
Date: September 7th 2020

Main function of basis set selector package..

Program will create and run nwchem quantum chemistry
calculations with various basis sets and identify which
basis sets produce a property type within a given threshold
of a reference value supplied by the user.

The code will return the least accurate and expensive basis set
as well as the most accurate and expensive basis set that fit
the threshold and reference criteria supplied by the user.

A list of all basis sets that fit within criteria is also created.
"""

import sys
import os
import logging
import time
from basis_selector import basis_sets as bs
from basis_selector import molecule
from basis_selector import nwchem
from basis_selector import parameters
from basis_selector import basis_library as lib
from basis_selector import compare_values

def main():
   
    try:
        inputFile = sys.argv[1]
    except IndexError:
        print("Invalid input file, please try again.")
        sys.exit(-1)

    if not os.path.exists('singlePoints'):
        os.makedirs('singlePoints')

    # Gather parameters from user input .json file.
    param = parameters.Parameters(inputFile)
    
    # Create output file to track calculation progress.
    logging.basicConfig(filename='output.log', level=logging.INFO)
    logging.info("############################")
    logging.info("Starting basis set selection.")
    logging.info("{} file supplied as input.".format(inputFile))
    logging.info("\t{} value for comparison is {} within a {} threshold.".format(param.par['reference_type'],
                                                                                 param.par['reference_value'],
                                                                                 param.par['property_threshold']))
    # List of all available NWChem basis sets.
    allNwchemBasis = lib.get_nwchem_basis_library()
    # Create list of possible pople & dunning basis sets for testing.
    basisSets = bs.create_basis_list()
    # Check to see if basis sets are available in NWChem software.
    for basis in basisSets:
        if basis not in allNwchemBasis:
            basisSets.remove(basis)

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

    # Collect results from basis set comparison to reference and threshold supplied by user.
    acceptableBasisSets, leastAccurateBasis, mostAccurateBasis = compare_values.check_property(param.par['molecule_name'],
                                                                                               param.par['reference_type'], 
                                                                                               param.par['property_threshold'], 
                                                                                               energies, 
                                                                                               param.par['reference_value'])

    logging.info("The following basis sets produce energies within {} of {}".format(param.par['property_threshold'], 
                                                                                    param.par['reference_value']))
    labelLength = len(param.par['molecule_name']) + 1
    if len (acceptableBasisSets) == 0:
        logging.info("No basis sets meet threshold and reference criteria.")
    else:
        for basis in acceptableBasisSets:
            logging.info("\t{}".format(basis[labelLength::]))


    print("Done with Basis Set Selection")
    print("{} is the cheapest and least accurate basis set that fits threshold criteria.".format(leastAccurateBasis))
    print("{} is the most expensive and most accurate basis set that fits threshold criteria.".format(mostAccurateBasis))
