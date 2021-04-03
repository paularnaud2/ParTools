import pytools.dq as dq
from pytools.common import init_log

init_log('run_dq')

dq.run_dq(
    IN_FILE_NAME_1='SGE',
    IN_FILE_NAME_2='GINKO',
)
