# Use this script to troubleshoot you connection problems to Oracle DB
# Here you can try to connect either by using a connection string, a DNS or a TNS_NAME

import cx_Oracle as cx
import pytools.conf as cfg

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

cx.init_oracle_client(cfg.ORACLE_CLIENT)

# 1) connect via connection string
# cnx = cx.connect(cnx_str)

# 2) connect via DSN
cnx = cx.connect("USERNAME", "PWD", dsn)

# 3) connection via TNS_NAME
# cnx = cx.connect("USERNAME", "PWD", "LOCAL_XE")

c = cnx.cursor()
c.execute(query)
print(c.fetchone()[0])
