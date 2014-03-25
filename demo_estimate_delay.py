# -*- coding: utf-8 -*-
"""Reports the maximum partial correlation as well as associated delay
obtained by shifting the affected variable behind the causal variable a
specified set of delays.

Also reports whether the sign changed compared to no delay.

Created on Thu Mar 13 09:44:16 2014

@author: Simon
"""

from demo_setup import runsetup
from ranking.gaincalc import create_connectionmatrix
from ranking.gaincalc import estimate_delay

from sklearn import preprocessing

import csv
import numpy as np
import os
import logging
import h5py
import jpype

logging.basicConfig(level=logging.INFO)


def writecsv(filename, items, header):
    with open(filename, 'wb') as f:
        csv.writer(f).writerow(header)
        csv.writer(f).writerows(items)

cases, saveloc, caseconfig, plantdir, sampling_rate, infodynamicsloc = \
    runsetup()

# Specify delay type either as 'datapoints' or 'timevalues'
delaytype = 'datapoints'
delays = []

# Specify method either as 'partial_correlation' or 'transfer_entropy'
# Store this in the case configuration file
method = 'transfer_entropy'
#method = 'partial_correlation'
logging.info("Method: " + method)

if delaytype == 'datapoints':
# Include first n sampling intervals
    delays = range(10)
elif delaytype == 'timevalues':
# Include first n 10-second shifts
    delays = [val * (10.0/3600.0) for val in range(1000)]

# Value chosen for demonstration purposes only
size = 400

if method == 'transfer_entropy':
    # Change location of jar to match yours:
    jarLocation = infodynamicsloc
    # Start the JVM
    # (add the "-Xmx" option with say 1024M if you get crashes
    # due to not enough memory space)
    jpype.startJVM(jpype.getDefaultJVMPath(), "-ea",
                   "-Djava.class.path=" + jarLocation)

# Only do a single case in the demo for coverage analysis purposes
for case in cases:
    logging.info("Running case {}".format(case))
    # Get connection (adjacency) matrix
    connectionloc = os.path.join(plantdir, 'connections',
                                 caseconfig[case]['connections'])
    # Get time series data
    tags_tsdata = os.path.join(plantdir, 'data', caseconfig[case]['data'])
    # Get dataset name
    dataset = caseconfig[case]['dataset']
    inputdata = np.array(h5py.File(tags_tsdata, 'r')[dataset])
    # Normalise (mean centre and variance scale) the input data
    inputdata_norm = preprocessing.scale(inputdata)

    # Get the variables and connection matrix
    [variables, connectionmatrix] = create_connectionmatrix(connectionloc)

    [weight_array, delay_array, datastore, data_header] = \
        estimate_delay(variables, connectionmatrix, inputdata_norm,
                       dataset, sampling_rate, delays,
                       size, delaytype, method, infodynamicsloc)

    # Define export directories and filenames
    datasavename = \
        os.path.join(saveloc, 'estimate_delay',
                     '{}_{}_estimate_delay_data.csv'.format(case, method))
    value_array_savename = \
        os.path.join(saveloc, 'estimate_delay',
                     '{}_{}_maxweight_array.csv'.format(case, method))
    delay_array_savename = \
        os.path.join(saveloc, 'estimate_delay',
                     '{}_{}_delay_array.csv'.format(case, method))

    # Write arrays to file
    np.savetxt(value_array_savename, weight_array, delimiter=',')
    np.savetxt(delay_array_savename, delay_array, delimiter=',')

    # Write datastore to file
    writecsv(datasavename, datastore, data_header)