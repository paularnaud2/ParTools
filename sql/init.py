import common as com
import sql.gl as gl

from common import g
from sql.rg import restart


def init():

    init_gl()
    get_query()
    init_tmp_dir()


def init_gl():
    TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    gl.IUTD_DIR = TMP_DIR + gl.IUTD_FILE
    gl.TMP_FILE_CHUNK = TMP_DIR + gl.CHUNK_FILE

    gl.conf = {}
    gl.conf_env = {}
    gl.bools = {}
    gl.bools['RANGE_QUERY'] = False
    gl.bools["COUNT"] = False
    gl.counters = {}
    gl.out_files = {}
    gl.th_dic = {}

    gl.counters["row"] = 0


def init_tmp_dir():
    gl.TMP_PATH = g.paths['TMP'] + gl.TMP_FOLDER + gl.DB + '/'
    com.mkdirs(gl.TMP_PATH)


def get_query():
    query = com.read_file(gl.QUERY_FILE)
    query = query.strip('\r\n;')
    query = com.replace_from_dict(query, gl.VAR_DICT)
    gl.query = query


def init_gko():
    s = f"Réquête exécutée pour toutes les instances :\n{gl.query}\n;"
    com.log_print(s)
    inst_list = gl.GKO_INSTANCES
    inst_list = restart(inst_list)
    if len(inst_list) == 0:
        com.log("Aucune instance à requêter.")
    else:
        com.log(f"Instances à requêter : {inst_list}")

    return inst_list
