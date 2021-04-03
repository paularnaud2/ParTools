import pytools.sql as sql
from pytools.common import init_log

init_log('run_sql')

sql.download(
    ENV="LOCAL",
    DB="XE",
    QUERY_FILE=query,
    OUT_FILE=out,
)

# table_name = 'TEST_AFF'
# sql.execute(
#     ENV="LOCAL",
#     DB="XE",
#     SCRIPT_FILE='sql/procs/create_table_aff.sql',
#     VAR_DICT={'@@TABLE_NAME@@': table_name},
#     PROC=True,
# )

# sql.upload(
#     ENV="LOCAL",
#     DB="XE",
#     SCRIPT_FILE='sql/scripts/insert_table_aff.sql',
#     UPLOAD_IN='C:/Py/OUT/test.csv',
#     VAR_DICT={'@@TABLE_NAME@@': table_name},
#     NB_MAX_ELT_INSERT=100,
# )
