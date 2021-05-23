import os
from shutil import move

import partools.utils as u
from . import gl


def finish():
    from .groupby import group_by

    if gl.MERGE_FILES or len(gl.QUERY_LIST) == 1:
        merge_tmp_files()
        group_by()
    else:
        move_tmp_folder()


def merge_tmp_files():
    (file_list, out_file, return_bool) = init_merge()
    if return_bool:
        return
    for i, elt in enumerate(file_list, 1):
        if i == 1:
            u.append_file(elt, out_file, remove_header=False)
        else:
            u.append_file(elt, out_file, remove_header=True)
        os.remove(elt)

    n = len(file_list)
    u.log(f"Merging and deleting of the {n} temporary files over")


def init_merge():
    gl.MERGE_OK = True
    file_list = u.list_files(gl.TMP_DIR)
    out_file = gl.OUT_PATH
    if check_ec(file_list) or check_mono(file_list, out_file):
        return ('', '', True)

    if os.path.exists(out_file):
        os.remove(out_file)

    n = len(file_list)
    u.log(f"Merging and deleting {n} temporary files...")
    return (file_list, out_file, False)


def move_tmp_folder():

    gl.MERGE_OK = False
    out_dir = gl.OUT_DIR

    u.mkdirs(out_dir, True)
    u.log(f"Output folder {out_dir} created")

    file_list = u.list_files(gl.TMP_DIR, False)
    n = len(file_list)
    u.log(f"Moving {n} files to the output folder....")
    for elt in file_list:
        cur_path = gl.TMP_DIR + elt
        target_path = out_dir + elt
        move(cur_path, target_path)
    u.log(f"Files moved to {out_dir}")


def check_ec(file_list):
    for elt in file_list:
        if gl.EC in elt:
            s = (f"EC file found ({elt})."
                 " Meging of temporary files aborted.")
            u.log(s)
            gl.MERGE_OK = False
            return True
    return False


def check_mono(file_list, out_file):
    if file_list == ['MONO' + gl.FILE_TYPE]:
        cur_path = gl.TMP_DIR + file_list[0]
        move(cur_path, out_file)
        return True
    return False
