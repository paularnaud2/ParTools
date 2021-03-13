import common as com
import sql.gl as gl
import sql.log as log

from common import g
from os import rename
from threading import RLock

verrou = RLock()


def get_final_script(script_file):
    script = com.read_file(script_file)
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
