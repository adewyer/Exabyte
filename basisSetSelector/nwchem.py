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
            'molname' : self.molname,
            'title': self.jobSummary,
            'charge': self.charge,
            'geom': geom,
            'basis': basisSet,
            'functional': self.dft_method,
            'mult': self.mult,
            'thresh': self.optThreshold
        }

    def qc_single_point(self):
        # Create single point calculation for NWChem and run it.

        # TO DO - GET BASIS SET FOR CALC 
        bas = '3-21G'
        kwargs = self.get_nwchem_args(bas)
        job = kwargs['molname'] + '_' + bas

        #template file = ____
        #open template
        template = template.format(molecule=kwargs['molname'],
                                   calc_summary=kwargs['title'],
                                   charge=self.charge,
                                   geom='',  # need to fill in
                                   atom='*',
                                   basis=bas,
                                   functional=kwargs['functional'],
                                   mult=self.mult,
                                   optThresh=kwargs['thresh'])
        #write job input files
        #close file

        #submite file

    def nwchem_submit(self, job):
        #nwFile = 'nwchemSubmit.sub'
        #fi = open(nwFile, 'w')
        cmd = 'nwchem ' + job + '.inp' + ' >> ' + job + '.out'
        #fi.write('#!/bin/bash\n' + cmd)
        #fi.close()
        print(cmd)
        #command1 = 'chmod u+x ' + nwFile
        #command2 = './' + nwFile
        #process1 = subprocess.Popen(command1, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #process2 = subprocess.Popen(command2, shell=False, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        nwchemRun = os.popen(cmd)

def main():
    params = Parameters('test.json')
    nwChem = Nwchem(param=params)
    nwChem.nwchem_submit('test')

main()         
