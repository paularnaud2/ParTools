import ssl
import smtplib

from common import g
from common import file
from common import tools
from .log import log
from os.path import exists
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mail(mail_name, recipients_file='', subject_file=''):
    conf = get_conf()
    host = conf['HOST']
    sender = conf['SENDER']
    From = conf['FROM']

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

    recipients = get_recipients(mail_name, recipients_file)
    To = ", ".join(recipients)
    subject = get_subject(mail_name, subject_file)
    body = get_body(mail_name)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = From
    msg["To"] = To
    msg.attach(body)

    log(f"Sending mail '{mail_name}' to {recipients}...")
    if ctx:
        with smtplib.SMTP_SSL(host, port, context=ctx) as server:
            server.login(user, pwd)
            server.sendmail(sender, recipients, msg.as_string())
    else:
        with smtplib.SMTP(host, port) as server:
            server.sendmail(sender, recipients, msg.as_string())

    log('Mail send')


def get_conf():
    conf_dir = g.paths['MAIL'] + 'conf.txt'
    if not exists(conf_dir):
        s = f"Config file missing ({conf_dir})"
        log(s)
        raise Exception(s)
    conf_list = file.load_txt(conf_dir)
    conf = tools.list_to_dict(conf_list)
    return conf


def get_recipients(mail_name, recipients_file):
    if recipients_file:
        recipients_dir = g.paths['MAIL'] + recipients_file
    else:
        recipients_dir = g.paths['MAIL'] + mail_name + '_recipients.txt'
    if not exists(recipients_dir):
        s = f"Recipients file missing ({recipients_dir})"
        log(s)
        raise Exception(s)
    recipients = file.load_txt(recipients_dir)
    return recipients


def get_subject(mail_name, subject_file):
    if subject_file:
        subject_dir = g.paths['MAIL'] + subject_file
    else:
        subject_dir = g.paths['MAIL'] + mail_name + '_subject.txt'
    if not exists(subject_dir):
        s = f"Subject file missing ({subject_dir})"
        log(s)
        raise Exception(s)
    subject = file.load_txt(subject_dir, list_out=False)
    return subject


def get_body(mail_name):
    body_dir = g.paths['MAIL'] + mail_name + '_body.html'
    if not exists(body_dir):
        s = f"Html body file missing ({body_dir})"
        log(s)
        raise Exception(s)
    html = file.load_txt(body_dir, list_out=False)
    body = MIMEText(html, "html")
    return body
