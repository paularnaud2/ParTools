# This script aims to fix ORA-12514 (problem with local TNS listener)

import pytools.utils.sTools as st

script = """
alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;
alter SYSTEM register;
exit;
"""

st.run_sqlplus(script)
