import pytools.common as com
from . import gl


def finish_find_dup(dup_list, out_dir, open_out):
    n = len(dup_list)
    if n == 0:
        com.log("No duplicates found")
        return

    bn = com.big_number(len(dup_list))
    com.log(f"{bn} duplicates found")
    com.log_example(dup_list)

    com.save_csv(dup_list, out_dir)
    com.log(f"List of duplicates saved in {out_dir}")
    if open_out:
        com.startfile(out_dir)


def finish_del_dup(out_list, out_dir, open_out):

    com.log(f"Saving list without duplicates in '{out_dir}'...")
    com.save_list(out_list, out_dir)
    bn_out = com.big_number(len(out_list))
    com.log(f"List saved, it has {bn_out} lines")
    if open_out:
        com.startfile(out_dir)


def finish_sbf(out_dir, start_time):

    if gl.FOUND:
        lowI = gl.c_row - 1 - gl.PRINT_SIZE // 2
        if lowI < 0:
            lowI = 0
        highI = gl.c_row - 1 + gl.PRINT_SIZE // 2
        com.save_list(gl.cur_list[lowI:highI], out_dir)
        s = f"Current list written in {out_dir}"
        com.log(s.format())
        if gl.OPEN_OUT_FILE:
            com.startfile(out_dir)
    else:
        bn = com.big_number(gl.c_main)
        s = (f"EOF reached ({bn} lines, {gl.c_list} temporary lists)"
             f", string '{gl.LOOK_FOR}' not found")
        com.log(s)

    dstr = com.get_duration_string(start_time)
    com.log(f"[toolBF] search_big_file: end ({dstr})\n")


def finish_xml(out_dir, start_time):
    dstr = com.get_duration_string(start_time)
    bn = com.big_number(gl.N_WRITE)
    s = f"[toolParseXML] parse_xml: end ({bn} lines written in {dstr})"
    com.log(s)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        com.startfile(out_dir)
