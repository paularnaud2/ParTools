import pytools.utils as u
import pytools.dq as dq
import pytools.test.rl as t
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.test import ttry
from pytools.test import is_test_db_defined
from pytools.test.sql import upload
from pytools.test.sql import clean_db


def test_rl():
    u.init_log('test_rl', True)
    if not is_test_db_defined():
        return

    u.mkdirs(gl.RL_TMP, True)
    u.mkdirs(gl.SQL_TMP, True)
    u.mkdirs(gl.RL_OUT, True)
    u.log_print()

    u.log('Test join-----------------------------------------------')
    t.left_join_files(gl.RL_LEFT_1, gl.RL_RIGHT_1, gl.RL_OUT_JOIN_REF_1)
    t.left_join_files(gl.RL_LEFT_2, gl.RL_RIGHT_2, gl.RL_OUT_JOIN_REF_2)
    t.left_join_files(gl.RL_LEFT_3, gl.RL_RIGHT_3, gl.RL_OUT_JOIN_REF_3)

    u.log('Preparing DB--------------------------------------------')
    upload(gl.SQL_IN)
    arr = u.load_csv(gl.SQL_IN)
    arr = [elt[0] for elt in arr]
    u.save_csv(arr, gl.RL_IN_1)

    u.log('Test rl - no sql output----------------------------')
    ttry(t.reqlist, u.g.E_VA, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_NO)

    u.log('Test rl - no var in query--------------------------')
    ttry(t.reqlist, u.g.E_MV, gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_MV)

    u.log('Test rl - missing header---------------------------')
    u.save_csv(arr[1:], gl.RL_IN_MH)
    ttry(t.reqlist, u.g.E_MH, gl.RL_IN_MH, gl.RL_OUT_1, gl.RL_QUERY_1)

    u.log('Test rl - standard---------------------------------')
    t.reqlist(gl.RL_IN_1, gl.RL_OUT_1, gl.RL_QUERY_1, cnx=1)
    t.reqlist(gl.RL_OUT_1, gl.RL_OUT_2, gl.RL_QUERY_2)
    t.dq.file_match(gl.SQL_IN, gl.RL_OUT_2, del_dup=True)
    t.dq.file_match(gl.OUT_DUP_TMP, gl.RL_OUT_DUP_REF)

    u.log('Test rl - interuption and recovery-----------------')
    u.mkdirs(gl.RL_TMP, True)
    u.log_print()
    t.reqlist_interrupted(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, cnx=6)
    t.reqlist(gl.RL_OUT_1, gl.RL_OUT_3, gl.RL_QUERY_2, True, cnx=6)
    dq.file_match(gl.RL_OUT_2, gl.RL_OUT_3)

    clean_db([gl.SQL_T_TEST])

    u.check_log(cl.RL)


if __name__ == '__main__':
    test_rl()
