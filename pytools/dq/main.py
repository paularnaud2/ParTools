from time import time

import pytools.utils as u
import pytools.utils.sTools as st
from pytools.tools.dup import del_dup_list

from . import gl
from .init import init_dq
from .init import init_compare_files
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
    s = f"Comparing files '{in1}' and '{in2}'..."
    u.log(s)
    ar1 = u.load_csv(in1)
    ar2 = u.load_csv(in2)
    ar1.sort()
    ar2.sort()
    if del_dup:
        ar1 = del_dup_list(ar1)
        ar2 = del_dup_list(ar2)

    res = ar1 == ar2
    if res:
        u.log("Files match")
    else:
        u.log("Files don't match")

    if not res or compare:
        init_compare_files(out_path)
        u.save_csv(ar1, gl.TMP_1)
        u.save_csv(ar2, gl.TMP_2)
        u.log(f"Deep comparison of '{gl.TMP_1}' and '{gl.TMP_2}'...")
        u.log_print('|')
        compare_files(gl.TMP_1, gl.TMP_2, gl.out_path)
        u.log_print('|')

    if not res and err:
        u.startfile(gl.out_path)
        assert res is True

    u.log("[dq] file_match: end")
    u.log_print()


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
