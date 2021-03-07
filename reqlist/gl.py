from common import g
from datetime import datetime

ENV = 'LOCAL'
DB = 'XE'

date = datetime.now().strftime("%Y%m%d")
QUERY_FILE = 'reqlist/queries/e_RL.sql'
IN_FILE = f"{g.paths['IN']}in.csv"
OUT_FILE = f"{g.paths['OUT']}export_RL_{DB}_{date}.csv"

MAX_DB_CNX = 8
SL_STEP_QUERY = 10
NB_MAX_ELT_IN_STATEMENT = 1000
IN_FIELD_NB = 1
MAX_DUP_PRINT = 5

SQUEEZE_JOIN = True
SQUEEZE_SQL = False
CHECK_DUP = True
OPEN_OUT_FILE = True
SEND_NOTIF = True
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
MD = ''
