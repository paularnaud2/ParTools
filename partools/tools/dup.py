import partools.utils as u


def find_dup(in_path, out_path='', open_out=False, col=0):
    """Finds the duplicates in in_path file

    - col: if the file is a csv, the duplicates will be searched in this column index
    """

    u.log("[toolDup] find_dup: start")
    (cur_list, out_path) = init_find_dup(in_path, out_path, col)
    bn = u.big_number(len(cur_list))
    u.log(f"File loaded, {bn} lines to be analysed")
    dup_list = find_dup_list(cur_list)
    finish_find_dup(dup_list, out_path, open_out)
    u.log("[toolDup] find_dup: end")


def init_find_dup(in_path, out_path, col):
    import os.path as p

    if not out_path:
        out_path = p.join(u.g.dirs['TMP'], 'out_dup.csv')

    s = "Searching duplicates in "
    if col == 0:
        u.log(f"{s} file {in_path}")
        cur_list = u.load_txt(in_path)
    else:
        u.log(f"{s}column no. {col} of file {in_path}")
        cur_list = u.load_csv(in_path)
        cur_list = [x[col - 1] for x in cur_list]
        if u.has_header(cur_list):
            cur_list = cur_list[1:]

    return (cur_list, out_path)


def del_dup(in_path, out_path, open_out=False):
    """Deletes the duplicates in in_path file"""

    u.log("[toolDup] del_dup: start")
    u.log(f"Deleting duplicates in file '{in_path}'...")
    cur_list = u.load_txt(in_path)
    bn = u.big_number(len(cur_list))
    u.log(f"File loaded, {bn} lines to be analysed")
    if u.has_header(cur_list):
        out_list = [cur_list[0]] + del_dup_list(cur_list[1:])
    else:
        out_list = del_dup_list(cur_list)
    finish_del_dup(out_list, out_path, open_out)
    u.log("[toolDup] del_dup: end")


def find_dup_list(in_list):
    """Returns a list of the duplicates in in_list"""

    if not in_list:
        return []

    in_sorted = sorted(in_list)
    dup_list = []
    old_elt = in_sorted[0]
    for elt in in_sorted[1:]:
        if elt == old_elt:
            dup_list.append(elt)
        else:
            old_elt = elt

    if dup_list:
        dup_list = del_dup_list(dup_list)

    return dup_list


def del_dup_list(in_list):
    """Returns in_list sorted and without duplicates"""

    if not in_list:
        return []

    # If in_list elements are hashable
    if isinstance(in_list[0], str):
        out_list = list(set(in_list))
        out_list.sort()
        return out_list

    # If not
    in_sorted = sorted(in_list)
    out_list = [in_sorted[0]]
    old_elt = in_sorted[0]
    for elt in in_sorted[1:]:
        if elt > old_elt:
            out_list.append(elt)
            old_elt = elt

    return out_list


def shuffle_file(in_path, out_path, open_out=False):
    """Shuffles the line order of a file using the native random package"""
    from random import shuffle

    u.log("[toolShuf] shuffle_file: start")
    cur_list = u.load_txt(in_path)
    if u.has_header(cur_list):
        header = cur_list[0]
        cur_list = cur_list[1:]
    shuffle(cur_list)
    cur_list = [header] + cur_list
    u.save_list(cur_list, out_path)
    u.log(f"Shuffled file saved in {out_path}")
    if open_out:
        u.startfile(out_path)
    u.log("[toolShuf] shuffle_file: end")


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
