import pytools.common as com
from pytools.test.sql import clean_db


def test_run():
    com.init_log('test_run', True)

    import run.dq
    import run.fix_tnslsnr
    import run.sql_dowload
    import run.sql_execute
    import run.sql_upload
    import run.reqlist
    import run.tools_bf
    import run.tools_dup
    import run.tools_filter
    import run.tools_split
    import run.tools_xml

    clean_db(['TEST'])


if __name__ == '__main__':
    test_run()
