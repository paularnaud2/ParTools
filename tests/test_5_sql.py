import pytools.utils as u
import pytools.dq as dq

import pytools.test.sql as t
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.test import ttry
from pytools.test import is_test_db_defined


def test_sql():
    u.init_log("test_sql", True)
    if not is_test_db_defined():
        return

    u.log_print("Test connect", dashes=100)
    t.connect()

    u.log_print("Test iutd", dashes=100)
    t.reset()
    t.iutd()

    u.log_print("Test upload - missing header in input file", dashes=100)
    ttry(t.upload, u.g.E_MH, gl.SQL_IN_MH)

    u.log_print("Test upload - interuption and recovery", dashes=100)
    t.upload_interrupted()
    t.upload(gl.SQL_IN, tr=True)

    u.log_print("Test download - no output", dashes=100)
    t.download(gl.SQL_QUERY_NO, gl.SQL_DL_OUT, ti=True)

    u.log_print("Test download standard", dashes=100)
    t.reset()
    t.download(gl.SQL_QUERY, gl.SQL_DL_OUT)
    dq.file_match(gl.SQL_IN, gl.SQL_DL_OUT)
    dq.file_match(gl.OUT_DUP_TMP, gl.SQL_OUT_DUP_REF)

    s = "Test download RG with merge - interuption and recovery"
    u.log_print(s, dashes=100)
    t.download_interrupted(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG)
    t.download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, tr=True, sl=50)
    dq.file_match(gl.SQL_DL_OUT, gl.SQL_DL_OUT_RG)

    u.log_print("Test download RG without merge", dashes=100)
    t.reset()
    t.download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, merge=False, cnx=1, sl=50)
    dq.file_match(gl.SQL_RG_REF, gl.SQL_RG_COMP)

    u.log_print("Test download - count simple", dashes=100)
    t.reset()
    t.download(gl.SQL_QUERY_COUNT_1, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)
    t.download(gl.SQL_QUERY_COUNT_1_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)

    u.log_print("Test download - count group by", dashes=100)
    t.reset()
    t.download(gl.SQL_QUERY_COUNT_2, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)
    t.download(gl.SQL_QUERY_COUNT_2_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)

    t.clean_db([gl.SQL_T_TEST, gl.SQL_T_IUTD])

    u.check_log(cl.SQ)


if __name__ == "__main__":
    test_sql()
