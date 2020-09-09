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
import numpy as np

class Molecule():
    """
    Class contains properties of molecule input by user.
    """

    def __init__(self, charge, mult, structure):
        self.charge = charge
        self.mult = mult
        self.structure = structure

    def get_atoms(self):
        self.natoms = len(self.structure) // 4
        self.atoms = self.structure[0:len(self.structure):4]
        return self.natoms, self.atoms
    
    def get_coords(self):
        structure = self.reshape_geom()
        self.coords = structure[:, 1:4].astype(float)
        return self.coords

    def get_charge(self):
        return self.charge

    def get_mult(self):
        return self.mult

    def mol_type(atoms):
        charge = self.get_charge()
        mult = self.get_mult()

def reshape_geom(self, structure):
    natoms = len(structure) // 4
    self.structure = np.reshape(self.structure, (natoms, 4))
    return self.structure

"""
def main():
    print("mol test")
    structure = ["O", 0.00000000, 0.00000000, 0.00000000, "H", 0.00000000, 1.43042809, -1.10715266, "H", 0.00000000, -1.43042809, -1.10715266] 
    mol = Molecule(0, 1, structure)
    print(mol.structure)
    print(mol.get_atoms())
    print(mol.get_coords())
    print(mol.get_charge())
    print(mol.get_mult())
    print(mol.structure)
main()
"""        
