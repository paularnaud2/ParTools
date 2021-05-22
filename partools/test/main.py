import partools.utils as u


def ttry(f, e_ref, *args, **kwargs):

    exception_occured = False
    try:
        f(*args, **kwargs)
    except Exception as e:
        assert u.like(str(e), e_ref)
        u.log(f"[ttry] Exception caught match expected ('{e_ref}')")
        exception_occured = True

    assert exception_occured
