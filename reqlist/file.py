import os
import common as com
import reqlist.gl as gl

from os.path import exists
from threading import RLock

verrou = RLock()


def gen_out_file():
    (file_list, out_file) = init_gen_out()
    i = 0
    for elt in file_list:
        i += 1
        cur_dir = gl.TMP_PATH + elt
        if i == 1:
            com.merge_files(cur_dir, out_file, remove_header=False)
        else:
            com.merge_files(cur_dir, out_file, remove_header=True)
        os.remove(cur_dir)

    s = f"Fusion et suppression terminées. Sortie enregistrée sous '{out_file}'"
    com.log(s)


def init_gen_out():
    file_list = com.get_file_list(gl.TMP_PATH)
    if gl.SQUEEZE_JOIN:
        out_file = gl.OUT_FILE
    else:
        out_file = gl.OUT_SQL

    if check_ec(file_list):
        return

    if exists(out_file):
        os.remove(out_file)

    s = f"Fusion et suppression de {len(file_list)} fichiers temporaires..."
    com.log(s)
    return (file_list, out_file)


def check_ec(file_list):
    for elt in file_list:
        if gl.EC in elt or gl.QN in elt:
            s = f"Elément inatendu trouvé dans les fichiers temporaire ({elt})"
            com.log(s)
            com.log_print("Abandon de la fusion des fichiers temporaires.")
            raise Exception(s)


def tmp_init(th_name, th_nb):
    with verrou:
        com.mkdirs(gl.TMP_PATH)
        path = gl.TMP_PATH + th_name + '{}' + gl.TMP_FILE_TYPE
        gl.tmp_file[th_name] = path.format('')
        gl.tmp_file[th_name + gl.EC] = path.format(gl.EC)
        gl.tmp_file[th_name + gl.QN] = path.format(gl.QN)

    if not init_qn(th_name, th_nb):
        return False

    return True


def tmp_update(res, th_name, query_nb, c):

    # On sauve un fichier QN avec qn à EC au cas où le
    # trt soit arrêté pendant l'écriture du fichier
    s = f"WRITING RES IN {gl.tmp_file[th_name + gl.EC]}"
    com.save_csv([s], gl.tmp_file[th_name + gl.QN])

    # Si c'est la première requête on crée le fichier
    # et on écrit le header
    if query_nb == 1:
        gen_header(c)
        com.save_csv([gl.header], gl.tmp_file[th_name + gl.EC])

    com.save_csv(res, gl.tmp_file[th_name + gl.EC], 'a')
    com.save_csv([str(query_nb)], gl.tmp_file[th_name + gl.QN])


def gen_header(c):
    with verrou:
        if gl.header == '':
            header = [elt[0] for elt in c.description]
            gl.header = header
            if gl.bools["EXPORT_INSTANCES"]:
                header.append('INSTANCE')


def tmp_finish(th_name):
    os.rename(gl.tmp_file[th_name + gl.EC], gl.tmp_file[th_name])
    os.remove(gl.tmp_file[th_name + gl.QN])


def init_qn(th_name, th_nb):
    pqn = gl.tmp_file[th_name + gl.QN]
    pec = gl.tmp_file[th_name + gl.EC]
    if exists(gl.tmp_file[th_name]):
        com.log(f"Le thread No.{th_nb} avait fini son execution")
        gl.TEST_RESTART = False
        return False
    elif exists(pqn):
        txt = com.load_txt(pqn)
        try:
            qn = int(txt[0])
        except Exception as e:
            s = f"Erreur lors de la reprise pour le thread {th_nb} : {str(e)}"
            com.log(s)
            if exists(pec):
                com.log(f"Suppression du fichier {pec}")
                os.remove(pec)
            qn = 0

        s = "Reprise du traitement à partir de "
        s += f"la requête No.{qn + 1} pour le thread No.{th_nb}"
        com.log(s)
        gl.TEST_RESTART = False
    else:
        qn = 0

    with verrou:
        gl.ec_query_nb[th_name] = qn

    return True
