import conf_main as cfg
from .file import mkdirs
from threading import RLock

# Misc
MIN_DUR_NOTIF_TRIGGER = 30
CSV_SEPARATOR = ';'
SLEEP_AFTER_DELETE_FOLDER = 0.1
VAR_DEL = '@@'
DEFAULT_FIELD = "FIELD"

counters = {}
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
paths = {}
paths['IN'] = cfg.ROOT_PATH + 'IN/'
paths['OUT'] = cfg.ROOT_PATH + 'OUT/'
paths['TMP'] = cfg.ROOT_PATH + 'TMP/'
paths['LOG'] = cfg.ROOT_PATH + 'LOG/'
paths['MAIL'] = cfg.ROOT_PATH + 'MAIL/'


def init_directories():
    for key in paths:
        cur_path = paths[key]
        mkdirs(cur_path)
