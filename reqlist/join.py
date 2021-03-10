import common as com
import reqlist.gl as gl

from common import g
from toolDup import del_dup_list
from toolDup import find_dup_list


def left_join_arrays(ar_left_in, ar_right_in):
    check_void_right_array(ar_right_in)
    com.log("Preparing left array...")
    (ar_left, first_line_l) = prepare_array(ar_left_in)
    com.save_csv(ar_left, gl.OUT_LEFT)
    log_prepare(gl.OUT_LEFT, com.big_number(len(ar_left)))

    com.log("Preparing right array...")
    (ar_right, first_line_r) = prepare_array(ar_right_in)
    com.save_csv(ar_right, gl.OUT_RIGHT)
    log_prepare(gl.OUT_RIGHT, com.big_number(len(ar_right)))

    com.log("Joining both arrays...")
    init_while_join(first_line_l, first_line_r)
    while gl.bools["end_left"] is False or gl.bools["end_right"] is False:
        (key_l, key_r) = update_key(ar_left, ar_right)
        key_l = compare_inf(key_l, key_r, ar_left)
        (key_l, key_r) = compare_sup(key_l, key_r, ar_left, ar_right)
        key_r = compare_equal(key_l, key_r, ar_left, ar_right)
        if incr_c_l(ar_left):
            break
    bn = com.big_number(len(gl.out_array))
    s = f"Output array generated. It has {bn} lines (including header)."
    com.log(s)


def prepare_array(arr):
    # Sorts input array and deletes its dupplicates

    if not com.has_header(arr):
        com.log("Error: input array must contain a header")
        raise Exception(g.E_MH)

    first_line = arr[0]
    gl.dup_list = find_dup_list(arr)
    arr = del_dup_list(arr[1:])

    return (arr, first_line)


def log_prepare(ar, bn_ar):
    n_dup = len(gl.dup_list)
    bn_dup = com.big_number(n_dup)
    s = f"Array prepared and saved in {ar} ({bn_ar} lines, {bn_dup} duplicates dismissed)"
    com.log(s)
    com.log_example(gl.dup_list)


def check_void_right_array(ar_right_in):
    if len(ar_right_in) == 1:
        com.log("Error: right array is void")
        raise Exception(g.E_VA)


def init_while_join(first_line_l, first_line_r):
    gl.out_array = []
    gl.old_key_l = 'old_key_init'
    gl.blank_right_row = ['' for elt in first_line_r[1:]]
    gl.out_array.append(first_line_l + first_line_r[1:])
    gl.counters["c_l"] = 0
    gl.counters["c_r"] = 0
    gl.counters["out"] = 0
    gl.bools["end_left"] = False
    gl.bools["end_right"] = False


def update_key(ar_left, ar_right):
    key_l = ar_left[gl.counters["c_l"]][0]
    if key_l == gl.old_key_l:
        # c_e_r cursor saves the right cursor position of the first
        # case of key equality. It allows us to come back to the position
        # when all equal left keys have been browsed
        gl.counters["c_r"] = gl.counters["c_e_r"]

    key_r = ar_right[gl.counters["c_r"]][0]

    return (key_l, key_r)


def compare_inf(key_l, key_r, ar_left):
    while key_l < key_r:
        out_line = ar_left[gl.counters["c_l"]] + gl.blank_right_row
        gl.out_array.append(out_line)
        gl.counters["out"] += 1
        debug('compare_inf', key_l, key_r, out_line)
        if incr_c_l(ar_left):
            break
        key_l = ar_left[gl.counters["c_l"]][0]

    return key_l


def compare_sup(key_l, key_r, ar_left, ar_right):
    while key_l > key_r:
        out_line = ar_left[gl.counters["c_l"]] + gl.blank_right_row
        if gl.bools["end_right"]:
            gl.out_array.append(out_line)
            gl.counters["out"] += 1
        debug('compare_sup', key_l, key_r)
        if not gl.bools["end_right"]:
            if incr_c_r(ar_right):
                break
            key_r = ar_right[gl.counters["c_r"]][0]
        else:
            if incr_c_l(ar_left):
                break
            key_l = ar_left[gl.counters["c_l"]][0]

    if key_l < key_r:
        gl.out_array.append(out_line)
        gl.counters["out"] += 1
    return (key_l, key_r)


def compare_equal(key_l, key_r, ar_left, ar_right):
    gl.counters["c_e_r"] = gl.counters["c_r"]
    while key_l == key_r:
        out_line = ar_left[gl.counters["c_l"]] + ar_right[
            gl.counters["c_r"]][1:]
        gl.out_array.append(out_line)
        gl.counters["out"] += 1
        debug('compare_equal', key_l, key_r, out_line)
        if incr_c_r(ar_right):
            break
        key_r = ar_right[gl.counters["c_r"]][0]
        gl.old_key_l = key_l

    return key_r


def incr_c_l(ar_left):
    # Increases left cursor and check if end of array has been reached.
    # In this case, cursor is set to -1

    gl.counters["c_l"] += 1
    if gl.counters["c_l"] == len(ar_left):
        gl.counters["c_l"] -= 1
        gl.bools["end_left"] = True
        return True
    return False


def incr_c_r(ar_right):
    # Same as incr_c_l but for right cursor

    gl.counters["c_r"] += 1
    if gl.counters["c_r"] == len(ar_right):
        gl.counters["c_r"] -= 1
        gl.bools["end_right"] = True
        return True
    return False


def debug(s, key_l, key_r, out_line=[]):
    if not gl.DEBUG_JOIN:
        return

    print(s)
    print([gl.counters["c_l"] + 2, gl.counters["c_r"] + 2])
    print([key_l, key_r])
    print(out_line)
    com.log_array(gl.out_array)
    com.log_print()
    # if s == 'compare_sup':
    #     print(key_l)
