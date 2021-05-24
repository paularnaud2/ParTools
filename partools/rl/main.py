from time import time
from importlib import reload

import partools.utils as u

from . import gl


@u.log_exeptions
def reqlist(**kwargs):
    """Performs multi threaded SQL queries on a given perimeter on an Oracle DB

    See README.md for guidance

    See partools/quickstart/reqlist.py for examples of use
    """
    from .init import init
    from .ql import gen_query_list
    from .functions import finish
    from .functions import download

    u.log("[rl] reqlist: start")
    reload(gl)  # reinit globals
    init(kwargs)
    start_time = time()
    if not gl.SKIP_SQL:
        gen_query_list()
        download()

    if not gl.SKIP_JOIN:
        left_join_files()

    finish(start_time)


def left_join_files(lpath='', rpath='', out='', debug=False):
    """Joints two files (lpath and rpath) on the first column of each file"""
    from .init import init_globals
    from .join import left_join_arrays

    u.log("[rl] left_join_files: start")
    start_time = time()
    if debug:
        gl.DEBUG_JOIN = True
    if lpath or rpath:
        init_globals()
        u.log(f"Loading arrays from '{lpath}' and '{rpath}'...")
        gl.ar_in = u.load_csv(lpath)
        ar_right = u.load_csv(rpath)
        u.log("Arrays loaded")
        u.log_print('|')
    else:
        u.log("Loading right arrays...")
        ar_right = u.load_csv(gl.OUT_SQL)
        u.log("Right array loaded")
    left_join_arrays(gl.ar_in, ar_right)
    if not out:
        out = gl.OUT_PATH
    u.log("Saving output file...")
    u.save_csv(gl.out_array, out)
    s = f"Output file saved in {out}"
    u.log(s)
    dstr = u.get_duration_string(start_time)
    u.log(f"[rl] left_join_files: end ({dstr})")
    u.log_print('|')
