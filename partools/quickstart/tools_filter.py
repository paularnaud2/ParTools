# This script allows you to filter and/or extract columns from a csv file.

import partools.tools as to
import partools.utils.g as g
import partools.quickstart as qs

# Input variables
# in_path = g.dirs['IN'] + "in.csv"
in_path = f'{qs.files_dir}in.csv'
out_path = g.dirs['OUT'] + "out_filtered.csv"
col_list = ['PRM', 'AFFAIRE']


def filter_function(line_list):
    # Lines for which this function returns True will be written in the output
    # file. If no filter function is given in input (ie. gl.FF is not defined),
    # no filter will be applied.
    cond = line_list[to.gl.fields['PRM']].find('01') == 0

    return cond


# This will extract the columns contained in col_list ('PRM' and 'AFFAIRE') and
# keep only the rows starting with '01' (see filter function)
to.flt(in_path, out_path, COL_LIST=col_list, FF=filter_function)
