import re

import pytools.common as com
import pytools.common.g as g

from . import gl


def range_query():

    rg_file_name = get_rg_file_name(gl.query)
    if not rg_file_name:
        gl.range_query = False
        return False

    gl.range_query = True
    gl.ql_replace = True
    gl.VAR_IN = rg_file_name
    gen_query_list(rg_file_name)

    return True


def get_rg_file_name(in_str):

    exp = '(.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m = re.search(exp, in_str)
    exp_comment = '(.*-{2,}.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m_comment = re.search(exp_comment, in_str)
    if m and not m_comment:
        rg_file_name = m.group(2)
        return rg_file_name
    else:
        return ''


def gen_query_list(rg_file_name):

    rg_path = gl.RANGE_DIR + rg_file_name + gl.FILE_TYPE
    gl.rg_list = com.load_txt(rg_path)
    gl.QUERY_LIST = [[elt, elt] for elt in gl.rg_list]
    com.log(f"Range query detected. Base query:\n{gl.query}\n;")
