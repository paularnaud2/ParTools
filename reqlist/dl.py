import sql
import common as com
import reqlist.gl as gl
import reqlist.file as file

from reqlist.functions import restart
from reqlist.functions import set_query_var
from reqlist.functions import gen_group_list
from reqlist.process import process_grp

from math import ceil
from time import time
from threading import Thread
from threading import RLock

verrou = RLock()


def download(query_file):
    com.log("[reqlist] download: start")
    start_time = time()
    init(query_file)

    group_array = split_group_list()
    n = len(group_array)
    sql.connect.gen_cnx_dict(gl.DB, gl.ENV, n)
    launch_threads(group_array)
    file.gen_out_file()

    com.delete_folder(gl.TMP_PATH)
    n = sum([gl.c[elt] for elt in gl.c])
    bn = com.big_number(n)
    dstr = com.get_duration_string(start_time)
    com.log(f"[reqlist] download: end ({bn} lines written in {dstr})")
    com.log_print('|')


def init(query_file):
    restart()
    set_query_var(query_file)
    gen_group_list()

    sql.init()
    gl.header = ''
    gl.c = {}


def launch_threads(group_array):
    i = 0
    thread_list = []
    for grp in group_array:
        i += 1
        th = Thread(target=dl_th, args=(grp, i))
        thread_list.append(th)
        th.start()

    for th in thread_list:
        th.join()

    if gl.MAX_DB_CNX > 1:
        com.log("All threads are done")
    com.log_print('|')


@com.log_exeptions
def dl_th(grp, th_nb):
    cnx = sql.gl.cnx_dict[th_nb]
    c = cnx.cursor()
    process_grp(c, grp, th_nb=th_nb)
    c.close()
    cnx.close()
    if gl.MAX_DB_CNX > 1:
        com.log(f"End of thread no. {th_nb}")


def split_group_list():
    if gl.MAX_DB_CNX < 2:
        return [gl.group_list]

    array_out = []
    cur_list = []
    n_max = ceil(len(gl.group_list) / gl.MAX_DB_CNX)
    i = 0
    for grp in gl.group_list:
        i += 1
        cur_list.append(grp)
        if len(cur_list) >= n_max:
            array_out.append(cur_list)
            cur_list = []
    if cur_list != []:
        array_out.append(cur_list)

    n = len(gl.group_list)
    if n > 1:
        gl.MULTI_TH = True
        bn = com.big_number(n)
        s = (f"The {bn} groups will be processed in parallel on"
             f" {len(array_out)} different connection pools"
             f" (max {n_max} groups per thread).")
        if gl.TEST_RESTART:
            # automatic stop when a thread reaches 80% of it's progress
            gl.n_stop = ceil(n_max * 0.8)
        com.log(s)

    return array_out
