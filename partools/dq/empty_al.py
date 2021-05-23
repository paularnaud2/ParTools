import partools.utils as u

from . import gl


def empty_array_list(out_path):
    from .init import init_prev_elt
    from .functions import write_min_elt

    s = "Emptying buffer array in output file (and removing dupes)..."
    u.log(s)
    n_col = len(gl.array_list)
    with open(out_path, 'a', encoding='utf-8') as out_file:
        u.init_sl_time()
        # cursor variable represents a reading cursor for gl.array_list
        (cursor, max_cursor, void_cursor) = init_cursors()
        init_prev_elt(gl.array_list[0])
        while cursor != void_cursor:
            (min_elt, min_col) = get_min_elt(cursor, n_col)
            write_min_elt(min_elt, out_file)
            if cursor[min_col] == max_cursor[min_col] - 1:
                # If one of the lists has entirely been read, array of lists
                # is generated again without the elements already extracted
                # in the output file and while loop is broken (return)
                cursor[min_col] += 1
                for i, l in enumerate(gl.array_list):
                    gl.array_list[i] = l[cursor[i]:]
                return
            cursor[min_col] += 1


def get_min_elt(cursor, n_col):
    # Determines the smallest element of all non empty list from the current cursor position
    from .functions import compare_elt

    # min_col initialised with the first non empty list (cursor != -1)
    min_col = -1
    while min_col < n_col - 1:
        min_col += 1
        if cursor[min_col] != -1:
            break
    min_elt = gl.array_list[min_col][cursor[min_col]]

    # min_col and min_elt are searched from init values
    i = min_col + 1
    while i < n_col:
        if cursor[i] != -1:
            cur_elt = gl.array_list[i][cursor[i]]
            if compare_elt(cur_elt, min_elt) == "<":
                min_elt = cur_elt
                min_col = i
        i += 1

    return (min_elt, min_col)


def init_cursors():

    cursor = []
    max_cursor = []
    void_cursor = []
    i = 0
    while i < len(gl.array_list):
        if len(gl.array_list[i]) == 0:
            cursor.append(-1)
        else:
            cursor.append(0)
        void_cursor.append(-1)
        max_cursor.append(len(gl.array_list[i]))
        i += 1
    return (cursor, max_cursor, void_cursor)
