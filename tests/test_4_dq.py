import partools.dq as dq
import partools.utils as u
import partools.test.dq as td
import partools.test.dq.gl as gl

from partools.utils import g
from partools.test import ttry


def test_dq():
    u.init_log('test_dq', True)
    u.mkdirs(gl.OUT_DIR, True)
    u.log_print()

    u.log_print("Test dq no header", dashes=100)
    ttry(td.dq_t, g.E_MH, gl.IN_MH, gl.IN12, gl.OUT1)
    ttry(td.dq_t, g.E_DH, gl.IN11, gl.IN_DH, gl.OUT1)

    u.log_print("Test dup key", dashes=100)
    td.dq_t(gl.IN_DK, gl.IN12, gl.OUT1, tpd=True)

    u.log_print("Test different files comparison", dashes=100)
    dq.file_match(gl.REF1_F, gl.REF2_F, err=False, out_path=gl.OUT_FM)
    dq.file_match(gl.OUT_FM, gl.REF_FDM)

    u.log_print("Test dq No. 1", dashes=100)
    td.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 100, gl.REF_DUP1, sl=10)
    td.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 15, gl.REF_DUP1)
    td.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1_E, eq=True)

    u.log_print("Test dq No. 2", dashes=100)
    td.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 100, gl.REF_DUP2, 2)
    td.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 15, gl.REF_DUP2, 2)
    td.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2_E, eq=True)

    u.log_print("Test dq No. 3", dashes=100)
    td.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 15)
    td.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3_E, eq=True)
    td.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 100, tps=True, mls=6)
    td.file_match(gl.REF_SPLIT_3, gl.OUT_SPLIT_3)

    u.check_log(td.CL)


if __name__ == '__main__':
    test_dq()
