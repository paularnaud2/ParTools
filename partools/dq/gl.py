from partools.utils import g

# Mandatory inputs---------------------------------------------------
IN_FILE_NAME_1 = ''
IN_FILE_NAME_2 = ''

# Optional inputs----------------------------------------------------
IN_DIR = g.dirs['IN']
OUT_DIR = g.dirs['OUT']

MAX_ROW_LIST = 12 * 10**6  # Max list size. Warning: a too high value may cause a Memory error
MAX_LINE_SPLIT = 900 * 10**3  # If the number of line of the output file exceeds this value, the file is split
MAX_FILE_NB_SPLIT = 10  # Maximum number of split files
SL_STEP = 5 * 10**6  # step_log setting (see README.md)
PIVOT_IDX = 0  # Index of the pivot column (ie. containing keys/IDs used as reference for comparison)

EQUAL_OUT = False  # If True, equal lines are written in the output file
DIFF_OUT = False  # If True, different lines are written in the output file (applies only when EQUAL_OUT = True)
OPEN_OUT_FILE = True

# Default const------------------------------------------------------
MAX_ROW_EQUAL_OUT = 1 * 10**6
FILE_TYPE = '.csv'
OUT_FILE_NAME = 'dq_out'
OUT_DUP_FILE_NAME = 'dq_out_dup'
OUT_E_FILE = 'out_e'
TMP_FOLDER = 'dq/'
EQUAL_LABEL = 'E'
COMPARE_SEPARATOR = '|'
COMPARE_FIELD = "COMPARE_RES"
TEST_PROMPT_SPLIT = False
TEST_PROMPT_DK = False
MSG_BOX_END = True  # If True, a message box will pop up at the end of the process, if the processing time is greater than MIN_DUR_TRIGGER
MIN_DUR_TRIGGER = 30
