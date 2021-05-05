import os
import pytools.common as com
from . import gl


def recover():

    file_list = com.list_files(gl.TMP_DIR, False)
    a = len(file_list)
    if a == 0:
        return

    s = "Work in progress detected. Recover? (y/n)"
    if gl.TEST_RECOVER:
        com.log(s)
        com.log_print("y (TEST_RECOVER = True)")
    elif com.log_input(s) == 'n':
        com.mkdirs(gl.TMP_DIR, True)
        return

    modify_ql(file_list)
    com.log("Query list modified according previous work in progress. "
            f"Recovering from query '{gl.QUERY_LIST[0][1]}'")


def modify_ql(file_list):
    # Modifies the query list by deleting element already
    # in file list. EC files are also deleted.

    list_out = []
    for elt in gl.QUERY_LIST:
        comp_elt = elt[1] + gl.FILE_TYPE
        comp_elt_ec = elt[1] + gl.EC + gl.FILE_TYPE
        if comp_elt not in file_list:
            list_out.append(elt)
        if comp_elt_ec in file_list:
            ec_path = gl.TMP_DIR + comp_elt_ec
            os.remove(ec_path)
            com.log(f"EC file {ec_path} deleted")

    gl.QUERY_LIST = list_out
