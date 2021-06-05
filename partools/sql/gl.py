import os.path as p
from partools.utils import g

# Mandatory inputs---------------------------------------------------
# Either CNX_INFO or DB have to be input. If both are filled, CNX_INFO is taken
CNX_INFO = ''  # Connection string: 'USER/PWD@HOST:PORT/SERVICE_NAME'
DB = ''  # DB name from partools.conf.CONF_ORACLE

# QUERY_IN or QUERY_LIST, or both if QUERY_IN is variabilized
QUERY_IN = ''
QUERY_LIST = []

# Optional inputs----------------------------------------------------
ENV = ''  # See comment in conf.py for details
OUT_PATH = f"{g.dirs['OUT']}sql_out.csv"
OUT_DIR = f"{g.dirs['OUT']}sql_out/"  # Used when MERGE_FILES = False

MAX_DB_CNX = 8  # Maximum number of connections allowed to work in parallel

OPEN_OUT_FILE = True
MERGE_FILES = True  # See quickstart/sql
EXPORT_RANGE = False  # See quickstart/sql
CHECK_DUP = True
MSG_BOX_END = True  # If True, a message box will pop up at the end of the process, if the processing time is greater than MIN_DUR_TRIGGER
MIN_DUR_TRIGGER = 30

# Default const------------------------------------------------------
SL_STEP = 100 * 10**3  # step_log setting (see README.md)
MAX_CHECK_DUP = 1 * 10**6  # If the output number of line exceeds this value, no duplicate check will be performed (avoids potential memory error)

TEST_RECOVER = False
TEST_IUTD = False

RANGE_NAME = "RANGE"
VAR_IN = "IN"
FILE_TYPE = '.csv'
EC = '_EC'

TMP_FOLDER = 'sql/'
RANGE_DIR = f'{p.dirname(__file__)}/ranges/'
QUERY_DIR = f'{p.dirname(__file__)}/queries/'
IUTD_FILE = 'last_iutd_check.csv'

# Strings
S_1 = "Connecting to database ({})..."
S_2 = "Connecting to database '{}' of environment '{}' ({})..."
S_3 = "Connecting to database {} ({})..."

# Exceptions
s = " Pease check the CONF_ORACLE conf var."
E_1 = "Error: either gl.CNX_INFO or gl.DB have to be defined"
E_2 = "Error: database '{}' doesn't seem to be defined." + s
E_3 = "Error: database '{}' of environment '{}' doesn't seem to be defined." + s

# Data bases in this list will be checked by the is_up_to_date function
IUTD_LIST = []

# Settable globales
VAR_DICT = {}
EXECUTE_KWARGS = {}

# Process manager
MD = None

# Execute
SCRIPT_IN = ''
NB_MAX_ELT_INSERT = 100000
PROC = True

# Upload
UPLOAD_IN = ''
