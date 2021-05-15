import os
import traceback

from partools import cfg
from . import g
from .log import log
from .log import log_input


def log_exeptions(f):
    """When conf.DEBUG = True, this decorator writes a potential exception in
    the current log file and kills all the running threads (os._exit(1))
    """
    def new(*arg, **kwargs):
        try:
            return f(*arg, **kwargs)
        except Exception:
            with g.verrou:
                s = "An error occured:\n" + traceback.format_exc()
                log(s)
                log_input("Execution aborted")
                os._exit(1)

    if cfg.DEBUG:
        return new
    else:
        return f
