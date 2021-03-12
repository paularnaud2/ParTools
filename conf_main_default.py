# Main-------------------------------------------------------------------------

# Basically where you want your log files and temporary files to be outputed
ROOT_PATH = 'C:/Py/'

# DEBUG = True enables function decorator in common.deco
# it basically temrinate the programm if one of the threads
# (or the main thread) throws an exeption and print the exception (full trace)
# in the current log file.
# Warning: DEBUG = True will make pytest fail!
DEBUG = False

# sql--------------------------------------------------------------------------

# Path of your Oracle instant client
# (the nb of bit has to match your python version)
ORACLE_CLIENT = 'C:/instantclient_19_6/'

# test-------------------------------------------------------------------------

# Default test environment is set to local. You can rename it as you wish,
# it just has to match with ENV_NAME of conf_oracle.py
TEST_ENV = 'LOCAL'

# For the tests to be working, the user of TEST_DB set in conf_oracle.py
# must have writing permissions.
# Note also that as with TEST_ENV, the name of the TEST_DB has to be
# set in conf_oracle.py so that the duplet (TEST_ENV, TEST_DB) has a defined
# connexion string
# Set TEST_DB to '' if you want SQL tests (test_sql and test_reqlist)
# to be skipped
TEST_DB = ''
