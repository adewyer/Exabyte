"""
Author: Amanda Dewyer
Date: September 7th 2020

File that contains all parameters for
the basis set basis set selector.
"""

import sys
import json
import logging

class Parameters:
    """
    Class defining all parameters to their
    default settings and redefines parameters
    to user chosen values when applicable."
    """

    def __init__(self, file=None):
        """
        Initialize all parameter variables and read in 
        the user input file.
        """
        
        # User input file
        self.inputFile = file
        self.par = {
            # General calculation & structure parameters
            'molecule_name' : '',
            'job_description' : '',
            'structure' : [],
            'charge' : 0,
            'multiplicity' : 1,

            # Basis set selector parameters
            'basis_set_selector' : 'Specific',
            'qc_method' : 'dft',
            'dft_method' : 'b3lyp',
            'opt_threshold' : '', # optimization scf threshold
            # 'model_phase' : 'testing',
            'reference_type' : 'energy',
            'reference_value' : '', # Units need to line up with output
            'reference_value_method' : 'CCSD(T)',
            'property_threshold' : ''  # Threshold should be entered as a float, i.e. 5.0 = 5% tolerance
            }

        # Reading parameter file functions
        if self.inputFile is not None:
            self.read_user_input()  # Overwrite any paramters defined by user

    def read_user_input(self):
        """
        Function to read input from user input .json file
        and overwrite any parameter defaults into the parameter
        dictionary.
        """
        try:
            with open(self.inputFile) as json_input:
                try:
                    userParameters = json.load(json_input)
                except ValueError:
                    err = 'Input .json file contains an error.'
                    raise ValueError(err)
        except IOError:
            err = 'The .json input file ({}) does not exist'.format(self.inputFile)
            raise IOError(err)
        for key in userParameters:
            if key in self.par:
                self.par[key] = userParameters[key]
            else:
                err = '{} is not a valid parameter'
                print(err.format(key))

    
    def print_parameters(self):
        """
        Function that creates a string of all parameters.
        Generally used for testing purposes.
        """
        parameters = ''
        for key in self.par:
            parameters += '{}\t{}\n'.format(key, self.par[key])

        return parameters
