"""
Author: Amanda Dewyer
Date: Sept 9 2020

Data analysis class to compare basis set value to
reference value supplied by user.
"""

import logging

def compare_property(threshold, property_dict, ref):
    """
    function to return whether or not a property value falls
    within the threshold for a given reference value
    """
    acceptableBasisSets = {}  # basis set, calculated tolerance
    for key, value in property_dict.items():
        if value == 0:
            logging.info("calculation for {} failed.".format(key))
        else:
            threshold = 1 - threshold
            calc_tol = float(value) / ref
            if calc_tol > ref:
                logging.info("{} basis set energy of {} falls within tolerance level of reference ({}).".format(key, value, ref))
                acceptableBasisSets[key] = calc_tol
            else:
                logging.info("{} basis set energy of {} not acceptable.".format(key, value))

    return acceptableBasisSets

def calc_kcalmol_diff(calc, ref):
    kcal = 627.6 * (calc - ref)
    print("difference (calc-ref) = {} kcal/mol".format(kcal))
    #testing
    calc_tol = calc/ref
    print("tolerance = {}".format(calc_tol))

"""
def main():
    e = [     -74.570860945438,
     -74.570860945438,
     -74.535156294619,
     -74.535156294619,
     -74.950699704907,
     -74.950699704907,
     -74.950460420773,
     -74.950460420773,
     -75.017261801213,
     -75.017261801213,
     -75.017156306580,
     -75.017156306580,
     -75.011341688037,
     -75.011341688037,
     -74.940081541759,
     -74.940081541759,
     -75.024187914629,
     -75.024187914629,
     -75.104285557349,
     -75.104285557349,
     -75.093479874347,
     -75.093479874347,
     -74.995389634402,
     -74.995389634402,
     -75.102919513263,
     -75.102919513263,
     -75.086068589520,
     -75.086068589520]
    ref = -76.06415778

    for en in e:
        calc_kcalmol_diff(en, ref)

main() 
"""    
