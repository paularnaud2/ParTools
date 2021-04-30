import ssl
import smtplib
import win32com.client as win32
from shutil import copytree

from pytools import cfg
import pytools.common as com

from . import gl
from . import get


def gmail(mail_name,
          subject,
          var_dict=[],
          attachments=[],
          TXTbody='',
          HTMLbody=''):

    init(mail_name)
    init_cfi()
    msg = get.msg(subject, TXTbody, HTMLbody, attachments, var_dict)

    host = gl.GMAIL_HOST
    port = gl.GMAIL_PORT
    user = gl.cfi['USER_GMAIL']
    pwd = gl.cfi['PWD_GMAIL']

    ctx = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=ctx) as server:
        server.login(user, pwd)
        server.sendmail(gl.sender, gl.recipients, msg.as_string())
    com.log('Mail sent')


def no_auth(mail_name,
            subject,
            var_dict=[],
            attachments=[],
            TXTbody='',
            HTMLbody=''):

    init(mail_name)
    init_cfi()
    msg = get.msg(subject, TXTbody, HTMLbody, attachments, var_dict)

    with smtplib.SMTP(gl.NO_AUTH_HOST) as server:
        server.sendmail(gl.sender, gl.recipients, msg.as_string())
    com.log('Mail sent')


def outlook(mail_name,
            subject,
            var_dict=[],
            attachments=[],
            TXTbody='',
            HTMLbody=''):

    init(mail_name)

    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(gl.recipients)
    mail.Subject = subject
    mail.Body = TXTbody
    mail.HTMLBody = HTMLbody
    for attachment in attachments:
        mail.Attachments.Add(attachment)
    mail.Send()
    com.log('Mail sent')


def init(mail_name):

    gl.mail_dir = cfg.MAILS_DIR + mail_name + '/'
    gl.recipients = get.recipients()
    com.log(f"Sending mail '{mail_name}' to {gl.recipients}...")


def init_cfi():

    gl.cfi = com.g.get_confidential(False)
    if not gl.cfi:
        com.log(gl.S_MISSING_CFI)
        raise Exception(com.g.E_CFI)
    gl.sender = gl.cfi['MAIL_FROM']
    gl.From = gl.cfi['MAIL_FROM']


def init_mail():

    com.delete_folder(cfg.MAILS_DIR)
    copytree('pytools/test/mails', cfg.MAILS_DIR)
    com.save_list(['*'], cfg.MAILS_DIR + '.gitignore')
    com.log(f"Mail folder '{cfg.MAILS_DIR}' successfully initialised")
