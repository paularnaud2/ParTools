from partools.utils import g

# Mandatory inputs---------------------------------------------------
# Either CNX_INFO or DB have to be input. If both are filled, CNX_INFO is taken
CNX_INFO = ''  # Connection string: 'USER/PWD@HOST:PORT/SERVICE_NAME'
DB = ''  # DB name from partools.conf.CONF_ORACLE

QUERY_IN = ''  # Must be a variabilized query containing '@@IN@@' (see quickstart/rl)

# Optional inputs----------------------------------------------------
ENV = ''  # See comment in conf.CONF_ORACLE for details
IN_PATH = f"{g.dirs['IN']}rl_in.csv"
OUT_PATH = f"{g.dirs['OUT']}rl_out.csv"

# Default const------------------------------------------------------
MAX_DB_CNX = 8  # Maximum number of connections allowed to work in parallel
NB_MAX_ELT_IN_STATEMENT = 1000  # Maximum number of elements in the 'IN' statement per queries
PIVOT_IDX = 0  # Index of the pivot column (column on which the queries and joint are performed)

SKIP_JOIN = False  # If True, no joint is performed and the SQL result is directly output
SKIP_SQL = False  # If True, no SQL query is performed and the joint is directly performed with the available SQL tmp file (only needed for test purpose)
CHECK_DUP = True
OPEN_OUT_FILE = True
MSG_BOX_END = True  # If True, a message box will pop up at the end of the process, if the processing time is greater than that defined in g.MIN_DUR_MSG_BOX_TRIGGER
DEBUG_JOIN = False
TEST_RECOVER = False

TMP_FOLDER = 'rl/'
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
