import common as com

from test import gl


def ttry(f, e_ref, *args, **kwargs):
    exception_occured = False
    try:
        f(*args, **kwargs)
    except Exception as e:
        assert str(e) == e_ref
        exception_occured = True

    assert exception_occured
    com.log_print()


def is_test_db_defined(test_name):
    if not gl.SQL_DB:
        s = f"TEST_DB is not defined in conf_main.py. {test_name} aborted."
        com.log(s)
        return False
    else:
        return True
