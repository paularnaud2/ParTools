import common as com
import test.check_log as cl

from common import g
from os.path import exists


def mail():
    mail_conf = g.paths['MAIL'] + 'conf.txt'
    com.log("Testing common.mail-----------------------------------------")
    if exists(mail_conf):
        com.mail('test')
    else:
        s = f"Conf file '{mail_conf}' missing."
        s += " common.mail counldn't be tested."
        com.log(s)
    com.log_print()


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
    com.send_notif('Notification test', 'Test', ndur=2)
    com.log_print()


def test_common():
    com.init_log('test_common', True)
    send_notif()
    get_duration()
    # mail()
    # com.check_log(cl.CO)


if __name__ == '__main__':
    test_common()
