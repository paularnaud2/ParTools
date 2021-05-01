# In order for the mail function to be worinkg, you have to initialise a mail
# folder by running the 'init_mail' function. This will create a folder in the
# MAIL_DIR defined in 'conf.py' ('mails/' by default).
#
# If you want to use the gmail or no_auth functions, you have to set a
# confidential.txt file.
# This file must be saved at the CFI_PATH defined in the pytools/conf.py file
# (root by default) using the example provided in the initialised folder.
#
# The initialised folder contains the mail folders corresponding to the mail_name
# passed in the mail function. As you'll notice, it initialy contains a 'test'
# folder, allowing you to quickly test the function and to provide you with an
# example of what a 'mail_name' folder is expected to contain.
# So you'll see two files in the mails/test folder:
# - template.html: the html template for the body of the mail. It can contain
# variables delimited by @@ (in the example @@NAME@@ and @@DATE@@) wich are
# replaced using the var_dict passed in input.
# - recipients.txt: the list of recipients here containing three fictive
# recipients. For your test, it es adviced to just let one line with your infos.

from datetime import date
import pytools.mail as mail

# First run init_mail and (only if you want to use gmail or no_auth) set a
# confidential.txt file at the root from the example
# in 'mails/'
# mail.init_mail()

var_dict = {
    'DATE': str(date.today()),
    'NAME': 'dear tester',
}

# Then run on of the following functions (on a personnal computer/network try
# gmail, on a business computer/network try either no_auth or outlook) to send
# a test mail (pointing to mails/test/)
mail.gmail('test', '[Test] Python mail', var_dict=var_dict)
# mail.no_auth('test', '[Test] Python mail', var_dict=var_dict)
# mail.outlook('test', '[Test] Python mail', var_dict=var_dict)
