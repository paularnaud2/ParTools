import sql.rg as rg
import sql.gl as gl
import common as com

from time import time
from os import startfile
from threading import Thread
from toolDup import find_dup
from sql.init import init
from sql.init import init_gko
from sql.groupby import group_by
from sql.process import process_range_list
from sql.process import process_gko_query


@com.log_exeptions
def download(**params):
    com.log('[sql] download')
    start_time = time()
    com.init_params(gl, params)
    init()
    if gl.DB == 'GINKO':
        download_gko()
    else:
        download_strd()

    group_by()
    finish(start_time)


def download_strd():
    rg_file_name = rg.get_rg_file_name(gl.query)
    range_list = rg.gen_range_list(rg_file_name)
    range_list = rg.restart(range_list)
    process_range_list(range_list, rg_file_name)
    if gl.MERGE_RG_FILES or not gl.bools['RANGE_QUERY']:
        rg.merge_tmp_files()
    else:
        rg.move_tmp_folder()


def download_gko():
    inst_list = init_gko()
    thread_list = []
    for inst in inst_list:
        th = Thread(target=process_gko_query, args=(inst, ))
        thread_list.append(th)
        th.start()

    for th in thread_list:
        th.join()

    rg.merge_tmp_files()


def finish(start_time):

    t = com.get_duration_ms(start_time)
    n = gl.counters["row"]
    bn = com.big_number(n)
    s = "Export terminé. {} lignes écrites en {}."
    s = s.format(bn, com.get_duration_string(t))
    com.log(s)

    if gl.bools["MERGE_OK"]:
        out_dir = gl.OUT_FILE
        com.log("Fichier de sortie {} alimenté avec succès".format(out_dir))
        a = n < gl.MAX_CHECK_DUP and n > 0

        if a and gl.CHECK_DUP and not gl.bools["COUNT"]:
            com.log_print('|')
            s = "Vérification des doublons sur la première colonne"
            s += " du fichier de sortie."
            com.log(s)
            find_dup(out_dir, col=1)
        if gl.OPEN_OUT_FILE:
            startfile(out_dir)

    com.log_print('|')
    com.log("Traitement terminé")
    com.log_print()
    if gl.SEND_NOTIF:
        com.send_notif(s, "sql", t)
