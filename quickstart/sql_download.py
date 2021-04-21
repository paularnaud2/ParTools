# sql.download allows you to simply and quickly retreive data from an Oracle DB
#
# In this file, you'll find four examples of use:
# 1) example_simple: a simple SELECT query (no multithread in this case) is processed.
# 2) example_ql_raw: a raw query list is processed. The 3 results are merged
# (default behavior, MERGE_FILES=True) and output in a single csv file.
# 3) example_ql_var: a variabilised query list is processed. The 3 results are
# output in 3 different csv files (MERGE_FILES=False).
# 4) example_rg: a 'range query' is processed. A range query is a variablilised
# query which executed in parralel for each range of ID contained in the file
# whose name appears in the variable (see example)
#
# Notes:
# - SCRIPT_IN accepts either a string or a file path
# - You can input either CNX_STR or DB, as long as the DB you pass is defined
# in the conf file (pytools/conf.py)
#
# For more details, see the README.md file.

from datetime import datetime

import pytools.sql as sql
from pytools.common import g
from pytools.common import init_log

init_log('run_sql.download')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

date = datetime.now().strftime("%Y%m%d")
out_file = f"{g.dirs['OUT']}sql_{db}_{date}.csv"


def example_simple():
    query_in = "SELECT 'HELLO WORLD' as TEST FROM DUAL"
    sql.download(
        CNX_STR=cnx_str,
        QUERY_IN=query_in,
        OUT_PATH=out_file,
    )


def example_ql_raw():
    # Expected format for the elements of a raw query list :
    # [query, name of query]
    #
    # Note that in the case of a raw query list, no QUERY_IN should be input

    query_list_raw = [
        ["SELECT 'HELLO WORLD 1' as TEST FROM DUAL", "query 1"],
        ["SELECT 'HELLO WORLD 2' as TEST FROM DUAL", "query 2"],
        ["SELECT 'HELLO WORLD 3' as TEST FROM DUAL", "query 3"],
    ]

    sql.download(
        CNX_STR=cnx_str,
        QUERY_LIST=query_list_raw,
        OUT_PATH=out_file,
    )


def example_ql_var():
    # Expected format for the elements of a var query list :
    # [replacing element, name of query]
    #
    # Note that in the case of a var query list, a QUERY_IN var should be input;
    # containing a variabilised query used for the replacing elements

    query_in_var = "SELECT 'HELLO WORLD @@IN@@' as TEST FROM DUAL"
    query_list_var = [
        ["1", "query 1"],
        ["2", "query 2"],
        ["3", "query 3"],
    ]

    sql.download(
        CNX_STR=cnx_str,
        QUERY_IN=query_in_var,
        QUERY_LIST=query_list_var,
        OUT_PATH=out_file,
        MERGE_FILES=False,
    )


def example_rg():
    # A range query should contain a variable element formatted as follows:
    # @@RG_<range_file>@@. The range file is a csv file located in
    # 'pytools/sql/ranges'

    query_in_rg = """
    SELECT * FROM TEST
    WHERE 1=1
    AND PRM LIKE '@@RG_PRM_2@@%'
    """

    sql.download(
        CNX_STR=cnx_str,
        QUERY_IN=query_in_rg,
        OUT_PATH=out_file,
    )


example_simple()
# example_ql_raw()
# example_ql_var()
# example_rg()
