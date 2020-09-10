"""
This file is used to installs basis_set_selector.
Type 
python setup.py build
python setup.py install
"""

from setuptools import setup, find_packages

setup(
    name = "basis_selector",
    version = "1.0",
    packages = find_packages(),
    package_data={'templates':[
        'nwchem_energy.tpl']},
    include_package_data=True,
    entry_points={'console_scripts':[
        'bss = basis_selector.bss:main',
        ]},
    install_requires=['numpy'],
    
    author="Amanda Dewyer",
    author_email = "adewyer@umich.edu",
    description = "Automatic basis set screening, analysis and selection for quantum chemical calculations.",
    license = "",
    url = "https://github.com/adewyer/Exabyte",
)
