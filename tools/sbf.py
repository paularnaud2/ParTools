from common import *
import tools.gl as gl
from os import startfile

IN_FILE = 'C:/Py/IN/2020_10_07_SITES.xml'
# IN_FILE = 'C:/Py/IN/2020_09_03_SITES_1.xml'
OUT_FILE = 'C:/Py/OUT/out_sbf.xml'
LINE_PER_LINE = True
LOOK_FOR = '06381331333501'
# LOOK_FOR = '00001291940930'
MAX_LIST_SIZE = 5 * 10**6
PRINT_SIZE = 100
BUFFER_SIZE = 100 * 10**3


def search_big_file():

    init()
    with open(IN_FILE, 'r', encoding='utf-8', errors='ignore') as in_file:
        while not gl.bool["EOF"]:
            fill_cur_list(in_file)
            if search_cur_list():
                break

    finish()


def init():

    gl.bool["found"] = False
    gl.bool["EOF"] = False
    gl.counters["main"] = 0
    gl.counters["list"] = 0
    gl.counters["cur_list_row"] = 0
    gl.cur_list = []
    if LINE_PER_LINE:
        gl.txt["sl_string"] = "{bn_1} lignes parcourues en {ds}"
    else:
        gl.txt[
            "sl_string"] = "{bn_1} buffers de {bn_3} caractères parcourus en {ds}"

    s = "Recherche de la chaîne '{}' dans le fichier '{}'..."
    s = s.format(LOOK_FOR, IN_FILE)
    log(s)


def finish():

    if gl.bool["found"]:
        lowI = gl.counters["row"] - PRINT_SIZE // 2
        if lowI < 0:
            lowI = 0
        highI = gl.counters["row"] + PRINT_SIZE // 2
        save_list(gl.cur_list[lowI:highI], OUT_FILE)
        s = "Liste courante écrite dans le fichier '{}'"
        log(s.format(OUT_FILE))
        startfile(OUT_FILE)
    else:
        s = "Fichier entier parcouru ({} lignes, {} listes temporaires), chaîne de caractère '{}' introuvable"
        log(
            s.format(big_number(gl.counters["main"]), gl.counters["list"],
                     LOOK_FOR))

    duration = get_duration_ms(gl.start_time)
    ds = get_duration_string(duration)
    s = "Exécution terminée en {}"
    log(s.format(ds))


def fill_cur_list(in_file):

    gl.counters["list"] += 1
    if gl.counters["list"] > 1:
        # on ajoute la dernière ligne de la liste précédente pour garantir l'intégrité de la chaîne cherchée
        n = len(gl.cur_list)
        last_line = gl.cur_list[n - 1]
        gl.cur_list = []
        gl.cur_list.append(last_line)
        gl.counters["cur_list_row"] = 1
    else:
        gl.cur_list = []
        gl.counters["cur_list_row"] = 0
    s = "Génération de la liste temporaire No.{}..."
    log(s.format(gl.counters["list"]), 1)

    while gl.counters["cur_list_row"] < MAX_LIST_SIZE:
        gl.counters["cur_list_row"] += 1
        if LINE_PER_LINE:
            line = get_line_lpl(in_file)
        else:
            line = get_line_buf(in_file)
        if gl.bool["EOF"]:
            return
        gl.cur_list.append(line)
    log("Liste temporaire générée", 1)


def get_line_lpl(in_file):

    line = in_file.readline()

    if line == '':
        gl.bool["EOF"] = True
        return
    return line


def get_line_buf(in_file):
    # Pour le buffer, on prend la fin de la ligne précédente pour garantir l'intégrité de la chaîne cherchée

    line = in_file.read(BUFFER_SIZE)
    if gl.counters["cur_list_row"] > 1:
        prev_line = gl.cur_list[gl.counters["cur_list_row"] - 2].strip('\n')
        end_prev_line = prev_line[-len(LOOK_FOR):]
        line = end_prev_line + line
    if line == '':
        gl.bool["EOF"] = True
        return
    return line + '\n'


def search_cur_list():

    s = "Recherche de la chaîne '{}' dans la liste temporaire No.{}"
    log(s.format(LOOK_FOR, gl.counters["list"]), 1)
    i = 0
    for elt in gl.cur_list:
        i += 1
        gl.counters["main"] += 1
        j = elt.find(LOOK_FOR)
        if j != -1:
            found_msg(i, j)
            gl.bool["found"] = True
            return True

    s = "Recherche dans la liste temporaire terminée, chaîne non trouvée ({} lignes parcourues au total)"
    log(s.format(big_number(gl.counters["main"])), 1)
    return False


def found_msg(i, j):

    bn = big_number(gl.counters["main"])
    gl.counters["row"] = i
    if LINE_PER_LINE:
        s = "Chaîne trouvée à la {}ème ligne de la liste tampon No.{} (ligne globale No.{}) ligne en position {} !"
        log(s.format(big_number(i), gl.counters["list"], bn, j + 1))
    else:
        s = "Chaîne trouvée dans le buffer No. {} (liste tampon No.{}) en position {}"
        s = s.format(bn, gl.counters["list"], big_number(j + 1))
        log(s)
