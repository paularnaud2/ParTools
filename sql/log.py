import sql.gl as gl
import common as com


def process_query_init(elt, query, th_nb):

    if elt == 'MONO':
        com.log("Executing query:")
        com.log_print(query + "\n;")
    elif gl.MAX_DB_CNX == 1:
        com.log(f"Executing query for range {elt}...")
    else:
        com.log(f"Executing query for range {elt} (connection no. {th_nb})...")


def process_query_finish(elt, th_nb):

    if elt == 'MONO':
        com.log("Query executed")
    elif gl.MAX_DB_CNX == 1:
        com.log(f"Query executed for range {elt}")
    else:
        com.log(f"Query executed for range {elt} (connection no. {th_nb})")


def write_rows_init(rg_name, th_nb):

    if rg_name == 'MONO':
        com.log("Writing lines...")
    elif gl.MAX_DB_CNX == 1 or th_nb == 0:
        com.log(f"Writing lines for range {rg_name}...")
    else:
        s = f"Writing lines for range {rg_name} (connection no. {th_nb})..."
        com.log(s)


def write_rows_finish(rg_name, i, cnx_nb):
    bn = com.big_number(i)
    if rg_name == 'MONO':
        return
    elif gl.MAX_DB_CNX == 1 or cnx_nb == 0:
        s = f"All lines written for range {rg_name} ({bn} lines written)"
        com.log(s)
    else:
        s = f"All lines written for range {rg_name}"
        s += f" ({bn} lines written, connection no. {cnx_nb})"
        com.log(s)


def inject():
    s1 = "Injecting data in DB"
    if gl.ref_chunk != 0:
        bn = com.big_number(gl.ref_chunk * gl.NB_MAX_ELT_INSERT)
        s = s1 + f" (restarting from line {bn})"
    else:
        s = s1
    s += "..."
    com.log(s)


def script(script):
    s = "Base script to be executed for each line of input file:"
    com.log(s)
    com.log_print(script)


def restart_fail(e, chunk, txt):
    com.log(f"Error while trying to restart: {str(e)}")
    com.log_print(f"Content of file {chunk}:")
    com.log_print(txt)
