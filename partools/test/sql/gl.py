from partools.test import gl
from partools.utils import g

import partools.sql.gl as sql

FILES_DIR = gl.TEST + 'sql/files/'
IN = FILES_DIR + 'in.csv'
OUT_DIR = g.dirs['TMP'] + gl.TEST_OUT + 'sql/'
TMP_DIR = g.dirs['TMP'] + sql.TMP_FOLDER
DB = 'XE'
ENV = 'LOCAL'
T_TEST = 'TEST'
T_IUTD = 'TEST_IUTD'
CNX_INFO = ['USERNAME', 'PWD', 'XE_TNS']
CREATE_TABLE = FILES_DIR + 'create_table.sql'
CREATE_TABLE_IUTD = FILES_DIR + 'create_table_iutd.sql'
DROP_TABLE = FILES_DIR + 'drop_table.sql'
INSERT_IUTD_OK = FILES_DIR + 'insert_iutd_ok.sql'
INSERT_IUTD_KO = FILES_DIR + 'insert_iutd_ko.sql'
INSERT_TABLE = FILES_DIR + 'insert_table.sql'
QUERY = FILES_DIR + 'export.sql'
QUERY_IUTD = FILES_DIR + 'iutd.sql'
QUERY_NO = FILES_DIR + 'export_no_output.sql'
QUERY_RG = FILES_DIR + 'export_rg.sql'
QUERY_COUNT_1 = FILES_DIR + 'count_1.sql'
QUERY_COUNT_1_RG = FILES_DIR + 'count_1_rg.sql'
QUERY_COUNT_2 = FILES_DIR + 'count_2.sql'
QUERY_COUNT_2_RG = FILES_DIR + 'count_2_rg.sql'
IN_MH = FILES_DIR + 'in_missing_header.csv'
OUT_DUP_REF = FILES_DIR + 'out_dup_ref.csv'
DL_OUT = OUT_DIR + 'out.csv'
DL_OUT_COUNT = OUT_DIR + 'out_count.csv'
DL_OUT_COUNT_1_REF = FILES_DIR + 'out_count_1_ref.csv'
DL_OUT_COUNT_2_REF = FILES_DIR + 'out_count_2_ref.csv'
DL_OUT_RG = OUT_DIR + 'out_rg.csv'
DL_OUT_RG_FOLDER = OUT_DIR + 'RG_TEST/'
RG_REF = FILES_DIR + '01_ref.csv'
RG_COMP = DL_OUT_RG_FOLDER + '01.csv'
MAX_ELT_INSERT = 200
