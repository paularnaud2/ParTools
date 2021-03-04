import sql
from common import init_log
init_log('run_sql')

if __name__ == '__main__':

    sql.download(
        MAX_DB_CNX=8,
        MERGE_RG_FILES=True,
        EXPORT_RANGE=False,
        CHECK_DUP=True,
    )

    # table_name = 'TEST_AFF'
    # sql.execute(
    #     SCRIPT_FILE='sql/procs/create_table_aff.sql',
    #     VAR_DICT={'@@TABLE_NAME@@': table_name},
    #     PROC=True,
    #     ENV='DIRECT',
    #     DB='CAPC5',
    # )

    # sql.upload(
    #     SCRIPT_FILE='sql/scripts/insert_table_aff.sql',
    #     UPLOAD_IN='C:/Py/OUT/test.csv',
    #     VAR_DICT={'@@TABLE_NAME@@': table_name},
    #     NB_MAX_ELT_INSERT=100,
    #     ENV='DIRECT',
    #     DB='CAPC5',
    # )
