from time import time

import partools.utils as u
from partools.tools import del_dup_list

from . import gl
from . import functions as f


def run_dq(**kwargs):
    """Compares two big csv files (> 100 Mo) and outputs a detailed result 
    of the comparison is output

    See partools/quickstart/dq.py for guidance
    """
    from .init import init_dq
    from .sort import sort_big_file

    start_time = time()
    init_dq(kwargs)
    u.check_header(gl.paths["in1"])
    u.check_header(gl.paths["in2"])
    f.compare_headers(gl.paths["in1"], gl.paths["in2"])
    sort_big_file(gl.paths["in1"], gl.paths["out1"], True, 1)
    sort_big_file(gl.paths["in2"], gl.paths["out2"], True, 2)
    args = [gl.paths["out1"], gl.paths["out2"], gl.paths["out"]]
    if not f.compare_files(*args):
        u.log_print('|')
        f.check_split(gl.paths["out"])
    f.finish_dq(start_time)


def file_match(in1, in2, del_dup=False, err=True, out_path=''):
    """Compares two files and outputs the diff if the files don't match.
    Note that the files are sorted before comparison.
    (more generic than run_dq but doesn't work for big files)

    - del_dup: if true, duplicates are deleted before comparison
    - err: if True, an exception is raised when the files don't match
    - out_path: specifies an output path for file comparison different from default
    """

    u.log("[dq] file_match: start")

    if not out_path:
        out_path = u.g.dirs['OUT'] + 'file_match_out.csv'

    s = f"Comparing files '{in1}' and '{in2}'..."
    u.log(s)
    l1, l2 = u.load_txt(in1), u.load_txt(in2)
    l1.sort(), l2.sort()
    if del_dup:
        l1, l2 = del_dup_list(l1), del_dup_list(l2)

    res = l1 == l2
    s = "Files match" if res else "Files don't match"
    u.log(s)

    if not res:
        f.diff_list(l1, l2, out_path)
        if err:
            u.startfile(out_path)
            assert res is True

    u.log("[dq] file_match: end")
    u.log_print()
