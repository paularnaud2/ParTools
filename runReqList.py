from common import init_log
init_log('run_reqlist')

if __name__ == '__main__':
    from reqlist import run_reqList
    run_reqList(
        MAX_DB_CNX=8,
        SQUEEZE_JOIN=False,
        SQUEEZE_SQL=False,
        CHECK_DUP=True,
        NB_MAX_ELT_IN_STATEMENT=500,
        SL_STEP_QUERY=50,
    )
