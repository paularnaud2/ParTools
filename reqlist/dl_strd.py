import common as com
import reqlist.gl as gl
import sql.gl as glsql
import sql.connect as sql
import reqlist.file as file

from math import ceil
from threading import Thread
from threading import RLock

from reqlist.process import process_grp

verrou = RLock()


def download():
    group_array = split_group_list()
    n = len(group_array)
    sql.gen_cnx_dict(gl.DB, gl.ENV, n)
    launch_threads(group_array)
    file.gen_out_file()


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
        com.log("Tous les threads ont terminé leur execution")
    com.log_print('|')


@com.log_exeptions
def dl_th(grp, th_nb):
    cnx = glsql.cnx_dict[th_nb]
    c = cnx.cursor()
    process_grp(c, grp, th_nb=th_nb)
    c.close()
    cnx.close()
    if gl.MAX_DB_CNX > 1:
        com.log(f"Fin de l'execution du thread No.{th_nb}")


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
        gl.bools['MULTI_TH'] = True
        bn = com.big_number(n)
        s = f"Les {bn} groupes seront traités en parallèle sur"
        s += f" {len(array_out)} pools"
        s += " de connexion différents"
        s = s + f" ({n_max} groupes max à traiter par thread)."
        if gl.TEST_RESTART:
            # automatic stop when a thread reaches 80% of it's progress
            gl.counters['N_STOP'] = ceil(n_max * 0.8)
        com.log(s)

    return array_out
