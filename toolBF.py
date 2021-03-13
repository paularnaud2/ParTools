# This script allows you to read or search a big file (> 100 Mo)

import common as com

from common import g
from time import time

from tools import gl
from tools.init import init_sbf
from tools.init import init_rbf
from tools.finish import finish_sbf
from tools.bf import read_file
from tools.bf import fill_cur_list
from tools.bf import search_cur_list
from tools.bf import check_counter

gl.IN_FILE = g.paths['IN'] + "in.csv"
gl.IN_FILE = "test/sql/in.csv"
gl.OUT_FILE = g.paths['OUT'] + "out.xml"
gl.LOOK_FOR = "22173227102607"

gl.LINE_PER_LINE = True
gl.OPEN_OUT_FILE = True
gl.N_READ = 10
gl.PRINT_SIZE = 10
gl.MAX_LIST_SIZE = 100
gl.BUFFER_SIZE = 100

# MAX_LIST_SIZE = 5 * 10**6
# BUFFER_SIZE = 100 * 10**3


def read_big_file():
    com.log("[toolRBF] read_big_file: start")
    init_rbf()
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

    com.log("[toolRBF] read_big_file: end")


def search_big_file():
    com.log("[toolSBF] search_big_file: start")
    start_time = time()
    init_sbf()
    with open(gl.IN_FILE, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.EOF:
            fill_cur_list(in_file)
            if search_cur_list():
                break

    finish_sbf(start_time)


if __name__ == '__main__':
    # read_big_file()
    search_big_file()
