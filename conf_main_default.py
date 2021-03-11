# Main-----------------------------------------------------------------------

# Basically where you want your log files and temporary files to be outputed
ROOT_PATH = 'C:/Py/'

# DEBUG = True enables thread decorator in common.deco
# it basically kills all threads as soon as on of them throws an exeption
# and print the exception (full trace) in the current log file
DEBUG = True

# sql------------------------------------------------------------------------

# Path of your Oracle instant client (the nb of bit has to match your python version)
ORACLE_CLIENT = 'C:/instantclient_19_6/'

# Test----------------------------------------------------------------------
TEST_ENV = 'LOCAL'
TEST_DB = ''
