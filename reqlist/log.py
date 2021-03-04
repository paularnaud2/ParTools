import common as com
import reqlist.gl as gl


def start_exec(inst, th_nb):
    if inst != '':
        s = f"Exécution des requêtes pour {inst}..."
    elif gl.bools['MULTI_TH'] is True:
        s = f"Exécution des requêtes (thread No. {th_nb})..."
    else:
        s = "Exécution des requêtes..."
    com.log(s)


def gen_group_list(elt_list, group_list):
    bn1 = com.big_number(len(elt_list))
    bn2 = com.big_number(len(group_list))
    s = f"Liste des groupes construite : {bn1} éléments à traiter répartis"
    s += f" en {bn2} groupes ({gl.NB_MAX_ELT_IN_STATEMENT} max par groupe)"
    com.log(s)


def get_sql_array_finish(th_nb):
    n_rows = gl.counters[th_nb]
    s_th = ''
    if gl.MAX_DB_CNX > 1:
        s_th = f" pour le thread No.{th_nb}"
    if n_rows > 0:
        bn = com.big_number(n_rows)
        s = f"Résultat récupéré{s_th} ({bn} lignes exportées)"
        com.log(s)
    else:
        com.log(f"Aucune ligne récupéré{s_th}")
