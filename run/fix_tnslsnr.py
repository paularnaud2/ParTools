# This script aims to solve problems with local TNS listener
import pytools.common.sTools as st
import conf._conf_main as cfg

script = """
alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;
alter SYSTEM register;
exit
"""

if cfg.TEST_DB == 'XE':
    st.run_sqlplus(script)
