# sql.execute allows you to simply execute a SQL script or
# a PL/SQL procedure on an Oracle DB.
#
# In this example of use, (you need write priviledge)
# For more details see the README.md file.
#
# Note that SCRIPT_IN accepts either a string or a file path

import pytools.sql as sql
from pytools.common import init_log

init_log('run_sql.execute')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'

script_in = f'sql/scripts/execute_{db}.sql'
sql.execute(
    DB=db,
    SCRIPT_IN='pytools/test/sql/files/create_table.sql',
    VAR_DICT={'TABLE_NAME': 'TEST'},
    PROC=True,
)

script_in = """
INSERT INTO TEST VALUES (1, 1, 1);
INSERT INTO TEST VALUES (2, 2, 2);
"""

sql.execute(
    CNX_STR=cnx_str,
    SCRIPT_IN=script_in,
    PROC=False,
)
