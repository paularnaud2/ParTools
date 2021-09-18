import warnings

import partools as pt
import partools.utils as u
import partools.sql as sql

from partools.test.sql import gl


def is_test_db_defined():
    if not pt.cfg.CONF_ORACLE:
        s = "cfg.CONF_ORACLE not defined. Test aborted."
        u.log(s)
        warnings.warn(s)
        return False
    else:
        return True


def connect():
    from partools.test import ttry

    u.log_print('Test - nothing configured')
    (sql.gl.CNX_INFO, sql.gl.DB, sql.gl.ENV) = ('', '', '')
    ttry(sql.connect, sql.gl.E_1)
    u.log_print()

    u.log_print('Test - DB undefined')
    sql.gl.DB = 'TEST_DB'
    ttry(sql.connect, sql.gl.E_2.format('TEST_DB'))
    u.log_print()

    u.log_print('Test - ENV undefined')
    (sql.gl.DB, sql.gl.ENV) = ('TEST_DB', 'TEST_ENV')
    ttry(sql.connect, sql.gl.E_3.format('TEST_DB', 'TEST_ENV'))
    u.log_print()

    u.log_print('Test - OK DB only')
    (sql.gl.DB, sql.gl.ENV) = (gl.DB, '')
    sql.connect()
    u.log_print()

    u.log_print('Test - OK DB + ENV')
    (sql.gl.DB, sql.gl.ENV) = (gl.DB, gl.ENV)
    sql.connect()
    u.log_print()

    u.log_print('Test - OK CNX_INFO (via TNS_NAMES)')
    sql.gl.CNX_INFO = gl.CNX_INFO
    sql.connect()
    u.log_print()
    pass


def upload(inp, tr=False, md=""):
    execute_kwargs = {
        "DB": gl.DB,
        "SCRIPT_IN": gl.CREATE_TABLE,
        "VAR_DICT": {
            "TABLE_NAME": gl.T_TEST
        },
        "PROC": True,
    }

    sql.upload(
        DB=gl.DB,
        EXECUTE_KWARGS=execute_kwargs,
        SCRIPT_IN=gl.INSERT_TABLE,
        VAR_DICT={"TABLE_NAME": gl.T_TEST},
        UPLOAD_IN=inp,
        NB_MAX_ELT_INSERT=gl.MAX_ELT_INSERT,
        TEST_RECOVER=tr,
        MD=md,
    )


def download(query, out, merge=True, tr=False, ti=False, cnx=3, sl=500, md=""):

    sql.download(
        DB=gl.DB,
        QUERY_IN=query,
        VAR_DICT={"TABLE_NAME": gl.T_TEST},
        OUT_PATH=out,
        OUT_DIR=gl.DL_OUT_RG_FOLDER,
        MAX_DB_CNX=cnx,
        SL_STEP=sl,
        MERGE_FILES=merge,
        EXPORT_RANGE=False,
        CHECK_DUP=True,
        OPEN_OUT_FILE=False,
        TEST_RECOVER=tr,
        TEST_IUTD=ti,
        MD=md,
    )


def reset():
    u.log("Resetting folders...")
    u.mkdirs(gl.TMP_DIR, True)
    u.mkdirs(gl.OUT_DIR, True)
    u.log("Reset over\n")


def clean_db(list_in):
    u.log("Cleaning DB...")
    for t in list_in:
        drop_table(t)
    u.log("DB cleaned\n")


def drop_table(table_name):
    sql.execute(
        DB=gl.DB,
        SCRIPT_IN=gl.DROP_TABLE,
        VAR_DICT={"TABLE_NAME": table_name},
        PROC=False,
    )
