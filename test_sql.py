import os
import sql
import qdd as q
import common as com

from test import gl
from test import ttry
from time import sleep
from common import g
from sql.connect import connect

from multiprocessing import Process
from multiprocessing import Manager


def prepare_iutp(sf):
    sql.gl.TEST_IUTD = False
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_FILE=gl.SQL_CREATE_TABLE_IUTD,
        PROC=True,
    )
    sql.execute(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        SCRIPT_FILE=sf,
        PROC=False,
    )


def upload(inp, tr=False, md=''):
    execute_params = {
        'ENV': gl.SQL_ENV,
        'DB': gl.SQL_DB,
        'SCRIPT_FILE': gl.SQL_CREATE_TABLE,
        'VAR_DICT': {
            'TABLE_NAME': gl.SQL_TABLE_NAME
        },
        'PROC': True,
    }

    sql.upload(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        EXECUTE_PARAMS=execute_params,
        SCRIPT_FILE=gl.SQL_INSERT_TABLE,
        VAR_DICT={'TABLE_NAME': gl.SQL_TABLE_NAME},
        UPLOAD_IN=inp,
        NB_MAX_ELT_INSERT=gl.SQL_MAX_ELT_INSERT,
        TEST_RESTART=tr,
        MD=md,
    )


def download(query, out, merge=True, tr=False, ti=False, md=''):

    sql.download(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        QUERY_FILE=query,
        VAR_DICT={'TABLE_NAME': gl.SQL_TABLE_NAME},
        OUT_FILE=out,
        OUT_RG_DIR=gl.SQL_DL_OUT_RG_FOLDER,
        MAX_DB_CNX=3,
        SL_STEP=500,
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
    p = Process(target=upload, args=(gl.SQL_IN_FILE, True, md))
    p.start()
    while not md['T']:
        pass
    t = md['T'] / 1000
    sleep(t)
    p.terminate()
    com.log('Arrêt automatique du traitement (upload_interrupted)\n')


def download_interrupted(query, out):
    manager = Manager()
    md = manager.dict()
    md['STOP'] = False
    md['N_STOP'] = 0.8 * 2900
    md['LOG_FILE'] = g.LOG_FILE
    p = Process(target=download, args=(query, out, True, True, False, md))
    p.start()
    while not md['STOP']:
        pass
    p.terminate()


def iutd():
    prepare_iutp(gl.SQL_INSERT_IUTD_OK)
    sql.gl.TEST_IUTD = True

    # test no iutd file date db ok
    connect(gl.SQL_ENV, gl.SQL_DB)
    com.log_print()
    # test iutd file date ok
    connect(gl.SQL_ENV, gl.SQL_DB)

    os.remove(sql.gl.IUTD_DIR)
    com.log('-----------------------------------------------------')
    prepare_iutp(gl.SQL_INSERT_IUTD_KO)
    sql.gl.TEST_IUTD = True
    # test no iutd file date db ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    # test iutd file date ko
    connect(gl.SQL_ENV, gl.SQL_DB)
    sql.gl.TEST_IUTD = False


def test_sql():
    com.init_log('test_sql', True)
    com.mkdirs(gl.SQL_TMP, True)
    com.mkdirs(gl.SQL_OUT, True)
    com.log_print()

    iutd()

    com.log('Test sql.upload------------------------------')
    # test missing header in input file
    ttry(upload, g.E_MH, gl.SQL_IN_FILE_MH)
    # test upload with interruption
    upload_interrupted()
    upload(gl.SQL_IN_FILE, tr=True)

    com.log('Test sql.dowload-----------------------------')
    # test download no output
    download(gl.SQL_QUERY_NO, gl.SQL_DL_OUT, ti=True)

    download(gl.SQL_QUERY, gl.SQL_DL_OUT)
    q.file_match(gl.SQL_IN_FILE, gl.SQL_DL_OUT)
    q.file_match(gl.OUT_DUP_TMP, gl.SQL_OUT_DUP_REF)

    com.log("Test sql.dowload RG avec merge---------------")
    download_interrupted(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG)
    download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, tr=True)
    q.file_match(gl.SQL_DL_OUT, gl.SQL_DL_OUT_RG)

    com.log("Test sql.dowload RG sans merge---------------")
    download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, merge=False)
    q.file_match(gl.SQL_RG_REF, gl.SQL_RG_COMP)

    com.log("Test count simple----------------------------")
    download(gl.SQL_QUERY_COUNT_1, gl.SQL_DL_OUT_COUNT)
    q.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)
    download(gl.SQL_QUERY_COUNT_1_RG, gl.SQL_DL_OUT_COUNT)
    q.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)

    com.log("Test count group by--------------------------")
    download(gl.SQL_QUERY_COUNT_2, gl.SQL_DL_OUT_COUNT)
    q.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)
    download(gl.SQL_QUERY_COUNT_2_RG, gl.SQL_DL_OUT_COUNT)
    q.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)


if __name__ == '__main__':
    test_sql()
