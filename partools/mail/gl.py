RECIPIENTS = 'recipients.txt'
GMAIL_HOST = 'smtp.gmail.com'
GMAIL_PORT = '465'
INTERNAL_STR = '@ubs.com'
TEST = False

S_MISSING_CFI = """The email couldn't be sent because the confidential file was not found.
Before running the gmail or no_auth functions, you have to run the init_mail function and set a confidential.txt file.
This file must be saved at the cwd root path using the example provided in the initialised folder.
See quickstart/mail for further guidance."""

S_MISSING = "{} file missing ({}). See quickstart/mail for guidance."
