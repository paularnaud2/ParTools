import pytools.utils as u
import pytools.utils.sTools as st
import pytools.test.check_log as cl


def msg_box():
    u.log("Test msg_box--------------------------------------------")
    st.msg_box('Message box test', 'Test')
    u.log_print()


def get_duration():
    u.log("Test string.get_duration--------------------------------")
    dstr = u.get_duration_string(0, end_time=0.35)
    u.log(dstr)
    assert dstr == "350 ms"
    dstr = u.get_duration_string(0, end_time=5.369)
    u.log(dstr)
    assert dstr == "5.3 seconds"
    dstr = u.get_duration_string(0, end_time=150)
    u.log(dstr)
    assert dstr == "2 minutes and 30 seconds"
    u.log_print()


def test_utils():
    u.init_log('test_utils', True)
    msg_box()
    get_duration()
    u.check_log(cl.CO)


if __name__ == '__main__':
    test_utils()
