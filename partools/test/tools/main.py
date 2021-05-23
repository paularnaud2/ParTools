import partools.dq as dq
import partools.tools as to
import partools.tools.bf as bf
import partools.test.sql as ts

from . import gl


def read_big_file():
    bf.read_big_file(
        ts.gl.IN,
        LINE_PER_LINE=True,
        OPEN_OUT_FILE=False,
        TEST=True,
        N_READ=10,
        MAX_LIST_SIZE=100,
    )


def search_big_file():
    bf.search_big_file(
        ts.gl.IN,
        gl.SEARCH_BF_OUT,
        gl.LOOK_FOR,
        LINE_PER_LINE=True,
        OPEN_OUT_FILE=False,
        TEST=True,
        N_READ=10,
        PRINT_SIZE=10,
        MAX_LIST_SIZE=100,
    )
    dq.file_match(gl.SEARCH_BF_OUT, gl.SEARCH_BF_OUT_REF)


def flt():
    to.flt(
        ts.gl.IN,
        gl.FLT_OUT,
        COL_LIST=['PRM', 'AFFAIRE'],
        FF=filter_function,
        EXTRACT_COL=True,
        OPEN_OUT_FILE=False,
        SL_STEP=500,
    )
    dq.file_match(gl.FLT_OUT, gl.FLT_OUT_REF)


def filter_function(line_list):
    # Lines for which this function returns True will be written in the output file
    # If not filter function is given in input (ie. gl.FF is not defined),
    # no filter will be applied.
    cond = line_list[2].find('01') == 0

    return cond


def split():
    to.split_file(
        ts.gl.IN,
        gl.OUT_DIR,
        MAX_LINE=1000,
        MAX_FILE_NB=3,
        ADD_HEADER=True,
    )
    dq.file_match(gl.S_OUT_1, gl.S_OUT_REF_1)
    dq.file_match(gl.S_OUT_2, gl.S_OUT_REF_2)
    dq.file_match(gl.S_OUT_3, gl.S_OUT_REF_3)


def parse_xml():
    to.parse_xml(
        gl.XML_IN,
        gl.XML_OUT,
        OPEN_OUT_FILE=False,
        SL_STEP_READ=10,
        SL_STEP_WRITE=2,
    )
