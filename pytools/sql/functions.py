from os import rename
from threading import RLock

import pytools.utils as u
from . import gl
from . import rg
from . import log

verrou = RLock()


def get_query_list():

    gl.query = get_query(gl.QUERY_IN)
    if gl.QUERY_LIST:
        gl.ql_replace = not gl.query == ''
        return

    if rg.range_query():
        return

    gl.ql_replace = False
    gl.QUERY_LIST = [[gl.query, "MONO"]]


def get_query(query_in):
    if u.like(query_in, "*.sql"):
        query_out = u.load_txt(query_in, False)
    else:
        query_out = query_in
    query_out = query_out.strip('\r\n;')
    query_out = u.replace_from_dict(query_out, gl.VAR_DICT)

    return query_out


def get_final_script(script_in):
    if u.like(script_in, "*.sql"):
        script = u.load_txt(script_in, False)
    else:
        script = script_in
    script = u.replace_from_dict(script, gl.VAR_DICT)
    return script


def write_rows(cursor, q_name='MONO', th_name='DEFAULT', th_nb=0):

    log.write_rows_init(q_name, th_nb)
    with open(gl.out_files[q_name + gl.EC], 'a', encoding='utf-8') as out_file:
        i = 0
        for row in cursor:
            iter = write_row(row, out_file, q_name)
            i += iter
            with verrou:
                gl.c_row += iter
            u.step_log(i, gl.SL_STEP, th_name=th_name)

    rename(gl.out_files[q_name + gl.EC], gl.out_files[q_name])
    log.write_rows_finish(q_name, i, th_nb)


def write_row(row, out_file, q_name='MONO'):

    s = u.csv_clean(str(row[0]))
    line_out = s
    for elt in row[1:]:
        s = str(elt)
        if s == 'None':
            s = ''
        else:
            s = u.csv_clean(s)
        line_out += u.g.CSV_SEPARATOR + s
    if line_out.strip(u.g.CSV_SEPARATOR) == '':
        return 0
    if gl.EXPORT_RANGE and q_name != 'MONO':
        line_out += u.g.CSV_SEPARATOR + q_name
    line_out += '\n'
    out_file.write(line_out)
    return 1
