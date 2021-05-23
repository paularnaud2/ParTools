import os
from time import time
from importlib import reload

import partools.utils as u

from . import gl
from . import log


@u.log_exeptions
def upload(**kwargs):
    u.log("[sql] upload: start")
    reload(gl)  # reinit globals
    start_time = time()
    init(kwargs)
    if not check_recover():
        prepare_bdd()
        init(kwargs)
    script = get_script()
    u.check_header(gl.UPLOAD_IN)
    with open(gl.UPLOAD_IN, "r", encoding="utf-8") as in_file:
        u.log(f"Input file {gl.UPLOAD_IN} opened")
        # First line is dismissed (header)
        in_file.readline()
        for line in in_file:
            line_list = u.csv_to_list(line)
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
    u.log_print()


def send_chunk_duration(start):
    """Sends The duration of one insert to the main process.

    It is not wanted to send the duration of the first insert as it
    might be longer than expected due to cache mechanisms. Hence, the
    duration of the second insert is sent to the main process
    """

    if not gl.MD:
        return

    # We only send the duration of the second insert
    if gl.c_main // gl.NB_MAX_ELT_INSERT != 2:
        return

    if not gl.MD["T"]:
        (dms, dstr) = u.get_duration_string(start, True)
        u.log(f"Sending duration to the main process ({dstr})...")
        if dms == 0:
            dms = 1
        gl.MD["T"] = dms


def prepare_bdd():
    from .execute import execute

    if gl.EXECUTE_KWARGS:
        u.log("Preparing DB before data injection...")
        u.log_print("|")
        execute(**gl.EXECUTE_KWARGS)


def finish_this(start_time):

    gl.cnx.close()
    os.remove(gl.tmp_file_chunk)
    bn = u.big_number(gl.c_main)
    dstr = u.get_duration_string(start_time)
    u.log(f"{bn} lines exported")
    u.log(f"[sql] upload: end ({dstr})")


def init(kwargs):
    from .connect import connect
    from .init import init_gl

    u.init_kwargs(gl, kwargs)
    init_gl()
    u.mkdirs(gl.TMP_DIR)

    gl.ref_chunk = 0
    gl.c_main = 0
    gl.c_chunk = 0
    gl.cnx = connect()
    gl.c = gl.cnx.cursor()
    gl.data = []


def get_script():
    from .functions import get_final_script

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
        u.save_csv([f"{snc}_COMMIT_RUNNING"], gl.tmp_file_chunk)
        gl.cnx.commit()
        u.save_csv([snc], gl.tmp_file_chunk)
        sn = u.big_number(gl.c_main)
        u.log(f"{sn} lines inserted in total")
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
            u.log(s)
            u.log_print("y (TEST_RECOVER = True)")
        elif u.log_input(s) == "n":
            os.remove(chunk)
            return False

        txt = u.load_txt(chunk)
        try:
            gl.ref_chunk = int(txt[0])
            return True
        except Exception as e:
            log.recover_fail(e, chunk, txt)
            os.remove(chunk)
            return False
