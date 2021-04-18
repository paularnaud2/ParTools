from time import time
from importlib import reload

import pytools.common as com
import pytools.dq as dq
import pytools.tools.bf_functions as bf

from pytools.tools import gl
from pytools.tools.init import init_sbf
from pytools.tools.init import init_rbf
from pytools.tools.finish import finish_sbf


def read_big_file(in_path, **kwargs):
    com.log("[toolBF] read_big_file: start")
    init_rbf()
    com.init_kwargs(gl, kwargs)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        line = bf.read_file(in_file)
        com.log_print(line.strip("\n"))
        while line != "":
            line = bf.read_file(in_file)
            com.log_print(line.strip("\n"))
            gl.c_read += 1
            if bf.check_counter(in_file):
                continue
            else:
                break

    com.log("[toolBF] read_big_file: end\n")


def search_big_file(in_path, out_path, look_for, **kwargs):
    com.log("[toolBF] search_big_file: start")
    start_time = time()
    init_sbf(in_path, look_for)
    com.init_kwargs(gl, kwargs)
    com.log(gl.s_init)
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.EOF:
            bf.fill_cur_list(in_file)
            if bf.search_cur_list():
                break

    finish_sbf(out_path, start_time)


def sort_big_file(in_path, out_path):
    reload(dq.gl)  # To reinitialise MAX_ROW_LIST value when pytest is run
    dq.init.init_tmp_dir()
    com.log_print()
    dq.sort.sort_big_file(in_path, out_path, main=True)
    com.log_print()
