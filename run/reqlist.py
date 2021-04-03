from pytools.common import init_log
from pytools.reqlist import run_reqList

init_log('run_reqlist')

run_reqList(
    MAX_DB_CNX=8,
    SQUEEZE_JOIN=False,
    SQUEEZE_SQL=False,
    CHECK_DUP=True,
    NB_MAX_ELT_IN_STATEMENT=500,
    SL_STEP_QUERY=50,
)
