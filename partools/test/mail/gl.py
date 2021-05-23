from datetime import date
from partools.test import gl

FILES_DIR = gl.TEST + 'mail/files/'
MAIL_NAME = 'test'
SUBJECT_BASE = '[Test] Python mail - '
S_VDHT = SUBJECT_BASE + 'var dict, HTML template with attachments'
S_VDPT = SUBJECT_BASE + 'var dict, Python template with recipients'
S_HT = SUBJECT_BASE + 'no var dict, HTML template'
S_PT = SUBJECT_BASE + 'no var dict, Python template'
P_VDHT = FILES_DIR + 'last_sent_VDHT.html'
P_VDPT = FILES_DIR + 'last_sent_VDPT.html'
P_HT = FILES_DIR + 'last_sent_HT.html'
P_PT = FILES_DIR + 'last_sent_PT.html'
VAR = '@@NAME@@'
NVAR = 'dear tester'
HT = 'HTML template case'
PT = 'Python template case'
VD = {'DATE': str(date.today()), 'NAME': 'dear tester'}
ATT = ['README.md', 'LICENSE']
TXTBODY = "Raw text test"
RECIPIENTS_IN = ['Paul ARNAUD (IN) <paularnaud2@gmail.com>']
RECIPIENTS_FILE = ['Paul ARNAUD (FILE) <paularnaud2@gmail.com>']
E_NO_AUT = '[Errno 11001] getaddrinfo failed'
E_OUTLOOK = '2147221005'
E_NOT_CONFIGURED = "The recipients list * hasn't been configured"
E_CFI = "The email couldn't be sent because the confidential file was not found"
