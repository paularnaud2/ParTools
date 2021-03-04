import os
import common as com

from tools import gl
from common import g

# Input variables default values
IN_FILE = 'C:/Py/IN/in.csv'
OUT_FIND_DUP = 'C:/Py/OUT/out_find_dup.csv'
OUT_DEL_DUP = 'C:/Py/OUT/out_del_dup.csv'

# Const
TMP_OUT = 'out_dup.csv'
MAX_DUP_PRINT = 5


def find_dup(in_dir, out_dir='', open_out=False, col=0):
    com.log("[toolDup] find_dup")
    (cur_list, out_dir) = init_find(in_dir, out_dir, col)
    bn = com.big_number(len(cur_list))
    com.log(f"Fichier chargé, {bn} lignes à analyser.")
    dup_list = find_dup_list(cur_list)
    finish_find(dup_list, out_dir, open_out)


def init_find(in_dir, out_dir, col):
    if not out_dir:
        tmp_path = g.paths['TMP'] + gl.TMP_FOLDER
        com.mkdirs(tmp_path)
        out_dir = tmp_path + TMP_OUT
    s = "Recherche des doublons dans "
    if col == 0:
        com.log(f"{s} le fichier {in_dir}")
        cur_list = com.load_txt(in_dir)
    else:
        com.log(f"{s}la colonne No.{col} du fichier {in_dir}")
        cur_list = com.load_csv(in_dir)
        cur_list = [x[col - 1] for x in cur_list]
        if com.has_header(cur_list):
            cur_list = cur_list[1:]

    return (cur_list, out_dir)


def del_dup(in_dir, out_dir, open_out=False):
    com.log("[toolDup] del_dup")
    com.log(f"Suppression des doublons dans le fichier {in_dir} en cours...")
    cur_list = com.load_txt(in_dir)
    bn = com.big_number(len(cur_list))
    com.log(f"Fichier chargé, {bn} lignes à analyser.")
    if com.has_header(cur_list):
        out_list = [cur_list[0]] + del_dup_list(cur_list[1:])
    else:
        out_list = del_dup_list(cur_list)
    finish_del(out_list, out_dir, open_out)


def find_dup_list(in_list):
    if not in_list:
        return []

    in_sorted = sorted(in_list)
    dup_list = []
    old_elt = in_sorted[0]
    for elt in in_sorted[1:]:
        if elt == old_elt:
            dup_list.append(elt)
        else:
            old_elt = elt

    if dup_list:
        dup_list = del_dup_list(dup_list)

    return dup_list


def del_dup_list(in_list):
    if not in_list:
        return []

    # if in_list elements are hashable
    if isinstance(in_list[0], str):
        out_list = list(set(in_list))
        out_list.sort()
        return out_list

    # if not
    in_sorted = sorted(in_list)
    out_list = [in_sorted[0]]
    old_elt = in_sorted[0]
    for elt in in_sorted[1:]:
        if elt > old_elt:
            out_list.append(elt)
            old_elt = elt

    return out_list


def finish_find(dup_list, out_dir, open_out):
    n = len(dup_list)
    if n == 0:
        com.log("Aucun doublon trouvé.")
        return

    bn = com.big_number(len(dup_list))
    s = f"{bn} doublons trouvés. Liste (tronquée à {MAX_DUP_PRINT} éléments) :"
    com.log(s)
    com.log_array(dup_list[:MAX_DUP_PRINT], 1)

    com.save_csv(dup_list, out_dir)
    com.log(f"Liste des doublons sauvegardée dans '{out_dir}'")
    if open_out:
        os.startfile(out_dir)


def finish_del(out_list, out_dir, open_out):

    com.log(f"Sauvegarde de la liste sans doublon triée dans '{out_dir}'...")
    com.save_list(out_list, out_dir)
    bn_out = com.big_number(len(out_list))
    com.log(f"Liste  sauvegardée, elle comporte {bn_out} lignes.")
    if open_out:
        os.startfile(out_dir)


if __name__ == '__main__':
    find_dup(IN_FILE, OUT_FIND_DUP, True)
    del_dup(IN_FILE, OUT_DEL_DUP, True)
