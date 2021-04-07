from datetime import datetime

import pytools.common as com
from pytools.common import g
from pytools.common import init_log
from pytools.reqlist import run_reqList

init_log('run_reqlist')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

date = datetime.now().strftime("%Y%m%d")
query_in = 'reqlist/queries/e_RL.sql'
query_in = 'pytools/test/reqlist/files/query1.sql'
in_file = f"{g.paths['IN']}rl_in.csv"
out_file = f"{g.paths['OUT']}export_RL_{db}_{date}.csv"

# Creates input file from test file
arr = com.load_csv('pytools/test/sql/files/in.csv')
arr = [elt[0] for elt in arr]
com.save_csv(arr, in_file)

query_in = """
SELECT AFFAIRE, DEM_ID
FROM TEST
WHERE 1=1
AND AFFAIRE IN @@IN@@
"""

if __name__ == '__main__':
    run_reqList(
        CNX_STR=cnx_str,
        # DB=db,
        QUERY_IN=query_in,
        IN_FILE=in_file,
        OUT_FILE=out_file,
        VAR_DICT={'TABLE_NAME': 'TEST'},
    )
else:
    run_reqList(
        CNX_STR=cnx_str,
        QUERY_IN=query_in,
        IN_FILE=in_file,
        OUT_FILE=out_file,
        VAR_DICT={'TABLE_NAME': 'TEST'},
        OPEN_OUT_FILE=False,
    )
