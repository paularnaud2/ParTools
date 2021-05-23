"""
sql.execute allows you to simply execute a SQL script or a PL/SQL procedure
on an Oracle DB.

In this example of use, a create table script is first executed followed by
insert commands. If your script contains a single command or is a PL/SQL
procedure (first example), you have to put PROC=True or nothing (default value);
if it contains several commands (second example), you have to set PROC=False.

Notes:
- SCRIPT_IN accepts either a string or a file path
- CNX_INFO and DB inputs follow the same rules as for sql.download

For more details, check out the README.md file.
"""

import partools.sql as sql
from partools.utils import init_log
from partools.quickstart import files_dir

init_log('sql_execute')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'
script_in = f'{files_dir}create_table.sql'

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
    CNX_INFO=cnx_str,
    SCRIPT_IN=script_in,
    PROC=False,
)
