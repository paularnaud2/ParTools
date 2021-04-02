import sys
from datetime import datetime
from os.path import exists

import pytools.common as com

from . import gl


def is_up_to_date(cnx):
    if not gl.TEST_IUTD:
        if gl.DB not in gl.IUTD_LIST or gl.iutd:
            return

    com.log(f"IUTD (Is Up To Date) check for DB {gl.DB}")
    d_now = datetime.now().strftime("%Y/%m/%d")
    if iutd_file(d_now):
        return

    iutd_db(d_now, cnx)


def iutd_db(d_now, cnx):
    d_bdd = get_bdd_date(cnx)
    com.save_csv([d_bdd], gl.IUTD_DIR)
    com.log(f"Check file saved in {gl.IUTD_DIR}")
    compare_dates(d_bdd, d_now)
    gl.iutd = True


def iutd_file(d_now):
    if exists(gl.IUTD_DIR):
        d_old = com.load_txt(gl.IUTD_DIR)[0]
        if d_now == d_old:
            gl.iutd_ok = True
            com.log("IUTD check OK")
            return True
        else:
            com.log_print('|')
            s = "The date found in the check file doesn't match the current date"
            com.log(s)
            return False
    else:
        com.log_print('|')
        com.log("Can't find IUTD check file")
        return False


def compare_dates(d_bdd, d_now):
    if d_bdd == d_now:
        com.log("IUTD check OK")
    else:
        s = (f"Warning: conf of DB '{gl.DB}' don't seem to be up to date:"
             f"\nDB date: {d_bdd}"
             f"\nToday's date: {d_now}"
             "\nContinue? (y/n)")
        if gl.TEST_IUTD:
            com.log_print(s)
            com.log_print('y (TEST_IUTD = True)')
        elif com.log_input(s) == 'n':
            sys.exit()

    com.log_print('|')


def get_bdd_date(cnx):

    c = cnx.cursor()
    query = get_iutd_query()
    com.log("Executing IUTD query: ")
    com.log_print(query)
    c.execute(query)
    com.log("Query executed")
    out = c.fetchone()
    out = str(out[0]).replace('-', '/')
    out = out[:10]

    return out


def get_iutd_query():
    if gl.TEST_IUTD:
        query = com.read_file(f"{gl.QUERY_PATH}IUTD_TEST.sql")
    else:
        query = com.read_file(f"{gl.QUERY_PATH}IUTD_{gl.DB}")

    return query
