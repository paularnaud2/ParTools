import cx_Oracle as cx
from os.path import exists
from threading import RLock

import pytools.common as com
from pytools.common import g
import pytools.conf as cfg

from . import gl
from . import gls
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
        s = gl.S_1.format(cnx_str)
    elif (gl.DB, gl.ENV) in cfg.CONF_ORACLE:
        cnx_str = cfg.CONF_ORACLE[(gl.DB, gl.ENV)]
        s = gl.S_2.format(gl.DB, gl.ENV, cnx_str)
    elif gl.DB in cfg.CONF_ORACLE:
        cnx_str = cfg.CONF_ORACLE[gl.DB]
        s = s = gl.S_3.format(gl.DB, cnx_str)
    elif not gl.DB:
        s = gl.E_1
        err = True
    elif not gl.ENV and gl.DB not in cfg.CONF_ORACLE:
        s = gl.E_2.format(gl.DB)
        err = True
    else:
        s = gl.E_3.format(gl.DB, gl.ENV)
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
        if gls.client_is_init is False:
            com.log("Initialising Oracle client...")
            gls.client_is_init = True
            if not exists(cfg.ORACLE_CLIENT):
                s = ("Error: The Oracle instant client path specified in"
                     f" {g.conf_path} (ORACLE_CLIENT = {cfg.ORACLE_CLIENT})"
                     " doesn't exist. Please enter a valid path for the"
                     " Oracle instant client.")
                com.log(s)
                raise Exception(s)
            cx.init_oracle_client(cfg.ORACLE_CLIENT)
            com.log("Client Oracle initialised")
