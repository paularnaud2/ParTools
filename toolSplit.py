import re
import common as com
import tools.gl as gl

from os import remove


def init_var(params):
    # Input variables default values
    gl.IN_DIR = 'C:/Py/IN/Enedis_APR_20201030_092105813.xml'
    gl.OUT_DIR = ''
    gl.MAX_LINE = 2 * 10**3
    gl.MAX_FILE_NB = 3
    gl.ADD_HEADER = True
    com.init_params(gl, params)

    # Global variables
    gl.QUIT = False
    gl.N_OUT = 0


def split_file(**params):
    com.log("[toolSplit] split_file")
    init_var(params)
    (file_dir, file_name, ext) = split_in_dir()
    gl.header = com.get_header(gl.IN_DIR)
    with open(gl.IN_DIR, 'r', encoding='utf-8') as in_file:
        while True:
            gl.N_OUT += 1
            out_dir = f'{file_dir}/{file_name}_{gl.N_OUT}.{ext}'
            if not gen_split_out(out_dir, in_file):
                break

    com.log("Traitement terminé")
    com.log_print()


def split_in_dir():
    exp = r'(.*)/(\w*).(\w*)$'
    m = re.search(exp, gl.IN_DIR)
    (file_dir, file_name, ext) = (m.group(1), m.group(2), m.group(3))
    if gl.OUT_DIR:
        file_dir = gl.OUT_DIR

    return (file_dir, file_name, ext)


def gen_split_out(split_dir, in_file):

    with open(split_dir, 'w', encoding='utf-8') as file:
        i = 0
        if gl.N_OUT > 1 and gl.ADD_HEADER:
            file.write(gl.header + '\n')
            i = 1
        in_line = 'init'
        while i < gl.MAX_LINE and in_line != '':
            i += 1
            in_line = in_file.readline()
            file.write(in_line)

    file_nb = gl.N_OUT
    s = f"Fichier découpé No.{file_nb} ({split_dir}) généré avec succès"
    if in_line == '':
        if i == 2 and gl.ADD_HEADER:
            remove(split_dir)
        else:
            com.log(s)
        return False

    com.log(s)

    if gl.N_OUT >= gl.MAX_FILE_NB:
        s = f"Nombre maximum de fichiers atteint ({gl.MAX_FILE_NB} fichiers max)."
        s += " Arrêt du traitement"
        com.log(s)
        return False

    return True


if __name__ == '__main__':
    split_file()
