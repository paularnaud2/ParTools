from pytools.common import g

MAILS_DIR = 'mails/'
CONF_PATH = MAILS_DIR + 'conf.txt'
RECIPIENTS = 'recipients.txt'
SUBJECT = 'subject.txt'
BODY = 'body.html'

test = g.root_dir + 'test/mails/test/'
conf = g.root_dir + 'test/mails/conf'

S_CONF = (f"The email couldn't be sent because the conf file '{CONF_PATH}'"
          f" was not found.\nSee {conf} for example")

S_MISSING = "{} file missing ({}). See {} for example."
