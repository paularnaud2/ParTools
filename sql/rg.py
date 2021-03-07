import os
import re
import sql.gl as gl
import common as com

from common import g
from shutil import move


def get_rg_file_name(in_str):
    exp = '(.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m = re.search(exp, in_str)
    exp_comment = '(.*-{2,}.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m_comment = re.search(exp_comment, in_str)
    if m and not m_comment:
        rg_file_name = m.group(2)
        return rg_file_name
    else:
        return ''


def gen_range_list(rg_file_name):
    if rg_file_name != '':
        gl.bools['RANGE_QUERY'] = True
        range_dir = gl.RANGE_PATH + rg_file_name + gl.FILE_TYPE
        range_list = com.load_txt(range_dir)
        com.log(f"Range query detected. Base query:\n{gl.query}\n;")
    else:
        gl.bools['RANGE_QUERY'] = False
        range_list = ['MONO']

    return range_list


def restart(range_list):
    file_list = com.get_file_list(gl.TMP_PATH)
    a = len(file_list)
    if a == 0:
        return range_list

    if gl.bools['RANGE_QUERY'] is False:
        com.mkdirs(gl.TMP_PATH, True)
        return range_list

    s = "Work in progress detected. Kill? (y/n)"
    if gl.TEST_RESTART:
        com.log(s)
        com.log_print("n (TEST_RESTART = True)")
    elif com.log_input(s) == 'y':
        com.mkdirs(gl.TMP_PATH, True)
        return range_list

    list_out = modify_restart(range_list, file_list)
    com.log("Range list modified")
    return list_out


def modify_restart(range_list, file_list):
    # Modifies the range list by deleting element already
    # in file list. EC files are also deleted.

    list_out = []
    for elt in range_list:
        comp_elt = elt + gl.FILE_TYPE
        comp_elt_ec = elt + gl.EC + gl.FILE_TYPE
        if comp_elt not in file_list:
            list_out.append(elt)
        if comp_elt_ec in file_list:
            ec_path = gl.TMP_PATH + comp_elt_ec
            os.remove(ec_path)
            com.log(f"EC file {ec_path} deleted")

    return list_out


def move_tmp_folder():

    gl.bools["MERGE_OK"] = False
    out_dir = gl.OUT_RG_DIR

    com.mkdirs(out_dir, True)
    com.log(f"Output folder {out_dir} created")

    file_list = com.get_file_list(gl.TMP_PATH)
    n = len(file_list)
    com.log(f"Moving {n} files to the output folder....")
    for elt in file_list:
        cur_dir = gl.TMP_PATH + elt
        target_dir = out_dir + elt
        move(cur_dir, target_dir)
    com.log(f"Files moved to {out_dir}")


def merge_tmp_files():
    (file_list, out_file, return_bool) = init_merge()
    if return_bool:
        return
    i = 0
    for elt in file_list:
        i += 1
        cur_dir = gl.TMP_PATH + elt
        if i == 1:
            com.merge_files(cur_dir, out_file, remove_header=False)
        else:
            com.merge_files(cur_dir, out_file, remove_header=True)
        os.remove(cur_dir)

    n = len(file_list)
    com.log(f"Merging and deleting of the {n} temporary files over")


def init_merge():
    gl.bools["MERGE_OK"] = True
    file_list = com.get_file_list(gl.TMP_PATH)
    out_file = gl.OUT_FILE
    if check_ec(file_list) or check_mono(file_list, out_file):
        return ('', '', True)

    if os.path.exists(out_file):
        os.remove(out_file)

    n = len(file_list)
    com.log(f"Merging and deleting {n} temporary files...")
    return (file_list, out_file, False)


def check_ec(file_list):
    for elt in file_list:
        if gl.EC in elt:
            s = f"EC file found ({elt})."
            s += " Meging of temporary files aborted."
            com.log(s)
            gl.bools["MERGE_OK"] = False
            return True
    return False


def check_mono(file_list, out_file):
    if file_list == ['MONO' + gl.FILE_TYPE]:
        cur_dir = gl.TMP_PATH + file_list[0]
        move(cur_dir, out_file)
        return True
    return False
