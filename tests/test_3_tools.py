import pytools.common as com
import pytools.dq as dq
import pytools.tools.filter as f
import pytools.tools.bf as bf
import pytools.tools.xml as xml
import pytools.test.check_log as cl

from pytools.test import gl
from pytools.tools.dup import find_dup
from pytools.tools.dup import del_dup
from pytools.tools.dup import find_dup_list
from pytools.tools.dup import shuffle_csv
from pytools.tools.split import split_file


def read_big_file():
    bf.read_big_file(
        gl.SQL_IN,
        LINE_PER_LINE=True,
        OPEN_OUT_FILE=False,
        TEST=True,
        N_READ=10,
        MAX_LIST_SIZE=100,
    )


def search_big_file():
    bf.search_big_file(
        gl.SQL_IN,
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


def filter():
    f.filter(
        gl.SQL_IN,
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
    split_file(
        gl.SQL_IN,
        gl.TOOLS_OUT,
        MAX_LINE=1000,
        MAX_FILE_NB=3,
        ADD_HEADER=True,
    )
    dq.file_match(gl.S_OUT_1, gl.S_OUT_REF_1)
    dq.file_match(gl.S_OUT_2, gl.S_OUT_REF_2)
    dq.file_match(gl.S_OUT_3, gl.S_OUT_REF_3)


def parse_xml():
    xml.parse_xml(
        gl.XML_IN,
        gl.XML_OUT,
        OPEN_OUT_FILE=False,
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
    bf.sort_big_file(gl.SQL_IN, gl.SORT_BF_OUT)
    dq.file_match(gl.SQL_IN, gl.SORT_BF_OUT, del_dup=True)

    com.check_log(cl.TO)


if __name__ == '__main__':
    test_tools()
