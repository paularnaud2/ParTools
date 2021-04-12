from threading import RLock
import conf._conf_main as cfg
from .file import mkdirs

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
paths = {}
paths['IN'] = cfg.IO_PATH + 'IN/'
paths['OUT'] = cfg.IO_PATH + 'OUT/'
paths['TMP'] = cfg.IO_PATH + 'TMP/'
paths['LOG'] = cfg.IO_PATH + 'LOG/'


def init_directories():
    for key in paths:
        cur_path = paths[key]
        mkdirs(cur_path)
