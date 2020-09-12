"""
Author: Amanda Dewyer
Date: Sept 9 2020

Data analysis functions to compare basis set value 
to reference value supplied by user.
"""

import operator
import logging

def check_property(molecule, prop, threshold, propertyDict, ref):
    """
    function to return whether or not a calculated roperty value falls
    within the threshold for a given reference value.
    """

    acceptableBasisSets = {}  # basis set, calculated ratio of calculated value:reference value
    fi = open('test_outcome.log', 'w')
    fi.write("{} reference value for {} = {}\n".format(prop, molecule, ref))

    # key = calcName, value = energy
    for key, value in propertyDict.items():
        value = float(value)
        if value == 0.:
            logging.info("calculation for {} failed.".format(key))
        else:
            # Calculate what the lowest percentage the calculated value can be of the reference
            threshold = 1 - threshold
            propertyRatio = calc_property_ratio(float(value), ref)

            fi.write("{} {} = {:.4f}, ratio = {:.4f}\n".format(key, prop, float(value), float(propertyRatio)))
            if abs(propertyRatio) > float(threshold):
                logging.info("{} basis set energy of {:.4f} falls within tolerance level of reference ({:.4f}).".format(key[4::], value, ref))
                acceptableBasisSets[key] = propertyRatio
            else:
                logging.info("{} basis set energy of {:.4f} is not within tolerance threshold level of reference.".format(key[4::], value))
        leastAccurateBasis, mostAccurateBasis = print_acceptable_basis(acceptableBasisSets, molecule, threshold)
    fi.close()
    return acceptableBasisSets, leastAccurateBasis, mostAccurateBasis

def sort_basis(basisSets):
    # Function to sort basis sets from most to least accurate

    basisSorted = sorted(basisSets.items(), key=operator.itemgetter(1))

    return basisSorted

def print_acceptable_basis(basis, molecule, threshold):
    """
    Function that does 2 things:
    2. Prints the most accurate, and least accurate basis set options. 
       Least accurate is likely the cheapest method.
    3. Prints all other basis sets that are considered acceptable 
       based on reference and threshold.
    """

    basisSorted = sort_basis(basis)
   
    fi = open('acceptableBasisSets.log', 'w')
    fi.write("Basis sets that fall within {:.4f} of the reference for {}:\n".format(threshold, molecule))

    if len(basisSorted) == 0:
        fi.write("None of the tested basis sets fit the threshold criteria")
        return 'No basis', 'No basis'

    basisKeys = [key[0] for key in basisSorted]
    fi.write("\n{} is the most accurate basis set tested, and most expensive to run\n".format(basisKeys[0][4::]))
    fi.write("{} is the least accurate basis set tested, and least expensive to run.\n".format(basisKeys[-1][4::]))
    fi.write("\nOther basis sets that meet threshold criteria are:")
    for key in basisKeys:
        fi.write("{}\n".format(key))
    fi.close()
    return basisKeys[-1][4::], basisKeys[0][4::]

def calc_property_ratio(calc, ref):
    # Function that will calculate the ratio between the calcualted property value and reference

    calcRatio = calc / ref
    
    return calcRatio
