import qdd.gl as gl
import common as com

from qdd.init import init_compare
from qdd.functions import read_list
from qdd.functions import compare_elt


def compare_sorted_files(in_file_dir_1, in_file_dir_2, out_file_dir):

    with open(out_file_dir, 'a', encoding='utf-8') as out_file:
        with open(in_file_dir_1, 'r', encoding='utf-8') as in_file_1:
            with open(in_file_dir_2, 'r', encoding='utf-8') as in_file_2:
                comp(in_file_1, in_file_2, out_file)

    finish(out_file_dir)


def comp(in1, in2, out):
    (l1, l2) = init_compare(in1, in2)
    com.init_sl_time()
    while compare_elt(l1, l2) != " ":
        (l1, l2) = compare_equal(l1, l2, in1, in2, out)
        (l1, l2) = compare_inf(l1, l2, in1, out)
        (l1, l2) = compare_sup(l1, l2, in2, out)


def finish(out_file_dir):

    s = "Fichier de sortie généré avec succès : {}\n"
    s += "\t\t{} lignes parcourues dans le fichier 1\n"
    s += "\t\t{} lignes parcourues dans le fichier 2\n"
    s += "\t\t{} lignes écrites dans le fichier de sortie"
    nb_out = com.big_number(gl.counters["out"])
    nb_1 = com.big_number(gl.counters["c1"])
    nb_2 = com.big_number(gl.counters["c2"])
    com.log(s.format(out_file_dir, nb_1, nb_2, nb_out))


def compare_equal(line_1_list, line_2_list, in_file_1, in_file_2, out_file):

    while compare_elt(line_1_list, line_2_list) == "=":
        if line_1_list != line_2_list:
            gl.counters["diff"] += 1
            if gl.bool["DIFF"]:
                line_diff = compare_line(line_1_list, line_2_list)
                com.write_csv_line(line_diff, out_file)
                gl.counters["out"] += 1
        elif gl.bool["EQUAL"]:
            line_1_list.append(gl.EQUAL_LABEL)
            com.write_csv_line(line_1_list, out_file)
            gl.counters["out"] += 1
        line_1_list = read_list(in_file_1)
        gl.counters["c1"] += 1
        line_2_list = read_list(in_file_2)
        gl.counters["c2"] += 1
        com.step_log(gl.counters["c1"], gl.SL_STEP, gl.msg, gl.counters["out"])

    return (line_1_list, line_2_list)


def compare_line(line_1_list, line_2_list):
    # comparaison de deux lignes dont l'élément pivot est égal
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
        gl.counters["diff"] += 1
        if gl.bool["DIFF"]:
            line_1_list.append(gl.LABEL_1)
            com.write_csv_line(line_1_list, out_file)
            gl.counters["out"] += 1
        line_1_list = read_list(in_file_1)
        gl.counters["c1"] += 1
        com.step_log(gl.counters["c1"], gl.SL_STEP, gl.msg, gl.counters["out"])

    return (line_1_list, line_2_list)


def compare_sup(line_1_list, line_2_list, in_file_2, out_file):

    while compare_elt(line_1_list, line_2_list) == ">":
        gl.counters["diff"] += 1
        if gl.bool["DIFF"]:
            line_2_list.append(gl.LABEL_2)
            com.write_csv_line(line_2_list, out_file)
            gl.counters["out"] += 1
        line_2_list = read_list(in_file_2)
        gl.counters["c2"] += 1

    return (line_1_list, line_2_list)
