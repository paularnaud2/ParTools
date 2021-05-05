import os

import pytools.utils as u
import pytools.sql as sql

from pytools.test import gl


def prepare_iutd(sf):
    sql.gl.TEST_IUTD = False
    sql.execute(
        DB=gl.SQL_DB,
        SCRIPT_IN=gl.SQL_CREATE_TABLE_IUTD,
        VAR_DICT={"TABLE_NAME": gl.SQL_T_IUTD},
        PROC=True,
    )
    sql.execute(
        DB=gl.SQL_DB,
        SCRIPT_IN=sf,
        PROC=False,
    )


def iutd():
    prepare_iutd(gl.SQL_INSERT_IUTD_OK)
    sql.gl.TEST_IUTD = True

    # Test no iutd file date db ok
    sql.connect()
    # Test iutd file date ok
    sql.connect()

    u.log_print()
    os.remove(sql.gl.iutd_path)
    prepare_iutd(gl.SQL_INSERT_IUTD_KO)
    sql.gl.TEST_IUTD = True

    # Test no iutd file date db ko
    sql.connect()
    # Test iutd file date ko
    sql.connect()
    sql.gl.TEST_IUTD = False
