import qdd
from common import init_log
init_log('run_qdd')

if __name__ == '__main__':
    qdd.run_qdd(
        IN_FILE_NAME_1='SGE',
        IN_FILE_NAME_2='GINKO',
    )
