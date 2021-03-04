import re
import os
import common as com
import tools.gl as gl

from common import g

# Const
MULTI_TAG_LIST = [
    'libelle',
    'civilite',
    'nom',
    'prenom',
    'telephone1Num',
    'telephone2Num',
    'adresseEmail',
]
RE_EXP_TAG_ELT = '<(.*)>(.*)</(.*)>'
RE_EXP_SUB_TAG = r'<(\w[^<]*\w)>$'
SL_STEP_READ = 1000 * 10**3
SL_STEP_WRITE = 100 * 10**3


def init(params):
    # Input variables default values
    gl.IN_DIR = 'test/tools/xml_in.xml'
    gl.OUT_DIR = 'C:/Py/OUT/out.csv'
    gl.OPEN_OUT_FILE = False
    com.init_params(gl, params)

    # Global variables
    gl.FIRST_TAG = ''
    gl.SUB_TAG = ''
    gl.N_ROW = 0


def parse_xml(**params):
    com.log("[toolParseXML] parse_xml")
    init(params)
    gen_img_dict()
    save_img_dict()
    finish()


def finish():
    dur = com.get_duration_ms(gl.start_time)
    bn = com.big_number(gl.N_WRITE)
    s = "Parsing terminé. {} lignes écrites en {}."
    s = s.format(bn, com.get_duration_string(dur))
    com.log(s)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        os.startfile(gl.OUT_DIR)


def gen_img_dict():
    s = f"Génération du dictionnaire image à partir du fichier '{gl.IN_DIR}'..."
    com.log(s)
    gl.parse_dict = {}
    with open(gl.IN_DIR, 'r', encoding='utf-8', errors='ignore') as in_file:
        gl.N_READ = 0
        line = read_one_line(in_file)
        fill_parse_dict(line)
        com.init_sl_time()
        while line != '':
            line = read_one_line(in_file)
            fill_parse_dict(line)

    even_dict()
    com.log('Dictionnaire image généré.')


def save_img_dict():
    com.log('Sauvegarde du dictionnaire au format csv...')
    header = []
    for elt in gl.parse_dict:
        header.append(elt)

    with open(gl.OUT_DIR, 'w', encoding='utf-8') as out_file:
        com.write_csv_line(header, out_file)
        com.init_sl_time()
        gl.N_WRITE = 0
        while gl.N_WRITE < gl.N_ROW:
            cur_row = []
            for elt in gl.parse_dict:
                cur_row.append(gl.parse_dict[elt][gl.N_WRITE])
            com.write_csv_line(cur_row, out_file)
            gl.N_WRITE += 1
            com.step_log(gl.N_WRITE, SL_STEP_WRITE, what='lignes écrites')

    com.log("Fichier csv généré à l'adresse {}".format(gl.OUT_DIR))


def read_one_line(in_file):
    line = in_file.readline()
    gl.N_READ += 1
    com.step_log(gl.N_READ, SL_STEP_READ, what='lignes traitées')

    return line


def fill_parse_dict(str_in):
    xml_out = get_xml(str_in)
    if xml_out != []:
        (tag, elt) = xml_out
        if tag in MULTI_TAG_LIST:
            tag = tag + '_' + gl.SUB_TAG
        if tag in gl.parse_dict:
            gl.parse_dict[tag].append(elt)
            if tag == gl.FIRST_TAG:
                gl.N_ROW += 1
                complete_dict()
        else:
            if gl.N_ROW > 1 and gl.parse_dict != {}:
                # on rencontre un nouvel élément
                # (absent dans la première boucle)
                new_col = gen_void_list(gl.N_ROW - 1)
                new_col.append(elt)
                gl.parse_dict[tag] = new_col
            else:
                gl.parse_dict[tag] = [elt]
                if len(gl.parse_dict) == 1:
                    gl.FIRST_TAG = tag
                    gl.N_ROW = 1


def get_xml(in_str):
    m1 = re.search(RE_EXP_TAG_ELT, in_str)
    m2 = re.search(RE_EXP_SUB_TAG, in_str)

    if m2 is not None:
        gl.SUB_TAG = m2.group(1)

    if m1 is None:
        return []

    tag = m1.group(1)
    elt = m1.group(2)
    elt = elt.replace(g.CSV_SEPARATOR, '')

    return (tag, elt)


def gen_void_list(size):
    i = 0
    out_list = []
    while i < size:
        i = i + 1
        out_list.append('')

    return out_list


def complete_dict():
    for tag in gl.parse_dict:
        n = len(gl.parse_dict[tag])
        if n < gl.N_ROW - 1:
            gl.parse_dict[tag].append('')
        elif n >= gl.N_ROW and tag != gl.FIRST_TAG:
            s = "Attention, la balise '{}' apparaît en doublon (id = {})."
            s += " Elle doit être ajoutée à la liste 'MULTI_TAG_LIST'"
            print(s.format(tag, gl.parse_dict[gl.FIRST_TAG][gl.N_ROW - 3]))
            import sys
            sys.exit()


def even_dict():
    for tag in gl.parse_dict:
        n = len(gl.parse_dict[tag])
        if n < gl.N_ROW:
            gl.parse_dict[tag].append('')


if __name__ == '__main__':
    parse_xml(OPEN_OUT_FILE=True)
