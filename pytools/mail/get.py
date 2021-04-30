from os.path import exists
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import pytools.common as com
from . import gl


def recipients():
    recipients_path = gl.mail_dir + gl.RECIPIENTS
    if not exists(recipients_path):
        s = gl.S_MISSING.format('Recipients', recipients_path)
        com.log(s)
        raise Exception(s)
    recipients = com.load_txt(recipients_path)
    return recipients


def HTML(var_dict):

    template_path = gl.mail_dir + 'template.html'
    if not exists(template_path):
        s = gl.S_MISSING.format('Template', template_path)
        com.log(s)
        raise Exception(s)
    template = com.load_txt(template_path, list_out=False)
    html = com.replace_from_dict(template, var_dict)
    return html


def msg(subject, TXTbody, HTMLbody, attachments, var_dict):

    if not HTMLbody:
        HTMLbody = HTML(var_dict)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = gl.From
    msg["To"] = '; '.join(gl.recipients)

    if TXTbody:
        partTXT = MIMEText(TXTbody, 'plain')
        msg.attach(partTXT)
    if HTMLbody:
        partHTML = MIMEText(HTMLbody, 'html')
        msg.attach(partHTML)

    for path in attachments:
        name = basename(path)
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=name)
        part['Content-Disposition'] = f'attachment; filename="{name}"'
        msg.attach(part)

    return msg
