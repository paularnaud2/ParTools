# The dup package allows you to find and/or remove duplicates as well as sort
# and shuffle a csv file or a list. Just uncomment and run this script to try
# out!

import pytools.common.g as g
from pytools.tools import dup

# Working with files-------------------------------------------------
in_path = "pytools/test/sql/files/in.csv"
out_path = g.dirs['OUT'] + "out_dup.csv"

dup.find_dup(in_path, out_path, True)
# dup.del_dup(in_path, out_path, True)
# dup.shuffle_csv(in_path, out_path, True)

# Working with lists-------------------------------------------------
in_list = ['2', '1', '3', '2', '1']

print(dup.find_dup_list(in_list))
# print(dup.del_dup_list(in_list))
