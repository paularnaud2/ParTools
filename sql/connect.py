import conf_main as cfg
import common as com
import sql.gl as gl
import sql.log as log
import cx_Oracle as cx

from conf_oracle import c
from threading import RLock
from sql.iutd import is_up_to_date

verrou = RLock()


def connect(ENV, DB):

    init_instant_client()
    cnx_str = c[(ENV, DB)]
    log.connect_init(ENV, DB, cnx_str)
    cnx = cx.connect(cnx_str)
    log.connect_finish(DB)
    is_up_to_date(cnx)

    return cnx


def gen_cnx_dict(DB, ENV, nb):

    init_instant_client()
    cnx_str = c[(ENV, DB)]
    gl.cnx_dict = dict()
    i = 1
    s = f"Création des connexions pour la BDD '{DB}' de l'environnement '{ENV}'"
    s += f" ({cnx_str})"
    com.log(s)
    while i <= nb:
        com.log(f'Connexion No. {i} en cours de création...')
        gl.cnx_dict[i] = cx.connect(cnx_str)
        is_up_to_date(gl.cnx_dict[i])
        com.log(f'Connexion No. {i} créée')
        i += 1


def init_instant_client():
    with verrou:
        if gl.client_is_init is False:
            com.log("Initialisation du client Oracle...")
            gl.client_is_init = True
            cx.init_oracle_client(cfg.ORACLE_CLIENT)
            com.log("Client Oracle initialisé")
