from time import time

import partools.utils as u
import partools.utils.sTools as st
from partools.tools.dup import del_dup_list

from . import gl
from .init import init_dq
from .csf import compare_sorted_files
from .sort import sort_big_file
from .functions import check_split
from .functions import compare_headers


def run_dq(**kwargs):
    start_time = time()
    init_dq(kwargs)
    u.check_header(gl.paths["in1"])
    u.check_header(gl.paths["in2"])
    compare_headers(gl.paths["in1"], gl.paths["in2"])
    sort_big_file(gl.paths["in1"], gl.paths["out1"], True, 1)
    sort_big_file(gl.paths["in2"], gl.paths["out2"], True, 2)
    if not compare_files(gl.paths["out1"], gl.paths["out2"], gl.paths["out"]):
        u.log_print('|')
        check_split(gl.paths["out"])
    finish_dq(start_time)


def finish_dq(start_time):

    (dms, dstr) = u.get_duration_string(start_time, True)
    s = f"[dq] run_dq: end ({dstr})"
    u.log(s)
    st.msg_box(s, "dq", dms)
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(gl.paths["out"])


def file_match(in1, in2, del_dup=False, compare=False, err=True, out_path=''):
    u.log("[dq] file_match: start")

    if not out_path:
        out_path = u.g.dirs['OUT'] + 'file_match_out.csv'

    s = f"Comparing files '{in1}' and '{in2}'..."
    u.log(s)
    l1 = u.load_txt(in1)
    l2 = u.load_txt(in2)
    l1.sort()
    l2.sort()
    if del_dup:
        l1 = del_dup_list(l1)
        l2 = del_dup_list(l2)

    res = l1 == l2
    if res:
        u.log("Files match")
    else:
        u.log("Files don't match")

    if not res or compare:
        diff_list(l1, l2, out_path)

    if not res and err:
        u.startfile(out_path)
        assert res is True

    u.log("[dq] file_match: end")
    u.log_print()


def diff_list(list1, list2, out_path):

    if not out_path:
        out_path = u.g.dirs['OUT'] + 'file_match_out.csv'

    out1 = [e for e in list1 if e not in list2]
    out2 = [e for e in list2 if e not in list1]
    out = del_dup_list(out1 + out2)
    u.save_list(out, out_path)
    u.log(f"Comparison result available here: {out_path}")


def compare_files(in_1, in_2, out_path):
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
