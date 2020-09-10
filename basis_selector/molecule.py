"""
Author: Amanda Dewyer
Date: September 7th 2020

Class for the defining a molecule object, and
being able to grab molecule features.

Molecule objects contain:
- XYZ geometry
- Atom list
- Charge
- Multiplicity

"""

import sys
import os
import logging
import numpy as np

class Molecule():
    """
    Class contains properties of molecule and 
    functions capable of returning specific features
    of a molecule object.

    Molecule objects require
    1. structure
    2. charge
    3. multiplicity
    """

    def __init__(self, charge, mult, xyz_structure):
        self.charge = charge
        self.mult = mult
        self.xyz_structure = xyz_structure

    def get_atoms(self):
        """
        Function grabs the number of atoms in a molecules, and the
        element symbol for each atom in order.

        Ex: Water molecule input structure = ["O", 0.60161, 1.68925, -0.00684,
                                              "H", 1.56949, 1.64563, 0.00906,
                                              "H", 0.32276, 0.81732, 0.31087]

        Returns 3 (natoms), ["O", "H", "H"] (atoms)
        """

        self.natoms = len(self.xyz_structure) // 4
        self.atoms = self.xyz_structure[0:len(self.xyz_structure):4]

        return self.natoms, self.atoms
    
    def get_coords(self):
        """
        Function grabs only the xyz coordinates from the molecule, ommiting the
        atoms element label.
        """

        formattedXYZ = reshape_geom(self, self.xyz_structure)
        self.coords = formattedXYZ[:, 1:4].astype(float)

        return self.coords

    def get_charge(self):
        # function returns molecules charge
        return self.charge

    def get_mult(self):
        # function returns molecules multiplicity
        return self.mult

    def reshape_geom(self, structure):
        """
        Reformats geometry from a list of coordinates into a natoms x 4 array
        column 1 = atom label (C, O, H, etc.)
        columns 2-4 = X, Y, Z coordinates for each atom

        Ex:

        input structure = ["O", 0.60161, 1.68925, -0.00684, "H", 1.56949, 1.64563, 0.00906, "H", 0.32276, 0.81732, 0.31087]

        Formatted structure = 
        "O", 0.60161, 1.68925, -0.00684,
        "H", 1.56949, 1.64563, 0.00906,
        "H", 0.32276, 0.81732, 0.31087

        """

        natoms = len(structure) // 4
        formattedStructure = np.reshape(structure, (natoms, 4))

        return formattedStructure
