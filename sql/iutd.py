import sys
import common as com

from datetime import datetime
from os.path import exists
from sql import gl


def is_up_to_date(cnx):
    if not gl.TEST_IUTD:
        if gl.DB not in gl.IUTD_LIST or gl.iutd:
            return

    com.log(f"Vérification is up to date (IUTD) pour la BDD {gl.DB}")
    d_now = datetime.now().strftime("%Y/%m/%d")
    if iutd_file(d_now):
        return

    iutd_db(d_now, cnx)


def iutd_db(d_now, cnx):
    d_bdd = get_bdd_date(cnx)
    com.save_csv([d_bdd], gl.IUTD_DIR)
    com.log(f"Fichier de vérification sauvegardé à l'adresse {gl.IUTD_DIR}")
    compare_dates(d_bdd, d_now)
    gl.iutd = True


def iutd_file(d_now):
    if exists(gl.IUTD_DIR):
        d_old = com.load_txt(gl.IUTD_DIR)[0]
        if d_now == d_old:
            gl.iutd_ok = True
            com.log("Vérification IUTD OK")
            return True
        else:
            com.log_print('|')
            s = "La date trouvée dans le fichier ne correspond pas à la date du jour"
            com.log(s)
            return False
    else:
        com.log_print('|')
        com.log("Fichier de vérification IUTD introuvable")
        return False


def compare_dates(d_bdd, d_now):
    if d_bdd == d_now:
        com.log("Vérification IUTD OK")
    else:
        s = f"Attention : les confs de la BDD {gl.DB} semblent"
        s += " ne pas être à jour :"
        s += f"\nDate BDD : {d_bdd}"
        s += f"\nDate du jour : {d_now}"
        s += "\nContinuer ? (o/n)"
        if gl.TEST_IUTD:
            com.log_print(s)
            com.log_print('o (TEST_IUTD = True)')
        elif com.log_input(s) == 'n':
            sys.exit()

    com.log_print('|')


def get_bdd_date(cnx):

    c = cnx.cursor()
    query = get_iutd_query()
    com.log("Exécution de la requête IUTD : ")
    com.log_print(query)
    c.execute(query)
    com.log("Requête exécutée")
    out = c.fetchone()
    out = str(out[0]).replace('-', '/')
    out = out[:10]

    return out


def get_iutd_query():
    if gl.TEST_IUTD:
        query = com.read_file(f"{gl.QUERY_PATH}IUTD_TEST.sql")
    else:
        query = com.read_file(f"{gl.QUERY_PATH}IUTD_{gl.DB}")

    return query
