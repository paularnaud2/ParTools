import partools.utils as u
import partools.tools as to

from partools.utils import g

from . import gl


def left_join_arrays(ar_left_in, ar_right_in):
    check_void_right_array(ar_right_in)
    u.log("Preparing left array...")
    (ar_left, first_line_l) = prepare_array(ar_left_in)
    u.save_csv(ar_left, gl.OUT_LEFT)
    log_prepare(gl.OUT_LEFT, u.big_number(len(ar_left)))

    u.log("Preparing right array...")
    (ar_right, first_line_r) = prepare_array(ar_right_in)
    u.save_csv(ar_right, gl.OUT_RIGHT)
    log_prepare(gl.OUT_RIGHT, u.big_number(len(ar_right)))

    u.log("Joining both arrays...")
    init_while_join(first_line_l, first_line_r)
    while gl.END_LEFT is False or gl.END_RIGHT is False:
        (key_l, key_r) = update_key(ar_left, ar_right)
        key_l = compare_inf(key_l, key_r, ar_left)
        (key_l, key_r) = compare_sup(key_l, key_r, ar_left, ar_right)
        key_r = compare_equal(key_l, key_r, ar_left, ar_right)
        if incr_c_l(ar_left):
            break
    bn = u.big_number(len(gl.out_array))
    s = f"Output array generated. It has {bn} lines (including header)."
    u.log(s)


def prepare_array(arr):
    # Sorts the input array and deletes its duplicates

    if not u.has_header(arr):
        u.log("Error: input array must contain a header")
        raise Exception(g.E_MH)

    first_line = arr[0]
    gl.dup_list = to.find_dup_list(arr)
    arr = to.del_dup_list(arr[1:])

    return (arr, first_line)


def log_prepare(ar, bn_ar):
    n_dup = len(gl.dup_list)
    bn_dup = u.big_number(n_dup)
    s = f"Array prepared and saved in {ar} ({bn_ar} lines, {bn_dup} duplicates dismissed)"
    u.log(s)
    u.log_example(gl.dup_list)


def check_void_right_array(ar_right_in):
    if len(ar_right_in) == 1:
        u.log("Error: right array is void")
        raise Exception(g.E_VA)


def init_while_join(first_line_l, first_line_r):
    gl.out_array = []
    gl.old_key_l = 'old_key_init'
    gl.blank_right_row = ['' for elt in first_line_r[1:]]
    gl.out_array.append(first_line_l + first_line_r[1:])
    gl.c_cl = 0
    gl.c_cr = 0
    gl.c_out = 0
    gl.END_LEFT = False
    gl.END_RIGHT = False


def update_key(ar_left, ar_right):
    key_l = ar_left[gl.c_cl][0]
    if key_l == gl.old_key_l:
        # c_e_r cursor saves the right cursor position of the first
        # case of key equality. It allows us to come back to the position
        # when all equal left keys have been browsed
        gl.c_cr = gl.c_cer

    key_r = ar_right[gl.c_cr][0]

    return (key_l, key_r)


def compare_inf(key_l, key_r, ar_left):
    while key_l < key_r:
        out_line = ar_left[gl.c_cl] + gl.blank_right_row
        gl.out_array.append(out_line)
        gl.c_out += 1
        debug('compare_inf', key_l, key_r, out_line)
        if incr_c_l(ar_left):
            break
        key_l = ar_left[gl.c_cl][0]

    return key_l


def compare_sup(key_l, key_r, ar_left, ar_right):
    while key_l > key_r:
        out_line = ar_left[gl.c_cl] + gl.blank_right_row
        if gl.END_RIGHT:
            gl.out_array.append(out_line)
            gl.c_out += 1
        debug('compare_sup', key_l, key_r)
        if not gl.END_RIGHT:
            if incr_c_r(ar_right):
                break
            key_r = ar_right[gl.c_cr][0]
        else:
            if incr_c_l(ar_left):
                break
            key_l = ar_left[gl.c_cl][0]

    if key_l < key_r:
        gl.out_array.append(out_line)
        gl.c_out += 1
    return (key_l, key_r)


def compare_equal(key_l, key_r, ar_left, ar_right):
    gl.c_cer = gl.c_cr
    while key_l == key_r:
        out_line = ar_left[gl.c_cl] + ar_right[gl.c_cr][1:]
        gl.out_array.append(out_line)
        gl.c_out += 1
        debug('compare_equal', key_l, key_r, out_line)
        if incr_c_r(ar_right):
            break
        key_r = ar_right[gl.c_cr][0]
        gl.old_key_l = key_l

    return key_r


def incr_c_l(ar_left):
    # Increases the left cursor and checks if the end of the array has been
    # reached. In this case, the cursor is set to -1

    gl.c_cl += 1
    if gl.c_cl == len(ar_left):
        gl.c_cl -= 1
        gl.END_LEFT = True
        return True
    return False


def incr_c_r(ar_right):
    # Same as incr_c_l but for right cursor

    gl.c_cr += 1
    if gl.c_cr == len(ar_right):
        gl.c_cr -= 1
        gl.END_RIGHT = True
        return True
    return False


def debug(s, key_l, key_r, out_line=[]):
    if not gl.DEBUG_JOIN:
        return

    print(s)
    print([gl.c_cl + 2, gl.c_cr + 2])
    print([key_l, key_r])
    print(out_line)
    u.log_array(gl.out_array)
    u.log_print()
    # if s == 'compare_sup':
    #     print(key_l)
