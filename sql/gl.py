# variables globales et constantes pour le package sql (import sql.gl as gl)
from common import g
from datetime import datetime

ENV = 'PROD'
DB = 'SGE'
DB = 'GINKO'
# DB = 'ADAM'

# ENV = 'DIRECT'
# DB = 'CAPC5'

# ENV = 'LOCAL'
# DB = 'XE'

date = datetime.now().strftime("%Y%m%d")
QUERY_FILE = f'sql/queries/e_{DB}.sql'
OUT_FILE = f"{g.paths['OUT']}export_SQL_{DB}_{date}.csv"
OUT_RG_DIR = f"{g.paths['OUT']}{DB}_OUT_{date}/"

# GKO_INSTANCES = [
# 'GKO1_IDF', 'GKO2_MMN', 'GKO3_EST', 'GKO4_RAB',
# 'GKO5_MED', 'GKO6_SUO', 'GKO7_OUE', 'GKO8_ACL',
# ]
GKO_INSTANCES = ['GKO1_IDF', 'GKO2_MMN', 'GKO3_EST']
# GKO_INSTANCES = ['GKO1_IDF']
EXPORT_INSTANCES = False

SL_STEP = 100000
MAX_DB_CNX = 10
MAX_CHECK_DUP = 1 * 10**6

MERGE_RG_FILES = True
EXPORT_RANGE = False
CHECK_DUP = True
OPEN_OUT_FILE = True
SEND_NOTIF = True
TEST_RESTART = False
TEST_IUTD = False

FILE_TYPE = '.csv'
TMP_FOLDER = 'sql/'
IUTD_FILE = 'last_iutd_check.csv'
RANGE_PATH = 'sql/ranges/'
QUERY_PATH = 'sql/queries/'
EC = '_EC'
RANGE_FIELD = "RANGE"

# Data bases in this list will be checked by the is_up_to_date function
IUTD_LIST = ['SGE']

# Super globals
client_is_init = False
iutd = False

# Globales paramétrables
VAR_DICT = {}
EXECUTE_PARAMS = {}

# Execute
SCRIPT_FILE = 'sql/scripts/create_table_aff.sql'
NB_MAX_ELT_INSERT = 100000
PROC = False

# Upload
UPLOAD_IN = g.paths['OUT'] + 'OUT/in.csv'
CHUNK_FILE = 'chunk.txt'

# Process manager
MD = ''
