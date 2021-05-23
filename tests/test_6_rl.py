import partools.utils as u
import partools.dq as dq

import partools.test as t
import partools.test.sql as ts
import partools.test.rl as tr
import partools.test.rl.gl as gl


def test_rl():
    u.init_log('test_rl', True)
    if not ts.is_test_db_defined():
        return

    u.mkdirs(gl.TMP_DIR, True)
    u.mkdirs(ts.gl.TMP_DIR, True)
    u.mkdirs(gl.OUT_DIR, True)
    u.log_print()

    u.log_print('Test join', dashes=100)
    tr.left_join_files(gl.LEFT_1, gl.RIGHT_1, gl.OUT_JOIN_REF_1)
    tr.left_join_files(gl.LEFT_2, gl.RIGHT_2, gl.OUT_JOIN_REF_2)
    tr.left_join_files(gl.LEFT_3, gl.RIGHT_3, gl.OUT_JOIN_REF_3)

    u.log_print('Preparing DB', dashes=100)
    ts.upload(ts.gl.IN)
    arr = u.load_csv(ts.gl.IN)
    arr = [elt[0] for elt in arr]
    u.save_csv(arr, gl.IN_1)

    u.log_print('Test rl - no sql output', dashes=100)
    t.ttry(tr.reqlist, u.g.E_VA, gl.IN_1, gl.OUT_1, gl.QUERY_NO)

    u.log_print('Test rl - no var in query', dashes=100)
    t.ttry(tr.reqlist, u.g.E_MV, gl.IN_1, gl.OUT_1, gl.QUERY_MV)

    u.log_print('Test rl - missing header', dashes=100)
    u.save_csv(arr[1:], gl.IN_MH)
    t.ttry(tr.reqlist, u.g.E_MH, gl.IN_MH, gl.OUT_1, gl.QUERY_1)

    u.log_print('Test rl - standard', dashes=100)
    tr.reqlist(gl.IN_1, gl.OUT_1, gl.QUERY_1, cnx=1)
    tr.reqlist(gl.OUT_1, gl.OUT_2, gl.QUERY_2)
    dq.file_match(ts.gl.IN, gl.OUT_2, del_dup=True)
    dq.file_match(t.gl.OUT_DUP_TMP, gl.OUT_DUP_REF)

    u.log_print('Test rl - interuption and recovery', dashes=100)
    u.mkdirs(gl.TMP_DIR, True)
    u.log_print()
    args = [gl.OUT_1, gl.OUT_3, gl.QUERY_2]
    tr.reqlist_interrupted(*args, cnx=6)
    tr.reqlist(gl.OUT_1, gl.OUT_3, gl.QUERY_2, True, cnx=6)
    dq.file_match(gl.OUT_2, gl.OUT_3)

    ts.clean_db([ts.gl.T_TEST])

    u.check_log(tr.CL)


if __name__ == '__main__':
    test_rl()
