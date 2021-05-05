"""
sql.upload allows you to simply upload data to an Oracle DB.

In this example of use, the file 'in.csv' is uploaded into the 'XE' DB. You can
input kwargs for the execute function to be run before the upload (EXECUTE_KWARGS).
Here, a create table script is passed ensuring that the 'TEST' table exists
before the upload and that the end result remains the same after each execution.

The input 'VAR_DICT' allows you to pass a dictionary containing variable names
and values to be replaced in the input script. Here, '@@TABLE_NAME@@' will be
replaced by 'TEST'.

Notes:
- SCRIPT_IN accepts either a string or a file path
- You can input either CNX_INFO or DB, as long as the DB you pass is defined
in the conf file (pytools/conf.py)

For more details, see the README.md file.
"""

import pytools.sql as sql
from pytools.utils import init_log

init_log('sql_upload')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'
script_in = 'pytools/test/sql/files/insert_table.sql'

execute_kwargs = {
    "SCRIPT_IN": 'pytools/test/sql/files/create_table.sql',
    "PROC": True,
}

sql.upload(
    # CNX_INFO=cnx_str,
    # CNX_INFO=cnx_tns,
    DB=db,
    UPLOAD_IN='pytools/test/sql/files/in.csv',
    SCRIPT_IN=script_in,
    VAR_DICT={'TABLE_NAME': 'TEST'},
    EXECUTE_KWARGS=execute_kwargs,
)
