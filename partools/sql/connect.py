import cx_Oracle as cx
from os.path import exists
from threading import RLock

from partools import cfg
import partools.utils as u

from . import gl
from . import gls
from .iutd import is_up_to_date

verrou = RLock()


def connect():

    init_instant_client()
    cnx_info = get_cnx_info()
    cnx = connect_with(cnx_info)
    u.log("Connected")
    is_up_to_date(cnx)

    return cnx


def connect_with(cnx_info):

    if isinstance(cnx_info, str):
        return cx.connect(cnx_info)
    else:
        return cx.connect(*cnx_info)


def get_cnx_info():
    err = False
    if gl.CNX_INFO:
        cnx_info = gl.CNX_INFO
        s = gl.S_1.format(cnx_info)
    elif (gl.DB, gl.ENV) in cfg.CONF_ORACLE:
        cnx_info = cfg.CONF_ORACLE[(gl.DB, gl.ENV)]
        s = gl.S_2.format(gl.DB, gl.ENV, cnx_info)
    elif gl.DB in cfg.CONF_ORACLE:
        cnx_info = cfg.CONF_ORACLE[gl.DB]
        s = gl.S_3.format(gl.DB, cnx_info)
    elif not gl.DB:
        s = gl.E_1
        err = True
    elif not gl.ENV and gl.DB not in cfg.CONF_ORACLE:
        s = gl.E_2.format(gl.DB)
        err = True
    else:
        s = gl.E_3.format(gl.DB, gl.ENV)
        err = True

    if err:
        raise Exception(s)
    else:
        u.log(s)

    return cnx_info


def gen_cnx_dict(nb):

    init_instant_client()
    cnx_info = get_cnx_info()
    gl.cnx_dict = dict()
    i = 1
    while i <= nb:
        u.log(f'Creating connection no. {i}...')
        gl.cnx_dict[i] = connect_with(cnx_info)
        is_up_to_date(gl.cnx_dict[i])
        u.log(f'Connection no. {i} created')
        i += 1


def init_instant_client():
    with verrou:
        if gls.client_is_init is False:
            u.log("Initialising Oracle client...")
            gls.client_is_init = True
            if not exists(cfg.ORACLE_CLIENT):
                s = ("Error: The Oracle instant client directory specified in"
                     f" {cfg.__file__} (ORACLE_CLIENT = {cfg.ORACLE_CLIENT})"
                     " doesn't exist. Please enter a valid directory for the"
                     " Oracle instant client.")
                u.log(s)
                raise Exception(s)
            cx.init_oracle_client(cfg.ORACLE_CLIENT)
            u.log("Client Oracle initialised")
