import qdd as q
import common as com
import qdd.gl as qgl

from test import gl
from test import ttry
from common import g


def qdd(in1,
        in2,
        out,
        ref='',
        mrl=100,
        ref_dup='',
        dup_nb=1,
        tps=False,
        tpd=False,
        eq=False,
        mls=100):

    q.run_qdd(
        IN_DIR=gl.TEST_QDD,
        IN_FILE_NAME_1=in1,
        IN_FILE_NAME_2=in2,
        OUT_DIR=gl.QDD_OUT,
        OUT_FILE_NAME=out,
        MAX_ROW_LIST=mrl,
        OUT_DUP_FILE_NAME='dup_',
        EQUAL_OUT=eq,
        DIFF_OUT=False,
        OPEN_OUT_FILE=False,
        TEST_PROMPT_SPLIT=tps,
        TEST_PROMPT_DK=tpd,
        MAX_LINE_SPLIT=mls,
        MAX_FILE_NB_SPLIT=10,
    )

    if ref:
        file_match(ref, out)
    if ref_dup:
        file_match(ref_dup, f'dup_{dup_nb}')


def file_match(ref, out):
    left = gl.TEST_QDD + ref
    right = gl.QDD_OUT + out + qgl.FILE_TYPE
    q.file_match(left, right)


def test_qdd():
    com.init_log('test_qdd', True)
    com.mkdirs(gl.QDD_OUT, True)
    com.log_print()

    # test qdd no header
    ttry(qdd, g.E_MH, gl.IN_MH, gl.IN12, gl.OUT1)
    ttry(qdd, g.E_DH, gl.IN11, gl.IN_DH, gl.OUT1)

    # test dup key
    qdd(gl.IN_DK, gl.IN12, gl.OUT1, tpd=True)

    # compare matching files
    q.file_match(gl.OUT_DK, gl.OUT_DK_REF, compare=True, out=gl.OUT_FM)
    q.file_match(gl.OUT_FM, gl.REF_FM)

    # compare different files
    q.file_match(gl.REF1_F, gl.REF2_F, err=False, out=gl.OUT_FM)
    q.file_match(gl.OUT_FM, gl.REF_FDM)

    qdd(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 100, gl.REF_DUP1)
    qdd(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 15, gl.REF_DUP1)
    qdd(gl.IN11, gl.IN12, gl.OUT1, gl.REF1_E, eq=True)

    qdd(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 100, gl.REF_DUP2, 2)
    qdd(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 15, gl.REF_DUP2, 2)
    qdd(gl.IN21, gl.IN22, gl.OUT2, gl.REF2_E, eq=True)

    qdd(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 15)
    qdd(gl.IN31, gl.IN32, gl.OUT3, gl.REF3_E, eq=True)
    qdd(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 100, tps=True, mls=6)
    file_match(gl.REF_SPLIT_3, gl.OUT_SPLIT_3)


if __name__ == '__main__':
    test_qdd()
