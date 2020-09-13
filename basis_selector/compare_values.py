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
    function to return whether or not a calculated property value falls
    within the threshold for a given reference value.
    """

    acceptableBasisSets = {}  # basis set, calculated ratio of calculated value:reference value
    fi = open('test_outcome.log', 'w')
    fi.write("{} reference value for {} = {}\n".format(prop, molecule, ref))

    # key = calcName, value = energy
    threshold = 1 - threshold
    for key, value in propertyDict.items():
        value = float(value)
        if value == 0.:
            logging.info("calculation for {} failed.".format(key))
        else:
            # Calculate what the lowest percentage the calculated value can be of the reference
            propertyRatio = calc_property_ratio(float(value), ref)
            labelLength = len(molecule) + 1  # calculate the length of the molecule string for formatting output
            fi.write("{} {} = {:.4f}, ratio = {:.4f}\n".format(key[labelLength::], prop, float(value), float(propertyRatio)))
            print("{} = {}, {}".format(key[labelLength::], propertyRatio, threshold))
            if abs(propertyRatio) > float(threshold):
                logging.info("{} basis set energy of {:.4f} falls within tolerance level of reference ({:.4f}).".format(key[labelLength::], value, ref))
                acceptableBasisSets[key] = propertyRatio
            else:
                logging.info("{} basis set energy of {:.4f} is not within tolerance threshold level of reference.".format(key[labelLength::], value))
        leastAccurateBasis, mostAccurateBasis = print_acceptable_basis(acceptableBasisSets, molecule, threshold)
    fi.close()
    return acceptableBasisSets, leastAccurateBasis, mostAccurateBasis

def sort_basis(basisSets):
    # Function to sort basis sets from most to least accurate

    basisSorted = sorted(basisSets.items(), key=operator.itemgetter(1))

    return basisSorted

def print_acceptable_basis(basis, molecule, threshold):
    """
    Function that prints the least and most expensive basis sets
    that fit the threshold and reference criteria along with a list
    of all basis sets that fit the criteria.
    """

    basisSorted = sort_basis(basis)
   
    fi = open('acceptableBasisSets.log', 'w')
    labelLength = len(molecule)  # calculate the length of the molecule string for formatting output
    fi.write("Basis sets that fall within {:.4f} of the reference for {}:\n".format(threshold, molecule))

    if len(basisSorted) == 0:
        fi.write("None of the tested basis sets fit the threshold criteria")
        return 'No basis', 'No basis'

    basisKeys = [key[0] for key in basisSorted]

    labelLength = len(molecule) + 1
    fi.write("\n{} is the most accurate basis set tested, and most expensive to run\n".format(basisKeys[0][labelLength::]))
    fi.write("{} is the least accurate basis set tested, and least expensive to run.\n".format(basisKeys[-1][labelLength::]))
    fi.write("\nOther basis sets that meet threshold criteria are:\n")

    for key in basisKeys:
        fi.write("{}\n".format(key[labelLength::]))
    fi.close()

    return basisKeys[-1][labelLength::], basisKeys[0][labelLength::]

def calc_property_ratio(calc, ref):
    # Function that will calculate the ratio between the calcualted property value and reference

    calcRatio = calc / ref
    
    return calcRatio
