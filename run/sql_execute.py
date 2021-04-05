import pytools.sql as sql
from pytools.common import init_log

init_log('run_sql.execute')

env = 'LOCAL'
db = 'XE'

script_in = f'sql/scripts/execute_{db}.sql'
sql.execute(
    ENV=env,
    DB=db,
    SCRIPT_IN='pytools/test/sql/files/create_table.sql',
    VAR_DICT={'TABLE_NAME': 'TEST'},
    PROC=True,
)

script_in = """
INSERT INTO TEST VALUES (1, 1, 1);
INSERT INTO TEST VALUES (2, 2, 2);
"""

sql.execute(SCRIPT_IN=script_in, PROC=False)
