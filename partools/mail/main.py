import ssl
import smtplib
import win32com.client as win32

from partools import cfg
import partools.utils as u

from . import gl
from . import get
from . import functions as f


def gmail(mail_name,
          subject,
          var_dict=[],
          attachments=[],
          HTMLbody='',
          recipients=[]):

    f.init(mail_name, recipients)
    f.init_cfi()
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

    f.init(mail_name, recipients, True)
    f.init_cfi()
    msg = get.msg(subject, HTMLbody, attachments, var_dict)

    u.log(f"Sending mail '{mail_name}' to {gl.recipients}...")
    with smtplib.SMTP(cfg.HOST_NO_AUTH) as server:
        server.sendmail(gl.sender, gl.recipients, msg.as_string())
    u.log('Mail sent')


def outlook(mail_name,
            subject,
            var_dict=[],
            attachments=[],
            HTMLbody='',
            recipients=[]):

    f.init(mail_name, recipients, True)

    HTMLbody = get.HTML(HTMLbody, var_dict)

    f.save_mail(HTMLbody)
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
