# pywin32
import win32com.client as win32


def mail_outlook(recipients, subject, TXTbody, HTMLbody, attachments=[]):
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = '; '.join(recipients)
    mail.Subject = subject
    mail.Body = TXTbody
    mail.HTMLBody = HTMLbody
    for attachment in attachments:
        mail.Attachments.Add(attachment)
    mail.Send()


recipients = ['paul.arnaud@ubs.com']
subject = 'Python mail test'
TXTbody = 'This email is system generated via a Python code.'
HTMLbody = '<h2>HTML Message body</h2>'
attachments = ['P:/Git/BamsChecks/README.md']

mail_outlook(recipients, subject, TXTbody, HTMLbody, attachments)
