import sys
from math import ceil
from os.path import exists

import pytools.common as com
import pytools.common.g as g
from pytools.tools.split import split_file

from . import gl


def check_header(inp):
    if not com.has_header(inp):
        s = (f"Error: missing header in file '{inp}'."
             " Input files must have a header.")
        com.log(s)
        raise Exception(g.E_MH)


def compare_headers(in1, in2):

    line1 = com.get_header(in1)
    line2 = com.get_header(in2)

    if line1 != line2:
        s = (f"Error: files {in1} and {in2} don't have the same header."
             " Input files must have the same header.")
        com.log(s)
        raise Exception(g.E_DH)

    return True


def compare_elt(elt1, elt2):
    if elt1 == [''] and elt2 == ['']:
        return " "
    if elt1 == ['']:
        return ">"
    if elt2 == ['']:
        return "<"
    if elt1[gl.COMPARE_FIELD_NB - 1] < elt2[gl.COMPARE_FIELD_NB - 1]:
        return "<"
    if elt1[gl.COMPARE_FIELD_NB - 1] == elt2[gl.COMPARE_FIELD_NB - 1]:
        return "="
    if elt1[gl.COMPARE_FIELD_NB - 1] > elt2[gl.COMPARE_FIELD_NB - 1]:
        return ">"


def write_min_elt(min_elt, out_file):
    cur_key = min_elt[gl.COMPARE_FIELD_NB - 1]
    prev_key = gl.prev_elt[gl.COMPARE_FIELD_NB - 1]

    if cur_key != prev_key:
        gl.DUP_KEY = False
        com.write_csv_line(min_elt, out_file)
        gl.c_tot_out += 1
        com.step_log(gl.c_tot_out, gl.SL_STEP)
        gl.prev_elt = min_elt
    elif check_dup(min_elt):
        # Pure duplicates are not written in output file
        # But key duplicates are (lines differ but key equal)
        com.write_csv_line(min_elt, out_file)
        gl.c_tot_out += 1
        com.step_log(gl.c_tot_out, gl.SL_STEP)


def check_dup(elt):
    if elt == gl.prev_elt:
        # Pure duplicates are written in a specific list
        gl.dup_list.append(elt)
        return False
    else:
        # Key duplicates are also written in a specific list
        if not gl.DUP_KEY:
            gl.dup_key_list.append(gl.prev_elt)
            gl.DUP_KEY = True
        gl.dup_key_list.append(elt)
        return True


def temp_files():
    counter = 0
    while counter < gl.c_file:
        counter += 1
        tmp_path = gl.TMP_DIR + "tmp_" + str(counter) + gl.FILE_TYPE
        if exists(tmp_path):
            return True

    return False


def array_list_not_void():
    for elt in gl.array_list:
        if elt != []:
            return True

    return False


def read_list(in_file):
    line = in_file.readline()
    line_list = line.strip("\n").split(g.CSV_SEPARATOR)
    return line_list


def check_split(in_path):

    if split_needed():
        split_file(
            in_path,
            MAX_LINE=gl.MAX_LINE_SPLIT,
            MAX_FILE_NB=gl.MAX_FILE_NB_SPLIT,
            ADD_HEADER=True,
        )


def split_needed():
    n_line = gl.c_out
    n_out_files = ceil(n_line / gl.MAX_LINE_SPLIT)
    if n_out_files == 1:
        return False

    n_line_2 = n_line + n_out_files - 1
    n_out_files = ceil(n_line_2 / gl.MAX_LINE_SPLIT)
    bn = com.big_number(gl.MAX_LINE_SPLIT)
    s = (f"Input file has more than {bn} lines."
         f" It will be splitted in {n_out_files} files "
         f"(max file nb set to {gl.MAX_FILE_NB_SPLIT}). Continue? (y/n)")
    if gl.TEST_PROMPT_SPLIT:
        com.log(s)
        com.log_print('y (TEST_PROMPT_SPLIT = True)')
        return True
    if com.log_input(s) == "n":
        sys.exit()

    return True
