import pytools.dq as dq
import pytools.common as com
import pytools.test.dq as t
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.test import ttry
from pytools.common import g


def test_dq():
    com.init_log('test_dq', True)
    com.mkdirs(gl.DQ_OUT, True)
    com.log_print()

    # Test dq no header
    ttry(t.dq_t, g.E_MH, gl.IN_MH, gl.IN12, gl.OUT1)
    ttry(t.dq_t, g.E_DH, gl.IN11, gl.IN_DH, gl.OUT1)

    # Test dup key
    t.dq_t(gl.IN_DK, gl.IN12, gl.OUT1, tpd=True)

    # Compare matching files
    dq.file_match(gl.OUT_DK, gl.OUT_DK_REF, compare=True, out=gl.OUT_FM)
    dq.file_match(gl.OUT_FM, gl.REF_FM)

    # Compare different files
    dq.file_match(gl.REF1_F, gl.REF2_F, err=False, out=gl.OUT_FM)
    dq.file_match(gl.OUT_FM, gl.REF_FDM)

    t.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 100, gl.REF_DUP1, sl=10)
    t.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 15, gl.REF_DUP1)
    t.dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1_E, eq=True)

    t.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 100, gl.REF_DUP2, 2)
    t.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 15, gl.REF_DUP2, 2)
    t.dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2_E, eq=True)

    t.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 15)
    t.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3_E, eq=True)
    t.dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 100, tps=True, mls=6)
    t.file_match(gl.REF_SPLIT_3, gl.OUT_SPLIT_3)

    com.check_log(cl.DQ)


if __name__ == '__main__':
    test_dq()