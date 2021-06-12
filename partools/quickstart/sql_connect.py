"""
Use this script to troubleshoot your connection problems.
Here you can try to connect either by using one of the following:
- Connection string,
- DNS
- TNS_NAME.
"""

import cx_Oracle as cx
from partools import cfg

cnx_str = 'USERNAME/PWD@localhost:1521/XE'
dsn = """
(DESCRIPTION =
    (ADDRESS_LIST =
        (ADDRESS =
            (PROTOCOL = TCP)
            (HOST = localhost)
            (PORT = 1521)
        )
    )
    (CONNECT_DATA =
        (SERVICE_NAME = XE)
    )
)
"""
query = "SELECT 'HELLO WORLD' as TEST FROM DUAL"

print("Initialising Oracle instant client...")
cx.init_oracle_client(cfg.ORACLE_CLIENT)
print("Initialising Oracle instant client initialised")
print("Connecting...")

# 1) connect via connection string
cnx = cx.connect(cnx_str)

# 2) connect via DSN
# cnx = cx.connect("USERNAME", "PWD", dsn)

# 3) connection via TNS_NAME
# cnx = cx.connect("USERNAME", "PWD", "XE_TNS")

print("Connected")
print(f'Executing "{query}"')
c = cnx.cursor()
c.execute(query)
print("Query executed. Output:")
print(c.fetchone()[0])
