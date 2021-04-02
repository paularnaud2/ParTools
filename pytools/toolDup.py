# This script allows you to shuffle, sort as well as find and/or remove
# duplicates in a csv file or a list

import os
from random import shuffle

import pytools.common as com
import pytools.common.g as g

from pytools.tools import gl
from pytools.tools.init import init_find_dup
from pytools.tools.finish import finish_find_dup
from pytools.tools.finish import finish_del_dup

# Input variables default values
gl.IN_FILE = g.paths['IN'] + "in.csv"
gl.OUT_FILE_SHUF = g.paths['OUT'] + "out.csv"
gl.OUT_FIND_DUP = g.paths['OUT'] + "out_find_dup.csv"
gl.OUT_DEL_DUP = g.paths['OUT'] + "out_del_dup.csv"

# Const
gl.TMP_OUT = 'out_dup.csv'


def find_dup(in_dir, out_dir='', open_out=False, col=0):
    com.log("[toolDup] find_dup: start")
    (cur_list, out_dir) = init_find_dup(in_dir, out_dir, col)
    bn = com.big_number(len(cur_list))
    com.log(f"File loaded, {bn} lines to be analysed")
    dup_list = find_dup_list(cur_list)
    finish_find_dup(dup_list, out_dir, open_out)
    com.log("[toolDup] find_dup: end")


def del_dup(in_dir, out_dir, open_out=False):
    com.log("[toolDup] del_dup: start")
    com.log(f"Deleting duplicates in file '{in_dir}'...")
    cur_list = com.load_txt(in_dir)
    bn = com.big_number(len(cur_list))
    com.log(f"File loaded, {bn} lines to be analysed")
    if com.has_header(cur_list):
        out_list = [cur_list[0]] + del_dup_list(cur_list[1:])
    else:
        out_list = del_dup_list(cur_list)
    finish_del_dup(out_list, out_dir, open_out)
    com.log("[toolDup] del_dup: end")


def shuffle_csv(in_dir, out_dir, open_out=False):
    com.log("[toolShuf] shuffle_csv: start")
    cur_list = com.load_csv(in_dir)
    if com.has_header(cur_list):
        header = cur_list[0]
        cur_list = cur_list[1:]
    shuffle(cur_list)
    cur_list = [header] + cur_list
    com.save_csv(cur_list, out_dir)
    com.log(f"Shuffled csv file saved in {out_dir}")
    if open_out:
        os.startfile(out_dir)
    com.log("[toolShuf] shuffle_csv: end")


def find_dup_list(in_list):
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


if __name__ == '__main__':
    find_dup(gl.IN_FILE, gl.OUT_FIND_DUP, True)
    del_dup(gl.IN_FILE, gl.OUT_DEL_DUP, True)
    shuffle_csv(gl.IN_FILE, gl.OUT_FILE_SHUF, True)
