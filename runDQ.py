import dq
from common import init_log
init_log('run_dq')

if __name__ == '__main__':
    dq.run_dq(
        IN_FILE_NAME_1='SGE',
        IN_FILE_NAME_2='GINKO',
    )
