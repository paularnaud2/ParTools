from time import time
from importlib import reload

import partools.utils as u
import partools.dq as dq

from . import gl
from . import bf_functions as f


def read_big_file(in_path, **kwargs):
    """Reads a potentially big file

    See in partools/tools/gl for other parameters (kwargs)

    See partools/quickstart/tools_bf.py for examples of use
    """
    from .init import init_rbf

    u.log("[toolBF] read_big_file: start")
    init_rbf()
    u.init_kwargs(gl, kwargs)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        line = f.read_file(in_file)
        u.log_print(line.strip("\n"))
        while line != "":
            line = f.read_file(in_file)
            u.log_print(line.strip("\n"))
            gl.c_read += 1
            if f.check_counter(in_file):
                continue
            else:
                break

    u.log("[toolBF] read_big_file: end\n")


def search_big_file(in_path, out_path, look_for, **kwargs):
    """Searches a potentially big file

    See in partools/tools/gl for other parameters (kwargs)

    See partools/quickstart/tools_bf.py for examples of use
    """
    from .init import init_sbf
    from .finish import finish_sbf

    u.log("[toolBF] search_big_file: start")
    start_time = time()
    init_sbf(in_path, look_for)
    u.init_kwargs(gl, kwargs)
    u.log(gl.s_init)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.EOF:
            f.fill_cur_list(in_file)
            if f.search_cur_list():
                break

    finish_sbf(out_path, start_time)


def sort_big_file(in_path, out_path):
    """Sorts a potentially big file

    See partools/quickstart/tools_bf.py for examples of use
    """
    from partools.dq.init import init_tmp_dir
    from partools.dq.sort import sort_big_file

    reload(dq.gl)  # To reinitialise MAX_ROW_LIST value when pytest is run
    init_tmp_dir()
    u.log_print()
    sort_big_file(in_path, out_path, main=True)
    u.log_print()
