import time
import partools.utils as pt
from . import g
from . import infi
from .dtry import retry  # available here for BAMS MC
from .dtry import try_except
from .browse import quit_driver


def new_driver(func):
    def new_f(*args, **kwargs):

        if not g.driver:
            return func(*args, **kwargs)

        pt.log(f"New driver for {func.__name__}")
        back_driver = g.driver
        g.driver = None

        try:
            out = func(*args, **kwargs)
        except Exception as e:
            quit_driver()
            g.driver = back_driver
            raise e

        quit_driver()
        g.driver = back_driver

        return out

    new_f.__name__ = func.__name__
    return new_f


def wrap_main(func):
    def new_f(*args, **kwargs):

        start_time = infi.init_main(func)
        out = func(*args, **kwargs)

        dstr = pt.get_duration_string(start_time)
        pt.log(f"[{func.__name__}] end ({dstr})")
        g.main_dur = dstr
        pt.log_print()
        return out

    new_f.__name__ = func.__name__
    return new_f


def wrap_simple(func):
    def new_f(*args, **kwargs):

        start_time = time.time()
        pt.log(f"[{func.__name__}] start")
        out = func(*args, **kwargs)
        dstr = pt.get_duration_string(start_time)
        pt.log(f"[{func. __name__}] end ({dstr})")
        pt.log_print('|')
        return out

    new_f.__name__ = func.__name__
    return new_f


def wrap_check(func):
    @try_except
    def new_f(*args, **kwargs):

        start_time, start_log = infi.init_check(kwargs)
        func(*args, **kwargs)
        infi.finish_check(start_time, start_log)

    new_f.__name__ = func.__name__
    return new_f


def wrap_sub_check(func):
    @try_except
    def new_f(*args, **kwargs):

        start_time = infi.init_sub_check(func, kwargs)
        func(*args, **kwargs)
        infi.finish_sub_check(start_time)

    new_f.__name__ = func.__name__
    return new_f
