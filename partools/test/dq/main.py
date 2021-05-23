import partools.dq as dq
import partools.dq.gl as qgl

from . import gl


def dq_t(in1,
         in2,
         out,
         ref='',
         mrl=100,
         ref_dup='',
         dup_nb=1,
         tps=False,
         tpd=False,
         eq=False,
         mls=100,
         sl=100):

    dq.run_dq(
        IN_DIR=gl.FILES_DIR,
        IN_FILE_NAME_1=in1,
        IN_FILE_NAME_2=in2,
        OUT_DIR=gl.OUT_DIR,
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
        SL_STEP=sl,
    )

    if ref:
        file_match(ref, out)
    if ref_dup:
        file_match(ref_dup, f'dup_{dup_nb}')


def file_match(ref, out):
    left = gl.FILES_DIR + ref
    right = gl.OUT_DIR + out + qgl.FILE_TYPE
    dq.file_match(left, right)
