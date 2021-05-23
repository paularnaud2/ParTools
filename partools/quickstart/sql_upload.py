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
- CNX_INFO and DB inputs follow the same rules as for sql.download

For more details, check out the README.md file.
"""

import partools.sql as sql
from partools.utils import init_log
from partools.quickstart import files_dir

init_log('sql_upload')

db = 'XE'
cnx_str = 'USERNAME/PWD@localhost:1521/XE'
script_in = f'{files_dir}insert_table.sql'

execute_kwargs = {
    "SCRIPT_IN": f'{files_dir}create_table.sql',
    "PROC": True,
}

sql.upload(
    # CNX_INFO=cnx_str,
    # CNX_INFO=cnx_tns,
    DB=db,
    UPLOAD_IN=f'{files_dir}in.csv',
    SCRIPT_IN=script_in,
    VAR_DICT={'TABLE_NAME': 'TEST'},
    EXECUTE_KWARGS=execute_kwargs,
)
