import os
import re

import pytools.common as com
import pytools.common.g as g

from . import gl


def range_query():

    rg_file_name = get_rg_file_name(gl.query)
    if not rg_file_name:
        gl.range_query = False
        return False

    gl.range_query = True
    gl.ql_replace = True
    gl.VAR_IN = rg_file_name
    gen_query_list(rg_file_name)
    restart()

    return True


def get_rg_file_name(in_str):

    exp = '(.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m = re.search(exp, in_str)
    exp_comment = '(.*-{2,}.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m_comment = re.search(exp_comment, in_str)
    if m and not m_comment:
        rg_file_name = m.group(2)
        return rg_file_name
    else:
        return ''


def gen_query_list(rg_file_name):

    range_dir = gl.RANGE_PATH + rg_file_name + gl.FILE_TYPE
    rg_list = com.load_txt(range_dir)
    gl.QUERY_LIST = [[elt, elt] for elt in rg_list]
    com.log(f"Range query detected. Base query:\n{gl.query}\n;")


def restart():

    file_list = com.get_file_list(gl.TMP_PATH)
    a = len(file_list)
    if a == 0:
        return

    s = "Work in progress detected. Kill? (y/n)"
    if gl.TEST_RESTART:
        com.log(s)
        com.log_print("n (TEST_RESTART = True)")
    elif com.log_input(s) == 'y':
        com.mkdirs(gl.TMP_PATH, True)
        return

    modify_ql(file_list)
    com.log("Range list modified according previous work in progress")


def modify_ql(file_list):
    # Modifies the range list by deleting element already
    # in file list. EC files are also deleted.

    list_out = []
    for elt in gl.QUERY_LIST:
        comp_elt = elt[0] + gl.FILE_TYPE
        comp_elt_ec = elt[0] + gl.EC + gl.FILE_TYPE
        if comp_elt not in file_list:
            list_out.append(elt)
        if comp_elt_ec in file_list:
            ec_path = gl.TMP_PATH + comp_elt_ec
            os.remove(ec_path)
            com.log(f"EC file {ec_path} deleted")

    gl.QUERY_LIST = list_out
