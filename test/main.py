def ttry(f, e_ref, *args, **kwargs):
    exception_occured = False
    try:
        f(*args, **kwargs)
    except Exception as e:
        assert str(e) == e_ref
        exception_occured = True

    assert exception_occured
