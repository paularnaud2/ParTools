# The dq package allows you to compare two big csv files (> 100 Mo).
# A details result of the comparison is ouput.

import pytools.dq as dq
from pytools.common import init_log
from pytools.test import gl

init_log('run_dq')

dq.run_dq(
    IN_DIR=gl.TEST_DQ,
    IN_FILE_NAME_1="in_11",
    IN_FILE_NAME_2="in_12",
)
