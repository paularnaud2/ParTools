"""
sql.download allows you to simply and quickly retrieve data from an Oracle DB.
In this file, you'll find four examples of use. For cases 2, 3, 4, the database
is queried in parallel by multiple threads.

1) example_simple: a simple SELECT query is processed (no multithread possible
in this case).

2) example_ql_raw: a raw query list is processed. The 3 results are merged
(default behavior, MERGE_FILES=True) and output in a single csv file.

3) example_ql_var: a variabilized query list is processed. The 3 results are
output in 3 different csv files (MERGE_FILES=False).

4) example_rg: a 'range query' is processed. A range query is a variabilized
query which is executed in parallel for each range of ID contained in the file
whose name appears in the variable. Before running this example, run
quickstart/sql_upload.py to create and populate the TEST table.

Notes:
- QUERY_IN accepts either a string or a file path
- You can input either CNX_INFO or DB, as long as the DB you pass in is defined
in the conf file (partools/conf.py, CONF_ORACLE)
- As you'll see below, CNX_INFO can either be a connection string:
'USER/PWD@HOST:PORT/SERVICE_NAME'
 or a list:
['USERNAME', 'PWD', 'TNS_NAME'] or ['USERNAME', 'PWD', 'DSN']

For more details, check out the README.md file.
"""

from datetime import datetime

import partools.sql as sql
from partools.utils import g
from partools.utils import init_log

init_log('sql_download')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

# Here 'XE_TNS' is a TNS_NAME that has to be defined in the tnsnames.ora file.
# You can also directly put a DSN instead.
cnx_tns = ['USERNAME', 'PWD', 'XE_TNS']

date = datetime.now().strftime("%Y%m%d")
out_file = f"{g.dirs['OUT']}sql_{db}_{date}.csv"


def example_simple():
    query_in = "SELECT 'HELLO WORLD' as TEST FROM DUAL"
    sql.download(
        CNX_INFO=cnx_str,
        # CNX_INFO=cnx_tns,
        # DB=db,
        QUERY_IN=query_in,
        OUT_PATH=out_file,
    )


def example_ql_raw():
    """Expected format for the elements of a raw query list :
    [query, name of query]
    Note that in the case of a raw query list, no QUERY_IN should be input."""

    query_list_raw = [
        ["SELECT 'HELLO WORLD 1' as TEST FROM DUAL", "query 1"],
        ["SELECT 'HELLO WORLD 2' as TEST FROM DUAL", "query 2"],
        ["SELECT 'HELLO WORLD 3' as TEST FROM DUAL", "query 3"],
    ]

    sql.download(
        CNX_INFO=cnx_str,
        QUERY_LIST=query_list_raw,
        OUT_PATH=out_file,
    )


def example_ql_var():
    """Expected format for the elements of a var query list :
    [replacing element, name of query]
    Note that in the case of a var query list, a QUERY_IN var should be input;
    containing a variabilized query used for the replacing elements."""

    query_in_var = "SELECT 'HELLO WORLD @@IN@@' as TEST FROM DUAL"
    query_list_var = [
        ["1", "query 1"],
        ["2", "query 2"],
        ["3", "query 3"],
    ]

    # With MERGE_FILES=False, the files from the three parallel queries won't be
    # merged but moved to OUT_DIR
    sql.download(
        CNX_INFO=cnx_str,
        QUERY_IN=query_in_var,
        QUERY_LIST=query_list_var,
        MERGE_FILES=False,
        OUT_DIR=f"{g.dirs['OUT']}sql_out/",
    )


def example_rg():
    """A range query should contain a variable element formatted as follows:
    @@RG_<range_file>@@ where the range file is a csv file located in
    'partools/sql/ranges'"""

    query_in_rg = """
    SELECT * FROM TEST
    WHERE 1=1
    AND PRM LIKE '@@RG_PRM_2@@%'
    """

    sql.download(
        CNX_INFO=cnx_str,
        QUERY_IN=query_in_rg,
        OUT_PATH=out_file,
    )


example_simple()
# example_ql_raw()
# example_ql_var()
# example_rg()
