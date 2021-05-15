import partools.utils as u
from partools import mail
from partools.test import gl
from partools.test import ttry
import partools.test.check_log as cl


def test_mail():
    u.init_log('test_mail', True)
    mail.gl.TEST = True
    args = [gl.MAIL_NAME, gl.MAIL_SUBJECT, [], gl.MAIL_VD, gl.MAIL_A]

    u.log_print("Test gmail", dashes=100)
    mail.gmail(*args)
    u.log_print()

    u.log_print("Test no_auth", dashes=100)
    ttry(mail.no_auth, gl.E_NO_AUT, *args)

    u.log_print("Test outlook", dashes=100)
    ttry(mail.outlook, gl.E_OUTLOOK, *args)

    u.check_log(cl.MAIL)


if __name__ == '__main__':
    test_mail()
