from time import time

import pytools.common.g as g
import pytools.common as com
import pytools.common.sTools as st
from pytools.tools.dup import find_dup

from . import gl
from .dl import download
from .join import left_join_arrays


@com.log_exeptions
def run_reqList(**kwargs):
    init(kwargs)
    start_time = time()
    if not gl.SQUEEZE_SQL:
        download(gl.QUERY_FILE)

    if not gl.SQUEEZE_JOIN:
        left_join_files()

    finish(start_time)


def left_join_files(ldir='', rdir='', out='', debug=False):
    com.log("[reqlist] left_join_files: start")
    start_time = time()
    if debug:
        gl.DEBUG_JOIN = True
    if ldir or rdir:
        init_globals()
        com.mkdirs(gl.TMP_PATH, True)
        com.log(f"Loading arrays from '{ldir}' and '{rdir}'...")
        gl.ar_in = com.load_csv(ldir)
        ar_right = com.load_csv(rdir)
        com.log("Arrays loaded")
        com.log_print('|')
    else:
        com.log("Loading right arrays...")
        ar_right = com.load_csv(gl.OUT_SQL)
        com.log("Right array loaded")
    left_join_arrays(gl.ar_in, ar_right)
    if not out:
        out = gl.OUT_FILE
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
        find_dup(gl.OUT_FILE, col=1)
        com.log_print('|')

    (dms, dstr) = com.get_duration_string(start_time, True)
    s = f"run_reqList: end ({dstr})"
    com.log("[reqlist] " + s)
    if gl.SEND_NOTIF:
        st.msg_box(s, "reqlist", dms)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        com.startfile(gl.OUT_FILE)


def init(kwargs):
    com.log("[reqlist] run_reqList: start")
    com.init_kwargs(gl, kwargs)
    init_globals()
    com.check_header(gl.IN_FILE)
    com.log(f"Loading input array from '{gl.IN_FILE}'...")
    gl.ar_in = com.load_csv(gl.IN_FILE)
    com.log("Input array loaded")
    com.log_print('|')


def init_globals():
    TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    gl.OUT_LEFT = TMP_DIR + gl.OUT_LEFT_FILE
    gl.OUT_RIGHT = TMP_DIR + gl.OUT_RIGHT_FILE
    gl.OUT_SQL = TMP_DIR + gl.OUT_SQL_FILE
    gl.TMP_PATH = TMP_DIR + gl.DB + '/'

    gl.c = {}
    gl.MULTI_TH = False
    gl.tmp_file = {}
    gl.ec_query_nb = {}