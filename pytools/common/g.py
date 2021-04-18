from threading import RLock
from os.path import exists

import pytools.conf as cfg
from pytools import get_root
from .file import mkdirs
from .file import save_list
from .log import log
from .log import init_log

# Misc
CSV_SEPARATOR = ';'
VAR_DEL = '@@'
DEFAULT_FIELD = "FIELD"
LIKE_MATCH_OUT = "like_match_out.csv"

MAX_EXAMPLE_PRINT = 5
MIN_DUR_NOTIF_TRIGGER = 30
MAX_LOG_VAR_CHAR = 100

verrou = RLock()

# Exceptions
E_MH = "Missing header (first elements of line 1 and 2 must be of different length)"
E_MV = "Missing variable"
E_DH = "Different headers"
E_VA = "Void array"

# Log
LOG_LEVEL = 0
LOG_FILE_INITIALISED = False
LOG_FILE = None
LOG_OUTPUT = True

sl_time_dict = {}
sl_detail = {}

# Path
r = cfg.FILES_PATH
paths = {}
paths['IN'] = r + 'in/'
paths['OUT'] = r + 'out/'
paths['TMP'] = r + 'tmp/'
paths['LOG'] = r + 'log/'

root_path = get_root()
conf_path = root_path + 'conf.py'


def init_directories():
    for key in paths:
        cur_path = paths[key]
        mkdirs(cur_path)


def init_PT():
    if exists(paths['LOG']):
        return

    init_directories()
    save_list(['*'], cfg.FILES_PATH + '.gitignore')
    init_log('init')
    log("PyTools package successfully initialised."
        f" Set up your conf here: {conf_path}\n")
