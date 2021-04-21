# sql.execute allows you to simply execute a SQL script or a PL/SQL procedure
# on an Oracle DB.
#
# In this example of use, a create table script is first executed followed by
# insert commands. When your script contains a single command or is a PL/SQL
# procedure (first example), you have to put PROC=True or nothing (default value);
# else if it contains several commands (second example),  then PROC=False.
#
# Notes:
# - SCRIPT_IN accepts either a string or a file path
# - You can input either CNX_STR or DB, as long as the DB you pass is defined
# in the conf file (pytools/conf.py)
#
# For more details see the README.md file.

import pytools.sql as sql
from pytools.common import init_log

init_log('run_sql.execute')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'
script_in = 'pytools/test/sql/files/create_table.sql'

sql.execute(
    DB=db,
    SCRIPT_IN=script_in,
    VAR_DICT={'TABLE_NAME': 'TEST'},
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
