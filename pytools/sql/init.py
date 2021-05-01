import pytools.common as com
from . import gl


def init():

    init_gl()
    init_tmp_dir()


def init_gl():
    get_footprint()
    gl.TMP_DIR = com.g.dirs['TMP'] + gl.TMP_FOLDER
    gl.iutd_path = gl.TMP_DIR + gl.IUTD_FILE
    gl.tmp_file_chunk = gl.TMP_DIR + 'chunk_' + gl.footprint + '.txt'

    gl.range_query = False
    gl.COUNT = False
    gl.out_files = {}
    gl.th_dic = {}

    gl.c_row = 0


def init_tmp_dir():

    tmp = gl.footprint + '/'
    gl.TMP_DIR = gl.TMP_DIR + tmp
    com.mkdirs(gl.TMP_DIR)


def get_footprint():

    fp = gl.DB + gl.ENV + str(gl.CNX_INFO) + gl.OUT_PATH
    fp += gl.QUERY_IN + str(gl.QUERY_LIST)
    fp = com.hash512(fp)
    gl.footprint = fp
