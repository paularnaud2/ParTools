from partools.test import gl
from partools.utils import g

FILES_DIR = gl.TEST + 'tools/files/'
OUT_DIR = g.dirs['TMP'] + gl.TEST_OUT + 'tools/'

# XML
XML_IN = FILES_DIR + 'xml_in.xml'
XML_OUT = OUT_DIR + 'out_xml.csv'
XML_OUT_REF = FILES_DIR + 'xml_out_ref.csv'

# Split
S_OUT_1 = OUT_DIR + 'in_1.csv'
S_OUT_2 = OUT_DIR + 'in_2.csv'
S_OUT_3 = OUT_DIR + 'in_3.csv'
S_OUT_REF_1 = FILES_DIR + 'split_out_ref_1.csv'
S_OUT_REF_2 = FILES_DIR + 'split_out_ref_2.csv'
S_OUT_REF_3 = FILES_DIR + 'split_out_ref_3.csv'

# Dup
DUP_IN = FILES_DIR + 'dup_in.csv'
DUP_OUT = OUT_DIR + 'out_dup.csv'
SHUF_OUT = OUT_DIR + 'out_shuf.csv'
DUP_OUT_REF = FILES_DIR + 'dup_out_ref.csv'
DEL_DUP_OUT_REF = FILES_DIR + 'del_dup_out_ref.csv'
DUP_COL_IN = FILES_DIR + 'dup_col_in.csv'
DUP_COL_REF = FILES_DIR + 'dup_out_ref_2.csv'

# Filter
FLT_OUT = OUT_DIR + 'filter_out.csv'
FLT_OUT_REF = FILES_DIR + 'filter_out_ref.csv'

# BF
LOOK_FOR = '22173227102607'
SEARCH_BF_OUT = OUT_DIR + 'search_bf_out.csv'
SEARCH_BF_OUT_REF = FILES_DIR + 'search_bf_out_ref.csv'
SORT_BF_OUT = OUT_DIR + 'sort_bf_out.csv'
