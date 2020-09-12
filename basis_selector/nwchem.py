"""
Author: Amanda Dewyer
Date: September 7, 2020

Class to create nwchem input file for basis set testing
"""

import re
import os
import sys
import logging
import subprocess
import pkg_resources
import basis_selector
from basis_selector import basis_sets as basis
from basis_selector import molecule as mol
from basis_selector.parameters import Parameters

class Nwchem:
    """
    Class  creates an NWChem object.
    NWChem objects are used to:
    1. Create NWChem input files
    2. Run NWChem calculations from input files
    3. Check the status of NWChem calculations (Running or Finished)
    4. Pull data about properties from NWChem output files
    """

    def __init__(self, param):
        self.param = param
        self.molname = param.par['molecule_name']
        self.jobDescription = param.par['job_description']
        self.charge = param.par['charge']
        self.mult = param.par['multiplicity']
        self.qcMethod = param.par['qc_method']  # Default set to DFT
        self.dft = param.par['dft_method']  # Default set to B3LYP
        self.optThreshold = param.par['opt_threshold']
        self.refType = param.par['reference_type']
        self.refVal = param.par['reference_value']
        self.propertyThreshold = param.par['property_threshold']
        self.structure = param.par['structure']

    def get_nwchem_args(self, basisSet):
        # Function to grab keyword arguments for NWChem input

        kwargs = {
            'molname': self.molname,
            'title': self.jobDescription,
            'charge': self.charge,
            'basis': basisSet,
            'functional': self.dft,
            'mult': self.mult,
            'thresh': self.optThreshold
        }
       
        return kwargs

    def write_nwchem_input(self, basis):
        """
        Creation of a single point calculation input file for NWChem.
        Input files with varying basis sets are created for the same molecule
        as defined by within the 'self' parameter.
        """

        # molecule object created based on the 'self' parameter
        molecule = mol.Molecule(self.charge, self.mult, self.structure)

        kwargs = self.get_nwchem_args(basis)
        molName = kwargs.get('molname')
        calcName = molName + '_' + basis  # Filename for NWChem input

        """
        Formatting of geometry for NWChem input so that
        each atom label and corresponding XYZ coordinates 
        on an individual line within the NWChem input file.
        """ 
        geometry = molecule.reshape_geom(self.structure)
        formattedGeom = []
        sep = '\t'
        for line in geometry:
           newLine = sep.join(line)
           formattedGeom.append(newLine)
        sep2 = '\n '
        formattedGeom = sep2.join(formattedGeom)

        # Use of NWChem template file to create NWChem input files 
        nwChemInpFi = pkg_resources.resource_filename(__name__, 'templates/nwchem_energy.tpl')
        with open(nwChemInpFi, 'r') as f:
            self.nwChemInpFi = f.read()   

        nwChemInput = self.nwChemInpFi.format(molname=calcName,
                                        description=kwargs.get('title'),
                                        charge=self.charge,
                                        structure=formattedGeom,
                                        basis=basis,
                                        functional=kwargs.get('functional'),
                                        mult=self.mult,
                                        method=self.qcMethod)

        # Creation of input files inside of the singlePoints dir.
        # SinglePoints Dir is where all single point calculations are stored
        with open('./singlePoints/' + calcName + '.inp', 'w') as nwChemFile:
            nwChemFile.write(nwChemInput)
        logging.info("NWChem input file created for {}.".format(calcName))

        return calcName


    def nwchem_submit(self, calcName):
        # Function that submits NWChem calculations to the computer for completion

        os.chdir('./singlePoints')
        cmd = 'nwchem ' + calcName + '.inp' + ' >> ' + calcName + '.out 2>' + calcName + '.err'
        nwchemRun = os.popen(cmd)
        os.chdir('../')

        return None

    def check_nwchem(self, calcName):
        """
        Function to check whether an NWChem calculation is running or not.
        Calculation status is checked by looking at the output on the
        final line of the output file.

        0 = running, 1 = done
        """

        status = 0
        os.chdir('./singlePoints')
        with open(calcName + '.out', 'r') as fi:
            line = fi.read().splitlines()
            sep=''
            finalLine = sep.join(line[-1])
            if 'Total times' in finalLine:
                status = 1  # calc done, finished successfully
            elif "For further details see manual section:" in finalLine:
                status = -1 # calc done, failed
                logging.info("Calculation failed for {}.".format(calcName))
        os.chdir('../')

        return status

    def get_nwchem_energy(self, calcName):
        # Function grabs and returns the energy from an NWChem output file. 

        energyKeywords = 'Total DFT energy'
        os.chdir('./singlePoints')
        with open(calcName + '.out', 'r') as fi:
            lines = fi.read().splitlines()
            if "For further details see manual section:" in lines[-1]:
                energy = 0  # Set energy to 0 if calculation failed
            else:
                for line in lines:
                    if energyKeywords in line:
                        energy = line[34::]  # Location of energy in file
            os.chdir('../')

        return energy
