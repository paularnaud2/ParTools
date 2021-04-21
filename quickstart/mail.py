# In order for the mail function to work,  you have to initialise a mail folder
# by running the 'init_mail' function. This will create a folder in the MAIL_DIR
# defined in 'pytool/conf.py' ('mails/' by default).
#
# The initialised folder contains two conf files. You have to rename one of them
# (depending on your case) to 'conf.txt'. The folder should also contain the mail
# folders corresponding to the mail_name passed in the mail function. As you'll notice,
# it initialy contains a 'test' folder, allowing you to quickly test the function and
# to provide you with an example of what a 'mail_name' folder is expected to contain.

from pytools.mail import mail
from pytools.mail import init_mail

# First run ini_mail and set a conf.txt file from one of the two examples
init_mail()

# Then run mail('test) function to send a test mail (pointing to mails/test/)
mail('test')
