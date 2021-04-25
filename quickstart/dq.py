# dq (data quality) allows you to compare two big csv files (> 100 Mo).
# A detailed result of the comparison is ouput.
#
# In order for the run_dq function to work correctly, the input files must both
# have a pivot column (ie. containing keys/IDs) and be free of 'key dupplicates'
# meaning having different lines with same ID. The index of the pivot column
# can be set in the gl file (default value: 1 -> first column).
#
# In this script, two files used for testing purpose are compared.
# Result interpretation:
# COMPARE_RES = in_11: the key is present in the file in_11 and not in the file in_12
# COMPARE_RES = in_12: the key is present in the file in_12 and not in the file in_11
# COMPARE_RES = in_11|in_12: the key is present in both files but lines differ.
# In the last case, the differences are outlined by writing the first and second
# files' values separated by '|' for each field that differs. For example 'O|N'
# in the field 'ETAT' means that the first file (in_11) has a 'O' and the second
# file (in_12) has a 'N'.
#
# For more information, see the README.md file.

import pytools.dq as dq
from pytools.common import init_log
from pytools.test import gl

init_log('run_dq')

dq.run_dq(
    IN_DIR=gl.TEST_DQ,
    IN_FILE_NAME_1="in_11",
    IN_FILE_NAME_2="in_12",
)
