# reqlist allows you to quickly retrieve data from an Oracle DB given an input
# perimeter. The SQL output result can be joint to the input csv file (which can
# contain more than one column). The database is queried in parallel by
# multiple threads.
#
# In this example of use, the input file is first created from the 'in.csv' file
# (used to populate the TEST table) an contains two columns.
# The result contains 3 colums: 2 from the input file and the third (PRM) from
# the SQL result.
#
# Notes:
# - The SQL result must contain the first column in order to operate the joint.
# In other words, the first field of both input and SQL has to be an ID.
#
# - QUERY_IN accepts either a string or a file path.
#
# - Before running this example, you have to populate the TEST table
# by running quickstart/sql_upload.py
#
# For more details see the README.md file.

from datetime import datetime

import pytools.common as com
from pytools.common import g
from pytools.common import init_log
from pytools.reqlist import run_reqList

init_log('run_reqlist')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

date = datetime.now().strftime("%Y%m%d")
query_in = 'pytools/test/reqlist/files/query1.sql'
in_file = f"{g.dirs['IN']}rl_in.csv"
out_file = f"{g.dirs['OUT']}export_RL_{db}_{date}.csv"

# Creates input file from test file
arr = com.load_csv('pytools/test/sql/files/in.csv')
arr = [elt[0:2] for elt in arr]
com.save_csv(arr, in_file)

query_in = """
SELECT AFFAIRE, PRM
FROM TEST
WHERE 1=1
AND AFFAIRE IN @@IN@@
"""

run_reqList(
    CNX_STR=cnx_str,
    QUERY_IN=query_in,
    IN_PATH=in_file,
    OUT_PATH=out_file,
    OPEN_OUT_FILE=True,
)
