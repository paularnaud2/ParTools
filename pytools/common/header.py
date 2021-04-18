from . import g
from .log import log
from .log import log_print
from .csv import csv_to_list


def get_header(in_path, csv=False):
    with open(in_path, 'r', encoding='utf-8') as in_file:
        header = in_file.readline().strip('\n')

    if csv:
        header = csv_to_list(header)

    return header


def gen_header(in_path, last_field='', out_path=''):

    if has_header(in_path):
        header = get_header(in_path)
    else:
        first_line = get_header(in_path, True)
        header = g.DEFAULT_FIELD + "_1"
        if len(first_line) > 1:
            counter = 1
            for elt in first_line[1:]:
                counter += 1
                header = f'{header}{g.CSV_SEPARATOR}{g.DEFAULT_FIELD}_{counter}'

    if last_field:
        header = header + g.CSV_SEPARATOR + last_field

    if out_path:
        with open(out_path, 'w', encoding='utf-8') as out_file:
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


def check_header(in_path):
    if not has_header(in_path):
        s = f"Error: the input file {in_path} must have a header"
        log(s)
        s = "Make sure the first elements of the first two lines are of different lengths"
        log_print(s)
        raise Exception(g.E_MH)
