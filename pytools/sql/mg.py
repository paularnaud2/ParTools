import os
from shutil import move

import pytools.common as com
from . import gl
from .groupby import group_by


def finish():
    if gl.MERGE_FILES or not gl.range_query:
        merge_tmp_files()
        group_by()
    else:
        move_tmp_folder()


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
    gl.MERGE_OK = True
    file_list = com.get_file_list(gl.TMP_PATH)
    out_file = gl.OUT_FILE
    if check_ec(file_list) or check_mono(file_list, out_file):
        return ('', '', True)

    if os.path.exists(out_file):
        os.remove(out_file)

    n = len(file_list)
    com.log(f"Merging and deleting {n} temporary files...")
    return (file_list, out_file, False)


def move_tmp_folder():

    gl.MERGE_OK = False
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


def check_ec(file_list):
    for elt in file_list:
        if gl.EC in elt:
            s = (f"EC file found ({elt})."
                 " Meging of temporary files aborted.")
            com.log(s)
            gl.MERGE_OK = False
            return True
    return False


def check_mono(file_list, out_file):
    if file_list == ['MONO' + gl.FILE_TYPE]:
        cur_dir = gl.TMP_PATH + file_list[0]
        move(cur_dir, out_file)
        return True
    return False
