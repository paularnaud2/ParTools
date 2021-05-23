from time import time
from importlib import reload

import partools.utils as u
import partools.sql as sql
import partools.tools as to
import partools.utils.sTools as st

from . import gl


@u.log_exeptions
def reqlist(**kwargs):
    from .init import init
    from .ql import gen_query_list

    u.log("[rl] reqlist: start")
    reload(gl)  # reinit globals
    init(kwargs)
    start_time = time()
    if not gl.SKIP_SQL:
        gen_query_list()
        download()

    if not gl.SKIP_JOIN:
        left_join_files()

    finish(start_time)


def download():
    if gl.SKIP_JOIN:
        gl.OUT_SQL = gl.OUT_PATH
    sql.download(
        CNX_INFO=gl.CNX_INFO,
        DB=gl.DB,
        ENV=gl.ENV,
        QUERY_IN=gl.QUERY_IN,
        QUERY_LIST=gl.query_list,
        OUT_PATH=gl.OUT_SQL,
        MAX_DB_CNX=gl.MAX_DB_CNX,
        VAR_DICT=gl.VAR_DICT,
        TEST_RECOVER=gl.TEST_RECOVER,
        OPEN_OUT_FILE=False,
        CHECK_DUP=False,
        MD=gl.MD,
    )


def left_join_files(lpath='', rpath='', out='', debug=False):
    from .init import init_globals
    from .join import left_join_arrays

    u.log("[rl] left_join_files: start")
    start_time = time()
    if debug:
        gl.DEBUG_JOIN = True
    if lpath or rpath:
        init_globals()
        u.log(f"Loading arrays from '{lpath}' and '{rpath}'...")
        gl.ar_in = u.load_csv(lpath)
        ar_right = u.load_csv(rpath)
        u.log("Arrays loaded")
        u.log_print('|')
    else:
        u.log("Loading right arrays...")
        ar_right = u.load_csv(gl.OUT_SQL)
        u.log("Right array loaded")
    left_join_arrays(gl.ar_in, ar_right)
    if not out:
        out = gl.OUT_PATH
    u.log("Saving output file...")
    u.save_csv(gl.out_array, out)
    s = f"Output file saved in {out}"
    u.log(s)
    dstr = u.get_duration_string(start_time)
    u.log(f"[rl] left_join_files: end ({dstr})")
    u.log_print('|')


def finish(start_time):
    if gl.CHECK_DUP:
        s = "Checking duplicates on the first column of the output file..."
        u.log(s)
        to.find_dup(gl.OUT_PATH, col=1)
        u.log_print('|')

    (dms, dstr) = u.get_duration_string(start_time, True)
    s = f"reqlist: end ({dstr})"
    u.log("[rl] " + s)
    if gl.MSG_BOX_END:
        st.msg_box(s, "rl", dms)
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(gl.OUT_PATH)
