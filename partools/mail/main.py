import smtplib

import partools.utils as u

from . import gl
from . import get
from . import functions as f


def gmail(mail_name,
          subject,
          var_dict=[],
          attachments=[],
          HTMLbody='',
          recipients=[],
          decrypt_key=''):
    """Sends emails using gmail

    See README.md for guidance

    See partools/quickstart/mail.py for examples of use

    - attachments: list of absolute path for attached files
    - var_dict: dictionary of variables to be replaced in HTMLbody
    - HTMLbody: if not input, mails/mail_name/template.html is taken
    - recipients: if not input, mails/mail_name/recipients.txt is taken
    """
    import ssl

    f.init(mail_name, recipients)
    f.init_cfi(decrypt_key)
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
            recipients=[],
            decrypt_key=''):
    """Sends emails using a no authentication smtp server

    See README.md for guidance

    See partools/quickstart/mail.py for examples of use

    - attachments: list of absolute path for attached files
    - var_dict: dictionary of variables to be replaced in HTMLbody
    - HTMLbody: if not input, mails/mail_name/template.html is taken
    - recipients: if not input, mails/mail_name/recipients.txt is taken
    """
    from partools import cfg

    f.init(mail_name, recipients, True)
    f.init_cfi(decrypt_key)
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
            recipients=[],
            decrypt_key=''):
    """Sends emails using installed Outlook application

    See README.md for guidance

    See partools/quickstart/mail.py for examples of use

    - attachments: list of absolute path for attached files
    - var_dict: dictionary of variables to be replaced in HTMLbody
    - HTMLbody: if not input, mails/mail_name/template.html is taken
    - recipients: if not input, mails/mail_name/recipients.txt is taken
    """
    import win32com.client as win32

    f.init(mail_name, recipients, True)

    HTMLbody = get.HTML(HTMLbody, var_dict)

    f.save_mail(HTMLbody)
    if gl.TEST:
        s = "Skipped sending (TEST = True). Simulated error 2147221005"
        raise Exception(s)
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
