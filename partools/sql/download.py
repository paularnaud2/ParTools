from time import time
from importlib import reload

import partools.utils as u
import partools.tools as to
import partools.utils.sTools as st

from . import gl
from .init import init
from .recover import recover
from .functions import get_query_list
from .process import process_query_list


@u.log_exeptions
def download(**kwargs):
    u.log('[sql] download: start')
    reload(gl)  # reinit globals
    start_time = time()
    u.init_kwargs(gl, kwargs)

    init()
    get_query_list()
    recover()
    process_query_list()
    finish(start_time)


def finish(start_time):

    n = gl.c_row
    bn = u.big_number(n)
    s = f"Data fetched from {gl.DB} ({bn} lines written)"
    u.log(s)

    if gl.MERGE_OK:
        out_path = gl.OUT_PATH
        u.log(f"Output file {out_path} successfully filled out")
        a = n < gl.MAX_CHECK_DUP and n > 0

        if a and gl.CHECK_DUP and not gl.COUNT:
            s = "Verifying duplicates on the first column of the output file..."
            u.log(s)
            u.log_print('|')
            to.find_dup(out_path, col=1)
        if gl.OPEN_OUT_FILE:
            u.startfile(out_path)

    u.log_print('|')
    (dms, dstr) = u.get_duration_string(start_time, True)
    s = f"download: end ({dstr})"
    u.log("[sql] " + s)
    u.log_print()
    if gl.MSG_BOX_END:
        st.msg_box(s, "sql", dms)
