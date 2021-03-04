import common as com
import reqlist.gl as gl
import sql.connect as sql
import reqlist.file as file

from reqlist.process import process_grp
from threading import Thread, RLock

verrou = RLock()


def download():

    thread_list = []
    for inst in gl.GKO_INSTANCES:
        th = Thread(target=process_inst_gko, args=(inst, ))
        thread_list.append(th)
        th.start()

    for th in thread_list:
        th.join()

    file.gen_out_file()


@com.log_exeptions
def process_inst_gko(inst):
    cnx = sql.connect(gl.ENV, inst)
    c = cnx.cursor()
    process_grp(c, gl.group_list, inst=inst[5:])
    c.close()
    cnx.close()
