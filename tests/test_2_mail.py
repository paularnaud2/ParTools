import warnings
from os.path import exists

import pytools.common as com
import conf._conf_main as cfg
from pytools.mail import gl
from pytools.mail import mail


def test_mail():
    com.init_log('test_mail', True)
    com.log("Testing mail.mail-----------------------------------------")
    cfg.MAIL_PATH = "pytools/mail/mails/"
    if exists(gl.CONF_FILE):
        mail('test')
    else:
        com.log(gl.S_MISSING_CONF)
        warnings.warn(gl.S_MISSING_CONF)
    com.log_print()


if __name__ == '__main__':
    test_mail()
