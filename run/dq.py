import pytools.dq as dq
from pytools.common import init_log
from pytools.test import gl

init_log('run_dq')

if __name__ == '__main__':
    dq.run_dq(
        IN_DIR=gl.TEST_DQ,
        IN_FILE_NAME_1="in_11",
        IN_FILE_NAME_2="in_12",
    )
else:
    dq.run_dq(
        IN_DIR=gl.TEST_DQ,
        IN_FILE_NAME_1="in_11",
        IN_FILE_NAME_2="in_12",
        OPEN_OUT_FILE=False,
    )
