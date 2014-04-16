"""
@author: Simon Streicher

"""


from ranking.gaincalc import weightcalc
import logging
logging.basicConfig(level=logging.INFO)

writeoutput = True

runs = ['epu5_compressor']

if 'weightcalc_tests' in runs:
    mode = 'test_cases'
    case = 'weightcalc_tests'
    weightcalc(mode, case, writeoutput)

if 'tennessee_eastman' in runs:
    mode = 'plants'
    case = 'tennessee_eastman'
    weightcalc(mode, case, writeoutput)

if 'epu5_compressor' in runs:
    mode = 'plants'
    case = 'epu5_compressor'
    weightcalc(mode, case, writeoutput)
