import sys
import time

from threading import Thread
from threading import RLock
from threading import Semaphore

import pytools.utils as u
from . import gl
from . import log
from . import merge
from .connect import gen_cnx_dict
from .functions import write_rows

verrou = RLock()


def process_query_list():

    gl.multi_th = len(gl.QUERY_LIST) > 1 and gl.MAX_DB_CNX > 1
    gl.c_query = 0
    init_th_dict()
    gl.sem = Semaphore(gl.MAX_DB_CNX)
    lauch_threads()
    merge.finish()


def lauch_threads():
    if gl.range_query:
        u.log(f"Ranges to be queried: {gl.rg_list}")
    thread_list = []
    n_cnx = min(gl.MAX_DB_CNX, len(gl.QUERY_LIST))
    gen_cnx_dict(n_cnx)
    for elt in gl.QUERY_LIST:
        th = Thread(target=process_ql_elt, args=(elt, ))
        thread_list.append(th)
        th.start()

    for th in thread_list:
        th.join()

    u.log("All threads are done")
    u.log_print('|')


@u.log_exeptions
def process_ql_elt(elt):
    with gl.sem:
        gl.c_query += 1
        cur_th = get_th_nb()
        cnx = gl.cnx_dict[cur_th]

        if gl.ql_replace:
            var = u.g.VAR_DEL + gl.VAR_IN + u.g.VAR_DEL
            query = gl.query.replace(var, elt[0])
        else:
            query = elt[0]

        c = cnx.cursor()
        process_query(c, query, elt[1], cur_th)
        c.close()
        with verrou:
            gl.th_dic[cur_th] = 0


def process_query(c, query, elt, th_nb):

    log.process_query_init(elt, query, th_nb)
    c.execute(query)
    test_recover(th_nb)
    log.process_query_finish(elt, th_nb)
    init_out_file(c, elt)
    th_name = u.gen_sl_detail(elt, th_nb, gl.multi_th)
    write_rows(c, elt, th_name, th_nb)


def test_recover(th_nb):
    if not (gl.TEST_RECOVER and gl.MD):
        return
    sleep = False
    with verrou:
        if gl.c_row > gl.MD['N_STOP'] and not gl.MD['STOP']:
            s = f"TEST_RECOVER: Automatic stop (thread no. {th_nb})\n"
            u.log(s)
            # A STOP flag is sent through the manager dict to the main process in order
            # to terminate this subprocess and all the threads.
            # However a bit of time can pass before all the treads are killed so other thread
            # can continue for a few ms while this thread is blocked by the time.sleep
            gl.MD['STOP'] = True
            sleep = True

    if sleep:
        time.sleep(1)
        u.log("sys.exit()")
        sys.exit()


def get_th_nb():
    with verrou:
        i = 1
        while gl.th_dic[i] == 1:
            i += 1

        gl.th_dic[i] = 1
    return i


def init_th_dict():
    for i in range(1, gl.MAX_DB_CNX + 1):
        gl.th_dic[i] = 0


def init_out_file(cursor, file_name):
    # Output file is initialised with cursor description
    # plus range name if EXPORT_RANGE parameter is set to True

    s = gl.TMP_DIR + file_name + "{}" + gl.FILE_TYPE
    s_ = s.format('')
    s_EC = s.format(gl.EC)
    with verrou:
        gl.out_files[file_name] = s_
        gl.out_files[file_name + gl.EC] = s_EC

    with open(s_EC, 'w', encoding='utf-8') as out_file:
        fields = [elt[0] for elt in cursor.description]
        if gl.range_query and gl.EXPORT_RANGE:
            fields.append(gl.RANGE_NAME)
        s = u.g.CSV_SEPARATOR.join(fields)
        out_file.write(s + '\n')
