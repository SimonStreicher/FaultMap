"""
Created on Thu Feb 06 10:50:28 2014

@author: Simon Streicher
"""

#from numpy import loadtxt, vstack
#import numpy as np
from autoregres_gen import autogen
from transfer_entropy import vectorselection, te_calc


def getdata(samples, delay):
    """Get dataset for testing.

    Select to generate each run or import an existing dataset.

    """

    # Generate autoregressive delayed data vectors internally
    data = autogen(samples, delay)

    # Alternatively, import data from file
#    autoregx = loadtxt('autoregx_data.csv')
#    autoregy = loadtxt('autoregy_data.csv')

    return data


def calculate_te(delay, timelag, samples, sub_samples, ampbins, k=1, l=1):
    """Calculates the transfer entropy for a specific timelag (equal to
    prediction horison) for a set of autoregressive data.

    sub_samples is the amount of samples in the dataset used to calculate the
    transfer entropy between two vectors (taken from the end of the dataset).
    sub_samples <= samples

    Currently only supports k = 1; l = 1;

    You can search through a set of timelags in an attempt to identify the
    original delay.
    The transfer entropy should have a maximum value when timelag = delay
    used to generate the autoregressive dataset.

    """
    # Get autoregressive datasets
    data = getdata(samples, delay)

    [x_pred, x_hist, y_hist] = vectorselection(data, timelag,
                                               sub_samples, k, l)

    transentropy = te_calc(x_pred, x_hist, y_hist, ampbins)

    return transentropy

# Test code

# FIXME: Find out why only certain combinations of samples, sub_sampels work
# FIXME: The numbers are not the right order of magnitude, typical 0.01 - 0.10

# Delay = 5, Timelag = 4
transentropy1 = calculate_te(5, 4, 1000, 400, 10)
# Delay = 5, Timelag = 5
transentropy2 = calculate_te(5, 5, 1000, 400, 10)
# Delay = 5, Timelag = 6
transentropy3 = calculate_te(5, 6, 1000, 400, 10)