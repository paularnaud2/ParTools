import pytools.common as com
from pytools import mail
from pytools.test import gl
from pytools.test import ttry


def test_mail():
    com.init_log('test_mail', True)
    mail.gl.TEST = True
    args = [gl.MAIL_NAME, gl.MAIL_SUBJECT, gl.MAIL_VD, gl.MAIL_A]

    com.log("Test gmail----------------------------------------------")
    mail.gmail(*args)
    com.log_print()

    com.log("Test no_auth--------------------------------------------")
    ttry(mail.no_auth, gl.E_NO_AUT, *args)

    com.log("Test outlook--------------------------------------------")
    ttry(mail.outlook, gl.E_OUTLOOK, *args)


if __name__ == '__main__':
    test_mail()
