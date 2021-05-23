import partools.utils as u
import partools.dq as dq

import partools.test as t
import partools.test.sql as ts
import partools.test.sql.gl as gl


def test_sql():
    u.init_log("test_sql", True)
    if not ts.is_test_db_defined():
        return

    u.log_print("Test connect", dashes=100)
    ts.connect()

    u.log_print("Test iutd", dashes=100)
    ts.reset()
    ts.iutd()

    u.log_print("Test upload - missing header in input file", dashes=100)
    t.ttry(ts.upload, u.g.E_MH, gl.IN_MH)

    u.log_print("Test upload - interuption and recovery", dashes=100)
    ts.upload_interrupted()
    ts.upload(gl.IN, tr=True)

    u.log_print("Test download - no output", dashes=100)
    ts.download(gl.QUERY_NO, gl.DL_OUT, ti=True)

    u.log_print("Test download standard", dashes=100)
    ts.reset()
    ts.download(gl.QUERY, gl.DL_OUT)
    dq.file_match(gl.IN, gl.DL_OUT)
    dq.file_match(t.gl.OUT_DUP_TMP, gl.OUT_DUP_REF)

    s = "Test download RG with merge - interuption and recovery"
    u.log_print(s, dashes=100)
    ts.download_interrupted(gl.QUERY_RG, gl.DL_OUT_RG)
    ts.download(gl.QUERY_RG, gl.DL_OUT_RG, tr=True, sl=50)
    dq.file_match(gl.DL_OUT, gl.DL_OUT_RG)

    u.log_print("Test download RG without merge", dashes=100)
    ts.reset()
    ts.download(gl.QUERY_RG, gl.DL_OUT_RG, merge=False, cnx=1, sl=50)
    dq.file_match(gl.RG_REF, gl.RG_COMP)

    u.log_print("Test download - count simple", dashes=100)
    ts.reset()
    ts.download(gl.QUERY_COUNT_1, gl.DL_OUT_COUNT)
    dq.file_match(gl.DL_OUT_COUNT, gl.DL_OUT_COUNT_1_REF)
    ts.download(gl.QUERY_COUNT_1_RG, gl.DL_OUT_COUNT)
    dq.file_match(gl.DL_OUT_COUNT, gl.DL_OUT_COUNT_1_REF)

    u.log_print("Test download - count group by", dashes=100)
    ts.reset()
    ts.download(gl.QUERY_COUNT_2, gl.DL_OUT_COUNT)
    dq.file_match(gl.DL_OUT_COUNT, gl.DL_OUT_COUNT_2_REF)
    ts.download(gl.QUERY_COUNT_2_RG, gl.DL_OUT_COUNT)
    dq.file_match(gl.DL_OUT_COUNT, gl.DL_OUT_COUNT_2_REF)

    ts.clean_db([gl.T_TEST, gl.T_IUTD])

    u.check_log(ts.CL)


if __name__ == "__main__":
    test_sql()
