# This script aims to solve problems with local TNS listener
import pytools.common.sTools as st

script = (
    "alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;\n"
    "alter SYSTEM register;\n"
    "exit")

st.run_sqlplus(script)
