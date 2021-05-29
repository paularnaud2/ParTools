import partools.utils as u
from . import gl


def finish_find_dup(dup_list, out_path, open_out):

    n = len(dup_list)
    if n == 0:
        u.log("No duplicates found")
        return

    bn = u.big_number(len(dup_list))
    u.log(f"{bn} duplicates found")
    u.log_example(dup_list)

    u.save_csv(dup_list, out_path)
    u.log(f"List of duplicates saved in {out_path}")
    if open_out:
        u.startfile(out_path)


def finish_del_dup(out_list, out_path, open_out):

    u.log(f"Saving list without duplicates in '{out_path}'...")
    u.save_list(out_list, out_path)
    bn_out = u.big_number(len(out_list))
    u.log(f"List saved, it has {bn_out} lines")
    if open_out:
        u.startfile(out_path)


def finish_sbf(out_path, start_time):

    if gl.FOUND:
        lowI = gl.c_row - 1 - gl.PRINT_SIZE // 2
        if lowI < 0:
            lowI = 0
        highI = gl.c_row - 1 + gl.PRINT_SIZE // 2
        u.save_list(gl.cur_list[lowI:highI], out_path)
        s = f"Current list written in {out_path}"
        u.log(s.format())
        if gl.OPEN_OUT_FILE:
            u.startfile(out_path)
    else:
        bn = u.big_number(gl.c_main)
        s = (f"EOF reached ({bn} lines, {gl.c_list} temporary lists)"
             f", string '{gl.LOOK_FOR}' not found")
        u.log(s)

    dstr = u.get_duration_string(start_time)
    u.log(f"[toolBF] search_big_file: end ({dstr})\n")


def finish_xml(out_path, start_time):

    dstr = u.get_duration_string(start_time)
    bn = u.big_number(gl.N_WRITE)
    s = f"[toolParseXML] parse_xml: end ({bn} lines written in {dstr})"
    u.log(s)
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(out_path)
