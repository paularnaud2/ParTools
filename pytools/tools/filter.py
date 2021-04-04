from time import time

import pytools.common as com
from pytools.tools import gl


def filter(in_dir, out_dir, **kwargs):
    com.log("[toolFilter] filter: start")
    start_time = time()
    com.init_kwargs(gl, kwargs)
    init_globals(in_dir)
    com.log(f"Filtering file '{in_dir}'...")
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        process_header(in_file)
        line = in_file.readline()
        while line:
            process_line(line)
            line = in_file.readline()
    finish(out_dir, start_time)


def init_globals(in_dir):
    gl.n_r = 0
    gl.n_o = 0
    gl.out_list = []
    com.init_sl_time()
    gl.fields = com.get_csv_fields_dict(in_dir)


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


def finish(out_dir, start_time):
    com.log("Filtering over")
    bn1 = com.big_number(gl.n_r)
    bn2 = com.big_number(gl.n_o)
    s = (f"{bn1} lines read in the input file and"
         f" {bn2} lines to be written in the output file")
    com.log(s)

    com.log("Writing output file...")
    com.save_csv(gl.out_list, out_dir)
    s = f"Output file saved in {out_dir}"
    com.log(s)
    dstr = com.get_duration_string(start_time)
    com.log(f"[toolFilter] filter: end ({dstr})")
    com.log_print()
    if gl.OPEN_OUT_FILE:
        com.startfile(out_dir)


def filter_line(line_list):
    if not gl.FF:
        return True

    # Lines for which cond = True are written in the output file
    cond = gl.FF(line_list)

    return cond


def extract_col(line):
    if gl.EXTRACT_COL is False:
        return line

    new_line = [line[gl.fields[elt]] for elt in gl.COL_LIST]
    return new_line
