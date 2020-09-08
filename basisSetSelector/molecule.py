"""
Author: Amanda Dewyer
Date: September 7th 2020

Class for the defining a molecule object.
Molecule objects contain:
- XYZ geometry
- Atom list
- Charge
- Multiplicity

Information is used to gauge which basis sets
are appropriate for use with both the general
and specific basis set selector options.
"""

import sys
import os
import logging

class Molecule():
    """
    Class contains properties of molecule input by user.
    """

    def __init__(self, charge, mult, structure)
        self.charge = charge
        self.mult = mult
        self.structure = structure

    def get_atoms(self):
        #strip structure to get only atoms

    def get_coords(self):
        #strip structure to get only xyz cordinates

    def get_charge(self):
        return self.charge

    def get_mult(self):
        return self.mult

    def mol_type(atoms):
        charge = self.get_charge()
        mult = self.get_mult()

def main():
   mol = Molecule(0, 1, )
   

main()        
