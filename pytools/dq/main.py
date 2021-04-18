from time import time

import pytools.common as com
import pytools.common.sTools as st
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
    com.check_header(gl.paths["in1"])
    com.check_header(gl.paths["in2"])
    compare_headers(gl.paths["in1"], gl.paths["in2"])
    sort_big_file(gl.paths["in1"], gl.paths["out1"], True, 1)
    sort_big_file(gl.paths["in2"], gl.paths["out2"], True, 2)
    if not compare_files(gl.paths["out1"], gl.paths["out2"], gl.paths["out"]):
        com.log_print('|')
        check_split(gl.paths["out"])
    finish_dq(start_time)


def finish_dq(start_time):

    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"[dq] run_dq: end ({dstr})"
    com.log(s)
    st.msg_box(s, "dq", dms)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        com.startfile(gl.paths["out"])


def file_match(in1, in2, del_dup=False, compare=False, err=True, out_path=''):
    com.log("[dq] file_match: start")
    s = f"Comparing files '{in1}' and '{in2}'..."
    com.log(s)
    ar1 = com.load_csv(in1)
    ar2 = com.load_csv(in2)
    ar1.sort()
    ar2.sort()
    if del_dup:
        ar1 = del_dup_list(ar1)
        ar2 = del_dup_list(ar2)

    res = ar1 == ar2
    if res:
        com.log("Files match")
    else:
        com.log("Files don't match")

    if not res or compare:
        init_compare_files(out_path)
        com.save_csv(ar1, gl.TMP_1)
        com.save_csv(ar2, gl.TMP_2)
        com.log(f"Deep comparison of '{gl.TMP_1}' and '{gl.TMP_2}'...")
        com.log_print('|')
        compare_files(gl.TMP_1, gl.TMP_2, gl.out_path)
        com.log_print('|')

    if not res and err:
        com.startfile(gl.out_path)
        assert res is True

    com.log("[dq] file_match: end")
    com.log_print()


def compare_files(in_1, in_2, out_path):
    com.log("[dq] compare_files: start")
    start_time = time()
    com.gen_header(in_1, gl.COMPARE_FIELD, out_path)
    compare_sorted_files(in_1, in_2, out_path)

    if gl.c_diff == 0:
        com.log("Files match")
        out = True
    else:
        bn = com.big_number(gl.c_diff)
        com.log(f"{bn} differences found")
        out = False

    dstr = com.get_duration_string(start_time)
    com.log(f"[dq] compare_files: end ({dstr})")

    return out
