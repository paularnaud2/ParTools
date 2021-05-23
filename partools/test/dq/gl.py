from partools.test import gl
from partools.utils import g

FILES_DIR = gl.TEST + 'dq/files/'
OUT_DIR = g.dirs['TMP'] + gl.TEST_OUT + 'dq/'

IN_MH = 'in_missing_header'
IN_DH = 'in_different_header'
IN_DK = 'in_dup_key'
OUT_DK = OUT_DIR + '1_dup_key.csv'
OUT_DK_REF = FILES_DIR + 'out_ref_dup_key.csv'
OUT_FM = OUT_DIR + 'file_match_out.csv'
REF_FM = FILES_DIR + 'out_ref_fm.csv'
REF_FDM = FILES_DIR + 'out_ref_fdm.csv'

IN11 = 'in_11'
IN12 = 'in_12'
REF1 = 'out_ref_1.csv'
REF1_F = FILES_DIR + 'out_ref_1.csv'
REF1_E = 'out_ref_1_e.csv'
REF_DUP1 = 'out_ref_dup_11.csv'
OUT1 = '1'

IN21 = 'in_21'
IN22 = 'in_22'
REF2 = 'out_ref_2.csv'
REF2_F = FILES_DIR + 'out_ref_2.csv'
REF2_E = 'out_ref_2_e.csv'
REF_DUP2 = 'out_ref_dup_22.csv'
OUT2 = '2'

IN31 = 'in_31'
IN32 = 'in_32'
REF3 = 'out_ref_3.csv'
REF3_E = 'out_ref_3_e.csv'
REF_SPLIT_3 = 'out_ref_split_3.csv'
REF_DUP3 = 'out_ref_dup_31.csv'
OUT3 = '3'
OUT_SPLIT_3 = '3_3'
