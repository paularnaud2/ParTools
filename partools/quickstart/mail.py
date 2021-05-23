"""
The mail package allows you to easily send HTML mails with Python.
For more details, check out the README.md file.
"""

from datetime import date
import partools.mail as mail
"""
First run init_mail() and (except if you only want to use mail.outlook) set a
confidential.txt file at the cwd root path using the example provided in 'mails/'."""
mail.init_mail()

var_dict = {
    'DATE': str(date.today()),
    'NAME': 'dear tester',
}
"""
Then set the mails/test/recipients.txt file with your email address and run one
of the following functions (on a personal computer/network try gmail, on a
business computer/network try either no_auth or outlook) to send a test mail
(pointing to mails/test/).
If you want to use the no_auth function, you need to set the host in the conf 
file (HOST_NO_AUTH)"""
mail.gmail('test', '[Test] Python mail', var_dict=var_dict)
# mail.no_auth('test', '[Test] Python mail', var_dict=var_dict)
# mail.outlook('test', '[Test] Python mail', var_dict=var_dict)
