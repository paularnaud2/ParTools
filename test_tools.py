import qdd as q
import common as com
import toolFilter as f

from test import gl
from toolParseXML import parse_xml
from toolSplit import split_file
from toolDup import del_dup
from toolDup import find_dup
from toolDup import find_dup_list


def filter():
    f.filter(
        IN_FILE=gl.SQL_IN_FILE,
        OUT_FILE=gl.FLT_OUT,
        FILTER=True,
        TEST_FILTER=True,
        EXTRACT_COL=True,
        OPEN_OUT_FILE=False,
        COL_LIST=['PRM', 'AFFAIRE'],
        SL_STEP=500,
    )
    q.file_match(gl.FLT_OUT, gl.FLT_OUT_REF)


def split():
    split_file(
        IN_DIR=gl.SQL_IN_FILE,
        OUT_DIR=gl.TOOLS_OUT,
        MAX_LINE=1000,
        MAX_FILE_NB=3,
        ADD_HEADER=True,
    )
    q.file_match(gl.S_OUT_1, gl.S_OUT_REF_1)
    q.file_match(gl.S_OUT_2, gl.S_OUT_REF_2)
    q.file_match(gl.S_OUT_3, gl.S_OUT_REF_3)


def test_tools():
    com.init_log('test_tools', True)
    com.mkdirs(gl.TOOLS_OUT, True)
    com.log_print()

    # test toolParseXML
    parse_xml(IN_DIR=gl.XML_IN, OUT_DIR=gl.XML_OUT)
    q.file_match(gl.XML_OUT, gl.XML_OUT_REF)

    # test toolSplit
    split()

    # test toolDup - find_dup simple
    find_dup(gl.DUP_IN, gl.DUP_OUT)
    com.log_print()
    q.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # test toolDup - find_dup col
    find_dup(gl.DUP_COL_IN, col=1)
    com.log_print()
    q.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # test toolDup - del_dup
    del_dup(gl.DUP_IN, gl.DUP_OUT)
    com.log_print()
    q.file_match(gl.DUP_OUT, gl.DEL_DUP_OUT_REF)

    # test toolDup - find_dup_list
    list_in = com.load_csv(gl.DUP_IN)
    dup_list = find_dup_list(list_in)
    com.save_csv(dup_list, gl.DUP_OUT)
    q.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    # test toolFilter
    filter()


if __name__ == '__main__':
    test_tools()
