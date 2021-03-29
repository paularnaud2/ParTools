import dq.gl as gl
import common as com

from dq.init import init_prev_elt
from dq.functions import write_min_elt


def gen_sorted_temp_files(in_file_dir, out_file_dir):
    # Generation of sorted temporary files

    has_header = com.has_header(in_file_dir)
    com.log("Generating first list to be sorted...")
    com.init_sl_time()
    with open(in_file_dir, 'r', encoding='utf-8') as in_file:
        first_line = in_file.readline()
        if not has_header:
            gl.cur_list.append(com.csv_to_list(first_line))
        gl.c_sf_read = 1
        for line in in_file:
            gl.c_sf_read += 1
            gl.cur_list.append(com.csv_to_list(line))
            s = "lines read"
            com.step_log(gl.c_sf_read, gl.SL_STEP, s)
            check_max_row(gl.c_sf_read)
    gen_last_file(out_file_dir)
    del gl.cur_list


def gen_last_file(out_file_dir):
    # Generation of the last temporary file

    gl.c_file += 1
    if gl.c_file == 1:
        bn = com.big_number(gl.c_sf_read)
        s = (f"Input file entirely read ({bn} lines)."
             " Sorting current list...")
        com.log(s)
        gl.cur_list.sort()
        s = "Current list sorted. Generating output file..."
        com.log(s)
        gen_out_file(out_file_dir)
        s = f"Output file saved in {out_file_dir}"
        com.log(s)
    else:
        if len(gl.cur_list) > 0:
            s = ("Input file entirely read ({} lines)."
                 " Sorting last current list...")
            com.log(s.format(com.big_number(gl.c_sf_read)))
            gl.cur_list.sort()
            s = ("Last current list sorted. Generating last temporary file"
                 f" (no. {gl.c_file})...")
            com.log(s.format())
            gen_temp_file()
            s = "Temporary file successfully generated"
            com.log(s)
        else:
            gl.c_file -= 1
        com.log(f"{gl.c_file} temporary files created")


def gen_out_file(out_file_dir):
    # Generating output file in the case of only one temporary list

    with open(out_file_dir, 'a', encoding='utf-8') as out_file:
        gl.c_tot_out = 1
        com.init_sl_time()
        init_prev_elt(gl.cur_list)
        for elt in gl.cur_list:
            write_min_elt(elt, out_file)


def check_max_row(counter):
    # It is checked whether max number of lines of cur_list is not more than
    # fixed limit in module (MAX_ROW_LIST) gl to avoid a memory error

    if counter % gl.MAX_ROW_LIST == 0:
        gl.c_file += 1
        bn = com.big_number(gl.MAX_ROW_LIST)
        list_nb = gl.c_file
        s = (f"Maximum number of lines reached ({bn} lines) for list"
             f" no. {list_nb}, sorting...")
        com.log(s)
        gl.cur_list.sort()
        tmp_nb = gl.c_file
        s = ("Current list sorted. Generating temporary file"
             f" no. {tmp_nb}...")
        com.log(s.format())
        gen_temp_file()
        s = "Temporary file successfully generated, input file reading goes on..."
        com.log(s)
        del gl.cur_list
        gl.cur_list = []


def gen_temp_file():
    # Generating one temporary file

    file_nb = gl.c_file
    tmp_file_dir = f"{gl.TMP_DIR}tmp_{file_nb}{gl.FILE_TYPE}"
    com.save_csv(gl.cur_list, tmp_file_dir)
