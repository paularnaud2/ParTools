import dq
import common as com
import dq.gl as qgl

from test import gl
from test import ttry
from common import g


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
        IN_DIR=gl.TEST_DQ,
        IN_FILE_NAME_1=in1,
        IN_FILE_NAME_2=in2,
        OUT_DIR=gl.DQ_OUT,
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
    left = gl.TEST_DQ + ref
    right = gl.DQ_OUT + out + qgl.FILE_TYPE
    dq.file_match(left, right)


def check_log():

    check_list = [
        "Log file initialised (",
        "Python version:",
        "Error: the input file * must have a header",
        "Make sure the first elements of the first two lines are of different lengths",
        "Error: files * and * don't have the same header. Input files must have the same header.",
        "Warning: 4 different lines with the same research key were identified",
        "File comparison may not work correctly. Here are your options:",
        "c (TEST_PROMPT_DK = True)",
        "List of key duplicates written in file",
        "run_dq job initialised. Input files * and * are going to be sorted and compared.",
        "lines read in * ms. * lines read in total.",
        "lines read in * ms. * lines read in total and * lines written in the output file.",
        "Maximum number of lines reached (* lines) for list no. 1, sorting...",
        "Current list sorted. Generating temporary file no. 1...",
        "Temporary file successfully generated, input file reading goes on...",
        "Filling buffer array - Iteration no. *",
        "Emptying buffer array in output file (and removing dupes)...",
        "Deleting temporary file no. 2",
        "Output file * successfully generated (* lines written, * duplicates removed).",
        "Examples of duplicates (limited to *):",
        "Input file has more than * lines. It will be splitted in * files (max file nb set to *). Continue? (y/n)",
        "y (TEST_PROMPT_SPLIT = True)",
        "Splitted file no. 1 (*) successfully generated",
        "[dq] run_dq: start",
        "[dq] sort_file: start (*)",
        "[dq] sort_file: end (* ms)",
        "[dq] compare_files: start",
        "[dq] compare_files: end (* ms)",
        "[dq] run_dq: end (* ms)",
        "[dq] file_match: start",
        "Deep comparison of '*' and '*'...",
        "[dq] file_match: end",
        "[toolSplit] split_file: start",
        "[toolSplit] split_file: end",
    ]
    com.check_log(check_list)


def test_dq():
    com.init_log('test_dq', True)
    com.mkdirs(gl.DQ_OUT, True)
    com.log_print()

    # Test dq no header
    ttry(dq_t, g.E_MH, gl.IN_MH, gl.IN12, gl.OUT1)
    ttry(dq_t, g.E_DH, gl.IN11, gl.IN_DH, gl.OUT1)

    # Test dup key
    dq_t(gl.IN_DK, gl.IN12, gl.OUT1, tpd=True)

    # Compare matching files
    dq.file_match(gl.OUT_DK, gl.OUT_DK_REF, compare=True, out=gl.OUT_FM)
    dq.file_match(gl.OUT_FM, gl.REF_FM)

    # Compare different files
    dq.file_match(gl.REF1_F, gl.REF2_F, err=False, out=gl.OUT_FM)
    dq.file_match(gl.OUT_FM, gl.REF_FDM)

    dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 100, gl.REF_DUP1, sl=10)
    dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1, 15, gl.REF_DUP1)
    dq_t(gl.IN11, gl.IN12, gl.OUT1, gl.REF1_E, eq=True)

    dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 100, gl.REF_DUP2, 2)
    dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2, 15, gl.REF_DUP2, 2)
    dq_t(gl.IN21, gl.IN22, gl.OUT2, gl.REF2_E, eq=True)

    dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 15)
    dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3_E, eq=True)
    dq_t(gl.IN31, gl.IN32, gl.OUT3, gl.REF3, 100, tps=True, mls=6)
    file_match(gl.REF_SPLIT_3, gl.OUT_SPLIT_3)

    check_log()


if __name__ == '__main__':
    test_dq()
