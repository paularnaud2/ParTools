import pytools.common as com
import pytools.common.g as g

from . import gl


def init():

    init_gl()
    init_tmp_dir()


def init_gl():
    TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    gl.IUTD_DIR = TMP_DIR + gl.IUTD_FILE
    gl.TMP_FILE_CHUNK = TMP_DIR + gl.CHUNK_FILE

    gl.range_query = False
    gl.COUNT = False
    gl.out_files = {}
    gl.th_dic = {}

    gl.c_row = 0


def init_tmp_dir():
    gl.TMP_PATH = g.paths['TMP'] + gl.TMP_FOLDER + 'recover/'
    com.mkdirs(gl.TMP_PATH)
