# This directory contains input, output, log, and temporary files folders.
FILES_DIR = 'PT/'

# Path to confidential data (used by mail package)
CFI_PATH = 'confidential.txt'

# This directory has to contain a conf.txt file and the mail folders corresponding
# to the mail_name passed in the mail function.
MAILS_DIR = 'mails/'
HOST_NO_AUTH = 'host.no_auth.com'

# DEBUG = True enables function decorator in utils.deco
# it basically terminates the program if one of the threads
# (or the main thread) throws an exception and prints the exception (full trace)
# in the current log file.
# Warning: DEBUG = True will make pytest fail!
DEBUG = False

# Default format for the log function
LOG_FORMAT = '%H:%M:%S -'
