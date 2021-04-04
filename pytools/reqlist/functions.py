import sys

import pytools.common as com
import pytools.common.g as g

from . import gl
from . import log


def restart():
    file_list = com.get_file_list(gl.TMP_PATH)
    a = len(file_list)
    if a == 0:
        return

    s = "Work in progress detected. Kill? (y/n)"
    if gl.TEST_RESTART:
        com.log(s)
        com.log_print("n (TEST_RESTART = True)")
        return
    if com.log_input(s) == 'y':
        com.delete_folder(gl.TMP_PATH)
        return
    return


def gen_group_list():
    com.log("Building groups of elements...")
    elt_list = prepare_elt_list(gl.ar_in)

    i = 0
    cur_elt_list = []
    group_list = []
    for elt in elt_list:
        cur_elt_list.append(elt)
        i += 1
        if len(cur_elt_list) % gl.NB_MAX_ELT_IN_STATEMENT == 0:
            grp = gen_group(cur_elt_list)
            group_list.append(grp)
            cur_elt_list = []
    if len(cur_elt_list) > 0:
        grp = gen_group(cur_elt_list)
        group_list.append(grp)

    gl.group_list = group_list
    log.gen_group_list(elt_list, group_list)


def gen_group(elt_list):
    in_st = "('" + elt_list[0]
    for elt in elt_list[1:]:
        in_st += "', '" + elt
    in_st += "')"

    return in_st


def set_query_var(query_file):
    query = com.read_file(query_file)
    query = query.strip('\r\n;')
    query = com.replace_from_dict(query, gl.VAR_DICT)
    check_var(query)
    gl.query_var = query
    com.log_print(f"Base query:\n{gl.query_var}\n;")


def check_var(query):
    var = g.VAR_DEL + gl.VAR_IN + g.VAR_DEL
    if var not in query:
        s = f"Error: query must contain {var}"
        com.log(s)
        com.log_print("Query:")
        com.log_print(query)
        raise Exception(g.E_MV)


def prepare_elt_list(array_in):
    # tri et suppression des doublons
    com.check_header(array_in)
    check_field_nb()
    elt_list = [elt[gl.IN_FIELD_NB - 1] for elt in array_in[1:]]
    elt_set = set()
    for elt in elt_list:
        elt_set.add(elt)

    elt_list = []
    for elt in elt_set:
        elt_list.append(elt)
    elt_list.sort()

    bn = com.big_number(len(elt_list))
    s = f"List of elements prepared, it contains {bn} elements"
    com.log(s)

    return elt_list


def check_field_nb():
    if gl.IN_FIELD_NB != 1:
        s = (f"Warning: queries will take field no. {gl.IN_FIELD_NB}"
             " of input file in the IN statement. Continue? (y/n)")
        if com.log_input(s) == 'n':
            sys.exit()