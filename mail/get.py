import common as com

from mail import gl
from os.path import exists
from email.mime.text import MIMEText


def conf():
    conf_dir = 'conf_mail.txt'
    if not exists(conf_dir):
        com.log(gl.S_MISSING_CONF)
        raise Exception(gl.S_MISSING_CONF)
    conf_list = com.load_txt(conf_dir)
    conf = com.list_to_dict(conf_list)
    return conf


def recipients(mail_name):
    recipients_dir = gl.MAIL_PATH + mail_name + '/recipients.txt'
    if not exists(recipients_dir):
        s = f"Recipients file missing ({recipients_dir})"
        com.log(s)
        raise Exception(s)
    recipients = com.load_txt(recipients_dir)
    return recipients


def subject(mail_name):
    subject_dir = gl.MAIL_PATH + mail_name + '/subject.txt'
    if not exists(subject_dir):
        s = f"Subject file missing ({subject_dir})"
        com.log(s)
        raise Exception(s)
    subject = com.load_txt(subject_dir, list_out=False)
    return subject


def body(mail_name):
    body_dir = gl.MAIL_PATH + mail_name + '/body.html'
    if not exists(body_dir):
        s = f"Html body file missing ({body_dir})"
        com.log(s)
        raise Exception(s)
    html = com.load_txt(body_dir, list_out=False)
    body = MIMEText(html, "html")
    return body
