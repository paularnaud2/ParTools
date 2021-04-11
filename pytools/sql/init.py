import pytools.common as com
import pytools.common.g as g

from . import gl


def init():

    init_gl()
    init_tmp_dir()


def init_gl():
    get_footprint()
    gl.TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    gl.IUTD_DIR = gl.TMP_DIR + gl.IUTD_FILE
    gl.TMP_FILE_CHUNK = gl.TMP_DIR + 'chunk_' + gl.footprint + '.txt'

    gl.range_query = False
    gl.COUNT = False
    gl.out_files = {}
    gl.th_dic = {}

    gl.c_row = 0


def init_tmp_dir():

    tmp = gl.footprint + '/'
    gl.TMP_PATH = gl.TMP_DIR + tmp
    com.mkdirs(gl.TMP_PATH)


def get_footprint():

    fp = gl.DB + gl.ENV + gl.CNX_STR + gl.OUT_FILE
    fp += gl.QUERY_IN + str(gl.QUERY_LIST)
    fp = com.hash(fp)
    gl.footprint = fp
