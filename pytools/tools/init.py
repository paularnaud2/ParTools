import pytools.common as com
import pytools.common.g as g

from . import gl


def init_find_dup(in_dir, out_dir, col):
    if not out_dir:
        tmp_path = g.paths['TMP'] + gl.TMP_FOLDER
        com.mkdirs(tmp_path)
        out_dir = tmp_path + gl.TMP_OUT
    s = "Searching duplicates in "
    if col == 0:
        com.log(f"{s} file {in_dir}")
        cur_list = com.load_txt(in_dir)
    else:
        com.log(f"{s}column no. {col} of file {in_dir}")
        cur_list = com.load_csv(in_dir)
        cur_list = [x[col - 1] for x in cur_list]
        if com.has_header(cur_list):
            cur_list = cur_list[1:]

    return (cur_list, out_dir)


def init_rbf():
    gl.c_main = 0
    gl.c_read = 1

    txt = '\n' + "Enter -> continue"
    txt += '\n' + "q -> quit"
    txt += '\n' + "e -> go to EOF"
    if gl.LINE_PER_LINE:
        txt += '\n' + "or enter the number of lines to skip"
    else:
        txt += '\n' + "or enter the number of buffers to skip"
    gl.s_prompt = txt


def init_sbf(in_dir, look_for):

    gl.FOUND = False
    gl.EOF = False
    gl.c_main = 0
    gl.c_list = 0
    gl.c_cur_row = 0
    gl.cur_list = []
    gl.LOOK_FOR = look_for
    if gl.LINE_PER_LINE:
        gl.s_sl = "{bn_1} lines read in {dstr}"
    else:
        gl.s_sl = "{bn_1} buffers of {bn_3} characters read in {dstr}"

    gl.s_init = f"Searching string '{gl.LOOK_FOR}' in file '{in_dir}'..."
