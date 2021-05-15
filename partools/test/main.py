import warnings

import partools.utils as u
from . import gl


def ttry(f, e_ref, *args, **kwargs):
    exception_occured = False
    try:
        f(*args, **kwargs)
    except Exception as e:
        assert u.like(str(e), e_ref)
        u.log(str(e))
        exception_occured = True

    assert exception_occured
    u.log_print()


def is_test_db_defined():
    if not gl.SQL_DB:
        s = f"TEST_DB is not defined in '{gl.__file__}'. Test aborted."
        u.log(s)
        warnings.warn(s)
        return False
    else:
        return True
