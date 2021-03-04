# variables globales et constantes pour le package qdd (import qdd.gl as gl)
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

# écrire les lignes égales dans le fichier de sortie
EQUAL_OUT = False
# écrire les lignes différentes dans le fichier de sortie
# (prend effet uniquement si EQUAL_OUT = True)
DIFF_OUT = False
EQUAL_LABEL = 'E'

FILE_TYPE = '.csv'
IN_DIR = cfg.ROOT_PATH + 'OUT/'
OUT_DIR = cfg.ROOT_PATH + 'OUT/'
OUT_FILE_NAME = 'qdd_out'
OUT_DUP_FILE_NAME = 'qdd_out_dup'
OUT_E_FILE = 'out_e'
TMP_FOLDER = 'qdd/'
COMPARE_FIELD = "COMPARE_RES"
MAX_DUP_PRINT = 5
MAX_ROW_LIST_PY_VERSION_ALERT = 5 * 10**6
MAX_FILE_SIZE_PY_VERSION_ALERT = 100 * 10**6
MAX_ROW_EQUAL_OUT = 1 * 10**6
OPEN_OUT_FILE = True
TEST_PROMPT_SPLIT = False
TEST_PROMPT_DK = False

bool = {}
counters = {}
