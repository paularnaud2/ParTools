import pytools.common as com
import pytools.sql as sql
from pytools.test import gl


def upload(inp, tr=False, md=""):
    execute_kwargs = {
        "ENV": gl.SQL_ENV,
        "DB": gl.SQL_DB,
        "SCRIPT_IN": gl.SQL_CREATE_TABLE,
        "VAR_DICT": {
            "TABLE_NAME": gl.SQL_T_TEST
        },
        "PROC": True,
    }

    sql.upload(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        EXECUTE_PARAMS=execute_kwargs,
        SCRIPT_IN=gl.SQL_INSERT_TABLE,
        VAR_DICT={"TABLE_NAME": gl.SQL_T_TEST},
        UPLOAD_IN=inp,
        NB_MAX_ELT_INSERT=gl.SQL_MAX_ELT_INSERT,
        TEST_RESTART=tr,
        MD=md,
    )


def download(query, out, merge=True, tr=False, ti=False, cnx=3, sl=500, md=""):

    sql.download(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        QUERY_IN=query,
        VAR_DICT={"TABLE_NAME": gl.SQL_T_TEST},
        OUT_FILE=out,
        OUT_RG_DIR=gl.SQL_DL_OUT_RG_FOLDER,
        MAX_DB_CNX=cnx,
        SL_STEP=sl,
        MERGE_RG_FILES=merge,
        EXPORT_RANGE=False,
        CHECK_DUP=True,
        OPEN_OUT_FILE=False,
        TEST_RESTART=tr,
        TEST_IUTD=ti,
        MD=md,
    )


def reset():
    com.log("Resetting folders...")
    com.mkdirs(gl.SQL_TMP, True)
    com.mkdirs(gl.SQL_OUT, True)
    com.log("Reset over\n")


def clean_db(list_in):
    com.log("Cleaning DB...")
    for t in list_in:
        drop_table(t)
    com.log("DB cleaned\n")


def drop_table(table_name):
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_IN=gl.SQL_DROP_TABLE,
        VAR_DICT={"TABLE_NAME": table_name},
        PROC=False,
    )
