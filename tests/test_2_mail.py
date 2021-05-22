import partools.utils as u

from partools import mail
from partools.test import gl
from partools.test import ttry
from partools.test.mail.template import BODY
import partools.test.check_log as cl


def ast(in1, in2):

    s = u.load_txt(mail.gl.last_sent, False)
    assert in1 in s and in2 in s
    u.log(f"'{in1}' and '{in2}' found in last_sent")


def test_mail():
    u.init_log('test_mail', True)

    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    u.log_print(f"Test gmail - {gl.S_VDHT}", dashes=100)
    mail.gmail(*args)
    ast(gl.NVAR, gl.HT)
    u.log_print()

    mail.gl.TEST = True
    u.log_print(f"Test gmail - {gl.S_VDPT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDPT, gl.VD, [], BODY, gl.RECIPIENTS]
    mail.gmail(*args)
    ast(gl.NVAR, gl.PT)
    u.log_print()

    args = [gl.MAIL_NAME, gl.S_HT]
    u.log_print(f"Test gmail - {gl.S_HT}", dashes=100)
    mail.gmail(*args)
    ast(gl.VAR, gl.HT)
    u.log_print()

    u.log_print(f"Test gmail - {gl.S_PT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_PT, [], [], BODY]
    mail.gmail(*args)
    ast(gl.VAR, gl.PT)
    u.log_print()

    u.log_print("Test no_auth", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    ttry(mail.no_auth, gl.E_NO_AUT, *args)
    ast(gl.NVAR, gl.HT)
    u.log_print()

    u.log_print("Test outlook", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDPT, gl.VD, [], BODY]
    ttry(mail.outlook, gl.E_OUTLOOK, *args)
    ast(gl.NVAR, gl.PT)
    u.log_print()

    u.check_log(cl.MAIL)


if __name__ == '__main__':
    test_mail()
