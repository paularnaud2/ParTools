import pytools.common as com
import pytools.dq as dq
import pytools.toolFilter as f
import pytools.toolBF as toolBF
import pytools.toolParseXML as xml
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.toolDup import find_dup
from pytools.toolDup import del_dup
from pytools.toolDup import find_dup_list
from pytools.toolDup import shuffle_csv
from pytools.toolSplit import split_file


def read_big_file():
    toolBF.read_big_file(
        IN_FILE=gl.SQL_IN,
        LINE_PER_LINE=True,
        OPEN_OUT_FILE=False,
        TEST=True,
        N_READ=10,
        MAX_LIST_SIZE=100,
    )


def search_big_file():
    toolBF.search_big_file(
        IN_FILE=gl.SQL_IN,
        OUT_FILE=gl.SEARCH_BF_OUT,
        LOOK_FOR=gl.LOOK_FOR,
        LINE_PER_LINE=True,
        OPEN_OUT_FILE=False,
        TEST=True,
        N_READ=10,
        PRINT_SIZE=10,
        MAX_LIST_SIZE=100,
    )
    dq.file_match(gl.SEARCH_BF_OUT, gl.SEARCH_BF_OUT_REF)


def filter():
    f.filter(
        IN_FILE=gl.SQL_IN,
        OUT_FILE=gl.FLT_OUT,
        FILTER=True,
        TEST_FILTER=True,
        EXTRACT_COL=True,
        OPEN_OUT_FILE=False,
        COL_LIST=['PRM', 'AFFAIRE'],
        SL_STEP=500,
    )
    dq.file_match(gl.FLT_OUT, gl.FLT_OUT_REF)


def split():
    split_file(
        IN_DIR=gl.SQL_IN,
        OUT_DIR=gl.TOOLS_OUT,
        MAX_LINE=1000,
        MAX_FILE_NB=3,
        ADD_HEADER=True,
    )
    dq.file_match(gl.S_OUT_1, gl.S_OUT_REF_1)
    dq.file_match(gl.S_OUT_2, gl.S_OUT_REF_2)
    dq.file_match(gl.S_OUT_3, gl.S_OUT_REF_3)


def parse_xml():

    xml.parse_xml(
        IN_DIR=gl.XML_IN,
        OUT_DIR=gl.XML_OUT,
        SL_STEP_READ=10,
        SL_STEP_WRITE=2,
    )


def test_tools():
    com.init_log('test_tools', True)
    com.mkdirs(gl.TOOLS_OUT, True)
    com.log_print()

    # Test toolParseXML
    parse_xml()
    dq.file_match(gl.XML_OUT, gl.XML_OUT_REF)

    # Test toolSplit
    split()

    # Test toolDup - find_dup simple
    find_dup(gl.DUP_IN, gl.DUP_OUT)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # Test toolDup - find_dup col
    find_dup(gl.DUP_COL_IN, col=1)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # Test toolDup - del_dup + shuffle
    shuffle_csv(gl.DUP_IN, gl.SHUF_OUT)
    com.log_print()
    del_dup(gl.SHUF_OUT, gl.DUP_OUT)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DEL_DUP_OUT_REF)

    # Test toolDup - find_dup_list
    list_in = com.load_csv(gl.DUP_IN)
    dup_list = find_dup_list(list_in)
    com.save_csv(dup_list, gl.DUP_OUT)
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # Test toolFilter
    filter()

    # Test BF
    read_big_file()
    search_big_file()
    toolBF.sort_big_file(gl.SQL_IN, gl.SORT_BF_OUT)
    dq.file_match(gl.SQL_IN, gl.SORT_BF_OUT, del_dup=True)

    com.check_log(cl.TO)


if __name__ == '__main__':
    test_tools()
