import pytools.sql as sql
from pytools.common import init_log

init_log('run_sql.upload')

db = 'XE'

script_in = f'sql/scripts/upload_{db}.sql'
script_in = 'pytools/test/sql/files/insert_table.sql'

# script_in = """
# INSERT INTO TEST (
# AFFAIRE
# , DEM_ID
# , PRM
# )
# VALUES (:1, :2, :3)
# """

execute_kwargs = {
    "SCRIPT_IN": 'pytools/test/sql/files/create_table.sql',
    "PROC": True,
}

sql.upload(
    DB=db,
    SCRIPT_IN=script_in,
    UPLOAD_IN='pytools/test/sql/files/in.csv',
    VAR_DICT={'TABLE_NAME': 'TEST'},
    EXECUTE_PARAMS=execute_kwargs,
)
