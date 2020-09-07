"""
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
        self.input_file = file
        
        self.par = {
            # General calculation & structure parameters
            'job_title' : '',
            'structure' : [],
            'charge' : 0,
            'multiplicity' : 1,

            # Basis set selector parameters
            'basis_set_selector' : '',
            'qc_method' : 'dft'
            'dft_method' : 'b3lyp'
            'integral' : '', # do we need this with nwchem
            'opt_threshold' : '', # optimization scf threshold
            'model_phase' : 'testing',
            'reference_type' : 'energy',
            'reference_value' : '', # Units need to line up with output
            'reference_value_method' : 'CCSD(T)',
            'selector_threshold' : ''
            }

        # Reading parameter file functions
        if self.input_file is not None:
            self.read_user_input()  # Overwrite any paramters defined by user

    def read_user_input(self):
        """
        Function to read input from user input .json file
        and overwrite any parameter defaults into the parameter
        dictionary.
        """
        try:
            with open(self.input_file) as json_input:
                try:
                    user_parameters = json.load(json_input)
                except ValueError:
                    err = 'Input .json file contains an error.'
                    raise ValueError(err)
        except IOError:
            err = 'The .json input file ({}) does not exist'.format(self.input_file)
            raise IOError(err)
        for key in user_parameters:
            if key in self.par:
                self.par[key] = user_parameter[key]
            else:
                err = '{} is not a valid parameter'
                print(err.format(key))

    def print_parameters(self):
        """
        Function that creates a string of all parameters.
        """
        parameters = ''
        for key in self.par:
            parameters += '{}\t{}\n'.format(key, self.par[key])

        return parameters
