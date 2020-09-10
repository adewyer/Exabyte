"""
Author: Amanda Dewyer
Date: September 9th 2020

This file pulls all basis sets listed in the nwchem library and adds them to a list
"""

import os
def get_all_nwchem_basis():
    basis = os.listdir('/usr/local/Cellar/nwchem/7.0.0_2/share/nwchem/libraries/')
    return basis

