import os
from math import floor

import pytools.utils as u
from . import gl
from .functions import read_list


def init_dq(kwargs):
    u.log("[dq] run_dq: start")
    u.init_kwargs(gl, kwargs)
    init_tmp_dir()
    set_paths()
    s = (
        f"run_dq job initialised. Input files {gl.paths['in1']} and {gl.paths['in2']}"
        " are going to be sorted and compared.")
    u.log(s)
    u.log_print('|')


def init_compare_files(out):

    init_tmp_dir()
    gl.IN_FILE_NAME_1 = '1'
    gl.IN_FILE_NAME_2 = '2'
    if out:
        gl.out_path = out
    else:
        gl.out_path = u.g.dirs['OUT'] + 'file_match_out.csv'
    gl.TMP_1 = gl.TMP_DIR + 'tmp_1.csv'
    gl.TMP_2 = gl.TMP_DIR + 'tmp_2.csv'
    gl.EQUAL_OUT = False
    gl.DIFF_OUT = False


def init_tmp_dir():
    gl.TMP_DIR = u.g.dirs['TMP'] + gl.TMP_FOLDER
    u.mkdirs(gl.TMP_DIR, True)


def set_paths():

    paths = {}

    paths["in1"] = gl.IN_DIR + gl.IN_FILE_NAME_1 + gl.FILE_TYPE
    paths["out1"] = gl.TMP_DIR + gl.OUT_FILE_NAME + "_1" + gl.FILE_TYPE
    paths["in2"] = gl.IN_DIR + gl.IN_FILE_NAME_2 + gl.FILE_TYPE
    paths["out2"] = gl.TMP_DIR + gl.OUT_FILE_NAME + "_2" + gl.FILE_TYPE
    paths["out"] = gl.OUT_DIR + gl.OUT_FILE_NAME + gl.FILE_TYPE

    gl.paths = paths


def init_stf(in_path, out_path):

    gl.c_file = 0
    gl.c_row_max = 0
    gl.c_iter = 0

    gl.DUP_KEY = False

    gl.prev_elt = []
    gl.cur_list = []
    gl.dup_list = []
    gl.dup_key_list = []
    gl.array_list = [[]]

    gl.OUT_DUP_FILE = gl.OUT_DIR + gl.OUT_DUP_FILE_NAME
    gl.OUT_DUP_KEY_FILE = gl.OUT_DIR + gl.OUT_FILE_NAME
    gl.OUT_DUP_KEY_FILE += "_dup_key" + gl.FILE_TYPE

    del_tmp_files()
    u.gen_header(in_path, out_path=out_path)


def init_prev_elt(list_in):

    if gl.prev_elt == []:
        gl.prev_elt = ['' for elt in list_in[0]]


def init_compare(in_file_1, in_file_2):

    init_equal_diff_bool()

    gl.c_1 = 1
    gl.c_2 = 1
    gl.c_out = 1
    gl.c_diff = 0

    gl.msg = "{bn_1} lines read in {dstr}."
    gl.msg += " {bn_2} lines read in total and {bn_3}"
    gl.msg += " lines written in the output file."

    gl.LABEL_1 = gl.IN_FILE_NAME_1
    gl.LABEL_2 = gl.IN_FILE_NAME_2

    in_file_1.readline()
    in_file_2.readline()
    line_1_list = read_list(in_file_1)
    line_2_list = read_list(in_file_2)

    return (line_1_list, line_2_list)


def init_equal_diff_bool():

    if gl.EQUAL_OUT:
        if gl.c_sf_read <= gl.MAX_ROW_EQUAL_OUT:
            gl.EQUAL = True
            gl.DIFF = gl.DIFF_OUT
        else:
            bn = u.big_number(gl.MAX_ROW_EQUAL_OUT)
            s = (f"Warning: file to be compared have more than {bn} lines"
                 " and EQUAL_OUT paramter is set to True.\n"
                 "Do you want to write matching lines in output file ? (y/n)")
            if u.log_input(s) == "y":
                gl.EQUAL = True
                gl.DIFF = gl.DIFF_OUT
            else:
                gl.EQUAL = False
                gl.DIFF = True
    else:
        gl.EQUAL = False
        gl.DIFF = True


def del_tmp_files():

    counter = 0
    while True:
        try:
            counter += 1
            tmp_path = gl.TMP_DIR + str(counter) + gl.FILE_TYPE
            os.remove(tmp_path)
        except FileNotFoundError:
            break


def init_msf():

    gl.prev_elt = []
    gl.c_tot_out = 1
    gl.c_row_max = floor(gl.MAX_ROW_LIST / gl.c_file)
    if gl.c_row_max == 0:
        gl.c_row_max = 1
    init_array_list()


def init_array_list():

    counter = 1
    gl.array_list = [[]]
    while counter < gl.c_file:
        counter += 1
        gl.array_list.append([])

    nb = gl.c_row_max
    s = (f"Buffer array initialised. It can hold a maximum of {nb} lines.")
    u.log(s)
