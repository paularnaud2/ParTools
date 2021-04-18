from pytools.common import g

# Mandatory inputs---------------------------------------------------
# CNX_STR or DB from conf.CONF_ORACLE
CNX_STR = ''
DB = ''
QUERY_IN = ''

# Optional inputs----------------------------------------------------
ENV = ''  # See comment in conf.CONF_ORACLE for details
IN_PATH = f"{g.dirs['IN']}rl_in.csv"
OUT_PATH = f"{g.dirs['OUT']}rl_out.csv"

# Default const------------------------------------------------------
MAX_DB_CNX = 8
NB_MAX_ELT_IN_STATEMENT = 1000
IN_FIELD_NB = 1

SQUEEZE_JOIN = False
SQUEEZE_SQL = False
CHECK_DUP = True
OPEN_OUT_FILE = True
MSG_BOX_END = True
DEBUG_JOIN = False
TEST_RECOVER = False

TMP_FOLDER = 'reqlist/'
OUT_LEFT_FILE = 'out_l.csv'
OUT_RIGHT_FILE = 'out_r.csv'
OUT_SQL_FILE = 'out_sql.csv'

VAR_IN = "IN"
TMP_FILE_TYPE = '.csv'
EC = '_EC'
QN = '_QN'

# Settable globales
VAR_DICT = {}

# Process manager
MD = None
