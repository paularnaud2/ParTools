# This script allows you to read, search or sort a big file (> 100 Mo)

import pytools.common.g as g
import pytools.tools.bf as bf

# Input variables
# in_path = g.dirs['IN'] + "in.csv"
in_path = "pytools/test/sql/files/in.csv"
out_path = g.dirs['OUT'] + "out.csv"
look_for = "22173227102607"

bf.read_big_file(in_path)
# bf.search_big_file(in_path, out_path, look_for)
# bf.sort_big_file(in_path, out_path)
