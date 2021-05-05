# This script allows you to filter and/or extract columns from a csv file

import pytools.utils.g as g
import pytools.tools.filter as f
from pytools.tools import gl

# Input variables
# in_path = g.dirs['IN'] + "in.csv"
in_path = "pytools/test/sql/files/in.csv"
out_path = g.dirs['OUT'] + "out_filtered.csv"
col_list = ['PRM', 'AFFAIRE']


def filter_function(line_list):
    # Lines for which this function returns True will be written in the output
    # file .If not filter function is given in input (ie. gl.FF is not defined),
    # no filter will be applied.
    cond = line_list[gl.fields['PRM']].find('01') == 0

    return cond


# This will extract colums containded in col_list ('PRM' and 'AFFAIRE') and
# filter with the rows starting with '01' (see filter function)
f.filter(in_path, out_path, COL_LIST=col_list, FF=filter_function)
