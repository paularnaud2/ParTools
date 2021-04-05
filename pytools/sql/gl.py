from pytools.common import g

# Mandatory inputs
ENV = ''
DB = ''

# Optional inputs
OUT_FILE = f"{g.paths['OUT']}sql_out.csv"
OUT_RG_DIR = f"{g.paths['OUT']}SQL_RG/"
QUERY_IN = 'pytools/sql/queries/query_in.sql'

# Default const
SL_STEP = 100000
MAX_DB_CNX = 10
MAX_CHECK_DUP = 1 * 10**6

MERGE_RG_FILES = True
EXPORT_RANGE = False
CHECK_DUP = True
OPEN_OUT_FILE = True
MSG_BOX_END = True
TEST_RESTART = False
TEST_IUTD = False

FILE_TYPE = '.csv'
EC = '_EC'
RANGE_FIELD = "RANGE"

TMP_FOLDER = 'sql/'
RANGE_PATH = 'pytools/sql/ranges/'
QUERY_PATH = 'pytools/sql/queries/'
IUTD_FILE = 'last_iutd_check.csv'

# Data bases in this list will be checked by the is_up_to_date function
IUTD_LIST = ['SGE']

# Super globals
client_is_init = False
iutd = False

# Settable globales
VAR_DICT = {}
EXECUTE_PARAMS = {}

# Execute
SCRIPT_IN = 'sql/scripts/script_in.sql'
NB_MAX_ELT_INSERT = 100000
PROC = False

# Upload
UPLOAD_IN = g.paths['OUT'] + 'sql_out.csv'
CHUNK_FILE = 'chunk.txt'

# Process manager
MD = None
