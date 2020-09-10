# Exabyte
ReWoTe Test for Exabyte.io

The Exabyte repository contains code developed for a real world test for application within exabyte.io software. 
The first program being implemented is an automated basis set selector for use with quantum chemical simulations.

To install and run the code run the following commands

```
python setup.py build
python setup.py install
```

If you lack administrative rights use this install command instead:
```
python setup.py install --user
```

The code will be installed into your python package bin. You can move it to your local bin.
The keyword to run basis set selector is:
```
bss input.json
```

The input.json file contains all parameters to run the code.
Keywords for the input.json file are as follows:
```
'molecule_name': ''  # name of molecule for simulation
'job_summary': ''  # description of job
'structure': [],  # list of XYZ coordinates for molecule
'charge': 0,  # charge of molecule
'multiplicity': 1,  # multiplicity of molecule
'basis_set_selector', : 'Specific',  # This is the only option currently available
'qc_method' : 'dft',  # method for computational simulation. Current demo is coded for DFT calculations
'opt_threshold' : '', # optimization scf threshold. Left at default for nwchem currently
'model_phase' : 'testing',  # Model phase will be used with heuristics methods not yet available
'reference_type' : 'energy',  # Property used to determine appropriate basis set for usage.
'reference_value' : '',  # Reference value for comparison to basis set calculations, units need to match output from nwchem (i.e. hartrees for energy)
'reference_value_method' : 'CCSD(T)',  # Method used to obtain reference value
'selector_threshold' : ''  # Threshold for testing whether a basis set produces an accurate enough property value. Type = float, i.e. 5.0 = 5% tolerance
```
