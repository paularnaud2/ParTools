import common as com
import qdd.gl as gl

from qdd.init import init_prev_elt
from qdd.functions import compare_elt
from qdd.functions import write_min_elt


def empty_array_list(out_file_dir):
    # on vide le tableau de listes triées dans le fichier de sortie trié
    s = "Vidange triée et sans doublons du tableau"
    s += " tampon dans le fichier de sortie..."
    com.log(s)
    n_col = len(gl.array_list)
    with open(out_file_dir, 'a', encoding='utf-8') as out_file:
        com.init_sl_time()
        (cursor, max_cursor, void_cursor) = init_cursors()
        init_prev_elt(gl.array_list[0])
        while cursor != void_cursor:
            (min_elt, min_col) = get_min_elt(cursor, n_col)
            write_min_elt(min_elt, out_file)
            if cursor[min_col] == max_cursor[min_col] - 1:
                # si l'une des listes a été entièrement parcourue,
                # alors on réécrit le tableau de listes
                # en supprimant les éléments déjà extraits vers
                # le fichier de sortie et on sort de la boucle
                cursor[min_col] += 1
                for i, l in enumerate(gl.array_list):
                    gl.array_list[i] = l[cursor[i]:]
                return
            cursor[min_col] += 1


def get_min_elt(cursor, n_col):
    # détermine le plus petit des éléments de chaque liste non déjà consommés

    min_col = -1
    while min_col < n_col - 1:
        min_col += 1
        if cursor[min_col] != -1:
            break
    min_elt = gl.array_list[min_col][cursor[min_col]]

    i = min_col + 1
    while i < n_col:
        if cursor[i] != -1:
            cur_elt = gl.array_list[i][cursor[i]]
            if compare_elt(cur_elt, min_elt) == "<":
                min_elt = cur_elt
                min_col = i
        i += 1

    return (min_elt, min_col)


def init_cursors():

    cursor = []
    max_cursor = []
    void_cursor = []

    i = 0
    while i < len(gl.array_list):
        if len(gl.array_list[i]) == 0:
            cursor.append(-1)
        else:
            cursor.append(0)
        void_cursor.append(-1)
        max_cursor.append(len(gl.array_list[i]))
        i += 1
    return (cursor, max_cursor, void_cursor)
