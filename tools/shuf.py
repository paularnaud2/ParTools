from common import *
from random import *

IN_FILE = 'C:/Py/OUT/in_out.csv'
OUT_FILE = 'C:/Py/OUT/in_out.csv'
HAS_HEADER = True


def shuffle_csv():

    cur_list = load_csv(IN_FILE)
    if HAS_HEADER:
        header = cur_list[0]
        cur_list = cur_list[1:]
    shuffle(cur_list)
    cur_list = [header] + cur_list
    save_csv(cur_list, OUT_FILE)
    log("Fichier csv {} mélangé avec succès et sauvegardé à l'adresse '{}'".
        format(IN_FILE, OUT_FILE))
    print('')
