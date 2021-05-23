from partools.test import gl
from partools.utils import g

import partools.rl.gl as rl

FILES_DIR = gl.TEST + 'rl/files/'
OUT_DIR = g.dirs['TMP'] + gl.TEST_OUT + 'rl/'
TMP_DIR = g.dirs['TMP'] + rl.TMP_FOLDER
OUT_JOIN = OUT_DIR + 'join.csv'
OUT_DUP_REF = FILES_DIR + 'out_dup_ref.csv'

IN_1 = OUT_DIR + 'in1.csv'
IN_MH = OUT_DIR + 'in_missing_header.csv'
OUT_1 = OUT_DIR + 'out1.csv'
QUERY_1 = FILES_DIR + 'query1.sql'
QUERY_NO = FILES_DIR + 'query_no_output.sql'
QUERY_MV = FILES_DIR + 'query_missing_var.sql'

IN_2 = OUT_DIR + 'in2.csv'
OUT_2 = OUT_DIR + 'out2.csv'
QUERY_2 = FILES_DIR + 'query2.sql'

OUT_3 = OUT_DIR + 'out3.csv'

LEFT_1 = FILES_DIR + 'left_1.csv'
RIGHT_1 = FILES_DIR + 'right_1.csv'
OUT_JOIN_REF_1 = FILES_DIR + 'join_ref_1.csv'

LEFT_2 = FILES_DIR + 'left_2.csv'
RIGHT_2 = FILES_DIR + 'right_2.csv'
OUT_JOIN_REF_2 = FILES_DIR + 'join_ref_2.csv'

LEFT_3 = FILES_DIR + 'left_3.csv'
RIGHT_3 = FILES_DIR + 'right_3.csv'
OUT_JOIN_REF_3 = FILES_DIR + 'join_ref_3.csv'
