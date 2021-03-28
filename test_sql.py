import os
import dq
import sql
import common as com
import test.check_log as cl

from time import sleep
from common import g
from sql.connect import connect

from test import gl
from test import ttry
from test import is_test_db_defined

from multiprocessing import Process
from multiprocessing import Manager


def prepare_iutp(sf):
    sql.gl.TEST_IUTD = False
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_FILE=gl.SQL_CREATE_TABLE_IUTD,
        VAR_DICT={'TABLE_NAME': gl.SQL_T_IUTD},
        PROC=True,
    )
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_FILE=sf,
        PROC=False,
    )


def clean_db(list_in):
    com.log("Cleaning DB...")
    for t in list_in:
        drop_table(t)
    com.log("DB cleaned\n")


def drop_table(table_name):
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_FILE=gl.SQL_DROP_TABLE,
        VAR_DICT={'TABLE_NAME': table_name},
        PROC=False,
    )


def upload(inp, tr=False, md=''):
    execute_kwargs = {
        'ENV': gl.SQL_ENV,
        'DB': gl.SQL_DB,
        'SCRIPT_FILE': gl.SQL_CREATE_TABLE,
        'VAR_DICT': {
            'TABLE_NAME': gl.SQL_T_TEST
        },
        'PROC': True,
    }

    sql.upload(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        EXECUTE_PARAMS=execute_kwargs,
        SCRIPT_FILE=gl.SQL_INSERT_TABLE,
        VAR_DICT={'TABLE_NAME': gl.SQL_T_TEST},
        UPLOAD_IN=inp,
        NB_MAX_ELT_INSERT=gl.SQL_MAX_ELT_INSERT,
        TEST_RESTART=tr,
        MD=md,
    )


def download(query, out, merge=True, tr=False, ti=False, cnx=3, sl=500, md=''):

    sql.download(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        QUERY_FILE=query,
        VAR_DICT={'TABLE_NAME': gl.SQL_T_TEST},
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


def upload_interrupted():
    manager = Manager()
    md = manager.dict()
    md['T'] = False
    md['LOG_FILE'] = g.LOG_FILE
    com.log("[sql] upload: start", c_out=False)
    p = Process(target=upload, args=(gl.SQL_IN, True, md))
    p.start()
    while not md['T']:
        pass
    com.log("Duration received")
    t = md['T'] / 1000
    sleep(t)
    com.log("Terminating subprocess...")
    p.terminate()
    com.log("Subprocess terminated (upload_interrupted)\n")


def download_interrupted(query, out):
    manager = Manager()
    md = manager.dict()
    md['STOP'] = False
    md['N_STOP'] = 0.8 * 2900
    md['LOG_FILE'] = g.LOG_FILE
    com.log("[sql] download: start", c_out=False)
    d = {'query': query, 'out': out, 'tr': True, 'md': md}
    p = Process(target=download, kwargs=d)
    p.start()
    while not md['STOP']:
        pass
    p.terminate()


def iutd():
    prepare_iutp(gl.SQL_INSERT_IUTD_OK)
    sql.gl.TEST_IUTD = True

    # Test no iutd file date db ok
    connect(gl.SQL_ENV, gl.SQL_DB)

    # Test iutd file date ok
    connect(gl.SQL_ENV, gl.SQL_DB)

    com.log_print()
    os.remove(sql.gl.IUTD_DIR)
    prepare_iutp(gl.SQL_INSERT_IUTD_KO)
    sql.gl.TEST_IUTD = True
    # Test no iutd file date db ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    # Test iutd file date ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    sql.gl.TEST_IUTD = False


def reset():
    com.log("Resetting folders...")
    com.mkdirs(gl.SQL_TMP, True)
    com.mkdirs(gl.SQL_OUT, True)
    com.log("Reset over\n")


def test_sql():
    com.init_log('test_sql', True)
    if not is_test_db_defined('test_sql'):
        return

    com.log('Test iutd---------------------------------------------')
    reset()
    iutd()

    com.log('Test upload-------------------------------------------')
    # Test missing header in input file
    ttry(upload, g.E_MH, gl.SQL_IN_MH)
    # Test upload with interruption
    upload_interrupted()
    upload(gl.SQL_IN, tr=True)

    com.log('Test download------------------------------------------')
    # Test download no output
    download(gl.SQL_QUERY_NO, gl.SQL_DL_OUT, ti=True)

    # Test download standard
    reset()
    download(gl.SQL_QUERY, gl.SQL_DL_OUT)
    dq.file_match(gl.SQL_IN, gl.SQL_DL_OUT)
    dq.file_match(gl.OUT_DUP_TMP, gl.SQL_OUT_DUP_REF)

    # Test download RG with merge
    download_interrupted(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG)
    download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, tr=True, sl=50)
    dq.file_match(gl.SQL_DL_OUT, gl.SQL_DL_OUT_RG)

    # Test download RG without merge
    reset()
    download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, merge=False, cnx=1, sl=50)
    dq.file_match(gl.SQL_RG_REF, gl.SQL_RG_COMP)

    # Test count simple
    reset()
    download(gl.SQL_QUERY_COUNT_1, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)
    download(gl.SQL_QUERY_COUNT_1_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)

    # Test count group by
    reset()
    download(gl.SQL_QUERY_COUNT_2, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)
    download(gl.SQL_QUERY_COUNT_2_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)

    # Cleaning DB
    clean_db([gl.SQL_T_TEST, gl.SQL_T_IUTD])

    com.check_log(cl.SQ)


if __name__ == '__main__':
    test_sql()
