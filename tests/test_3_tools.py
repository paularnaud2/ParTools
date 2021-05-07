import pytools.utils as u
import pytools.dq as dq
import pytools.tools.bf as bf
import pytools.test.tools as t
import pytools.tools.dup as dup
import pytools.test.check_log as cl

from pytools.test import gl


def test_tools():
    u.init_log('test_tools', True)
    u.mkdirs(gl.TOOLS_OUT, True)
    u.log_print()

    u.log_print("Test tools.xml", dashes=100)
    t.parse_xml()
    dq.file_match(gl.XML_OUT, gl.XML_OUT_REF)

    u.log_print("Test toolSplit", dashes=100)
    t.split()

    u.log_print("Test toolDup - dup.find_dup simple", dashes=100)
    dup.find_dup(gl.DUP_IN, gl.DUP_OUT)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolDup - dup.find_dup col", dashes=100)
    dup.find_dup(gl.DUP_COL_IN, col=1)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolDup - dup.del_dup + shuffle", dashes=100)
    dup.shuffle_csv(gl.DUP_IN, gl.SHUF_OUT)
    u.log_print()
    dup.del_dup(gl.SHUF_OUT, gl.DUP_OUT)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DEL_DUP_OUT_REF)

    u.log_print("Test toolDup - dup.find_dup_list", dashes=100)
    list_in = u.load_csv(gl.DUP_IN)
    dup_list = dup.find_dup_list(list_in)
    u.save_csv(dup_list, gl.DUP_OUT)
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolFilter", dashes=100)
    t.filter()

    u.log_print("Test BF", dashes=100)
    t.read_big_file()
    t.search_big_file()
    bf.sort_big_file(gl.SQL_IN, gl.SORT_BF_OUT)
    dq.file_match(gl.SQL_IN, gl.SORT_BF_OUT, del_dup=True)

    u.check_log(cl.TO)


if __name__ == '__main__':
    test_tools()
