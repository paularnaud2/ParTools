# Main---------------------------------------------------------------
TMP_FOLDER = 'tools/'
OPEN_OUT_FILE = True

# Dup----------------------------------------------------------------
TMP_OUT = 'out_dup.csv'

# XML----------------------------------------------------------------
# Const
RE_EXP_TAG_ELT = '<(.*)>(.*)</(.*)>'
RE_EXP_SUB_TAG = r'<(\w[^<]*\w)>$'

# Optional input defaults
MULTI_TAG_LIST = [
    'libelle',
    'civilite',
    'nom',
    'prenom',
    'telephone1Num',
    'telephone2Num',
    'adresseEmail',
]
SL_STEP_READ = 1000 * 10**3  # step_log setting (see README.md)
SL_STEP_WRITE = 100 * 10**3  # step_log setting (see README.md)

# Filter-------------------------------------------------------------
# Const
s = ("{bn_1} lines read in {dstr}."
     " {bn_2} lines read in total "
     "({bn_3} lines written in output list).")

# Optional input defaults
EXTRACT_COL = True
SL_STEP = 500 * 10**3  # step_log setting (see README.md)

# Globals
COL_LIST = []
FF = None

# Split--------------------------------------------------------------
MAX_LINE = 10**6  # Maximum number of lines for a split file
MAX_FILE_NB = 10  # Maximum number of split files
ADD_HEADER = True  # Adds the header of the input file to each split file
