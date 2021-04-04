import re
from os import remove

import pytools.common as com
from pytools.tools import gl


def split_file(in_dir, out_dir='', **kwargs):
    com.log("[toolSplit] split_file: start")
    com.init_kwargs(gl, kwargs)
    init_globals()
    (file_dir, file_name, ext) = split_in_dir(in_dir, out_dir)
    gl.header = com.get_header(in_dir)
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        while True:
            gl.N_OUT += 1
            out_dir = f'{file_dir}{file_name}_{gl.N_OUT}.{ext}'
            if not gen_split_out(out_dir, in_file):
                break

    com.log("[toolSplit] split_file: end")
    com.log_print()


def init_globals():
    gl.QUIT = False
    gl.N_OUT = 0


def split_in_dir(in_dir, out_dir):
    exp = r'(.*)/(\w*).(\w*)$'
    m = re.search(exp, in_dir)
    (file_dir, file_name, ext) = (m.group(1), m.group(2), m.group(3))
    file_dir += '/'
    if out_dir:
        file_dir = out_dir

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
    s = f"Splitted file no. {file_nb} ({split_dir}) successfully generated"
    if in_line == '':
        if i == 2 and gl.ADD_HEADER:
            remove(split_dir)
        else:
            com.log(s)
        return False

    com.log(s)

    if gl.N_OUT >= gl.MAX_FILE_NB:
        com.log(f"Maximum number of files reached ({gl.MAX_FILE_NB})")
        return False

    return True
