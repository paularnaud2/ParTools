import sys
from math import ceil
from time import time
from os.path import exists

import partools.utils as u
import partools.tools as to
import partools.utils.sTools as st

from . import gl


def check_header(inp):
    if not u.has_header(inp):
        s = (f"Error: missing header in file '{inp}'."
             " Input files must have a header.")
        u.log(s)
        raise Exception(u.g.E_MH)


def compare_headers(in1, in2):

    line1 = u.get_header(in1)
    line2 = u.get_header(in2)

    if line1 != line2:
        s = (f"Error: files {in1} and {in2} don't have the same header."
             " Input files must have the same header.")
        u.log(s)
        raise Exception(u.g.E_DH)

    return True


def compare_elt(elt1, elt2):
    if elt1 == [''] and elt2 == ['']:
        return " "
    if elt1 == ['']:
        return ">"
    if elt2 == ['']:
        return "<"
    if elt1[gl.PIVOT_IDX] < elt2[gl.PIVOT_IDX]:
        return "<"
    if elt1[gl.PIVOT_IDX] == elt2[gl.PIVOT_IDX]:
        return "="
    if elt1[gl.PIVOT_IDX] > elt2[gl.PIVOT_IDX]:
        return ">"


def write_min_elt(min_elt, out_file):
    cur_key = min_elt[gl.PIVOT_IDX]
    prev_key = gl.prev_elt[gl.PIVOT_IDX]

    if cur_key != prev_key:
        gl.DUP_KEY = False
        u.write_csv_line(min_elt, out_file)
        gl.c_tot_out += 1
        u.step_log(gl.c_tot_out, gl.SL_STEP)
        gl.prev_elt = min_elt
    elif check_dup(min_elt):
        # Pure duplicates are not written in output file
        # But key duplicates are (lines differ but key equal)
        u.write_csv_line(min_elt, out_file)
        gl.c_tot_out += 1
        u.step_log(gl.c_tot_out, gl.SL_STEP)


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
    line_list = line.strip("\n").split(u.g.CSV_SEPARATOR)
    return line_list


def check_split(in_path):

    if split_needed():
        to.split_file(
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
    bn = u.big_number(gl.MAX_LINE_SPLIT)
    s = (f"Input file has more than {bn} lines."
         f" It will be split in {n_out_files} files "
         f"(max file nb set to {gl.MAX_FILE_NB_SPLIT}). Continue? (y/n)")
    if gl.TEST_PROMPT_SPLIT:
        u.log(s)
        u.log_print('y (TEST_PROMPT_SPLIT = True)')
        return True
    if u.log_input(s) == "n":
        sys.exit()

    return True


def diff_list(list1, list2, out_path):

    if not out_path:
        out_path = u.g.dirs['OUT'] + 'file_match_out.csv'

    out1 = [e for e in list1 if e not in list2]
    out2 = [e for e in list2 if e not in list1]
    out = to.del_dup_list(out1 + out2)
    u.save_list(out, out_path)
    u.log(f"Comparison result available here: {out_path}")


def compare_files(in_1, in_2, out_path):
    from .csf import compare_sorted_files

    u.log("[dq] compare_files: start")
    start_time = time()
    u.gen_header(in_1, gl.COMPARE_FIELD, out_path)
    compare_sorted_files(in_1, in_2, out_path)

    if gl.c_diff == 0:
        u.log("Files match")
        out = True
    else:
        bn = u.big_number(gl.c_diff)
        u.log(f"{bn} differences found")
        out = False

    dstr = u.get_duration_string(start_time)
    u.log(f"[dq] compare_files: end ({dstr})")

    return out


def finish_dq(start_time):

    (dms, dstr) = u.get_duration_string(start_time, True)
    s = f"[dq] run_dq: end ({dstr})"
    u.log(s)
    if gl.MSG_BOX_END:
        st.msg_box(s, "dq", dms, gl.MIN_DUR_TRIGGER)
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(gl.paths["out"])
