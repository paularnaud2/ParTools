"""
The dup script allows you to find and/or remove duplicates as well as sort and
shuffle a csv file or a list.
"""

import partools.utils.g as g
from partools.tools import dup
from partools.quickstart import files_dir

# Working with files-------------------------------------------------
# in_path = g.dirs['IN'] + "in.csv"
in_path = f'{files_dir}in.csv'
out_path = g.dirs['OUT'] + "out_dup.csv"

dup.find_dup(in_path, out_path, True)
# dup.del_dup(in_path, out_path, True)
# dup.shuffle_file(in_path, out_path, True)

# Working with lists-------------------------------------------------
in_list = ['2', '1', '3', '2', '1']

print(dup.find_dup_list(in_list))
print(dup.del_dup_list(in_list))
