import time
from multiprocessing import Process
from multiprocessing import Manager

import pytools.common as com
import pytools.common.g as g
import pytools.dq as dq
import pytools.reqlist as rl
import pytools.test.check_log as cl

from pytools.test.sql import upload
from pytools.test.sql import clean_db

from pytools.test import gl
from pytools.test import ttry
from pytools.test import is_test_db_defined


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
        VAR_DICT={'TABLE_NAME': gl.SQL_T_TEST},
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


def rl_interrupted(inp, out, query, sleep=False, cnx=3, elt=100):
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
