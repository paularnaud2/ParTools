# This script allows you to filter and/or extract columns from a csv file
import pytools.common.g as g
import pytools.tools.filter as f
from pytools.tools import gl

# Input variables
in_dir = g.paths['IN'] + "in.csv"
in_dir = "pytools/test/sql/files/in.csv"
out_dir = g.paths['OUT'] + "out_filtered.csv"
col_list = ['PRM', 'AFFAIRE']


def filter_function(line_list):
    # Lines for which this function returns True will be written in the output file
    # If not filter function is given in input (ie. gl.FF is not defined),
    # no filter will be applied.
    cond = line_list[gl.fields['PRM']].find('01') == 0

    return cond


if __name__ == '__main__':
    f.filter(in_dir, out_dir, COL_LIST=col_list, FF=filter_function)
else:
    f.gl.OPEN_OUT_FILE = False
    f.filter(in_dir, out_dir, COL_LIST=col_list, FF=filter_function)
