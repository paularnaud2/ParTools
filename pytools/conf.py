# This directory contains input, output, log, and temporary files folders.
# If you whish to change it, run import pytools.common after to initialise the
# new folder.
FILES_DIR = 'PT/'

# This directory has to contain a conf.txt file and the mail folders corresponding
# to the mail_name passed in the mail function.
MAILS_DIR = 'mails/'

# DEBUG = True enables function decorator in common.deco
# it basically terminates the program if one of the threads
# (or the main thread) throws an exception and prints the exception (full trace)
# in the current log file.
# Warning: DEBUG = True will make pytest fail!
DEBUG = False

# sql--------------------------------------------------------------------------

# Path of your Oracle instant client
# (the nb of bit has to match your python version)
ORACLE_CLIENT = 'C:/instantclient/'

# yapf: disable
CONF_ORACLE = {
    # A conf line should match with one of the two following expected formats:
    # 'DB_NAME': CNX_INFO,
    # ('DB_NAME', 'ENV_NAME'): CNX_INFO,
    # Where CNX_INFO can either be a connection string:
    # 'USER/PWD@HOST:PORT/SERVICE_NAME'
    #  or a list:
    # ['USERNAME', 'PWD', 'TNS_NAME'] or ['USERNAME', 'PWD', 'DSN']
    #
    # Note that ENV_NAME can be defined to differentiate between two DB of same
    # name but of different environment.

    'XE': 'USERNAME/PWD@localhost:1521/XE',
    # 'XE': ['USERNAME', 'PWD', 'XE_TNS'],
    ('XE', 'LOCAL'): 'USERNAME/PWD@localhost:1521/XE',
}
# yapf: enable
