import os
import qdd.gl as gl
import common as com

from common import g
from math import floor
from qdd.functions import read_list


def init_compare_files(out):

    init_tmp_dir()
    gl.IN_FILE_NAME_1 = '1'
    gl.IN_FILE_NAME_2 = '2'
    if out:
        gl.OUT_DIR = out
    else:
        gl.OUT_DIR = g.paths['OUT'] + 'file_match_out.csv'
    gl.TMP_1 = gl.TMP_DIR + 'tmp_1.csv'
    gl.TMP_2 = gl.TMP_DIR + 'tmp_2.csv'
    gl.EQUAL_OUT = False
    gl.DIFF_OUT = False


def init_tmp_dir():
    gl.TMP_DIR = g.paths['TMP'] + gl.TMP_FOLDER
    com.mkdirs(gl.TMP_DIR, True)


def set_dirs():

    dirs = {}

    dirs["in1"] = gl.IN_DIR + gl.IN_FILE_NAME_1 + gl.FILE_TYPE
    dirs["out1"] = gl.TMP_DIR + gl.OUT_FILE_NAME + "_1" + gl.FILE_TYPE
    dirs["in2"] = gl.IN_DIR + gl.IN_FILE_NAME_2 + gl.FILE_TYPE
    dirs["out2"] = gl.TMP_DIR + gl.OUT_FILE_NAME + "_2" + gl.FILE_TYPE
    dirs["out"] = gl.OUT_DIR + gl.OUT_FILE_NAME + gl.FILE_TYPE

    return dirs


def init_stf(in_file_dir, out_file_dir):

    gl.counters["file"] = 0
    gl.counters["row_max"] = 0
    gl.counters["iter"] = 0

    gl.bool["dup_key"] = False

    gl.prev_elt = []
    gl.cur_list = []
    gl.dup_list = []
    gl.dup_key_list = []
    gl.array_list = [[]]

    gl.OUT_DUP_FILE = gl.OUT_DIR + gl.OUT_DUP_FILE_NAME
    gl.OUT_DUP_KEY_FILE = gl.OUT_DIR + gl.OUT_FILE_NAME
    gl.OUT_DUP_KEY_FILE += "_dup_key" + gl.FILE_TYPE

    del_tmp_files()
    com.gen_header(in_file_dir, out_dir=out_file_dir)


def init_prev_elt(list_in):

    if gl.prev_elt == []:
        gl.prev_elt = ['' for elt in list_in[0]]


def init_compare(in_file_1, in_file_2):

    init_equal_diff_bool()

    gl.counters["c1"] = 1
    gl.counters["c2"] = 1
    gl.counters["out"] = 1
    gl.counters["diff"] = 0

    gl.msg = "{bn_1} lignes parcourues en {ds}."
    gl.msg += " {bn_2} lignes parcourues au total et {bn_3} "
    gl.msg += " lignes écrites dans le fichier de sortie."

    gl.LABEL_1 = gl.IN_FILE_NAME_1
    gl.LABEL_2 = gl.IN_FILE_NAME_2

    in_file_1.readline()
    in_file_2.readline()
    line_1_list = read_list(in_file_1)
    line_2_list = read_list(in_file_2)

    return (line_1_list, line_2_list)


def init_equal_diff_bool():

    if gl.EQUAL_OUT:
        if gl.counters["sf_read"] <= gl.MAX_ROW_EQUAL_OUT:
            gl.bool["EQUAL"] = True
            gl.bool["DIFF"] = gl.DIFF_OUT
        else:
            bn = com.big_number(gl.MAX_ROW_EQUAL_OUT)
            s = f"Attention les fichiers à comparer dépassent les {bn} lignes"
            s += " et le paramètre EQUAL_OUT est activé."
            s += "\nÉcrire les champs égaux dans le fichier de sortie ? (o/n)"
            if com.log_input(s) == "o":
                gl.bool["EQUAL"] = True
                gl.bool["DIFF"] = gl.DIFF_OUT
            else:
                gl.bool["EQUAL"] = False
                gl.bool["DIFF"] = True
    else:
        gl.bool["EQUAL"] = False
        gl.bool["DIFF"] = True


def del_tmp_files():

    counter = 0
    while True:
        try:
            counter += 1
            tmp_file_dir = gl.TMP_DIR + str(counter) + gl.FILE_TYPE
            os.remove(tmp_file_dir)
        except FileNotFoundError:
            break


def init_msf():

    gl.prev_elt = []
    gl.counters["tot_written_lines_out"] = 1
    gl.counters["row_max"] = floor(gl.MAX_ROW_LIST / gl.counters["file"])
    if gl.counters["row_max"] == 0:
        gl.counters["row_max"] = 1
    init_array_list()


def init_array_list():

    counter = 1
    gl.array_list = [[]]
    while counter < gl.counters["file"]:
        counter += 1
        gl.array_list.append([])

    nb = gl.counters["row_max"]
    s = "Tableau tampon initialisé."
    s += f" Il pourra contenir un maximum de {nb} lignes."
    com.log(s)
