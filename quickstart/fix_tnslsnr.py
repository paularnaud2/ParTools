# This script aims to fix ORA-12514 (problem with local TNS listener)
import pytools.common.sTools as st
import pytools.conf as cfg

script = """
alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;
alter SYSTEM register;
exit
"""

if cfg.TEST_DB == 'XE':
    st.run_sqlplus(script)
