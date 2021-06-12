"""
In this file, you'll find examples of use for the different sTools (special tools)
script functions. Just uncomment the one you want to try out (see end of script).
"""

import partools.utils.sTools as st


def cmd():
    # Runs a Windows shell command

    st.run_cmd("echo Hello world")


def sqlplus():
    # This script aims to fix ORA-12514 (problem with local TNS listener on Oracle XE)

    script = """
    alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;
    alter SYSTEM register;
    exit;
    """

    st.run_sqlplus(script)


def msg_box():
    # Opens a non threaded and then a threaded message box

    st.msg_box("This is a non threaded message box", 'test', threaded=False)
    print('<code after non threaded message box>')
    st.msg_box("This is a threaded message box", 'test')
    print('<code after threaded message box>')


if __name__ == '__main__':
    # cmd()
    sqlplus()
    # msg_box()
