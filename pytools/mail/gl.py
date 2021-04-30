RECIPIENTS = 'recipients.txt'
GMAIL_HOST = 'smtp.gmail.com'
GMAIL_PORT = '465'
NO_AUTH_HOST = 'host.no_auth.com'
INTERNAL_STR = '@ubs.com'

S_MISSING_CFI = """The email couldn't be sent because the confidential file was not found.
Before running the gmail or no_auth functions, you have to run the init_mail function and set a confidential.txt file.
This file must be saved at the root path using the example provided in the initialised folder."
See quickstart/mail for further guidance."""

S_MISSING = "{} file missing ({}). See quickstart/mail for guidance."
