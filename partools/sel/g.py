import partools as pt
from sel import cfg

if cfg.TEST:
    OUT_DIR = 'tests/files/'
else:
    r = pt.utils.g.dirs['OUT']
    OUT_DIR = f'{r}TPA/{cfg.DATE_DIR}/'

driver = None
start_time = None
main_st = None
all_sub_check_ok = False
version_printed = False
retry = 0
sum = {}
sub_sum = {}
s_dir = ''
main = ''
check = ''
check_key = ''
sub_check = ''
sub_check_key = ''
env = ''
main_dur = ''
path = ''
dir = ''
cur_url = ''
source = ''
