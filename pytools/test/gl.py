from pytools.common import g

import pytools.tools.gl as gt
import pytools._conf_main as cfg
import pytools.tools.gl as tools
import pytools.reqlist.gl as rl
import pytools.sql.gl as sql

# Main
TEST = 'pytools/test/'
TEST_OUT = 'test/'
OUT_DUP_TMP = g.paths['TMP'] + tools.TMP_FOLDER + gt.TMP_OUT

# test_sql
TEST_SQL = TEST + 'sql/files/'
TEST_SQL_OUT = TEST_OUT + 'sql/'
SQL_OUT = g.paths['TMP'] + TEST_SQL_OUT
SQL_TMP = g.paths['TMP'] + sql.TMP_FOLDER
SQL_ENV = cfg.TEST_ENV
SQL_DB = cfg.TEST_DB
SQL_T_TEST = 'TEST'
SQL_T_IUTD = 'TEST_IUTD'
SQL_CREATE_TABLE = TEST_SQL + 'create_table.sql'
SQL_CREATE_TABLE_IUTD = TEST_SQL + 'create_table_iutd.sql'
SQL_DROP_TABLE = TEST_SQL + 'drop_table.sql'
SQL_INSERT_IUTD_OK = TEST_SQL + 'insert_iutd_ok.sql'
SQL_INSERT_IUTD_KO = TEST_SQL + 'insert_iutd_ko.sql'
SQL_INSERT_TABLE = TEST_SQL + 'insert_table.sql'
SQL_QUERY = TEST_SQL + 'export.sql'
SQL_QUERY_IUTD = TEST_SQL + 'iutd.sql'
SQL_QUERY_NO = TEST_SQL + 'export_no_output.sql'
SQL_QUERY_RG = TEST_SQL + 'export_rg.sql'
SQL_QUERY_COUNT_1 = TEST_SQL + 'count_1.sql'
SQL_QUERY_COUNT_1_RG = TEST_SQL + 'count_1_rg.sql'
SQL_QUERY_COUNT_2 = TEST_SQL + 'count_2.sql'
SQL_QUERY_COUNT_2_RG = TEST_SQL + 'count_2_rg.sql'
SQL_IN = TEST_SQL + 'in.csv'
SQL_IN_MH = TEST_SQL + 'in_missing_header.csv'
SQL_OUT_DUP_REF = TEST_SQL + 'out_dup_ref.csv'
SQL_DL_OUT = SQL_OUT + 'out.csv'
SQL_DL_OUT_COUNT = SQL_OUT + 'out_count.csv'
SQL_DL_OUT_COUNT_1_REF = TEST_SQL + 'out_count_1_ref.csv'
SQL_DL_OUT_COUNT_2_REF = TEST_SQL + 'out_count_2_ref.csv'
SQL_DL_OUT_RG = SQL_OUT + 'out_rg.csv'
SQL_DL_OUT_RG_FOLDER = SQL_OUT + 'RG_TEST/'
SQL_RG_REF = TEST_SQL + '01_ref.csv'
SQL_RG_COMP = SQL_DL_OUT_RG_FOLDER + '01.csv'
SQL_MAX_ELT_INSERT = 200

# test_reqlist
TEST_RL = TEST + 'reqlist/'
TEST_RL_OUT = TEST_OUT + 'reqlist/'
RL_OUT = g.paths['TMP'] + TEST_RL_OUT
RL_TMP = g.paths['TMP'] + rl.TMP_FOLDER
RL_OUT_JOIN = RL_OUT + 'join.csv'
RL_OUT_DUP_REF = TEST_RL + 'out_dup_ref.csv'

RL_IN_1 = RL_OUT + 'in1.csv'
RL_IN_MH = RL_OUT + 'in_missing_header.csv'
RL_OUT_1 = RL_OUT + 'out1.csv'
RL_QUERY_1 = TEST_RL + 'query1.sql'
RL_QUERY_NO = TEST_RL + 'query_no_output.sql'
RL_QUERY_MV = TEST_RL + 'query_missing_var.sql'

RL_IN_2 = RL_OUT + 'in2.csv'
RL_OUT_2 = RL_OUT + 'out2.csv'
RL_QUERY_2 = TEST_RL + 'query2.sql'

RL_OUT_3 = RL_OUT + 'out3.csv'

RL_LEFT_1 = TEST_RL + 'left_1.csv'
RL_RIGHT_1 = TEST_RL + 'right_1.csv'
RL_OUT_JOIN_REF_1 = TEST_RL + 'join_ref_1.csv'

RL_LEFT_2 = TEST_RL + 'left_2.csv'
RL_RIGHT_2 = TEST_RL + 'right_2.csv'
RL_OUT_JOIN_REF_2 = TEST_RL + 'join_ref_2.csv'

RL_LEFT_3 = TEST_RL + 'left_3.csv'
RL_RIGHT_3 = TEST_RL + 'right_3.csv'
RL_OUT_JOIN_REF_3 = TEST_RL + 'join_ref_3.csv'

# test_dq
TEST_DQ = TEST + 'dq/'
TEST_DQ_OUT = TEST_OUT + 'dq/'
DQ_OUT = g.paths['TMP'] + TEST_DQ_OUT

IN_MH = 'in_missing_header'
IN_DH = 'in_different_header'
IN_DK = 'in_dup_key'
OUT_DK = DQ_OUT + '1_dup_key.csv'
OUT_DK_REF = TEST_DQ + 'out_ref_dup_key.csv'
OUT_FM = DQ_OUT + 'file_match_out.csv'
REF_FM = TEST_DQ + 'out_ref_fm.csv'
REF_FDM = TEST_DQ + 'out_ref_fdm.csv'

IN11 = 'in_11'
IN12 = 'in_12'
REF1 = 'out_ref_1.csv'
REF1_F = TEST_DQ + 'out_ref_1.csv'
REF1_E = 'out_ref_1_e.csv'
REF_DUP1 = 'out_ref_dup_11.csv'
OUT1 = '1'

IN21 = 'in_21'
IN22 = 'in_22'
REF2 = 'out_ref_2.csv'
REF2_F = TEST_DQ + 'out_ref_2.csv'
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

# test_tools
TEST_TOOL = TEST + tools.TMP_FOLDER
TEST_TOOL_OUT = TEST_OUT + tools.TMP_FOLDER
TOOLS_OUT = g.paths['TMP'] + TEST_TOOL_OUT

# XML
XML_IN = TEST_TOOL + 'xml_in.xml'
XML_OUT = TOOLS_OUT + 'out_xml.csv'
XML_OUT_REF = TEST_TOOL + 'xml_out_ref.csv'

# Split
S_OUT_1 = TOOLS_OUT + 'in_1.csv'
S_OUT_2 = TOOLS_OUT + 'in_2.csv'
S_OUT_3 = TOOLS_OUT + 'in_3.csv'
S_OUT_REF_1 = TEST_TOOL + 'split_out_ref_1.csv'
S_OUT_REF_2 = TEST_TOOL + 'split_out_ref_2.csv'
S_OUT_REF_3 = TEST_TOOL + 'split_out_ref_3.csv'

# Dup
DUP_IN = TEST_TOOL + 'dup_in.csv'
DUP_OUT = TOOLS_OUT + 'out_dup.csv'
SHUF_OUT = TOOLS_OUT + 'out_shuf.csv'
DUP_OUT_REF = TEST_TOOL + 'dup_out_ref.csv'
DEL_DUP_OUT_REF = TEST_TOOL + 'del_dup_out_ref.csv'
DUP_COL_IN = TEST_TOOL + 'dup_col_in.csv'
DUP_COL_REF = TEST_TOOL + 'dup_out_ref_2.csv'

# Filter
FLT_OUT = TOOLS_OUT + 'filter_out.csv'
FLT_OUT_REF = TEST_TOOL + 'filter_out_ref.csv'

# BF
LOOK_FOR = '22173227102607'
SEARCH_BF_OUT = TOOLS_OUT + 'search_bf_out.csv'
SEARCH_BF_OUT_REF = TEST_TOOL + 'search_bf_out_ref.csv'
SORT_BF_OUT = TOOLS_OUT + 'sort_bf_out.csv'
