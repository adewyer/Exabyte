"""
Author: Amanda Dewyer
Date: September 7, 2020

Class to create nwchem input file for basis set testing
"""

import os
import sys
import logging
import pkg_resources
import subprocess
import basis_sets as basis
import molecule as mol
from parameters import Parameters

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

    def write_nwchem_input(self):
        # Create single point calculation for NWChem and run it.

        # TO DO - GET BASIS SET FOR CALC 
        bas = '3-21G'
        kwargs = self.get_nwchem_args(bas)
        print(kwargs)
        name = kwargs.get('molname')
        print(name)
        job = name + '_' + bas

        # TO DO TURN GEOM INTO A STRING
        geometry = mol.reshape_geom(self, self.structure)

        #with open(pkg_resources.resource_filename('templates', 'nwchem_energy.tpl')) as inpFile:
        with open('nwchem_energy.tpl', 'r') as inpFile:
           self.inpFile = inpFile.read()

        nwChem_input = self.inpFile.format(molname=name,
                                           description=kwargs.get('title'),
                                           charge=self.charge,
                                           structure=geometry,
                                           basis=bas,
                                           functional=kwargs.get('functional'),
                                           mult=self.mult,
                                           method='dft')

        with open(job + '.inp', 'w') as inp:
            inp.write(nwChem_input)
        logging.info("NWChem input file created for {}.".format(job))

        self.nwchem_submit(job)

        return 0


    def nwchem_submit(self, job):
        # submite nwchem calculation to local machine
        cmd = 'nwchem ' + job + '.inp' + ' >> ' + job + '.out'
        nwchemRun = os.popen(cmd)

def main():
    params = Parameters('test.json')
    nwChem = Nwchem(param=params)
    nwChem.write_nwchem_input()
main()         
