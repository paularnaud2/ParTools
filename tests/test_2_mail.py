import pytools.utils as u
from pytools import mail
from pytools.test import gl
from pytools.test import ttry
import pytools.test.check_log as cl


def test_mail():
    u.init_log('test_mail', True)
    mail.gl.TEST = True
    args = [gl.MAIL_NAME, gl.MAIL_SUBJECT, gl.MAIL_VD, gl.MAIL_A]

    u.log("Test gmail----------------------------------------------")
    mail.gmail(*args)
    u.log_print()

    u.log("Test no_auth--------------------------------------------")
    ttry(mail.no_auth, gl.E_NO_AUT, *args)

    u.log("Test outlook--------------------------------------------")
    ttry(mail.outlook, gl.E_OUTLOOK, *args)

    u.check_log(cl.MAIL)


if __name__ == '__main__':
    test_mail()
