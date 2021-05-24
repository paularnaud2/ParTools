from . import gl


def download():
    import partools.sql as sql

    if gl.SKIP_JOIN:
        gl.OUT_SQL = gl.OUT_PATH

    sql.download(
        CNX_INFO=gl.CNX_INFO,
        DB=gl.DB,
        ENV=gl.ENV,
        QUERY_IN=gl.QUERY_IN,
        QUERY_LIST=gl.query_list,
        OUT_PATH=gl.OUT_SQL,
        MAX_DB_CNX=gl.MAX_DB_CNX,
        VAR_DICT=gl.VAR_DICT,
        TEST_RECOVER=gl.TEST_RECOVER,
        OPEN_OUT_FILE=False,
        CHECK_DUP=False,
        MD=gl.MD,
    )


def finish(start_time):
    import partools.utils as u
    import partools.tools as to
    import partools.utils.sTools as st

    if gl.CHECK_DUP:
        s = "Checking duplicates on the first column of the output file..."
        u.log(s)
        to.find_dup(gl.OUT_PATH, col=1)
        u.log_print('|')

    (dms, dstr) = u.get_duration_string(start_time, True)
    s = f"reqlist: end ({dstr})"
    u.log("[rl] " + s)
    if gl.MSG_BOX_END:
        st.msg_box(s, "rl", dms)
    u.log_print()
    if gl.OPEN_OUT_FILE:
        u.startfile(gl.OUT_PATH)
