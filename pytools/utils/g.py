from threading import RLock
from os.path import exists

from pytools import cfg
from .file import mkdirs
from .file import load_txt
from .file import save_list
from .log import log
from .log import init_log
from .tools import list_to_dict

# Misc
CSV_SEPARATOR = ';'
VAR_DEL = '@@'
DEFAULT_FIELD = "FIELD"

MAX_EXAMPLE_PRINT = 5
MIN_DUR_MSG_BOX_TRIGGER = 30
MAX_LOG_VAR_CHAR = 100

verrou = RLock()

# Exceptions
E_MH = "Missing header (first elements of line 1 and 2 must be of different length)"
E_MV = "Missing variable"
E_DH = "Different headers"
E_VA = "Void array"
E_CFI = f"Confidential file '{cfg.CFI_PATH}' not found"

# Log
LOG_LEVEL = 0
log_file_initialised = False
log_path = ''
logs = []
sl_time_dict = {}
sl_detail = {}

# Path
r = cfg.FILES_DIR
dirs = {}
dirs['IN'] = r + 'in/'
dirs['OUT'] = r + 'out/'
dirs['TMP'] = r + 'tmp/'
dirs['LOG'] = r + 'log/'


def init_directories():
    for key in dirs:
        cur_dir = dirs[key]
        mkdirs(cur_dir)


def init_PT():
    if exists(dirs['LOG']):
        return

    init_directories()
    save_list(['*'], cfg.FILES_DIR + '.gitignore')
    init_log('init')
    log("PyTools package successfully initialised."
        f" Set up your conf here: {cfg.__file__}\n")


def get_confidential(raise_e=True):

    if not exists(cfg.CFI_PATH):
        log(E_CFI)
        if raise_e:
            raise Exception(E_CFI)
        else:
            return False
    cfi_list = load_txt(cfg.CFI_PATH)
    cfi = list_to_dict(cfi_list)
    return cfi
