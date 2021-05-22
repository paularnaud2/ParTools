import os.path as p
from threading import RLock

from partools import cfg
from partools import quickstart

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
GITHUB_LINK = 'https://github.com/paularnaud2/ParTools'
GITHUB_ISSUES = GITHUB_LINK + '/issues'

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
    """Initialises the partools package"""

    if p.exists(dirs['LOG']):
        return

    init_directories()
    save_list(['*'], cfg.FILES_DIR + '.gitignore')
    init_log('init')
    path = cfg.__file__
    if p.basename(path) == 'conf.py':
        s = (" or set up your own 'PTconf.py' file (by copying the"
             " default conf.py file) at the root of your cwd")
    else:
        path = p.abspath(path)
        s = ''
    log("ParTools package successfully initialised\n"
        f"Checkout the README.md on GitHub: {GITHUB_LINK}\n"
        f"Get started here: {p.dirname(quickstart.__file__)}\n"
        f"Set up your conf here: {path}{s}\n"
        "Happy scripting!\n")


def get_confidential(raise_e=True):

    if not p.exists(cfg.CFI_PATH):
        log(E_CFI)
        if raise_e:
            raise Exception(E_CFI)
        else:
            return False
    cfi_list = load_txt(cfg.CFI_PATH)
    cfi = list_to_dict(cfi_list)
    return cfi
