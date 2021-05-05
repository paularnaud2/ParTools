import pytools.utils as u
from . import gl


def init(kwargs):

    u.init_kwargs(gl, kwargs)
    init_globals()
    u.check_header(gl.IN_PATH)
    u.log(f"Loading input array from '{gl.IN_PATH}'...")
    gl.ar_in = u.load_csv(gl.IN_PATH)
    u.log("Input array loaded")
    u.log_print('|')


def init_globals():

    get_footprint()
    TMP_DIR = u.g.dirs['TMP'] + gl.TMP_FOLDER + gl.footprint + '/'
    u.mkdirs(TMP_DIR)
    gl.OUT_LEFT = TMP_DIR + gl.OUT_LEFT_FILE
    gl.OUT_RIGHT = TMP_DIR + gl.OUT_RIGHT_FILE
    gl.OUT_SQL = TMP_DIR + gl.OUT_SQL_FILE


def get_footprint():

    fp = gl.DB + gl.ENV + str(gl.CNX_INFO)
    fp += gl.QUERY_IN + gl.IN_PATH + gl.OUT_PATH
    fp = u.hash512(fp)
    gl.footprint = fp
