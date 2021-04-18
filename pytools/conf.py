# This directory contains input, output, log, and temporary files folders.
# If you whish to change it, run import pytools.common after to initialise the
# new folder.
FILES_DIR = 'PT/'

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

# yapf: disable
CONF_ORACLE = {
    # Expected format:
    # 'DB_NAME': 'USER/PWD@HOST:PORT/SERVICE_NAME',
    # Or
    # ('DB_NAME', 'ENV_NAME'): 'USER/PWD@HOST:PORT/SERVICE_NAME',
    # Note that ENV_NAME can be defined to differentiate between two DB of same
    # name but of different environment.

    'XE': 'USERNAME/PWD@localhost:1521/XE',
    ('XE', 'LOCAL'): 'USERNAME/PWD@localhost:1521/XE',
}
# yapf: enable

# test-------------------------------------------------------------------------

# For the tests to be working, the user of TEST_DB set in CONF_ORACLE
# must have writing permissions.
# Note also that as with TEST_ENV, the name of the TEST_DB has to be
# set in CONF_ORACLE so that the duplet (TEST_ENV, TEST_DB) has a defined
# connexion string
# Set TEST_DB to '' if you want SQL tests (test_sql and test_reqlist)
# to be skipped (though a warning will be thrown is this case)
TEST_DB = 'XE'
