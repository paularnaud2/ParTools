from time import time
from importlib import reload

import partools.utils as u

from . import gl
from .init import init
from .functions import finish
from .functions import get_query_list
from .process import process_query_list
from .recover import recover


@u.log_exeptions
def download(**kwargs):

    u.log('[sql] download: start')
    reload(gl)  # reinit globals
    start_time = time()
    u.init_kwargs(gl, kwargs)

    init()
    get_query_list()
    recover()
    process_query_list()
    finish(start_time)
