import sys
from os.path import exists
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import partools.utils as u
from . import gl


def recipients(check_internal):
    recipients_path = gl.mail_dir + gl.RECIPIENTS
    u.log(f"Getting recipients from {recipients_path}")
    if not exists(recipients_path):
        s = gl.S_MISSING.format('Recipients', recipients_path)
        raise Exception(s)

    recipients = u.load_txt(recipients_path)
    if not check_internal:
        return recipients

    i = gl.INTERNAL_STR
    u.log(f"Checking if all recipients are internal (ie. contain '{i}')")
    for elt in recipients:
        if i not in elt:
            s = f'Warning: "{elt}" is not an internal email address. Send anyways? (y/n)'
            if gl.TEST:
                u.log(s)
                u.log_print('y (TEST = True)')
            elif not u.log_input(s) == 'y':
                sys.exit()
    return recipients


def HTML(var_dict):

    template_path = gl.mail_dir + 'template.html'
    if not exists(template_path):
        s = gl.S_MISSING.format('Template', template_path)
        raise Exception(s)
    template = u.load_txt(template_path, list_out=False)
    html = u.replace_from_dict(template, var_dict)
    return html


def msg(subject, TXTbody, HTMLbody, attachments, var_dict):

    if not HTMLbody and var_dict:
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
        save_mail(HTMLbody)

    for path in attachments:
        name = basename(path)
        with open(path, "rb") as f:
            part = MIMEApplication(f.read(), Name=name)
        part['Content-Disposition'] = f'attachment; filename="{name}"'
        msg.attach(part)

    return msg


def save_mail(HTMLbody):

    path = gl.mail_dir + 'last_sent.html'
    u.save_list([HTMLbody], path)
    u.log(f"Mail saved to {path}")
