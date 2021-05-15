# This script allows you to read, search or sort a big file (> 100 Mo).

import partools.utils.g as g
import partools.tools.bf as bf
from partools.quickstart import files_dir

# Input variables
# in_path = g.dirs['IN'] + "in.csv"
in_path = f'{files_dir}in.csv'
out_path = g.dirs['OUT'] + "out.csv"
look_for = "22173227102607"

bf.read_big_file(in_path)
# bf.search_big_file(in_path, out_path, look_for)
# bf.sort_big_file(in_path, out_path)
