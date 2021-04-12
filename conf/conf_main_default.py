# Main-------------------------------------------------------------------------

# Where you want your Input/Output, log, and temporary files to be output
IO_PATH = 'IO/'

# Input path for mails to be sent (see pytools/mail/mails/test for example)
MAIL_PATH = 'pytools/mail/mails/'

# DEBUG = True enables function decorator in common.deco
# it basically terminates the program if one of the threads
# (or the main thread) throws an exception and prints the exception (full trace)
# in the current log file.
# Warning: DEBUG = True will make pytest fail!
DEBUG = False

# sql--------------------------------------------------------------------------

# Path of your Oracle instant client
# (the nb of bit has to match your python version)
ORACLE_CLIENT = 'C:/instantclient_19_6/'

# test-------------------------------------------------------------------------

# For the tests to be working, the user of TEST_DB set in conf_oracle.py
# must have writing permissions.
# Note also that as with TEST_ENV, the name of the TEST_DB has to be
# set in conf_oracle.py so that the duplet (TEST_ENV, TEST_DB) has a defined
# connexion string
# Set TEST_DB to '' if you want SQL tests (test_sql and test_reqlist)
# to be skipped (though a warning will be thrown is this case)
TEST_DB = ''
