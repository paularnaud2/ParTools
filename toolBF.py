# This script allows you to read or search a big file (> 100 Mo)

import common as com
import dq

from common import g
from time import time
from importlib import reload

from tools import gl
from tools.init import init_sbf
from tools.init import init_rbf
from tools.finish import finish_sbf
from tools.bf import read_file
from tools.bf import fill_cur_list
from tools.bf import search_cur_list
from tools.bf import check_counter

# Input variables default values
gl.IN_FILE = g.paths['IN'] + "in.csv"
gl.IN_FILE = "test/sql/in.csv"
gl.OUT_FILE = g.paths['OUT'] + "out.csv"
gl.LOOK_FOR = "22173227102607"

gl.LINE_PER_LINE = True
gl.OPEN_OUT_FILE = True
gl.TEST = False

gl.N_READ = 10
gl.PRINT_SIZE = 10

gl.MAX_LIST_SIZE = 5 * 10**6
gl.BUFFER_SIZE = 100 * 10**3


def read_big_file(**kwargs):
    com.log("[toolBF] read_big_file: start")
    init_rbf()
    com.init_kwargs(gl, kwargs)
    with open(gl.IN_FILE, 'r', encoding='utf-8', errors='ignore') as in_file:
        line = read_file(in_file)
        com.log_print(line.strip("\n"))
        while line != "":
            line = read_file(in_file)
            com.log_print(line.strip("\n"))
            gl.c_read += 1
            if check_counter(in_file):
                continue
            else:
                break

    com.log("[toolBF] read_big_file: end\n")


def search_big_file(**kwargs):
    com.log("[toolBF] search_big_file: start")
    start_time = time()
    init_sbf()
    com.init_kwargs(gl, kwargs)
    com.log(gl.s_init)
    with open(gl.IN_FILE, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.EOF:
            fill_cur_list(in_file)
            if search_cur_list():
                break

    finish_sbf(start_time)


def sort_big_file(in_dir, out_dir):
    reload(dq.gl)  # To reinitialise MAX_ROW_LIST value when pytest is run
    dq.init.init_tmp_dir()
    com.log_print()
    dq.sort.sort_big_file(in_dir, out_dir, main=True)
    com.log_print()


if __name__ == '__main__':
    # read_big_file()
    # search_big_file()
    sort_big_file(gl.IN_FILE, gl.OUT_FILE)
