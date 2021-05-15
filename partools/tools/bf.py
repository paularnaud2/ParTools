from time import time
from importlib import reload

import partools.utils as u
import partools.dq as dq
import partools.tools.bf_functions as bf

from partools.tools import gl
from partools.tools.init import init_sbf
from partools.tools.init import init_rbf
from partools.tools.finish import finish_sbf


def read_big_file(in_path, **kwargs):
    u.log("[toolBF] read_big_file: start")
    init_rbf()
    u.init_kwargs(gl, kwargs)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        line = bf.read_file(in_file)
        u.log_print(line.strip("\n"))
        while line != "":
            line = bf.read_file(in_file)
            u.log_print(line.strip("\n"))
            gl.c_read += 1
            if bf.check_counter(in_file):
                continue
            else:
                break

    u.log("[toolBF] read_big_file: end\n")


def search_big_file(in_path, out_path, look_for, **kwargs):
    u.log("[toolBF] search_big_file: start")
    start_time = time()
    init_sbf(in_path, look_for)
    u.init_kwargs(gl, kwargs)
    u.log(gl.s_init)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.EOF:
            bf.fill_cur_list(in_file)
            if bf.search_cur_list():
                break

    finish_sbf(out_path, start_time)


def sort_big_file(in_path, out_path):
    reload(dq.gl)  # To reinitialise MAX_ROW_LIST value when pytest is run
    dq.init.init_tmp_dir()
    u.log_print()
    dq.sort.sort_big_file(in_path, out_path, main=True)
    u.log_print()
