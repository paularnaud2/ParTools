import sys
import math

import pytools.utils as u
import pytools.sql as sql

from . import gl
from pytools.tools import dup


def gen_query_list():
    u.log("Building query list to be input in sql.dowload...")

    gl.query_var = sql.get_query(gl.QUERY_IN)
    check_var(gl.query_var)
    u.log_print(f"Base query:\n{gl.query_var}\n;")

    elt_list = prepare_elt_list(gl.ar_in)
    n_grp = math.ceil(len(elt_list) / gl.NB_MAX_ELT_IN_STATEMENT)
    size_elt_list = math.floor(math.log10(n_grp)) + 1
    i, n = 0, 0
    cur_elt_list, query_list = [], []
    for elt in elt_list:
        cur_elt_list.append(elt)
        i += 1
        if len(cur_elt_list) % gl.NB_MAX_ELT_IN_STATEMENT == 0:
            n += 1
            n_str = u.extend_str(n, '0', size_elt_list, True)
            grp = gen_group(cur_elt_list)
            query_list.append([grp, n_str])
            cur_elt_list = []
    if len(cur_elt_list) > 0:
        n += 1
        n_str = u.extend_str(n, '0', size_elt_list, True)
        grp = gen_group(cur_elt_list)
        query_list.append([grp, n_str])

    gl.query_list = query_list
    log_gen_query_list(elt_list, query_list)


def log_gen_query_list(elt_list, group_list):
    bn1 = u.big_number(len(elt_list))
    bn2 = u.big_number(len(group_list))
    s = (
        f"Query list built: {bn1} elements to be processed distributed"
        f" in {bn2} groups ({gl.NB_MAX_ELT_IN_STATEMENT} max per group)."
        f" They will be processed in parallel by {gl.MAX_DB_CNX} connection pools."
    )
    u.log(s)


def gen_group(elt_list):
    in_st = "('" + elt_list[0]
    for elt in elt_list[1:]:
        in_st += "', '" + elt
    in_st += "')"

    return in_st


def set_query_var(query_in):
    if u.like(query_in, "*.sql"):
        query = u.load_txt(query_in, False)
    else:
        query = query_in
    query = query.strip('\r\n;')
    check_var(query)
    gl.query_var = query


def check_var(query):
    var = u.g.VAR_DEL + gl.VAR_IN + u.g.VAR_DEL
    if var not in query:
        s = f"Error: query must contain {var}"
        u.log(s)
        u.log_print("Query:")
        u.log_print(query)
        raise Exception(u.g.E_MV)


def prepare_elt_list(array_in):
    u.check_header(array_in)
    check_field_nb()

    elt_list = [elt[gl.PIVOT_IDX] for elt in array_in[1:]]
    elt_list = dup.del_dup_list(elt_list)

    return elt_list


def check_field_nb():
    if gl.PIVOT_IDX != 0:
        s = (f"Warning: pivot index is set to {gl.PIVOT_IDX}."
             " Continue? (y/n)")
        if u.log_input(s) == 'n':
            sys.exit()
