import pytools.common as com
import pytools.dq as dq
import pytools.tools.bf as bf
import pytools.tools.dup as dup
import pytools.test.tools as t
import pytools.test.check_log as cl

from pytools.test import gl


def test_tools():
    com.init_log('test_tools', True)
    com.mkdirs(gl.TOOLS_OUT, True)
    com.log_print()

    com.log("Test tools.xml------------------------------------------")
    t.parse_xml()
    dq.file_match(gl.XML_OUT, gl.XML_OUT_REF)

    com.log("Test toolSplit------------------------------------------")
    t.split()

    com.log("Test toolDup - dup.find_dup simple----------------------")
    dup.find_dup(gl.DUP_IN, gl.DUP_OUT)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    com.log("Test toolDup - dup.find_dup col-------------------------")
    dup.find_dup(gl.DUP_COL_IN, col=1)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    com.log("Test toolDup - dup.del_dup + shuffle--------------------")
    dup.shuffle_csv(gl.DUP_IN, gl.SHUF_OUT)
    com.log_print()
    dup.del_dup(gl.SHUF_OUT, gl.DUP_OUT)
    com.log_print()
    dq.file_match(gl.DUP_OUT, gl.DEL_DUP_OUT_REF)

    com.log("Test toolDup - dup.find_dup_list------------------------")
    list_in = com.load_csv(gl.DUP_IN)
    dup_list = dup.find_dup_list(list_in)
    com.save_csv(dup_list, gl.DUP_OUT)
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    com.log("Test toolFilter-----------------------------------------")
    t.filter()

    com.log("Test BF-------------------------------------------------")
    t.read_big_file()
    t.search_big_file()
    bf.sort_big_file(gl.SQL_IN, gl.SORT_BF_OUT)
    dq.file_match(gl.SQL_IN, gl.SORT_BF_OUT, del_dup=True)

    com.check_log(cl.TO)


if __name__ == '__main__':
    test_tools()
