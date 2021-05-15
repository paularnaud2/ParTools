import re
import sys
from time import time

import partools.utils as u
from .finish import finish_xml
from . import gl


def parse_xml(in_path, out_path, **kwargs):
    u.log("[toolParseXML] parse_xml: start")
    start_time = time()
    u.init_kwargs(gl, kwargs)
    init_globals()
    gen_img_dict(in_path)
    save_img_dict(out_path)
    finish_xml(out_path, start_time)


def init_globals():
    gl.FIRST_TAG = ''
    gl.SUB_TAG = ''
    gl.N_ROW = 0


def gen_img_dict(in_path):
    s = f"Generating parse dictionary from file '{in_path}'..."
    u.log(s)
    gl.parse_dict = {}
    with open(in_path, 'r', encoding='utf-8', errors='ignore') as in_file:
        gl.N_READ = 0
        line = read_one_line(in_file)
        fill_parse_dict(line)
        u.init_sl_time()
        while line != '':
            line = read_one_line(in_file)
            fill_parse_dict(line)

    even_dict()
    u.log(f"Parse dictionary generated ({gl.N_READ} lines processed)")


def save_img_dict(out_path):
    u.log('Saving parse dictionary as csv...')
    header = []
    for elt in gl.parse_dict:
        header.append(elt)

    with open(out_path, 'w', encoding='utf-8') as out_file:
        u.write_csv_line(header, out_file)
        u.init_sl_time()
        gl.N_WRITE = 0
        while gl.N_WRITE < gl.N_ROW:
            cur_row = []
            for elt in gl.parse_dict:
                cur_row.append(gl.parse_dict[elt][gl.N_WRITE])
            u.write_csv_line(cur_row, out_file)
            gl.N_WRITE += 1
            u.step_log(gl.N_WRITE, gl.SL_STEP_WRITE, what='lines written')

    u.log(f"csv file saved in {out_path}")


def read_one_line(in_file):
    line = in_file.readline()
    gl.N_READ += 1
    u.step_log(gl.N_READ, gl.SL_STEP_READ, what='lines processed')

    return line


def fill_parse_dict(str_in):
    xml_out = get_xml(str_in)
    if xml_out != []:
        (tag, elt) = xml_out
        if tag in gl.MULTI_TAG_LIST:
            tag = tag + '_' + gl.SUB_TAG
        if tag in gl.parse_dict:
            gl.parse_dict[tag].append(elt)
            if tag == gl.FIRST_TAG:
                gl.N_ROW += 1
                complete_dict()
        else:
            if gl.N_ROW > 1 and gl.parse_dict != {}:
                # A new element (not in the first loop) is found
                new_col = gen_void_list(gl.N_ROW - 1)
                new_col.append(elt)
                gl.parse_dict[tag] = new_col
            else:
                gl.parse_dict[tag] = [elt]
                if len(gl.parse_dict) == 1:
                    gl.FIRST_TAG = tag
                    gl.N_ROW = 1


def get_xml(in_str):
    m1 = re.search(gl.RE_EXP_TAG_ELT, in_str)
    m2 = re.search(gl.RE_EXP_SUB_TAG, in_str)

    if m2 is not None:
        gl.SUB_TAG = m2.group(1)

    if m1 is None:
        return []

    tag = m1.group(1)
    elt = m1.group(2)
    elt = elt.replace(u.g.CSV_SEPARATOR, '')

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
            id = gl.parse_dict[gl.FIRST_TAG][gl.N_ROW - 2]
            s = (f"Warning: tag '{tag}' appears more than once (id = {id})."
                 " It must be added to MULTI_TAG_LIST.")
            u.log(s)
            u.log_print("Execution aborted")
            sys.exit()


def even_dict():
    for tag in gl.parse_dict:
        n = len(gl.parse_dict[tag])
        if n < gl.N_ROW:
            gl.parse_dict[tag].append('')
