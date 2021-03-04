import time
import qdd as q
import common as com
import reqlist as rl

from common import g
from test import gl
from test import ttry
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


def left_join(left, right, ref):
    rl.left_join(left, right, gl.RL_OUT_JOIN, debug=False)
    q.file_match(ref, gl.RL_OUT_JOIN)


def test_reqlist():
    com.init_log('test_reqlist', True)
    com.mkdirs(gl.RL_TMP, True)
    com.mkdirs(gl.RL_OUT, True)
    com.log_print()
    com.log('Test join----------------------------------------')
    left_join(gl.RL_LEFT_1, gl.RL_RIGHT_1, gl.RL_OUT_JOIN_REF_1)
    left_join(gl.RL_LEFT_2, gl.RL_RIGHT_2, gl.RL_OUT_JOIN_REF_2)
    left_join(gl.RL_LEFT_3, gl.RL_RIGHT_3, gl.RL_OUT_JOIN_REF_3)

    com.log("Préparation de la BDD----------------------------")
    upload(gl.SQL_IN_FILE)
    arr = com.load_csv(gl.SQL_IN_FILE)
    arr = [elt[0] for elt in arr]
    com.save_csv(arr, gl.RL_IN_1)

    com.log('Test reqlist--------------------------------------')
    # test no sql output
    ttry(reqlist, g.E_VA, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_NO)

    # test no var
    ttry(reqlist, g.E_MV, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_MV)

    # test missing header
    com.save_csv(arr[1:], gl.RL_IN_MH)
    ttry(reqlist, g.E_MH, gl.RL_IN_MH, gl.RL_OUT_1, gl.RL_QUERY_1)

    # test nominal conditions
    reqlist(gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_1, cnx=1)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_2, gl.RL_QUERY_2)
    q.file_match(gl.SQL_IN_FILE, gl.RL_OUT_2, del_dup=True)
    q.file_match(gl.OUT_DUP_TMP, gl.RL_OUT_DUP_REF)

    # test interruption other threads not finished
    com.mkdirs(gl.RL_TMP, True)
    reqlist_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, cnx=6, elt=10)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True, cnx=6, elt=10)
    q.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    # test interruption other threads finished
    com.mkdirs(gl.RL_TMP, True)
    reqlist_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    q.file_match(gl.RL_OUT_2, gl.RL_OUT_3)


def reqlist_interrupted(inp, out, query, sleep=False, cnx=3, elt=100):
    manager = Manager()
    md = manager.dict()
    md['STOP'] = False
    md['LOG_FILE'] = g.LOG_FILE
    p = Process(target=reqlist, args=(inp, out, query, True, md, cnx, elt))
    p.start()
    while not md['STOP']:
        pass
    if sleep:
        # if sleep = True, a bit of time is let to the other threads to finish
        # their run as it is valuable to test the restart in this case
        # (more code coverage)
        time.sleep(0.5)
    p.terminate()


if __name__ == '__main__':
    test_reqlist()
