import common as com
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
        while not gl.EOF:
            fill_cur_list(in_file)
            if search_cur_list():
                break

    finish()


def init():

    gl.FOUND = False
    gl.EOF = False
    gl.c_main = 0
    gl.c_list = 0
    gl.c_cur_row = 0
    gl.cur_list = []
    if LINE_PER_LINE:
        gl.s_sl = "{bn_1} lignes parcourues en {dstr}"
    else:
        gl.s_sl = "{bn_1} buffers de {bn_3} caractères parcourus en {dstr}"

    s = "Recherche de la chaîne '{}' dans le fichier '{}'..."
    s = s.format(LOOK_FOR, IN_FILE)
    com.log(s)


def finish():

    if gl.FOUND:
        lowI = gl.c_row - PRINT_SIZE // 2
        if lowI < 0:
            lowI = 0
        highI = gl.c_row + PRINT_SIZE // 2
        com.save_list(gl.cur_list[lowI:highI], OUT_FILE)
        s = "Liste courante écrite dans le fichier '{}'"
        com.log(s.format(OUT_FILE))
        startfile(OUT_FILE)
    else:
        s = "Fichier entier parcouru ({} lignes, {} listes temporaires), chaîne de caractère '{}' introuvable"
        com.log(s.format(com.big_number(gl.c_main), gl.c_list, LOOK_FOR))

    dstr = com.get_duration_string(gl.start_time)
    com.log(f"Exécution terminée en {dstr}")


def fill_cur_list(in_file):

    gl.c_list += 1
    if gl.c_list > 1:
        # on ajoute la dernière ligne de la liste précédente pour garantir l'intégrité de la chaîne cherchée
        n = len(gl.cur_list)
        last_line = gl.cur_list[n - 1]
        gl.cur_list = []
        gl.cur_list.append(last_line)
        gl.c_cur_row = 1
    else:
        gl.cur_list = []
        gl.c_cur_row = 0
    s = "Génération de la liste temporaire No.{}..."
    com.log(s.format(gl.c_list), 1)

    while gl.c_cur_row < MAX_LIST_SIZE:
        gl.c_cur_row += 1
        if LINE_PER_LINE:
            line = get_line_lpl(in_file)
        else:
            line = get_line_buf(in_file)
        if gl.EOF:
            return
        gl.cur_list.append(line)
    com.log("Liste temporaire générée", 1)


def get_line_lpl(in_file):

    line = in_file.readline()

    if line == '':
        gl.EOF = True
        return
    return line


def get_line_buf(in_file):
    # Pour le buffer, on prend la fin de la ligne précédente pour garantir l'intégrité de la chaîne cherchée

    line = in_file.read(BUFFER_SIZE)
    if gl.c_cur_row > 1:
        prev_line = gl.cur_list[gl.c_cur_row - 2].strip('\n')
        end_prev_line = prev_line[-len(LOOK_FOR):]
        line = end_prev_line + line
    if line == '':
        gl.EOF = True
        return
    return line + '\n'


def search_cur_list():

    s = "Recherche de la chaîne '{}' dans la liste temporaire No.{}"
    com.log(s.format(LOOK_FOR, gl.c_list), 1)
    i = 0
    for elt in gl.cur_list:
        i += 1
        gl.c_main += 1
        j = elt.find(LOOK_FOR)
        if j != -1:
            found_msg(i, j)
            gl.FOUND = True
            return True
    bn = com.big_number(gl.c_main)
    s = f"Recherche dans la liste temporaire terminée, chaîne non trouvée ({bn} lignes parcourues au total)"
    com.log(s)
    return False


def found_msg(i, j):

    bn = com.big_number(gl.c_main)
    gl.c_row = i
    if LINE_PER_LINE:
        s = "Chaîne trouvée à la {}ème ligne de la liste tampon No.{} (ligne globale No.{}) ligne en position {} !"
        com.log(s.format(com.big_number(i), gl.c_list, bn, j + 1))
    else:
        s = "Chaîne trouvée dans le buffer No. {} (liste tampon No.{}) en position {}"
        s = s.format(bn, gl.c_list, com.big_number(j + 1))
        com.log(s)
