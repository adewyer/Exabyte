"""
Author: Amanda Dewyer
Date: Sept 9 2020

Data analysis functions to compare basis set value 
to reference value supplied by user.
"""

import logging

def check_property(molecule, prop, threshold, property_dict, ref):
    """
    function to return whether or not a calculated roperty value falls
    within the threshold for a given reference value.
    """

    acceptableBasisSets = {}  # basis set, calculated ratio of calculated value:reference value
    fi = open('test_outcome.log', 'w')
    fi.write("{} reference value for {} = {}\n".format(prop, molecule, ref))

    # key = calcName, value = energy
    for key, value in property_dict.items():
        if value == 0:
            logging.info("calculation for {} failed.".format(key))
        else:
            # Calculate what the lowest percentage the calculated value can be of the reference
            threshold = 1 - threshold
            propertyRatio = calc_property_ratio(float(value), ref)

            fi.write("{} {} = {}, ratio = {}\n".format(key, prop, value, propertyRatio))
            if abs(propertyRatio) > float(threshold):
                logging.info("{} basis set energy of {} falls within tolerance level of reference ({}).".format(key, value, ref))
                acceptableBasisSets[key] = propertyRatio
            else:
                logging.info("{} basis set energy of {} is not within tolerance threshold level of reference.".format(key, value))
        print_acceptable_basis(acceptableBasisSets, molecule, threshold)
    fi.close()
    return acceptableBasisSets

def print_acceptable_basis(basis, molecule, threshold):
    fi = open('acceptableBasisSets.log', 'w')
    fi.write("Basis sets that fall within {} of the reference for {}:".format(threshold, molecule))
    for key, value in basis.items():
        fi.write("{}\n".format(key))
    fi.close()
    return 0

def calc_property_ratio(calc, ref):
    # Function that will calculate the ratio between the calcualted property value and reference

    calc_ratio = calc / ref
    
    return calc_ratio
