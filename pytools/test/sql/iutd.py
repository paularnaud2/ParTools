import os

import pytools.common as com
import pytools.sql as sql

from pytools.test import gl
from pytools.sql.connect import connect


def prepare_iutd(sf):
    sql.gl.TEST_IUTD = False
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_IN=gl.SQL_CREATE_TABLE_IUTD,
        VAR_DICT={"TABLE_NAME": gl.SQL_T_IUTD},
        PROC=True,
    )
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_IN=sf,
        PROC=False,
    )


def iutd():
    prepare_iutd(gl.SQL_INSERT_IUTD_OK)
    sql.gl.TEST_IUTD = True

    # Test no iutd file date db ok
    connect(gl.SQL_ENV, gl.SQL_DB)

    # Test iutd file date ok
    connect(gl.SQL_ENV, gl.SQL_DB)

    com.log_print()
    os.remove(sql.gl.IUTD_DIR)
    prepare_iutd(gl.SQL_INSERT_IUTD_KO)
    sql.gl.TEST_IUTD = True
    # Test no iutd file date db ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    # Test iutd file date ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    sql.gl.TEST_IUTD = False
