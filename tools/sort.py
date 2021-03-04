from qdd.main import sort_file
import qdd.gl as gl
import os
from common import log
import common as com
from shutil import copyfile

#IN_DIR = "C:/Py/IN/Tests/test_sort_dup.csv"
IN_DIR = "C:/Py/OUT/in_out.csv"
OUT_DIR = "C:/Py/OUT/in_out.csv"
OUT_DIR_TMP = com.TMP_PATH_TOOLS + 'out_tmp.csv'


def sort_csv_file_main():

    if IN_DIR == OUT_DIR:
        sort_file(IN_DIR, OUT_DIR_TMP)
        copyfile(OUT_DIR_TMP, OUT_DIR)
        os.remove(OUT_DIR_TMP)
        log("Fichier temporaire supprimé. Fichier de sortie sauvegardé à l'adresse '{}'"
            .format(OUT_DIR))
    else:
        sort_file(IN_DIR, OUT_DIR)
