import pytools.common as com
import pytools.common.g as g
import pytools.dq as dq
import pytools.test.reqlist as t
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.test import ttry
from pytools.test import is_test_db_defined
from pytools.test.sql import upload
from pytools.test.sql import clean_db


def test_reqlist():
    com.init_log('test_reqlist', True)
    if not is_test_db_defined('test_reqlist'):
        return

    com.mkdirs(gl.RL_TMP, True)
    com.mkdirs(gl.RL_OUT, True)
    com.log_print()

    com.log('Test join---------------------------------------------')
    t.left_join_files(gl.RL_LEFT_1, gl.RL_RIGHT_1, gl.RL_OUT_JOIN_REF_1)
    t.left_join_files(gl.RL_LEFT_2, gl.RL_RIGHT_2, gl.RL_OUT_JOIN_REF_2)
    t.left_join_files(gl.RL_LEFT_3, gl.RL_RIGHT_3, gl.RL_OUT_JOIN_REF_3)

    com.log('Preparing DB------------------------------------------')
    upload(gl.SQL_IN)
    arr = com.load_csv(gl.SQL_IN)
    arr = [elt[0] for elt in arr]
    com.save_csv(arr, gl.RL_IN_1)

    com.log('Test reqlist------------------------------------------')
    # Test no sql output
    ttry(t.reqlist, g.E_VA, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_NO)

    # Test no var
    ttry(t.reqlist, g.E_MV, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_MV)

    # Test missing header
    com.save_csv(arr[1:], gl.RL_IN_MH)
    ttry(t.reqlist, g.E_MH, gl.RL_IN_MH, gl.RL_OUT_1, gl.RL_QUERY_1)

    # Test nominal conditions
    t.reqlist(gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_1, cnx=1)
    t.reqlist(gl.RL_OUT_1, gl.RL_OUT_2, gl.RL_QUERY_2)
    t.dq.file_match(gl.SQL_IN, gl.RL_OUT_2, del_dup=True)
    t.dq.file_match(gl.OUT_DUP_TMP, gl.RL_OUT_DUP_REF)

    # Test interruption other threads not finished
    com.mkdirs(gl.RL_TMP, True)
    com.log_print()
    t.rl_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, cnx=6, elt=10)
    t.reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True, cnx=6, elt=10)
    dq.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    # Test interruption other threads finished
    com.mkdirs(gl.RL_TMP, True)
    com.log_print()
    t.rl_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    t.reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True)
    dq.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    # Cleaning DB
    clean_db([gl.SQL_T_TEST])

    com.check_log(cl.RL)


if __name__ == '__main__':
    test_reqlist()
