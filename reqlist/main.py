import common as com
import reqlist.gl as gl

from common import g
from time import time
from os import startfile
from toolDup import find_dup
from reqlist.dl import download
from reqlist.join import join_arrays


@com.log_exeptions
def run_reqList(**params):
    init(params)
    if not gl.SQUEEZE_SQL:
        download(gl.QUERY_FILE)

    if not gl.SQUEEZE_JOIN:
        left_join()

    finish(gl.start_time)


def left_join(ldir='', rdir='', out='', debug=False):
    if debug:
        gl.DEBUG_JOIN = True
    if ldir or rdir:
        init_globals()
        com.mkdirs(gl.TMP_PATH, True)
        com.log(f"Chargement des tableaux {ldir} et {rdir}...")
        gl.ar_in = com.load_csv(ldir)
        ar_right = com.load_csv(rdir)
        com.log("Tableaux chargés")
        com.log_print('|')
    else:
        com.log("Chargement du tableau de droite...")
        ar_right = com.load_csv(gl.OUT_SQL)
        com.log("Tableau de droite chargé")
        com.log_print('|')
    join_arrays(gl.ar_in, ar_right)
    if not out:
        out = gl.OUT_FILE
    com.log("Sauvegarde du fichier de sortie...")
    com.save_csv(gl.out_array, out)
    s = f"Fichier de sortie sauvegardé à l'adresse '{out}'"
    com.log(s)


def finish(start_time):
    if gl.CHECK_DUP:
        com.log_print('|')
        s = "Vérification des doublons sur la première colonne"
        s += " du fichier de sortie"
        com.log(s)
        find_dup(gl.OUT_FILE, col=1)
        com.log_print('|')

    s = "Exécution terminée en {}"
    t = com.get_duration_ms(start_time)
    s = s.format(com.get_duration_string(t))
    com.log(s)
    if gl.SEND_NOTIF:
        com.send_notif(s, "reqlist", t)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        startfile(gl.OUT_FILE)


def init(params):
    com.log("[reqlist] run_reqList")
    com.init_params(gl, params)
    init_globals()
    com.check_header(gl.IN_FILE)
    com.log(f"Chargement du tableau d'entrée depuis {gl.IN_FILE}...")
    gl.ar_in = com.load_csv(gl.IN_FILE)
    com.log("Tableau d'entrée chargé")
    com.log_print('|')


def init_globals():

    TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    gl.OUT_LEFT = TMP_DIR + gl.OUT_LEFT_FILE
    gl.OUT_RIGHT = TMP_DIR + gl.OUT_RIGHT_FILE
    gl.OUT_SQL = TMP_DIR + gl.OUT_SQL_FILE
    gl.TMP_PATH = TMP_DIR + gl.DB + '/'

    gl.counters = {}
    gl.bools = {}
    gl.bools['MULTI_TH'] = False
    gl.tmp_file = {}
    gl.ec_query_nb = {}
    gl.start_time = time()
