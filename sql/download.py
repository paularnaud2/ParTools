import common as com
import common.sTools as st

import sql.rg as rg
import sql.gl as gl

from time import time
from os import startfile
from toolDup import find_dup
from sql.init import init
from sql.groupby import group_by
from sql.process import process_range_list


@com.log_exeptions
def download(**kwargs):
    com.log('[sql] download: start')
    start_time = time()
    com.init_kwargs(gl, kwargs)
    init()

    rg_file_name = rg.get_rg_file_name(gl.query)
    range_list = rg.gen_range_list(rg_file_name)
    range_list = rg.restart(range_list)
    process_range_list(range_list, rg_file_name)
    if gl.MERGE_RG_FILES or not gl.RANGE_QUERY:
        rg.merge_tmp_files()
        group_by()
    else:
        rg.move_tmp_folder()

    finish(start_time)


def finish(start_time):

    n = gl.c_row
    bn = com.big_number(n)
    s = f"Data fetched from {gl.DB} ({bn} lines written)"
    com.log(s)

    if gl.MERGE_OK:
        out_dir = gl.OUT_FILE
        com.log(f"Output file {out_dir} successfully filled out")
        a = n < gl.MAX_CHECK_DUP and n > 0

        if a and gl.CHECK_DUP and not gl.COUNT:
            s = "Verifying duplicates on the first column of the output file..."
            com.log(s)
            com.log_print('|')
            find_dup(out_dir, col=1)
        if gl.OPEN_OUT_FILE:
            startfile(out_dir)

    com.log_print('|')
    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"download: end ({dstr})"
    com.log("[sql] " + s)
    com.log_print()
    if gl.SEND_NOTIF:
        st.send_notif(s, "sql", dms)
