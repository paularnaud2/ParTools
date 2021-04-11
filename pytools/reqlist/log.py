import pytools.common as com
from . import gl


def start_exec(th_nb):
    if gl.multi_th is True:
        s = f"Executing queries (thread no. {th_nb})..."
    else:
        s = "Executing queries..."
    com.log(s)


def gen_query_list(elt_list, group_list):
    bn1 = com.big_number(len(elt_list))
    bn2 = com.big_number(len(group_list))
    s = (
        f"Query list built: {bn1} elements to be processed distributed"
        f" in {bn2} groups ({gl.NB_MAX_ELT_IN_STATEMENT} max per group)."
        f" They will be processed in parallel by {gl.MAX_DB_CNX} connection pools."
    )
    com.log(s)


def get_sql_array_finish(th_nb):
    n_rows = gl.c[th_nb]
    s_th = ''
    if gl.MAX_DB_CNX > 1:
        s_th = f" for thread no. {th_nb}"
    if n_rows > 0:
        bn = com.big_number(n_rows)
        s = f"All queries executed{s_th} ({bn} lines written)"
        com.log(s)
    else:
        com.log(f"No lines were fetched{s_th}")
