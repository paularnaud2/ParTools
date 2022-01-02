import sys
import os.path as p
from shutil import copytree

from partools import cfg
import partools.utils as u

from . import gl


def is_configured(recipients, path):

    for elt in recipients:
        if 'username' in elt:
            s = f"The recipients list ({path}) hasn't been configured"
            raise Exception(s)


def check_internal(recipients):

    sint = gl.INTERNAL_STR
    u.log(f"Checking if all recipients are internal (ie. contain '{sint}')")
    not_int = [elt for elt in recipients if sint not in elt]
    if not_int:
        if len(not_int) > 1:
            s = f'Warning: "{not_int}" are not internal email addresses. Send anyways? (y/n)'
        else:
            s = f'Warning: "{not_int}" is not an internal email address. Send anyways? (y/n)'

        if gl.TEST:
            u.log(s)
            u.log_print('y (TEST = True)')
        elif not u.log_input(s) == 'y':
            sys.exit()


def save_mail(HTMLbody):

    u.mkdirs(gl.mail_dir)
    gl.last_sent = gl.mail_dir + 'last_sent.html'
    u.save_list([HTMLbody], gl.last_sent)
    u.log(f"Mail saved to {gl.last_sent}")


def init(mail_name, recipients, check_internal=False):
    from . import get

    init_mail()
    gl.mail_dir = cfg.MAILS_DIR + mail_name + '/'
    if recipients:
        gl.recipients = recipients
    else:
        gl.recipients = get.recipients(check_internal)


def init_cfi(decrypt_key=''):

    gl.cfi = u.get_confidential(decrypt_key, False)
    if not gl.cfi:
        raise Exception(gl.S_MISSING_CFI)
    u.log(f"Password decrypted: '{gl.cfi['PWD_GMAIL']}'")
    gl.sender = gl.cfi['MAIL_FROM']
    gl.From = gl.cfi['MAIL_FROM']


def init_mail():

    if p.exists(cfg.MAILS_DIR):
        return
    files_dir = f'{p.dirname(__file__)}/files'
    files_dir = files_dir.replace('\\', '/')
    if not p.exists(files_dir):
        s = f"Warning: mail folder couldn't be initialised because {files_dir} was not found"
        u.log(s)
        return

    copytree(files_dir, cfg.MAILS_DIR)
    u.save_list(['*'], cfg.MAILS_DIR + '.gitignore')
    u.log(f"Mail folder '{cfg.MAILS_DIR}' successfully initialised")
