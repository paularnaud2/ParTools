from os.path import exists
from email.mime.text import MIMEText

import pytools.common as com
from . import gl


def conf():
    if not exists(gl.CONF_PATH):
        com.log(gl.S_MISSING_CONF)
        raise Exception(gl.S_MISSING_CONF)
    conf_list = com.load_txt(gl.CONF_PATH)
    conf = com.list_to_dict(conf_list)
    return conf


def recipients():
    recipients_path = gl.mail_dir + gl.RECIPIENTS
    if not exists(recipients_path):
        s = gl.S_MISSING.format('Recipients', recipients_path, gl.test)
        com.log(s)
        raise Exception(s)
    recipients = com.load_txt(recipients_path)
    return recipients


def subject():
    subject_path = gl.mail_dir + gl.SUBJECT
    if not exists(subject_path):
        s = gl.S_MISSING.format('Subject', subject_path, gl.test)
        com.log(s)
        raise Exception(s)
    subject = com.load_txt(subject_path, list_out=False)
    return subject


def body():
    body_path = gl.mail_dir + gl.BODY
    if not exists(body_path):
        s = gl.S_MISSING.format('Body', body_path, gl.test)
        com.log(s)
        raise Exception(s)
    html = com.load_txt(body_path, list_out=False)
    body = MIMEText(html, "html")
    return body
