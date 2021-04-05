import cx_Oracle as cx
from os.path import exists
from threading import RLock

import pytools.common as com
import conf._conf_main as cfg
from conf._conf_oracle import conf

from . import gl
from .iutd import is_up_to_date

verrou = RLock()


def connect():

    init_instant_client()
    if gl.CNX_STR:
        cnx_str = gl.CNX_STR
        s = f"Connecting to data base ({cnx_str})..."
    elif (gl.ENV, gl.DB) not in conf:
        s = (f"Error: data base '{gl.DB}' of environment '{gl.ENV}'"
             " doesn't seem to be defined."
             " Pease check your conf_oracle.py file.")
        com.log(s)
        raise Exception(s)
    else:
        cnx_str = conf[(gl.ENV, gl.DB)]
        s = (f"Connecting to data base '{gl.DB}' of '{gl.ENV}'"
             f" environment ({cnx_str})...")
    com.log(s)
    cnx = cx.connect(cnx_str)
    com.log("Connected")
    is_up_to_date(cnx)

    return cnx


def gen_cnx_dict(nb):

    init_instant_client()
    if gl.CNX_STR:
        cnx_str = gl.CNX_STR
        s = f"Creating connections from {cnx_str}"
    else:
        cnx_str = conf[(gl.ENV, gl.DB)]
        s = (f"Creating connections for DB '{gl.DB}' of '{gl.ENV}'"
             f" environnement ({cnx_str})")
    gl.cnx_dict = dict()
    i = 1
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
            if not exists(cfg.ORACLE_CLIENT):
                s = ("Error: The Oracle instant client path specified in"
                     f" conf_main.py (ORACLE_CLIENT = {cfg.ORACLE_CLIENT})"
                     " doesn't exist. Please enter a valid path for the"
                     " Oracle instant client.")
                com.log(s)
                raise Exception(s)
            cx.init_oracle_client(cfg.ORACLE_CLIENT)
            com.log("Client Oracle initialised")
