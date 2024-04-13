# Programmer: Connor Fricke
# File: validation.py
# Latest Revision: 13-APRIL-2024 --> Created
#
# Simple Python script for reading in two data files and comparing results
# using absolute error:
#   abserr = |estimate - exact|/exact
# In this case, we are comparing data from two .dat files, python_results.dat
# and limit_cycles.dat. Both files were generated using the same 4th order
# Runge-Kutta differential equation solving algorithm, only in different languages,
# Python and C++, respectively.

from pandas import read_csv
from math import fabs
import os


# *** GET PATHS, CHOOSE FILES, IMPORT TO DATAFRAMES ***
PROJ_DIR = os.getcwd()
DATA_PATH = PROJ_DIR + "/datafiles/"

colnames = ["t", "theta", "thetadot"]
pythonDF = read_csv(DATA_PATH+"python_results.dat", comment='#', sep=" ", names=colnames)
cppDF = read_csv(DATA_PATH+"limit_cycles.dat", comment='#', sep=' ', names=colnames)

# ***** FUNCTIONS *****
# simple function for calculating the absolute error between two values,
# where the second parameter (b) is considered the "exact" value for comparison
# and calculation of the relative error.
def absErr(a, b) -> float:
    return fabs((a - b) / b)

# IO function for calculating error for a particular row and column between dataframes
def displayError(rowNum, colName, df1, df2):
    err = absErr(df1[colName][rowNum], df2[colName][rowNum])
    print("{} error: ".format(colName) + str(err))

# ***** MAIN PROGRAM ******
checkRows = [1, 10, 50, 100, 200, 500, 1000, 1500, 2000]
for row in checkRows:
    print("Calculating error at row: " + str(row))
    print("t: " + str(pythonDF["t"][row]))
    # we consider the C++ data to be "exact" then print the relative error of the Python data.
    displayError(row, "theta", pythonDF, cppDF)
    displayError(row, "thetadot", pythonDF, cppDF)
    print("\n")
# ****** END *******