# This script allows you to filter and/or extract columns from a csv file.

import partools.utils.g as g
import partools.tools.filter as f
from partools.tools import gl
from partools.quickstart import files_dir

# Input variables
# in_path = g.dirs['IN'] + "in.csv"
in_path = f'{files_dir}in.csv'
out_path = g.dirs['OUT'] + "out_filtered.csv"
col_list = ['PRM', 'AFFAIRE']


def filter_function(line_list):
    # Lines for which this function returns True will be written in the output
    # file. If no filter function is given in input (ie. gl.FF is not defined),
    # no filter will be applied.
    cond = line_list[gl.fields['PRM']].find('01') == 0

    return cond


# This will extract the columns contained in col_list ('PRM' and 'AFFAIRE') and
# keep only the rows starting with '01' (see filter function)
f.filter(in_path, out_path, COL_LIST=col_list, FF=filter_function)
