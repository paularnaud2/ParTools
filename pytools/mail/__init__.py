import ssl
import smtplib
from email.mime.multipart import MIMEMultipart

import pytools.common as com

from . import get


def mail(mail_name):
    conf = get.conf()
    host = conf['HOST']
    sender = conf['SENDER']
    From = conf['FROM']
    user, pwd, ctx, port = get_infos(conf)

    recipients = get.recipients(mail_name)
    msg = gen_msg(recipients, mail_name, From)

    com.log(f"Sending mail '{mail_name}' to {recipients}...")
    if ctx:
        with smtplib.SMTP_SSL(host, port, context=ctx) as server:
            server.login(user, pwd)
            server.sendmail(sender, recipients, msg.as_string())
    else:
        with smtplib.SMTP(host, port) as server:
            server.sendmail(sender, recipients, msg.as_string())

    com.log('Mail send')


def get_infos(conf):

    if 'USER' in conf:
        user = conf['USER']
        pwd = conf['PWD']
        ctx = ssl.create_default_context()
    else:
        ctx = ''

    if 'PORT' in conf:
        port = conf['PORT']
    else:
        port = ''

    return user, pwd, ctx, port


def gen_msg(recipients, mail_name, From):

    To = ", ".join(recipients)
    subject = get.subject(mail_name)
    body = get.body(mail_name)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = From
    msg["To"] = To
    msg.attach(body)

    return msg
