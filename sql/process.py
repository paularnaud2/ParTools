import sys
import time
import common as com
import sql.log as log
import sql.gl as gl

from common import g
from sql.functions import write_rows
from sql.connect import gen_cnx_dict
from threading import Thread
from threading import RLock
from threading import Semaphore

verrou = RLock()


def process_range_list(range_list, rg_file_name):
    gl.counters['QUERY_RANGE'] = 0
    init_th_dict()
    gl.sem = Semaphore(gl.MAX_DB_CNX)
    if range_list == ['MONO']:
        gen_cnx_dict(gl.DB, gl.ENV, 1)
        process_range()
    else:
        lauch_threads(range_list, rg_file_name)


def lauch_threads(range_list, rg_file_name):
    com.log(f"Ranges to be queried: {range_list}")
    thread_list = []
    gen_cnx_dict(gl.DB, gl.ENV, gl.MAX_DB_CNX)
    for elt in range_list:
        th = Thread(target=process_range, args=(
            elt,
            rg_file_name,
        ))
        thread_list.append(th)
        th.start()

    for th in thread_list:
        th.join()

    com.log("All threads are done")
    com.log_print('|')


@com.log_exeptions
def process_range(elt='MONO', rg_file_name=''):
    with gl.sem:
        gl.counters['QUERY_RANGE'] += 1
        cur_th = get_th_nb()
        cnx = gl.cnx_dict[cur_th]
        elt_query = elt.replace("'", "''")
        query = gl.query.replace(
            g.VAR_DEL + rg_file_name + g.VAR_DEL,
            elt_query,
        )
        c = cnx.cursor()
        process_query(c, query, elt, cur_th)
        c.close()
        with verrou:
            gl.th_dic[cur_th] = 0


def process_query(c, query, elt, th_nb):

    log.process_query_init(elt, query, th_nb)
    c.execute(query)
    test_restart(th_nb)
    log.process_query_finish(elt, th_nb)
    init_out_file(c, elt)
    th_name = com.gen_sl_detail(elt, th_nb)
    write_rows(c, elt, th_name, th_nb)


def test_restart(th_nb):
    if not (gl.TEST_RESTART and gl.MD):
        return
    sleep = False
    with verrou:
        if gl.counters["row"] > gl.MD['N_STOP'] and not gl.MD['STOP']:
            s = f"TEST_RESTART: Automatic stop (thread no. {th_nb})\n"
            com.log(s)
            # A STOP flag is sent through the manager dict to the main process in order
            # to terminate this subprocess and all the threads.
            # However a bit of time can pass before all the treads are killed so other thread
            # can continue for a few ms while this thread is blocked by the time.sleep
            gl.MD['STOP'] = True
            sleep = True

    if sleep:
        time.sleep(1)
        com.log("sys.exit()")
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


def init_out_file(cursor, range_name='MONO'):
    # Output file is initialised with cursor description
    # plus range name is EXPORT_RANGE parameter is set to True

    s = gl.TMP_PATH + range_name + "{}" + gl.FILE_TYPE
    s_ = s.format('')
    s_EC = s.format(gl.EC)
    with verrou:
        gl.out_files[range_name] = s_
        gl.out_files[range_name + gl.EC] = s_EC

    with open(s_EC, 'w', encoding='utf-8') as out_file:
        fields = [elt[0] for elt in cursor.description]
        if gl.EXPORT_RANGE and range_name != 'MONO':
            fields.append("RANGE")
        s = g.CSV_SEPARATOR.join(fields)
        out_file.write(s + '\n')
