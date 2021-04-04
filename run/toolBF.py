# This script allows you to read or search a big file (> 100 Mo)
import pytools.common.g as g
import pytools.tools.bf as bf

# Input variables
in_dir = g.paths['IN'] + "in.csv"
in_dir = "pytools/test/sql/files/in.csv"
out_dir = g.paths['OUT'] + "out.csv"
look_for = "22173227102607"

# bf.read_big_file(in_dir)
# bf.search_big_file(in_dir, out_dir, look_for)
bf.sort_big_file(in_dir, out_dir)
