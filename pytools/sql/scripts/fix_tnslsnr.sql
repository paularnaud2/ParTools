alter SYSTEM set LOCAL_LISTENER='(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))' scope=both;
alter SYSTEM register;
exit
