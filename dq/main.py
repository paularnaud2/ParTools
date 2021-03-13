import os
import common as com

import dq.gl as gl

from time import time
from dq.init import init_dq
from dq.init import init_compare_files
from toolDup import del_dup_list
from dq.csf import compare_sorted_files
from dq.sort import sort_file
from dq.functions import check_split
from dq.functions import compare_headers


def run_dq(**params):
    (start_time, dirs) = init_dq(params)
    com.check_header(dirs["in1"])
    com.check_header(dirs["in2"])
    compare_headers(dirs["in1"], dirs["in2"])
    sort_file(dirs["in1"], dirs["out1"], True, 1)
    sort_file(dirs["in2"], dirs["out2"], True, 2)
    if not compare_files(dirs["out1"], dirs["out2"], dirs["out"]):
        com.log_print('|')
        check_split(dirs["out"])
    finish_dq(start_time, dirs)


def finish_dq(start_time, dirs):

    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"[dq] run_dq: end ({dstr})"
    com.log(s)
    com.send_notif(s, "dq", dms)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        os.startfile(dirs["out"])


def file_match(in1, in2, del_dup=False, compare=False, err=True, out=''):
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
        init_compare_files(out)
        com.save_csv(ar1, gl.TMP_1)
        com.save_csv(ar2, gl.TMP_2)
        com.log(f"Deep comparison of '{gl.TMP_1}' and '{gl.TMP_2}'...")
        com.log_print('|')
        compare_files(gl.TMP_1, gl.TMP_2, gl.OUT_DIR)
        com.log_print('|')

    if not res and err:
        os.startfile(gl.OUT_DIR)
        assert res is True

    com.log("[dq] file_match: end")
    com.log_print()


def compare_files(in_1, in_2, out):
    com.log("[dq] compare_files: start")
    start_time = time()
    com.gen_header(in_1, gl.COMPARE_FIELD, out)
    compare_sorted_files(in_1, in_2, out)

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
