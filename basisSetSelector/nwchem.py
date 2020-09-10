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
import basisSetSelector
from basisSetSelector import basis_sets as basis
from basisSetSelector import molecule as mol
from basisSetSelector.parameters import Parameters

class Nwchem:
    """
    Class allows for the basis set selector code to connect
    to NWChem so that quantum chemistry calculations for 
    testing basis sets can be done.
    """

    def __init__(self, param):
        self.param = param
        self.molname = param.par['molecule_name']
        self.jobSummary = param.par['job_summary']
        self.charge = param.par['charge']
        self.mult = param.par['multiplicity']
        self.qc_method = param.par['qc_method']
        self.dft = param.par['dft_method']
        self.grid = param.par['integral']
        self.optThreshold = param.par['opt_threshold']
        self.refType = param.par['reference_type']
        self.refVal = param.par['reference_value']
        self.basisThreshold = param.par['selector_threshold']
        self.structure = param.par['structure']

    def get_nwchem_args(self, basisSet):
        #parse structure into geom

        kwargs = {
            'molname': self.molname,
            'title': self.jobSummary,
            'charge': self.charge,
            'basis': basisSet,
            'functional': self.dft,
            'mult': self.mult,
            'thresh': self.optThreshold
        }
       
        return kwargs

    def write_nwchem_input(self, basis):
        # Create single point calculation for NWChem and run it.

        # bas = '3-21G'
        bas = basis
        kwargs = self.get_nwchem_args(bas)
        name = kwargs.get('molname')
        self.structure = self.structure
        job = name + '_' + bas

        geometry = mol.reshape_geom(self, self.structure)
        formattedGeom = []
        sep = '\t'
        for line in geometry:
           newLine = sep.join(line)
           formattedGeom.append(newLine)
        sep2 = '\n '
        formattedGeom = sep2.join(formattedGeom)

        inpFile = os.path.join(basisSetSelector.__path__[0], 'templates', 'nwchem_energy.tpl')
        with open(inpFile, 'r') as f:
            self.inpFile = f.read()   
        #with open(pkg_resources.resource_filename('templates', 'nwchem_energy.tpl')) as inpFile:
        #with open('./templates/nwchem_energy.tpl', 'r') as inpFile:
        #   self.inpFile = inpFile.read()

        nwChem_input = self.inpFile.format(molname=job,
                                           description=kwargs.get('title'),
                                           charge=self.charge,
                                           structure=formattedGeom,
                                           basis=bas,
                                           functional=kwargs.get('functional'),
                                           mult=self.mult,
                                           method='dft')

        with open('./singlePoints/' + job + '.inp', 'w') as inp:
        #with open(job + '.inp', 'w') as inp:
            inp.write(nwChem_input)
        logging.info("NWChem input file created for {}.".format(job))

        return job


    def nwchem_submit(self, job):
        # submit nwchem calculation to local machine
        # cmd = 'nwchem ./singlePoints/' + job + '.inp' + ' >> ./singlePoints/' + job + '.out'
        os.chdir('./singlePoints')
        cmd = 'nwchem ' + job + '.inp' + ' >> ' + job + '.out 2>' + job + '.err'
        nwchemRun = os.popen(cmd)
        os.chdir('../')

    def check_nwchem(self, job):
        status = 0
        os.chdir('./singlePoints')
        with open(job + '.out', 'r') as fi:
            line = fi.read().splitlines()
            sep=''
            finalLine = sep.join(line[-1])
            if 'Total times' in finalLine:
                status = 1  # calc done
            elif "For further details see manual section:" in finalLine:
                status = 1
                logging.info("Calculation failed for {}.".format(job))
        os.chdir('../')
        return status

    def get_nwchem_energy(self, job):
        # energy in hartrees 

        #keywords = ['Total', 'DFT', 'energy']
        keywords = 'Total DFT energy'
        os.chdir('./singlePoints')
        print(os.getcwd())
        with open(job + '.out', 'r') as fi:
            lines = fi.read().splitlines()
            if "For further details see manual section:" in lines[-1]:
                energy = 0
            else:
                for line in lines:
                    if keywords in line:
                        energy = line[34::]
            os.chdir('../')
        return energy
        
#def main():
#    params = Parameters('test.json')
#    nwChem = Nwchem(param=params)
#    nwChem.write_nwchem_input('3-21G')
#    nwChem.check_nwchem('test_3-21G')
#    nwChem.get_nwchem_energy('test_3-21G')
#main()        
