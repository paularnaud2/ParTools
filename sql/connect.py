import conf_main as cfg
import common as com
import sql.gl as gl
import cx_Oracle as cx

from conf_oracle import conf
from threading import RLock
from sql.iutd import is_up_to_date

verrou = RLock()


def connect(ENV, DB):

    init_instant_client()
    if (ENV, DB) not in conf:
        s = f"DB '{DB}' of ENV '{ENV}' doesn't seem to be defined."
        s += " Pease check your conf_oracle.py file."
        raise Exception(s)
    cnx_str = conf[(ENV, DB)]
    com.log(f"Connecting to DB '{DB}' of '{ENV}' environment ({cnx_str})")
    cnx = cx.connect(cnx_str)
    com.log(f"Connected to {DB}")
    is_up_to_date(cnx)

    return cnx


def gen_cnx_dict(DB, ENV, nb):

    init_instant_client()
    cnx_str = conf[(ENV, DB)]
    gl.cnx_dict = dict()
    i = 1
    s = f"Creating connections for DB '{DB}' of '{ENV}' environnement"
    s += f" ({cnx_str})"
    com.log(s)
    while i <= nb:
        com.log(f'Creating connection no. {i}...')
        gl.cnx_dict[i] = cx.connect(cnx_str)
        is_up_to_date(gl.cnx_dict[i])
        com.log(f'Connection no. {i} created')
        i += 1


def init_instant_client():
    with verrou:
        if gl.client_is_init is False:
            com.log("Initialising Oracle client...")
            gl.client_is_init = True
            cx.init_oracle_client(cfg.ORACLE_CLIENT)
            com.log("Client Oracle initialised")
