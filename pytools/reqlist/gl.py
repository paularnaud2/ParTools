from pytools.common import g

# Mandatory inputs
ENV = ''
DB = ''

# Optional inputs
IN_FILE = f"{g.paths['IN']}rl_in.csv"
OUT_FILE = f"{g.paths['OUT']}rl_out.csv"
QUERY_IN = 'reqlist/queries/query_in_rl.sql'

# Default const
MAX_DB_CNX = 8
SL_STEP_QUERY = 10
NB_MAX_ELT_IN_STATEMENT = 1000
IN_FIELD_NB = 1

SQUEEZE_JOIN = True
SQUEEZE_SQL = False
CHECK_DUP = True
OPEN_OUT_FILE = True
MSG_BOX_END = True
DEBUG_JOIN = False
TEST_RESTART = False

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
