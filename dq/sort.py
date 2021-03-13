import sys
import common as com
import dq.gl as gl

from time import time
from dq.init import init_stf
from dq.init import init_msf
from dq.gstf import gen_sorted_temp_files
from dq.functions import temp_files
from dq.functions import array_list_not_void
from dq.fill_al import fill_array_list
from dq.empty_al import empty_array_list


def sort_file(in_file_dir, out_file_dir, prompt=False, nb=0):
    # nb variable is used to differentiate input file when main run is dq

    com.log(f"[dq] sort_file: start ({in_file_dir})")
    start_time = time()
    init_stf(in_file_dir, out_file_dir)
    gen_sorted_temp_files(in_file_dir, out_file_dir)
    com.log_print('|')
    nb_files = gl.c_file
    if nb_files > 1:
        s = f"Generating sorted output file from {nb_files} sorted temporary files..."
        com.log(s)
        merge_sorted_files(out_file_dir)
    finish(out_file_dir, prompt, nb, start_time)
    com.log_print('|')


def merge_sorted_files(out_file_dir):

    init_msf()
    while temp_files() or array_list_not_void():
        fill_array_list()
        empty_array_list(out_file_dir)


def finish(out_file_dir, prompt, nb, start_time):

    n_dup_key = len(gl.dup_key_list)
    n_dup = len(gl.dup_list)
    bn1 = com.big_number(gl.c_tot_out)
    bn2 = com.big_number(n_dup)
    s = f"Output file {out_file_dir} successfully generated"
    s += f" ({bn1} lines written, {bn2} duplicates removed)."
    com.log(s)
    if n_dup > 0:
        if nb != 0:
            out_dup = gl.OUT_DUP_FILE + str(nb) + gl.FILE_TYPE
        else:
            out_dup = gl.OUT_DUP_FILE + gl.FILE_TYPE
        com.save_csv(gl.dup_list, out_dup)
        com.log(f"Duplicates list written in {out_dup}")
        com.log_example(gl.dup_list)
    if n_dup_key > 0:
        if prompt:
            prompt_dup_key(n_dup_key)
        else:
            com.save_csv(gl.dup_key_list, gl.OUT_DUP_KEY_FILE)
            s = f"{n_dup_key} key duplicates found. List written in {gl.OUT_DUP_KEY_FILE}"
            com.log(s)

    dstr = com.get_duration_string(start_time)
    com.log(f"[dq] sort_file: end ({dstr})")


def prompt_dup_key(n_dup_key):

    com.log_print('|')
    bn = com.big_number(n_dup_key)
    s = f"Warning: {bn} different lines with the same research key were identified"
    com.log(s)
    com.log_example(gl.dup_key_list)

    s = "\nFile comparison may not work correctly. Here are your options:"
    s += "\na -> save duplicates list and quit"
    s += "\nb -> quit without saving duplicates list"
    s += "\nc -> save duplicates list and continue"
    s += "\nd -> continue without saving duplicates list"
    if gl.TEST_PROMPT_DK:
        com.log_print(s)
        com.log_print('c (TEST_PROMPT_DK = True)')
        command = 'c'
    else:
        command = com.log_input(s)
    com.log_print('|')
    if command == 'a' or command == 'c':
        com.save_csv(gl.dup_key_list, gl.OUT_DUP_KEY_FILE)
        s = f"List of key duplicates written in file {gl.OUT_DUP_KEY_FILE}"
        com.log(s)
    if command == 'a' or command == 'b':
        sys.exit()
