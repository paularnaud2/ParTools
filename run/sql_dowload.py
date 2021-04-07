from datetime import datetime

import pytools.sql as sql
from pytools.common import g
from pytools.common import init_log

init_log('run_sql.download')

date = datetime.now().strftime("%Y%m%d")

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

query_in = f'sql/queries/{db}_dl.sql'
out_file = f"{g.paths['OUT']}sql_{db}_{date}.csv"
# out_rg_dir = f"{g.paths['OUT']}{db}_OUT_{date}/"

query_in = """
SELECT 'HELLO WORLD' as TEST
FROM DUAL
"""

if __name__ == '__main__':
    sql.download(
        # CNX_STR=cnx_str,
        DB=db,
        QUERY_IN=query_in,
        OUT_FILE=out_file,
    )
else:
    sql.gl.OPEN_OUT_FILE = False
    sql.download(DB='XE', QUERY_IN=query_in, OUT_FILE=out_file)