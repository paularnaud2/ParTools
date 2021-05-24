import partools as pt
import partools.utils as u
import partools.utils.sTools as st
import partools.test.check_log as cl

back = pt.cfg.FILES_DIR


def init_PT():

    u.delete_folder('PT_test/')
    pt.cfg.FILES_DIR = 'PT_test/'
    u.g.init_PT()


def msg_box():
    u.log_print("Test msg_box", dashes=100)
    st.msg_box('Message box test', 'Test')
    u.log('Message box notification successfully sent')
    u.log_print()


def get_duration():
    u.log_print("Test string.get_duration", dashes=100)
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
    init_PT()
    msg_box()
    get_duration()
    u.check_log(cl.CO)

    pt.cfg.FILES_DIR = back
    u.g.init_PT(True)
    u.delete_folder('PT_test/')


if __name__ == '__main__':
    test_utils()
