import dq
import time
import common as com
import reqlist as rl
import test.check_log as cl

from common import g
from test import gl
from test import ttry
from test import is_test_db_defined
from test_sql import upload

from multiprocessing import Process
from multiprocessing import Manager


def reqlist(in_file,
            out_file,
            query_file,
            test_restart=False,
            md='',
            cnx=3,
            elt=100):

    rl.run_reqList(
        ENV=gl.SQL_ENV,
        DB=gl.SQL_DB,
        QUERY_FILE=query_file,
        IN_FILE=in_file,
        OUT_FILE=out_file,
        VAR_DICT={'TABLE_NAME': gl.SQL_TABLE_NAME},
        MAX_DB_CNX=cnx,
        NB_MAX_ELT_IN_STATEMENT=elt,
        SL_STEP_QUERY=5,
        SQUEEZE_JOIN=False,
        SQUEEZE_SQL=False,
        CHECK_DUP=True,
        OPEN_OUT_FILE=False,
        TEST_RESTART=test_restart,
        MD=md,
    )


def left_join_files(left, right, ref):
    rl.left_join_files(left, right, gl.RL_OUT_JOIN, debug=False)
    dq.file_match(ref, gl.RL_OUT_JOIN)


def reqlist_interrupted(inp, out, query, sleep=False, cnx=3, elt=100):
    manager = Manager()
    md = manager.dict()
    md['STOP'] = False
    md['LOG_FILE'] = g.LOG_FILE
    com.log("[reqlist] run_reqList: start", c_out=False)
    p = Process(target=reqlist, args=(inp, out, query, True, md, cnx, elt))
    p.start()
    while not md['STOP']:
        pass
    if sleep:
        # If sleep = True, a bit of time is let to the other threads to finish
        # their run as it is valuable to test the restart in this case
        # (more code coverage)
        time.sleep(0.5)
    p.terminate()


def test_reqlist():
    com.init_log('test_reqlist', True)
    if not is_test_db_defined('test_reqlist'):
        return

    com.mkdirs(gl.RL_TMP, True)
    com.mkdirs(gl.RL_OUT, True)
    com.log_print()

    com.log('Test join---------------------------------------------')
    left_join_files(gl.RL_LEFT_1, gl.RL_RIGHT_1, gl.RL_OUT_JOIN_REF_1)
    left_join_files(gl.RL_LEFT_2, gl.RL_RIGHT_2, gl.RL_OUT_JOIN_REF_2)
    left_join_files(gl.RL_LEFT_3, gl.RL_RIGHT_3, gl.RL_OUT_JOIN_REF_3)

    com.log('Preparing DB------------------------------------------')
    upload(gl.SQL_IN_FILE)
    arr = com.load_csv(gl.SQL_IN_FILE)
    arr = [elt[0] for elt in arr]
    com.save_csv(arr, gl.RL_IN_1)

    com.log('Test reqlist------------------------------------------')
    # Test no sql output
    ttry(reqlist, g.E_VA, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_NO)

    # Test no var
    ttry(reqlist, g.E_MV, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_MV)

    # Test missing header
    com.save_csv(arr[1:], gl.RL_IN_MH)
    ttry(reqlist, g.E_MH, gl.RL_IN_MH, gl.RL_OUT_1, gl.RL_QUERY_1)

    # Test nominal conditions
    reqlist(gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_1, cnx=1)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_2, gl.RL_QUERY_2)
    dq.file_match(gl.SQL_IN_FILE, gl.RL_OUT_2, del_dup=True)
    dq.file_match(gl.OUT_DUP_TMP, gl.RL_OUT_DUP_REF)

    # Test interruption other threads not finished
    com.mkdirs(gl.RL_TMP, True)
    com.log_print()
    reqlist_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, cnx=6, elt=10)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True, cnx=6, elt=10)
    dq.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    # Test interruption other threads finished
    com.mkdirs(gl.RL_TMP, True)
    com.log_print()
    reqlist_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    dq.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    com.check_log(cl.RL)


if __name__ == '__main__':
    test_reqlist()
