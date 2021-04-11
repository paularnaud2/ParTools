import pytools.common.g as g
import pytools.common as com

from . import gl


def init(kwargs):

    com.init_kwargs(gl, kwargs)
    init_globals()
    com.check_header(gl.IN_FILE)
    com.log(f"Loading input array from '{gl.IN_FILE}'...")
    gl.ar_in = com.load_csv(gl.IN_FILE)
    com.log("Input array loaded")
    com.log_print('|')


def init_globals():

    get_footprint()
    TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER + gl.footprint + '/'
    com.mkdirs(TMP_DIR)
    gl.OUT_LEFT = TMP_DIR + gl.OUT_LEFT_FILE
    gl.OUT_RIGHT = TMP_DIR + gl.OUT_RIGHT_FILE
    gl.OUT_SQL = TMP_DIR + gl.OUT_SQL_FILE


def get_footprint():

    fp = gl.DB + gl.ENV + gl.CNX_STR
    fp += gl.QUERY_IN + gl.IN_FILE + gl.OUT_FILE
    fp = com.hash(fp)
    gl.footprint = fp
