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
    cnx_str = get_cnx_str()
    cnx = cx.connect(cnx_str)
    com.log("Connected")
    is_up_to_date(cnx)

    return cnx


def get_cnx_str():
    err = False
    if gl.CNX_STR:
        cnx_str = gl.CNX_STR
        s = f"Connecting to data base ({cnx_str})..."
    elif (gl.DB, gl.ENV) in conf:
        cnx_str = conf[(gl.DB, gl.ENV)]
        s = (f"Connecting to data base '{gl.DB}' of"
             f" environment '{gl.ENV}' ({cnx_str})...")
    elif gl.DB in conf:
        cnx_str = conf[gl.DB]
        s = f"Connecting to data base {gl.DB} ({cnx_str})..."
    elif not gl.DB:
        s = ("Error: either gl.CNX_STR or gl.DB have to be defined")
        err = True
    elif not gl.ENV and gl.DB not in conf:
        s = (f"Error: data base '{gl.DB}' doesn't seem to be defined."
             " Pease check your conf_oracle.py file.")
        err = True
    else:
        s = (f"Error: data base '{gl.DB}' of environment '{gl.ENV}'"
             " doesn't seem to be defined."
             " Pease check your conf_oracle.py file.")
        err = True

    com.log(s)
    if err:
        raise Exception(s)
    return cnx_str


def gen_cnx_dict(nb):

    init_instant_client()
    cnx_str = get_cnx_str()
    gl.cnx_dict = dict()
    i = 1
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
