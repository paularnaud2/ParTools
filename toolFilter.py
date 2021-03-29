# This script allows you to filter and/or extract columns from a csv file

import os
import common as com

from common import g
from time import time
from tools import gl

# Input variables default values
gl.IN_FILE = g.paths['IN'] + "in.csv"
gl.IN_FILE = "test/sql/in.csv"
gl.OUT_FILE = g.paths['OUT'] + "out_filtered.csv"
gl.COL_LIST = ['PRM', 'AFFAIRE']

gl.FILTER = False
gl.EXTRACT_COL = True
gl.OPEN_OUT_FILE = False
gl.TEST_FILTER = False
gl.SL_STEP = 500 * 10**3

# Const
gl.s = ("{bn_1} lines read in {dstr}. {bn_2} lines read in total "
        "({bn_3} lines written in output list).")


def filter(**kwargs):
    com.log("[toolFilter] filter: start")
    start_time = time()
    com.init_kwargs(gl, kwargs)
    init_globals()
    com.log(f"Filtering file '{gl.IN_FILE}'...")
    with open(gl.IN_FILE, 'r', encoding='utf-8') as in_file:
        process_header(in_file)
        line = in_file.readline()
        while line:
            process_line(line)
            line = in_file.readline()
    finish(start_time)


def init_globals():
    gl.n_r = 0
    gl.n_o = 0
    gl.out_list = []
    com.init_sl_time()
    gl.fields = com.get_csv_fields_dict(gl.IN_FILE)


def process_header(in_file):
    line = in_file.readline()
    gl.n_r += 1
    line_list = com.csv_to_list(line)
    line_list = extract_col(line_list)
    gl.out_list.append(line_list)
    gl.n_o += 1


def process_line(line):
    gl.n_r += 1
    line_list = com.csv_to_list(line)
    if filter_line(line_list):
        line_list = extract_col(line_list)
        gl.out_list.append(line_list)
        gl.n_o += 1
    com.step_log(gl.n_r, gl.SL_STEP, what=gl.s, nb=gl.n_o)


def finish(start_time):
    com.log("Filtering over")
    bn1 = com.big_number(gl.n_r)
    bn2 = com.big_number(gl.n_o)
    s = (f"{bn1} lines read in the input file and"
         f" {bn2} lines to be written in the output file")
    com.log(s)

    com.log("Writing output file...")
    com.save_csv(gl.out_list, gl.OUT_FILE)
    s = f"Output file saved in {gl.OUT_FILE}"
    com.log(s)
    dstr = com.get_duration_string(start_time)
    com.log(f"[toolFilter] filter: end ({dstr})")
    com.log_print()
    if gl.OPEN_OUT_FILE:
        os.startfile(gl.OUT_FILE)


def filter_line(in_list):
    if gl.FILTER is False:
        return True

    # lines for which cond = True are written in the output file
    if gl.TEST_FILTER:
        cond = in_list[gl.fields['PRM']].find('01') == 0
    else:
        cond = True  # enter your conditions here
    if cond:
        return True
    else:
        return False


def extract_col(line):
    if gl.EXTRACT_COL is False:
        return line

    new_line = [line[gl.fields[elt]] for elt in gl.COL_LIST]
    return new_line


if __name__ == '__main__':
    filter(OPEN_OUT_FILE=True)
