import pytools.common as com
import pytools.common.sTools as st
import pytools.test.check_log as cl


def get_duration():
    com.log("Testing common.string.get_duration--------------------------")
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


def send_notif():
    com.log("Testing common.send_notif-----------------------------------")
    st.send_notif('Notification test', 'Test', ndur=2)
    com.log_print()


def test_common():
    com.init_log('test_common', True)
    send_notif()
    get_duration()
    com.check_log(cl.CO)


if __name__ == '__main__':
    test_common()
