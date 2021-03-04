import os
import common as com
import sql.gl as gl
import sql.log as log
import sql.init as sql

from time import time
from sql.connect import connect
from sql.functions import get_final_script
from sql.execute import execute


@com.log_exeptions
def upload(**params):
    com.log('[sql] upload')
    init(params)
    if not check_restart():
        prepare_bdd()
        init(params)
    script = get_script()
    start_time = time()
    com.check_header(gl.UPLOAD_IN)
    com.log(f"Ouverture du fichier d'entrée {gl.UPLOAD_IN}")
    with open(gl.UPLOAD_IN, 'r', encoding='utf-8') as in_file:
        # on saute la première ligne (entête)
        in_file.readline()
        for line in in_file:
            line_list = com.csv_to_list(line)
            if len(line_list) == 1:
                line_list = line_list[0]
            gl.data.append(line_list)
            gl.counters['main'] += 1
            if gl.counters['main'] % gl.NB_MAX_ELT_INSERT == 0:
                insert(script)
                send_chunk_duration(start_time)

    if gl.counters['main'] % gl.NB_MAX_ELT_INSERT != 0:
        insert(script)

    finish_this(start_time)
    com.log_print()


def prepare_bdd():
    if gl.EXECUTE_PARAMS:
        com.log("Préparation de la base de donnée avant l'injection")
        com.log_print('|')
        execute(**gl.EXECUTE_PARAMS)


def finish_this(start_time):
    gl.cnx.close()
    os.remove(gl.TMP_FILE_CHUNK)
    bn = com.big_number(gl.counters['main'])
    dur = com.get_duration_ms(start_time)
    durs = com.get_duration_string(dur)
    s = f"Injection des données terminée. {bn} lignes insérées en {durs}."
    com.log(s)


def init(params):
    com.init_params(gl, params)
    sql.init()

    gl.ref_chunk = 0
    gl.counters['main'] = 0
    gl.counters['chunk'] = 0
    gl.cnx = connect(ENV=gl.ENV, DB=gl.DB)
    gl.c = gl.cnx.cursor()
    gl.data = []


def get_script():
    script = get_final_script(gl.SCRIPT_FILE)
    log.script(script)
    log.inject()

    return script


def insert(script):

    if gl.counters['chunk'] >= gl.ref_chunk:
        gl.data = [tuple(line) for line in gl.data]
        gl.c.executemany(script, gl.data)
        gl.counters['chunk'] += 1
        snc = str(gl.counters['chunk'])
        com.save_csv([f"{snc}_COMMIT_RUNNING"], gl.TMP_FILE_CHUNK)
        gl.cnx.commit()
        com.save_csv([snc], gl.TMP_FILE_CHUNK)
        sn = com.big_number(gl.counters['main'])
        com.log(f"{sn} lignes insérées au total")
        gl.c.close()
        gl.c = gl.cnx.cursor()
    else:
        gl.counters['chunk'] += 1

    gl.data = []


def send_chunk_duration(start):
    if not gl.MD:
        return

    if not gl.MD['T']:
        gl.MD['T'] = com.get_duration_ms(start)


def check_restart():
    chunk = gl.TMP_FILE_CHUNK
    if os.path.exists(chunk):
        s = "Injection de données en cours détectée. Reprendre ? (o/n)"
        if gl.TEST_RESTART:
            com.log(s)
            com.log_print("o (TEST_RESTART = True)")
        elif com.log_input(s) == 'n':
            os.remove(chunk)
            return False

        txt = com.load_txt(chunk)
        try:
            gl.ref_chunk = int(txt[0])
            return True
        except Exception as e:
            log.restart_fail(e, chunk, txt)
            os.remove(chunk)
            return False
