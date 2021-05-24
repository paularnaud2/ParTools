import partools.dq as dq
import partools.utils as u
import partools.tools as to
import partools.tools.bf as bf

import partools.test.sql as ts
import partools.test.tools as tt
import partools.test.tools.gl as gl


def test_tools():
    u.init_log('test_tools', True)
    u.mkdirs(gl.OUT_DIR, True)
    u.log_print()

    u.log_print("Test tools.xml", dashes=100)
    tt.parse_xml()
    dq.file_match(gl.XML_OUT, gl.XML_OUT_REF)

    u.log_print("Test toolSplit", dashes=100)
    tt.split()

    u.log_print("Test toolDup - to.find_dup simple", dashes=100)
    to.find_dup(gl.DUP_IN, gl.DUP_OUT)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolDup - to.find_dup col", dashes=100)
    to.find_dup(gl.DUP_COL_IN, col=1)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolDup - to.del_dup + shuffle", dashes=100)
    to.shuffle_file(gl.DUP_IN, gl.SHUF_OUT)
    u.log_print()
    to.del_dup(gl.SHUF_OUT, gl.DUP_OUT)
    u.log_print()
    dq.file_match(gl.DUP_OUT, gl.DEL_DUP_OUT_REF)

    u.log_print("Test toolDup - to.find_dup_list", dashes=100)
    list_in = u.load_csv(gl.DUP_IN)
    dup_list = to.find_dup_list(list_in)
    u.save_csv(dup_list, gl.DUP_OUT)
    dq.file_match(gl.DUP_OUT, gl.DUP_OUT_REF)

    u.log_print("Test toolFilter", dashes=100)
    tt.flt()

    u.log_print("Test BF", dashes=100)
    tt.read_big_file()
    tt.search_big_file()
    bf.sort_big_file(ts.gl.IN, gl.SORT_BF_OUT)
    dq.file_match(ts.gl.IN, gl.SORT_BF_OUT, del_dup=True)

    u.check_log(tt.CL)


if __name__ == '__main__':
    test_tools()
