import partools.rl as rl
import partools.test.sql as ts

from . import gl


def reqlist(inp, out, query, tr=False, md='', cnx=3, elt=200):

    rl.reqlist(
        DB=ts.gl.DB,
        QUERY_IN=query,
        IN_PATH=inp,
        OUT_PATH=out,
        VAR_DICT={'TABLE_NAME': ts.gl.T_TEST},
        MAX_DB_CNX=cnx,
        NB_MAX_ELT_IN_STATEMENT=elt,
        SKIP_JOIN=False,
        SKIP_SQL=False,
        CHECK_DUP=True,
        OPEN_OUT_FILE=False,
        TEST_RECOVER=tr,
        MD=md,
    )


def left_join_files(left, right, ref):
    import partools.dq as dq

    rl.left_join_files(left, right, gl.OUT_JOIN, debug=False)
    dq.file_match(ref, gl.OUT_JOIN)


def reqlist_interrupted(inp, out, query, cnx):
    init_msg = "[rl] reqlist: start"
    kwargs = {"inp": inp, "out": out, "query": query, "tr": True, "cnx": cnx}
    ts.interrupt(reqlist, kwargs, init_msg)
