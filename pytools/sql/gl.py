from pytools.common import g

# Mandatory inputs---------------------------------------------------
# CNX_STR or DB from conf.CONF_ORACLE
CNX_STR = ''
DB = ''

# QUERY_IN or QUERY_LIST, or both if QUERY_IN is variabilised
QUERY_IN = ''
QUERY_LIST = []

# Optional inputs----------------------------------------------------
ENV = ''  # See comment in conf.py for details
OUT_PATH = f"{g.dirs['OUT']}sql_out.csv"
OUT_DIR = f"{g.dirs['OUT']}sql_out/"

# Default const------------------------------------------------------
SL_STEP = 100000
MAX_DB_CNX = 10
MAX_CHECK_DUP = 1 * 10**6

MERGE_FILES = True
EXPORT_RANGE = False
CHECK_DUP = True
OPEN_OUT_FILE = True
MSG_BOX_END = True
TEST_RECOVER = False
TEST_IUTD = False

RANGE_NAME = "RANGE"
VAR_IN = "IN"
FILE_TYPE = '.csv'
EC = '_EC'
RANGE_FIELD = "RANGE"

TMP_FOLDER = 'sql/'
RANGE_DIR = 'pytools/sql/ranges/'
QUERY_DIR = 'pytools/sql/queries/'
IUTD_FILE = 'last_iutd_check.csv'

# Strings
S_1 = "Connecting to data base ({})..."
S_2 = "Connecting to data base '{}' of environment '{}' ({})..."
S_3 = "Connecting to data base {} ({})..."

# Exceptions
s = " Pease check the CONF_ORACLE conf var."
E_1 = "Error: either gl.CNX_STR or gl.DB have to be defined"
E_2 = "Error: data base '{}' doesn't seem to be defined." + s
E_3 = "Error: data base '{}' of environment '{}' doesn't seem to be defined." + s

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
