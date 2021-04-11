from time import time
from importlib import reload

import pytools.common as com
import pytools.common.sTools as st
from pytools.tools.dup import find_dup

from . import gl
from .init import init
from .restart import restart
from .functions import get_query_list
from .process import process_query_list


@com.log_exeptions
def download(**kwargs):
    com.log('[sql] download: start')
    reload(gl)  # reinit globals
    start_time = time()
    com.init_kwargs(gl, kwargs)

    init()
    get_query_list()
    restart()
    process_query_list()
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
            com.startfile(out_dir)

    com.log_print('|')
    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"download: end ({dstr})"
    com.log("[sql] " + s)
    com.log_print()
    if gl.MSG_BOX_END:
        st.msg_box(s, "sql", dms)
