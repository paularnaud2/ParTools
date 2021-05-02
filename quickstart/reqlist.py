"""
reqlist allows you to quickly retrieve data from an Oracle DB given an input
perimeter. The SQL output result can be joint to the input csv file (which can
contain more than one column). The database is queried in parallel by multiple
threads.

In this example of use, the input file is first created from the 'in.csv' file
(used to populate the TEST table) and contains two columns. The result contains 3
columns: 2 from the input file and the third (PRM) from the SQL result.

Notes:
- If SKIP_JOIN is False, the SQL result must contain the pivot column (column
used for the queries and for the joint) so that the script can operate the joint.
- The index of the pivot column is an input parameter (gl.PIVOT_IDX = 0)
- In other words, with the default value (PIVOT_IDX), the first field of both
input and SQL output have to contain IDs/keys (as in the example below).
- QUERY_IN accepts either a string or a file path.
- QUERY_IN must be (or point to) a variabilized query, ie. containing '@@IN@@'
after a IN statement, which will be replaced by the elements of the pivot column
while building the final queries being run in parallel.
- Before running this example, you have to populate the TEST table by running
quickstart/sql_upload.py

For more details, see the README.md file.
"""

from datetime import datetime

import pytools.common as com
from pytools.common import g
from pytools.common import init_log
from pytools.rl import reqlist

init_log('rl')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

date = datetime.now().strftime("%Y%m%d")
query_in = 'pytools/test/rl/files/query1.sql'
in_file = f"{g.dirs['IN']}rl_in.csv"
out_file = f"{g.dirs['OUT']}export_RL_{db}_{date}.csv"

# Creates input file from test file
arr = com.load_csv('pytools/test/sql/files/in.csv')
arr = [elt[0:2] for elt in arr]
com.save_csv(arr, in_file)

# The input query has to be variabilized
query_in = """
SELECT AFFAIRE, PRM
FROM TEST
WHERE 1=1
AND AFFAIRE IN @@IN@@
"""

reqlist(
    CNX_INFO=cnx_str,
    QUERY_IN=query_in,
    IN_PATH=in_file,
    OUT_PATH=out_file,
    OPEN_OUT_FILE=True,
)
