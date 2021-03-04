from common import g
from .csv import csv_to_list
from .log import log
from .log import log_print


def get_header(in_dir, csv=False):
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        header = in_file.readline().strip('\n')

    if csv:
        header = csv_to_list(header)

    return header


def gen_header(in_dir, last_field='', out_dir=''):

    if has_header(in_dir):
        header = get_header(in_dir)
    else:
        first_line = get_header(in_dir, True)
        header = g.DEFAULT_FIELD + "_1"
        if len(first_line) > 1:
            counter = 1
            for elt in first_line[1:]:
                counter += 1
                header = f'{header}{g.CSV_SEPARATOR}{g.DEFAULT_FIELD}_{counter}'

    if last_field:
        header = header + g.CSV_SEPARATOR + last_field

    if out_dir:
        with open(out_dir, 'w', encoding='utf-8') as out_file:
            out_file.write(header + '\n')

    return header


def has_header(in_var):
    out = True
    if isinstance(in_var, str):
        ar = []
        with open(in_var, 'r', encoding='utf-8') as in_file:
            ar.append(csv_to_list(in_file.readline()))
            ar.append(csv_to_list(in_file.readline()))
    else:
        ar = in_var

    if not ar:
        return False
    if len(ar) == 1:
        return True
    if isinstance(ar[0], str):
        if len(ar[0]) == len(ar[1]):
            out = False
    else:
        if len(ar[0][0]) == len(ar[1][0]):
            out = False

    return out


def check_header(in_dir):
    if not has_header(in_dir):
        s = f"Erreur : Le fichier d'entrée {in_dir} doit contenir une en-tête"
        log(s)
        s = "Assurez-vous que les premiers éléments des deux premières lignes"
        s += " sont de longeur différente."
        log_print(s)
        raise Exception(g.E_MH)
