import os
import traceback
import _conf_main as cfg

from common import g
from .log import log
from .log import log_input


def log_exeptions(f):
    # When cfg.DEBUG = True, this decorator write potential exeption in current log file
    # and kills all the running threads (os._exit(1))
    def new(*arg, **kwargs):
        try:
            return f(*arg, **kwargs)
        except Exception:
            with g.verrou:
                s = "An error occured:\n"
                s += traceback.format_exc()
                log(s)
                log_input("Execution aborted")
                os._exit(1)

    if cfg.DEBUG:
        return new
    else:
        return f
