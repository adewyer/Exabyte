"""
Author: Amanda Dewyer
Date: September 7th 2020

Main class to run basis set selector program.
Functionality includes:
1. Reading in user input from .json file.
2. Running basis set selector method designated by user.
3. Returns optimal basis set for user, based on input.
"""

import sys
import os
import logging
import basis_sets as basis

def main():
   
    try:
        input_file = sys.argv[1]
    except IndexError:
        print("Invalid input file, please try again.")
        sys.exit(-1)

    param = Parameters(input_file)
    logging.basicConfig(filename='basis_set_selector.log', level=logging.INFO)
    logging.info("Starting basis set selection.")
    logging.info("Method for basis set selection set to {}".format(param.par['basis_set_selector']))
    if param.par['basis_set_selector'] == 'General':
        logging.info("\tModel phase selected: {}".format(param.par['model_phase']))
    elif param.par['basis_set_selector'] = 'Specific':
        logging.info("\t{} value for comparison is {} within a threshold of {} units.".format(param.par['reference_type'],
                                                                                              param.par['reference_value'],
                                                                                              param.par['selector_threshold']))
    else:
        logging.info("Method for basis set selection is invalid, method should be either 'General' or 'Specific'")
        print("Invalid parameter input for method selection, please try again.")
        sys.exit(-1)
    
    # test works to connect to basis sets module
    basis.generate_basis('pople', '6-31G', '++', '**') 

main()    
