import os
import pytools.common as com

from . import gl


def fill_array_list():
    # Filling buffer array with tmp files

    gl.c_iter += 1
    s = "Filling buffer array - Iteration no. {}"
    com.log(s.format(gl.c_iter))
    gl.c_col = 0
    while gl.c_col < gl.c_file:
        gl.c_col += 1
        n = gl.c_col
        com.log(f"Reading tmp file no. {n}...", 1)
        tmp_file_dir = f"{gl.TMP_DIR}tmp_{n}{gl.FILE_TYPE}"
        if n > 1:
            com.log("Deleting previous tmp list...", 1)
            del tmp_file_list
            com.log("Previous tmp list deleted", 1)
        tmp_file_list = read_tmp_file(tmp_file_dir)
        # if current tmp file doesn't exist, we directly jump to the next one
        if tmp_file_list == "empty":
            com.log(f"Tmp file no. {n} not found", 1)
            continue
        com.log(f"Writing tmp file no. {n} in buffer array...", 1)
        n_written_rows = write_tmp_file_in_array(tmp_file_list)
        com.log(f"Rewriting tmp file no. {n}...", 1)
        rewrite_tmp_file(tmp_file_list, tmp_file_dir, n_written_rows)


def read_tmp_file(tmp_file_dir):
    # Reading one tmp file

    try:
        with open(tmp_file_dir, 'r', encoding='utf-8') as tmp_file:
            tmp_file_list = tmp_file.readlines()
    except FileNotFoundError:
        tmp_file_list = "empty"
    except MemoryError:
        com.log_print(MemoryError)
        breakpoint()

    return tmp_file_list


def write_tmp_file_in_array(tmp_file_list):
    # Writing part of a tmp file in buffer array so that
    # it's length reaches at most counters["row_max"]

    cur_rm = min(len(tmp_file_list), gl.c_row_max)
    counter = 0
    cur_l = gl.array_list[gl.c_col - 1]
    while counter < cur_rm and len(cur_l) < gl.c_row_max:
        counter += 1
        cur_l.append(com.csv_to_list(tmp_file_list[counter - 1]))
    return counter


def rewrite_tmp_file(tmp_file_list, tmp_file_dir, n_written_rows):
    # Rewriting tmp file without the lines written in buffer array

    if len(tmp_file_list) > 0:
        with open(tmp_file_dir, 'w', encoding='utf-8') as tmp_file:
            for line in tmp_file_list[n_written_rows:]:
                tmp_file.write(line)
    else:
        # If void, tmp file is deleted
        os.remove(tmp_file_dir)
        com.log(f"Deleting temporary file no. {gl.c_col}")
