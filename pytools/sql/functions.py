from os import rename
from threading import RLock

import pytools.common as com
import pytools.common.g as g

from . import gl
from . import log

verrou = RLock()


def get_query():
    if com.like(gl.QUERY_IN, "*.sql"):
        query = com.read_file(gl.QUERY_IN)
    else:
        query = gl.QUERY_IN
    query = query.strip('\r\n;')
    query = com.replace_from_dict(query, gl.VAR_DICT)
    gl.query = query


def get_final_script(script_in):
    if com.like(script_in, "*.sql"):
        script = com.read_file(script_in)
    else:
        script = script_in
    script = com.replace_from_dict(script, gl.VAR_DICT)
    return script


def write_rows(cursor, rg_name='MONO', th_name='DEFAULT', th_nb=0):

    log.write_rows_init(rg_name, th_nb)
    with open(gl.out_files[rg_name + gl.EC], 'a',
              encoding='utf-8') as out_file:
        i = 0
        for row in cursor:
            iter = write_row(row, out_file, rg_name)
            i += iter
            with verrou:
                gl.c_row += iter
            com.step_log(i, gl.SL_STEP, th_name=th_name)

    rename(gl.out_files[rg_name + gl.EC], gl.out_files[rg_name])
    log.write_rows_finish(rg_name, i, th_nb)


def write_row(row, out_file, rg_name='MONO'):

    s = com.csv_clean(str(row[0]))
    line_out = s
    for elt in row[1:]:
        s = str(elt)
        if s == 'None':
            s = ''
        else:
            s = com.csv_clean(s)
        line_out += g.CSV_SEPARATOR + s
    if line_out.strip(g.CSV_SEPARATOR) == '':
        return 0
    if gl.EXPORT_RANGE and rg_name != 'MONO':
        line_out += g.CSV_SEPARATOR + rg_name
    line_out += '\n'
    out_file.write(line_out)
    return 1
