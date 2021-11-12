import time

import partools.utils as pt

from . import g
from . import infi
from .functions import log_e


def try_except(func):
    from .browse import save_source

    def new_f(*args, **kwargs):
        start_log = len(pt.g.logs)
        start_time = time.time()
        try:
            return func(*args, **kwargs)
        except Exception as e:
            log_e(e)
            if g.sub_check:
                infi.finish_sub_check(start_time, False)
            else:
                if g.driver:
                    save_source('SOURCE_NOK')
                infi.finish_check(start_time, start_log, False)

    new_f.__name__ = func.__name__
    return new_f


def retry(n_retry):
    from .browse import screenshot

    def decorator(func):
        def new_f(*args, **kwargs):
            retry_back = g.retry
            for g.retry in range(n_retry + 1):
                if g.retry:
                    pt.log(f"[Try No. {g.retry + 1}]...")
                try:
                    out = func(*args, **kwargs)
                    g.retry = retry_back
                    return out
                except Exception as e:
                    stre = type(e)
                    cur_e = e
                    s = f"[Try No. {e.retry + 1}] {func.__name__} failed throwing {stre}"
                    pt.log(s)
                    pt.log_print('1')
                    screenshot()

            s = f"[Retry] Maximum number of retries reached. {func.__name__} failed {n_retry + 1} times."
            pt.log(s)
            raise cur_e

        new_f.__name__ = func.__name__
        return new_f

    return decorator
