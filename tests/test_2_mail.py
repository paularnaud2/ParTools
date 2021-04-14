import warnings
from os.path import exists

import pytools.common as com
from pytools.mail import gl
from pytools.mail import mail


def test_mail():
    com.init_log('test_mail', True)
    com.log("Testing mail.mail-----------------------------------------")
    if exists(gl.CONF_PATH):
        mail('test')
    else:
        com.log(gl.S_CONF)
        warnings.warn(gl.S_CONF)
    com.log_print()


if __name__ == '__main__':
    test_mail()
