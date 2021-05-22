from os.path import exists
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import partools.utils as u

from . import gl
from . import functions as f


def recipients(check_internal):
    recipients_path = gl.mail_dir + gl.RECIPIENTS
    u.log(f"Getting recipients from {recipients_path}")
    if not exists(recipients_path):
        s = gl.S_MISSING.format('Recipients', recipients_path)
        raise Exception(s)

    recipients = u.load_txt(recipients_path)
    f.is_configured(recipients, recipients_path)
    if check_internal:
        f.check_internal(recipients)

    return recipients


def HTML(HTMLbody, var_dict):

    if not HTMLbody:
        html_path = gl.mail_dir + 'template.html'
        if not exists(html_path):
            s = gl.S_MISSING.format('Template', html_path)
            raise Exception(s)
        HTMLbody = u.load_txt(html_path, list_out=False)
        u.log(f"HTML template {html_path} successfully loaded")

    if var_dict:
        HTMLbody = u.replace_from_dict(HTMLbody, var_dict)
        u.log("Template variables have been replaced")

    return HTMLbody


def msg(subject, HTMLbody, attachments, var_dict):

    HTMLbody = HTML(HTMLbody, var_dict)

    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = gl.From
    msg["To"] = '; '.join(gl.recipients)

    if HTMLbody:
        partHTML = MIMEText(HTMLbody, 'html')
        msg.attach(partHTML)
        f.save_mail(HTMLbody)

    for path in attachments:
        name = basename(path)
        with open(path, "rb") as file:
            part = MIMEApplication(file.read(), Name=name)
        part['Content-Disposition'] = f'attachment; filename="{name}"'
        msg.attach(part)

    return msg
