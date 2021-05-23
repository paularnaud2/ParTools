from time import time

import partools.utils as u
from partools.tools import gl


def flt(in_path, out_path, **kwargs):
    u.log("[toolFilter] filter: start")
    start_time = time()
    u.init_kwargs(gl, kwargs)
    init_globals(in_path)
    u.log(f"Filtering file '{in_path}'...")
    with open(in_path, 'r', encoding='utf-8') as in_file:
        process_header(in_file)
        line = in_file.readline()
        while line:
            process_line(line)
            line = in_file.readline()
    finish(out_path, start_time)


def init_globals(in_path):
    gl.n_r = 0
    gl.n_o = 0
    gl.out_list = []
    u.init_sl_time()
    gl.fields = u.get_csv_fields_dict(in_path)


def process_header(in_file):
    line = in_file.readline()
    gl.n_r += 1
    line_list = u.csv_to_list(line)
    line_list = extract_col(line_list)
    gl.out_list.append(line_list)
    gl.n_o += 1


def process_line(line):
    gl.n_r += 1
    line_list = u.csv_to_list(line)
    if filter_line(line_list):
        line_list = extract_col(line_list)
        gl.out_list.append(line_list)
        gl.n_o += 1
    u.step_log(gl.n_r, gl.SL_STEP, what=gl.s, nb=gl.n_o)


def finish(out_path, start_time):
    u.log("Filtering over")
    bn1 = u.big_number(gl.n_r)
    bn2 = u.big_number(gl.n_o)
    s = (f"{bn1} lines read in the input file and"
         f" {bn2} lines to be written in the output file")
    u.log(s)

    u.log("Writing output file...")
    u.save_csv(gl.out_list, out_path)
    s = f"Output file saved in {out_path}"
    u.log(s)
    dstr = u.get_duration_string(start_time)
    u.log(f"[toolFilter] filter: end ({dstr})")
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(out_path)


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
