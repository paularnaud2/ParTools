from time import time
from importlib import reload

import pytools.common as com
import pytools.sql as sql
import pytools.common.sTools as st
from pytools.tools.dup import find_dup

from . import gl
from .init import init
from .init import init_globals
from .ql import gen_query_list
from .join import left_join_arrays


@com.log_exeptions
def run_reqList(**kwargs):
    com.log("[reqlist] run_reqList: start")
    reload(gl)  # reinit globals
    init(kwargs)
    start_time = time()
    if not gl.SQUEEZE_SQL:
        gen_query_list()
        download()

    if not gl.SQUEEZE_JOIN:
        left_join_files()

    finish(start_time)


def download():
    if gl.SQUEEZE_JOIN:
        gl.OUT_SQL = gl.OUT_PATH
    sql.download(
        CNX_STR=gl.CNX_STR,
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
    com.log("[reqlist] left_join_files: start")
    start_time = time()
    if debug:
        gl.DEBUG_JOIN = True
    if lpath or rpath:
        init_globals()
        com.log(f"Loading arrays from '{lpath}' and '{rpath}'...")
        gl.ar_in = com.load_csv(lpath)
        ar_right = com.load_csv(rpath)
        com.log("Arrays loaded")
        com.log_print('|')
    else:
        com.log("Loading right arrays...")
        ar_right = com.load_csv(gl.OUT_SQL)
        com.log("Right array loaded")
    left_join_arrays(gl.ar_in, ar_right)
    if not out:
        out = gl.OUT_PATH
    com.log("Saving output file...")
    com.save_csv(gl.out_array, out)
    s = f"Output file saved in {out}"
    com.log(s)
    dstr = com.get_duration_string(start_time)
    com.log(f"[reqlist] left_join_files: end ({dstr})")
    com.log_print('|')


def finish(start_time):
    if gl.CHECK_DUP:
        s = "Checking duplicates on the first column of the output file..."
        com.log(s)
        find_dup(gl.OUT_PATH, col=1)
        com.log_print('|')

    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"run_reqList: end ({dstr})"
    com.log("[reqlist] " + s)
    if gl.MSG_BOX_END:
        st.msg_box(s, "reqlist", dms)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        com.startfile(gl.OUT_PATH)
