"""
Author: Amanda Dewyer
Date: September 9th 2020

This file puts together a list of all basis sets in the nwchem library.

Note: Future version of this code will need to be edited to grab library
from any computer. Current functionality is specific.
"""

import os

def get_all_nwchem_basis():
    basisList = os.listdir('/usr/local/Cellar/nwchem/7.0.0_2/share/nwchem/libraries/')
    return basisList

