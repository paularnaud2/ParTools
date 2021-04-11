from pytools.common import g

# Mandatory inputs (DB from conf/_conf_oracle.py or CNX_STR)
CNX_STR = ''
DB = ''

# Optional inputs
ENV = ''  # See comment in conf/_conf_oracle.py for details
IN_FILE = f"{g.paths['IN']}rl_in.csv"
OUT_FILE = f"{g.paths['OUT']}rl_out.csv"
QUERY_IN = 'reqlist/queries/query_in_rl.sql'

# Default const
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
