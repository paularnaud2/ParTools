import pytools.common as com
import pytools.common.sTools as st
import pytools.test.check_log as cl


def msg_box():
    com.log("Test msg_box--------------------------------------------")
    st.msg_box('Message box test', 'Test')
    com.log_print()


def get_duration():
    com.log("Test string.get_duration--------------------------------")
    dstr = com.get_duration_string(0, end_time=0.35)
    com.log(dstr)
    assert dstr == "350 ms"
    dstr = com.get_duration_string(0, end_time=10)
    com.log(dstr)
    assert dstr == "10.0 seconds"
    dstr = com.get_duration_string(0, end_time=150)
    com.log(dstr)
    assert dstr == "2 minutes and 30 seconds"
    com.log_print()


def test_common():
    com.init_log('test_common', True)
    msg_box()
    get_duration()
    com.check_log(cl.CO)


if __name__ == '__main__':
    test_common()
