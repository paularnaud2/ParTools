import os
from shutil import copytree

import partools.utils as u
import partools.test.mail as tm
import partools.test.mail.gl as gl

from partools import cfg
from partools import mail
from partools.test import ttry

from partools.crypto import KEY


def ast(in1, in2):

    s = u.load_txt(mail.gl.last_sent, False)
    assert in1 in s and in2 in s
    u.log(f"'{in1}' and '{in2}' found in last_sent")


def test_mail():
    u.init_log('test_mail', True)

    u.delete_folder('mail_back')
    if os.path.exists(cfg.MAILS_DIR):
        copytree(cfg.MAILS_DIR, 'mail_back')
        u.delete_folder(cfg.MAILS_DIR)

    u.log_print("Test gmail - KO, recipients not configureed", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    ttry(mail.gmail, gl.E_NOT_CONFIGURED, *args)
    u.log_print()

    u.log_print("Test gmail - KO, confidential file not found", dashes=100)
    recipients_path = cfg.MAILS_DIR + gl.MAIL_NAME + '/' + mail.gl.RECIPIENTS
    u.save_list(gl.RECIPIENTS_FILE, recipients_path)
    if os.path.exists(cfg.CFI_PATH):
        os.rename(cfg.CFI_PATH, cfg.CFI_PATH + '_')
    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    ttry(mail.gmail, gl.E_CFI, *args)
    os.rename(cfg.CFI_PATH + '_', cfg.CFI_PATH)
    u.log_print()

    mail.gl.TEST = True
    u.log_print(f"Test gmail - {gl.S_VDHT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    mail.gmail(*args)
    ast(gl.NVAR, gl.HT)
    u.log_print()

    u.log_print(f"Test gmail - {gl.S_VDPT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDPT, gl.VD, [], tm.BODY, gl.RECIPIENTS_IN, KEY]
    mail.gmail(*args)
    ast(gl.NVAR, gl.PT)
    u.log_print()

    u.log_print(f"Test gmail - {gl.S_HT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_HT]
    mail.gmail(*args)
    ast(gl.VAR, gl.HT)
    u.log_print()

    u.log_print(f"Test gmail - {gl.S_PT}", dashes=100)
    args = [gl.MAIL_NAME, gl.S_PT, [], [], tm.BODY]
    mail.gmail(*args)
    ast(gl.VAR, gl.PT)
    u.log_print()

    u.log_print("Test no_auth", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDHT, gl.VD, gl.ATT]
    ttry(mail.no_auth, gl.E_NO_AUT, *args)
    ast(gl.NVAR, gl.HT)
    u.log_print()

    u.log_print("Test outlook", dashes=100)
    args = [gl.MAIL_NAME, gl.S_VDPT, gl.VD, [], tm.BODY]
    ttry(mail.outlook, gl.E_OUTLOOK, *args)
    ast(gl.NVAR, gl.PT)
    u.log_print()

    # Restauring mail backup
    u.delete_folder(cfg.MAILS_DIR)
    copytree('mail_back', cfg.MAILS_DIR)
    u.delete_folder('mail_back')

    u.check_log(tm.CL)


if __name__ == '__main__':
    test_mail()
