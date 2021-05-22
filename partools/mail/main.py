import ssl
import smtplib
import os.path as p
import win32com.client as win32
from shutil import copytree

from partools import cfg
import partools.utils as u

from . import gl
from . import get
from . import functions


def gmail(mail_name,
          subject,
          var_dict=[],
          attachments=[],
          HTMLbody='',
          recipients=[]):

    init(mail_name, recipients)
    init_cfi()
    msg = get.msg(subject, HTMLbody, attachments, var_dict)

    host = gl.GMAIL_HOST
    port = gl.GMAIL_PORT
    user = gl.cfi['USER_GMAIL']
    pwd = gl.cfi['PWD_GMAIL']

    ctx = ssl.create_default_context()
    u.log(f"Sending mail '{mail_name}' to {gl.recipients}...")
    if gl.TEST:
        u.log("Skipped sending (TEST = True)")
        return
    with smtplib.SMTP_SSL(host, port, context=ctx) as server:
        server.login(user, pwd)
        server.sendmail(gl.sender, gl.recipients, msg.as_string())
    u.log('Mail sent')


def no_auth(mail_name,
            subject,
            var_dict=[],
            attachments=[],
            HTMLbody='',
            recipients=[]):

    init(mail_name, recipients, True)
    init_cfi()
    msg = get.msg(subject, HTMLbody, attachments, var_dict)

    u.log(f"Sending mail '{mail_name}' to {gl.recipients}...")
    with smtplib.SMTP(gl.NO_AUTH_HOST) as server:
        server.sendmail(gl.sender, gl.recipients, msg.as_string())
    u.log('Mail sent')


def outlook(mail_name,
            subject,
            var_dict=[],
            attachments=[],
            HTMLbody='',
            recipients=[]):

    init(mail_name, recipients, True)

    HTMLbody = get.HTML(HTMLbody, var_dict)

    functions.save_mail(HTMLbody)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(gl.recipients)
    mail.Subject = subject
    mail.HTMLBody = HTMLbody
    for attachment in attachments:
        mail.Attachments.Add(attachment)
    u.log(f"Sending mail '{mail_name}' to {gl.recipients}...")
    mail.Send()
    u.log('Mail sent')


def init(mail_name, recipients, check_internal=False):

    gl.mail_dir = cfg.MAILS_DIR + mail_name + '/'
    if recipients:
        gl.recipients = recipients
    else:
        gl.recipients = get.recipients(check_internal)


def init_cfi():

    gl.cfi = u.g.get_confidential(False)
    if not gl.cfi:
        raise Exception(gl.S_MISSING_CFI)
    gl.sender = gl.cfi['MAIL_FROM']
    gl.From = gl.cfi['MAIL_FROM']


def init_mail():

    if p.exists(cfg.MAILS_DIR):
        u.log(f"'{cfg.MAILS_DIR}' already exists."
              " Initialisation of mail folder aborted.")
        return
    files_dir = f'{p.dirname(__file__)}/files'
    files_dir = files_dir.replace('\\', '/')
    u.delete_folder(cfg.MAILS_DIR)
    copytree(files_dir, cfg.MAILS_DIR)
    u.save_list(['*'], cfg.MAILS_DIR + '.gitignore')
    u.log(f"Mail folder '{cfg.MAILS_DIR}' successfully initialised")
