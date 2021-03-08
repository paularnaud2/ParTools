import sql
import common as com
import reqlist.gl as gl
import reqlist.dl_strd as strd

from reqlist.functions import restart
from reqlist.functions import set_query_var
from reqlist.functions import gen_group_list


def download(query_file):
    init(query_file)
    strd.download()

    com.delete_folder(gl.TMP_PATH)
    com.log_print('|')
    n = sum([gl.counters[elt] for elt in gl.counters])
    bn = com.big_number(n)
    s = f"Export récupéré ({bn} lignes écrites)"
    com.log(s)


def init(query_file):
    restart()
    set_query_var(query_file)
    gen_group_list()

    sql.init()
    com.log_print('|')
    com.log(f"Récupération des données depuis la base {gl.DB}...")
    gl.header = ''
    gl.counters = {}
