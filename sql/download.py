import sql.rg as rg
import sql.gl as gl
import common as com

from time import time
from os import startfile
from toolDup import find_dup
from sql.init import init
from sql.groupby import group_by
from sql.process import process_range_list


@com.log_exeptions
def download(**params):
    com.log('[sql] download: start')
    start_time = time()
    com.init_params(gl, params)
    init()

    rg_file_name = rg.get_rg_file_name(gl.query)
    range_list = rg.gen_range_list(rg_file_name)
    range_list = rg.restart(range_list)
    process_range_list(range_list, rg_file_name)
    if gl.MERGE_RG_FILES or not gl.bools['RANGE_QUERY']:
        rg.merge_tmp_files()
        group_by()
    else:
        rg.move_tmp_folder()

    finish(start_time)


def finish(start_time):

    n = gl.counters["row"]
    bn = com.big_number(n)
    s = f"Data fetched from {gl.DB} ({bn} lines written)"
    com.log(s)

    if gl.bools["MERGE_OK"]:
        out_dir = gl.OUT_FILE
        com.log(f"Output file {out_dir} successfully filled out")
        a = n < gl.MAX_CHECK_DUP and n > 0

        if a and gl.CHECK_DUP and not gl.bools["COUNT"]:
            com.log_print('|')
            s = "Verifying duplicates on the first column of the output file..."
            com.log(s)
            find_dup(out_dir, col=1)
        if gl.OPEN_OUT_FILE:
            startfile(out_dir)

    com.log_print('|')
    dms = com.get_duration_ms(start_time)
    dstr = com.get_duration_string(dms)
    s = f"download: end ({dstr})"
    com.log("[sql] " + s)
    com.log_print()
    if gl.SEND_NOTIF:
        com.send_notif(s, "sql", dms)
