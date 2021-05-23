"""
reqlist allows you to quickly retrieve data from an Oracle DB given an input
perimeter. The SQL output can be joint to the input csv file (which can
contain more than one column). The database is queried in parallel by multiple
threads.

In this example of use, the input file is first created from the 'in.csv' file
(used to populate the TEST table) and contains two columns.
The output contains 3 columns:
2 from the input file and the third (PRM) from the SQL output.

Notes:
- If SKIP_JOIN is False, the SQL output must contain the pivot column (column
used for the queries and for the joint) so that the script can operate the joint.
- The index of the pivot column is an input parameter (gl.PIVOT_IDX = 0)
- In other words, with the default value (PIVOT_IDX), the first field of both
input and SQL output have to contain IDs/keys (as in the example below).
- QUERY_IN accepts either a string or a file path.
- QUERY_IN must be (or point to) a variabilized query, ie. containing '@@IN@@'
after a IN statement, which will be replaced by the elements of the pivot column
while building the final queries being run in parallel.
- Before running this example, you run quickstart/sql_upload.py to create and 
populate the TEST table.
- CNX_INFO and DB inputs follow the same rules as for sql.download

For more details, check out the README.md file.
"""

from datetime import datetime

import partools.utils as u
from partools.utils import g
from partools.utils import init_log
from partools.rl import reqlist
from partools.quickstart import files_dir

init_log('rl')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

date = datetime.now().strftime("%Y%m%d")
in_file = f"{g.dirs['IN']}rl_in.csv"
out_file = f"{g.dirs['OUT']}export_RL_{db}_{date}.csv"

# Creates input file from test file
arr = u.load_csv(f'{files_dir}in.csv')
arr = [elt[0:2] for elt in arr]
u.save_csv(arr, in_file)

# The input query has to be variabilized ie. contain @@IN@@:
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
)
