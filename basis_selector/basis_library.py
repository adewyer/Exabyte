"""
Author: Amanda Dewyer
Date: September 9th 2020

This file puts together a list of all basis sets 
in a quantum chemistry package library.

Currently only works for NWChem, other quantum chem
packages can be added through similar functions.

"""

import os
import pkg_resources

def get_nwchem_basis_library():
    # Function returns list of all available nwchem basis sets

    basisList = pkg_resources.resource_listdir(__name__, 'nwchem_basis')

    return basisList


