import os.path as p
from threading import RLock

import partools as pt

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

verrou = RLock()

# Exceptions
E_MH = "Missing header (first elements of line 1 and 2 must be of different length)"
E_MV = "Missing variable"
E_DH = "Different headers"
E_VA = "Void array"
E_CFI = f"Confidential file '{pt.cfg.CFI_PATH}' not found"

# Log
LOG_LEVEL = 0
log_file_initialised = False
log_path = ''
logs = []
sl_time_dict = {}
sl_detail = {}
dirs = {}

# Paths
r = pt.cfg.FILES_DIR
dirs['IN'] = r + 'in/'
dirs['OUT'] = r + 'out/'
dirs['TMP'] = r + 'tmp/'
dirs['LOG'] = r + 'log/'


def init_directories():
    global dirs

    r = pt.cfg.FILES_DIR
    dirs['IN'] = r + 'in/'
    dirs['OUT'] = r + 'out/'
    dirs['TMP'] = r + 'tmp/'
    dirs['LOG'] = r + 'log/'
    for key in dirs:
        cur_dir = dirs[key]
        mkdirs(cur_dir)


def init_PT(force=False):
    """Initialises the partools package"""
    global log_file_initialised
    from partools import quickstart

    if p.exists(pt.cfg.FILES_DIR) and not force:
        return

    init_directories()
    save_list(['*'], pt.cfg.FILES_DIR + '.gitignore')
    log_file_initialised = False
    init_log('init')
    path = pt.cfg.__file__
    if p.basename(path) == 'conf.py':
        s = (" or set up your own 'PTconf.py' file (by copying the"
             " default conf.py file) at the root of your cwd")
    else:
        path = p.abspath(path)
        s = ''
    log("ParTools package successfully initialised\n"
        f"Checkout the README.md on GitHub: {pt.GITHUB_LINK}\n"
        f"Get started here: {p.dirname(quickstart.__file__)}\n"
        f"Set up your conf here: {path}{s}\n"
        "Happy scripting!\n")


def get_confidential(raise_e=True):

    if not p.exists(pt.cfg.CFI_PATH):
        log(E_CFI)
        if raise_e:
            raise Exception(E_CFI)
        else:
            return False
    cfi_list = load_txt(pt.cfg.CFI_PATH)
    cfi = list_to_dict(cfi_list)
    return cfi
