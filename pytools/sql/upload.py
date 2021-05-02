import os
from time import time
from importlib import reload

import pytools.common as com

from . import gl
from . import log
from .init import init_gl
from .connect import connect
from .functions import get_final_script
from .execute import execute


@com.log_exeptions
def upload(**kwargs):
    com.log("[sql] upload: start")
    reload(gl)  # reinit globals
    start_time = time()
    init(kwargs)
    if not check_recover():
        prepare_bdd()
        init(kwargs)
    script = get_script()
    com.check_header(gl.UPLOAD_IN)
    with open(gl.UPLOAD_IN, "r", encoding="utf-8") as in_file:
        com.log(f"Input file {gl.UPLOAD_IN} opened")
        # First line is dismissed (header)
        in_file.readline()
        for line in in_file:
            line_list = com.csv_to_list(line)
            if len(line_list) == 1:
                line_list = line_list[0]
            gl.data.append(line_list)
            gl.c_main += 1
            if gl.c_main % gl.NB_MAX_ELT_INSERT == 0:
                st_insert = time()
                insert(script)
                send_chunk_duration(st_insert)

    if gl.c_main % gl.NB_MAX_ELT_INSERT != 0:
        insert(script)

    finish_this(start_time)
    com.log_print()


def send_chunk_duration(start):
    """Sends The duration of one insert to the main process.

    It is not wanted to send the duration of the first insert as it
    might be longer than expected due to cache mecanisms. Hence, the
    duration of the second insert is sent to the main process
    """

    if not gl.MD:
        return

    # We only send the duration of the second insert
    if gl.c_main // gl.NB_MAX_ELT_INSERT != 2:
        return

    if not gl.MD["T"]:
        (dms, dstr) = com.get_duration_string(start, True)
        com.log(f"Sending duration to the main process ({dstr})...")
        if dms == 0:
            dms = 1
        gl.MD["T"] = dms


def prepare_bdd():
    if gl.EXECUTE_KWARGS:
        com.log("Preparing DB before data injection...")
        com.log_print("|")
        execute(**gl.EXECUTE_KWARGS)


def finish_this(start_time):
    gl.cnx.close()
    os.remove(gl.tmp_file_chunk)
    bn = com.big_number(gl.c_main)
    dstr = com.get_duration_string(start_time)
    com.log(f"{bn} lines exported")
    com.log(f"[sql] upload: end ({dstr})")


def init(kwargs):
    com.init_kwargs(gl, kwargs)
    init_gl()
    com.mkdirs(gl.TMP_DIR)

    gl.ref_chunk = 0
    gl.c_main = 0
    gl.c_chunk = 0
    gl.cnx = connect()
    gl.c = gl.cnx.cursor()
    gl.data = []


def get_script():
    script = get_final_script(gl.SCRIPT_IN)
    log.script(script)
    log.inject()

    return script


def insert(script):

    if gl.c_chunk >= gl.ref_chunk:
        gl.data = [tuple(line) for line in gl.data]
        gl.c.executemany(script, gl.data)
        gl.c_chunk += 1
        snc = str(gl.c_chunk)
        com.save_csv([f"{snc}_COMMIT_RUNNING"], gl.tmp_file_chunk)
        gl.cnx.commit()
        com.save_csv([snc], gl.tmp_file_chunk)
        sn = com.big_number(gl.c_main)
        com.log(f"{sn} lines inserted in total")
        gl.c.close()
        gl.c = gl.cnx.cursor()
    else:
        gl.c_chunk += 1

    gl.data = []


def check_recover():

    chunk = gl.tmp_file_chunk
    if os.path.exists(chunk):
        s = "Injection running detected. Recover? (y/n)"
        if gl.TEST_RECOVER:
            com.log(s)
            com.log_print("y (TEST_RECOVER = True)")
        elif com.log_input(s) == "n":
            os.remove(chunk)
            return False

        txt = com.load_txt(chunk)
        try:
            gl.ref_chunk = int(txt[0])
            return True
        except Exception as e:
            log.recover_fail(e, chunk, txt)
            os.remove(chunk)
            return False
