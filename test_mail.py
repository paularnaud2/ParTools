import common as com

from mail import gl
from mail import mail
from os.path import exists


def test_mail():
    com.log("Testing mail.mail-----------------------------------------")
    if exists(gl.CONF_FILE):
        mail('test')
    else:
        com.log(gl.S_MISSING_CONF)
    com.log_print()


if __name__ == '__main__':
    test_mail()
