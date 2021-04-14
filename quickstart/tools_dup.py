# This script allows you to shuffle, sort as well as find and/or remove
# duplicates in a csv file or a list.
import pytools.common.g as g
from pytools.tools import dup

# Input variables
in_dir = g.paths['IN'] + "in.csv"
in_dir = "pytools/test/sql/files/in.csv"
out_dir = g.paths['OUT'] + "out_dup.csv"

if __name__ == '__main__':
    dup.find_dup(in_dir, out_dir, True)
    # dup.del_dup(in_dir, out_dir, True)
    # dup.shuffle_csv(in_dir, out_dir, True)
else:
    dup.find_dup(in_dir, out_dir, False)
    dup.del_dup(in_dir, out_dir, False)
    dup.shuffle_csv(in_dir, out_dir, False)
