from pytools.common import g
import pytools.conf as cfg

CONF_PATH = cfg.MAILS_DIR + 'conf.txt'
RECIPIENTS = 'recipients.txt'
SUBJECT = 'subject.txt'
BODY = 'body.html'

test = g.root_dir + 'test/mails/test/'
conf = g.root_dir + 'test/mails/conf'

S_MISSING_CONF = (
    f"The email couldn't be sent because the conf file '{CONF_PATH}' was not found."
    "\nBefore running the mail function, you have to run the init_mail function"
    " and to set a conf file from one of the two examples (see quickstart).")

S_MISSING = "{} file missing ({}). See {} for example."
