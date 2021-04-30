import pytools.common as com
import pytools.common.g as g
import pytools.dq as dq

import pytools.test.sql as t
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.test import ttry
from pytools.test import is_test_db_defined


def test_sql():
    com.init_log("test_sql", True)
    if not is_test_db_defined():
        return

    com.log("Test connect------------------------------------------")
    t.connect()

    com.log("Test iutd---------------------------------------------")
    t.reset()
    t.iutd()

    com.log("Test upload-------------------------------------------")
    # Test missing header in input file
    ttry(t.upload, g.E_MH, gl.SQL_IN_MH)
    # Test upload with interruption
    t.upload_interrupted()
    t.upload(gl.SQL_IN, tr=True)

    com.log("Test download------------------------------------------")
    # Test download no output
    t.download(gl.SQL_QUERY_NO, gl.SQL_DL_OUT, ti=True)

    # Test download standard
    t.reset()
    t.download(gl.SQL_QUERY, gl.SQL_DL_OUT)
    dq.file_match(gl.SQL_IN, gl.SQL_DL_OUT)
    dq.file_match(gl.OUT_DUP_TMP, gl.SQL_OUT_DUP_REF)

    # Test download RG with merge
    t.download_interrupted(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG)
    t.download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, tr=True, sl=50)
    dq.file_match(gl.SQL_DL_OUT, gl.SQL_DL_OUT_RG)

    # Test download RG without merge
    t.reset()
    t.download(gl.SQL_QUERY_RG, gl.SQL_DL_OUT_RG, merge=False, cnx=1, sl=50)
    dq.file_match(gl.SQL_RG_REF, gl.SQL_RG_COMP)

    # Test count simple
    t.reset()
    t.download(gl.SQL_QUERY_COUNT_1, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)
    t.download(gl.SQL_QUERY_COUNT_1_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_1_REF)

    # Test count group by
    t.reset()
    t.download(gl.SQL_QUERY_COUNT_2, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)
    t.download(gl.SQL_QUERY_COUNT_2_RG, gl.SQL_DL_OUT_COUNT)
    dq.file_match(gl.SQL_DL_OUT_COUNT, gl.SQL_DL_OUT_COUNT_2_REF)

    # Cleaning DB
    t.clean_db([gl.SQL_T_TEST, gl.SQL_T_IUTD])

    com.check_log(cl.SQ)


if __name__ == "__main__":
    test_sql()
