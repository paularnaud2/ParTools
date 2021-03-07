import conf_main as cfg

IN_FILE_NAME_1 = 'SGE'
IN_FILE_NAME_2 = 'GINKO'
# IN_FILE_1 = 'OLD'
# IN_FILE_2 = 'NEW'

MAX_ROW_LIST = 12 * 10**6
SL_STEP = 5 * 10**6
MAX_LINE_SPLIT = 900 * 10**3
MAX_FILE_NB_SPLIT = 10

COMPARE_FIELD_NB = 1
COMPARE_SEPARATOR = '|'

# Write equal lines in output file
EQUAL_OUT = False
# Write différent lines in output file (applies only when EQUAL_OUT = True)
DIFF_OUT = False
EQUAL_LABEL = 'E'

FILE_TYPE = '.csv'
IN_DIR = cfg.ROOT_PATH + 'OUT/'
OUT_DIR = cfg.ROOT_PATH + 'OUT/'
OUT_FILE_NAME = 'dq_out'
OUT_DUP_FILE_NAME = 'dq_out_dup'
OUT_E_FILE = 'out_e'
TMP_FOLDER = 'dq/'
COMPARE_FIELD = "COMPARE_RES"
MAX_ROW_EQUAL_OUT = 1 * 10**6
OPEN_OUT_FILE = True
TEST_PROMPT_SPLIT = False
TEST_PROMPT_DK = False

bool = {}
counters = {}
