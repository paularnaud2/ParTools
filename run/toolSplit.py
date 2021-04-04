# This script allows you to split a file into multiple files (e.g. if it is too
# big to be opened with an app such as Excel)
import pytools.common.g as g
from pytools.tools import split

# Input variables default values
in_dir = g.paths['IN'] + "in.csv"
in_dir = "pytools/test/sql/files/in.csv"
out_dir = g.paths['OUT']

split.split_file(in_dir, out_dir)
