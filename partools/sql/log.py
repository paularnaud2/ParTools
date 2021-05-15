import partools.utils as u
from . import gl


def process_query_init(elt, query, th_nb):

    if elt == 'MONO':
        u.log("Executing query:")
        u.log_print(query + "\n;")
    elif gl.MAX_DB_CNX == 1:
        u.log(f"Executing query '{elt}'...")
    else:
        u.log(f"Executing query '{elt}' (connection no. {th_nb})...")


def process_query_finish(elt, th_nb):

    if elt == 'MONO':
        u.log("Query executed")
    elif gl.MAX_DB_CNX == 1:
        u.log(f"Query '{elt}' executed")
    else:
        u.log(f"Query '{elt}' executed (connection no. {th_nb})")


def write_rows_init(q_name, th_nb):

    if q_name == 'MONO':
        u.log("Writing lines...")
    elif gl.MAX_DB_CNX == 1 or th_nb == 0:
        u.log(f"Writing lines for query '{q_name}'...")
    else:
        s = f"Writing lines for query '{q_name}' (connection no. {th_nb})..."
        u.log(s)


def write_rows_finish(q_name, i, cnx_nb):
    bn = u.big_number(i)
    if q_name == 'MONO':
        return
    elif gl.MAX_DB_CNX == 1 or cnx_nb == 0:
        s = f"All lines written for query '{q_name}' ({bn} lines written)"
        u.log(s)
    else:
        s = (f"All lines written for query '{q_name}'"
             f" ({bn} lines written, connection no. {cnx_nb})")
        u.log(s)


def inject():
    s1 = "Injecting data in DB"
    if gl.ref_chunk != 0:
        bn = u.big_number(gl.ref_chunk * gl.NB_MAX_ELT_INSERT)
        s = s1 + f" (recovering from line {bn})"
    else:
        s = s1
    s += "..."
    u.log(s)


def script(script):
    s = "Base script to be executed for each line of input file:"
    u.log(s)
    u.log_print(script)


def recover_fail(e, chunk, txt):
    u.log(f"Error while trying to recover: {str(e)}")
    u.log_print(f"Content of file {chunk}:")
    u.log_print(txt)
