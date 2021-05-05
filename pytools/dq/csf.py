import pytools.utils as u

from . import gl
from .init import init_compare
from .functions import read_list
from .functions import compare_elt


def compare_sorted_files(in_path_1, in_path_2, out_path):

    with open(out_path, 'a', encoding='utf-8') as out_file:
        with open(in_path_1, 'r', encoding='utf-8') as in_file_1:
            with open(in_path_2, 'r', encoding='utf-8') as in_file_2:
                comp(in_file_1, in_file_2, out_file)

    finish(out_path)


def comp(in1, in2, out):
    (l1, l2) = init_compare(in1, in2)
    u.init_sl_time()
    while compare_elt(l1, l2) != " ":
        (l1, l2) = compare_equal(l1, l2, in1, in2, out)
        (l1, l2) = compare_inf(l1, l2, in1, out)
        (l1, l2) = compare_sup(l1, l2, in2, out)


def finish(out_path):

    nb_out = u.big_number(gl.c_out)
    nb_1 = u.big_number(gl.c_1)
    nb_2 = u.big_number(gl.c_2)
    s = (f"Output file successfully generated in {out_path}\n"
         f"\t\t{nb_1} lines read in file 1\n"
         f"\t\t{nb_2} lines read in file 2\n"
         f"\t\t{nb_out} lines written in output file")
    u.log(s)


def compare_equal(line_1_list, line_2_list, in_file_1, in_file_2, out_file):

    while compare_elt(line_1_list, line_2_list) == "=":
        if line_1_list != line_2_list:
            gl.c_diff += 1
            if gl.DIFF:
                line_diff = compare_line(line_1_list, line_2_list)
                u.write_csv_line(line_diff, out_file)
                gl.c_out += 1
        elif gl.EQUAL:
            line_1_list.append(gl.EQUAL_LABEL)
            u.write_csv_line(line_1_list, out_file)
            gl.c_out += 1
        line_1_list = read_list(in_file_1)
        gl.c_1 += 1
        line_2_list = read_list(in_file_2)
        gl.c_2 += 1
        u.step_log(gl.c_1, gl.SL_STEP, gl.msg, gl.c_out)

    return (line_1_list, line_2_list)


def compare_line(line_1_list, line_2_list):
    # Comparing two lines whose pivot element is equal

    line_diff = []
    for i, elt_1 in enumerate(line_1_list):
        elt_2 = line_2_list[i]
        if elt_1 == elt_2:
            line_diff.append(elt_1)
        else:
            line_diff.append(elt_1 + gl.COMPARE_SEPARATOR + elt_2)

    line_diff.append(gl.LABEL_1 + gl.COMPARE_SEPARATOR + gl.LABEL_2)
    return line_diff


def compare_inf(line_1_list, line_2_list, in_file_1, out_file):

    while compare_elt(line_1_list, line_2_list) == "<":
        gl.c_diff += 1
        if gl.DIFF:
            line_1_list.append(gl.LABEL_1)
            u.write_csv_line(line_1_list, out_file)
            gl.c_out += 1
        line_1_list = read_list(in_file_1)
        gl.c_1 += 1
        u.step_log(gl.c_1, gl.SL_STEP, gl.msg, gl.c_out)

    return (line_1_list, line_2_list)


def compare_sup(line_1_list, line_2_list, in_file_2, out_file):

    while compare_elt(line_1_list, line_2_list) == ">":
        gl.c_diff += 1
        if gl.DIFF:
            line_2_list.append(gl.LABEL_2)
            u.write_csv_line(line_2_list, out_file)
            gl.c_out += 1
        line_2_list = read_list(in_file_2)
        gl.c_2 += 1

    return (line_1_list, line_2_list)
