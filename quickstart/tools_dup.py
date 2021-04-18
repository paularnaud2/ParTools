# This script allows you to shuffle, sort as well as find and/or remove
# duplicates in a csv file or a list.
import pytools.common.g as g
from pytools.tools import dup

# Input variables
in_path = g.dirs['IN'] + "in.csv"
in_path = "pytools/test/sql/files/in.csv"
out_path = g.dirs['OUT'] + "out_dup.csv"

dup.find_dup(in_path, out_path, True)
# dup.del_dup(in_path, out_path, True)
# dup.shuffle_csv(in_path, out_path, True)
