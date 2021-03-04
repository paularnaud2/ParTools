import os
import re
import sql.gl as gl
import common as com

from common import g
from shutil import move


def get_rg_file_name(in_str):
    exp = '(.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m = re.search(exp, in_str)
    exp_comment = '(.*-{2,}.*)' + g.VAR_DEL + '(RG_.*)' + g.VAR_DEL
    m_comment = re.search(exp_comment, in_str)
    if m and not m_comment:
        rg_file_name = m.group(2)
        return rg_file_name
    else:
        return ''


def gen_range_list(rg_file_name):
    if rg_file_name != '':
        gl.bools['RANGE_QUERY'] = True
        range_dir = gl.RANGE_PATH + rg_file_name + gl.FILE_TYPE
        range_list = com.load_txt(range_dir)
        s = "Requêtage par plage détecté. Requête modèle :\n{}\n;"
        com.log(s.format(gl.query))
    else:
        gl.bools['RANGE_QUERY'] = False
        range_list = ['MONO']

    return range_list


def restart(range_list):
    file_list = com.get_file_list(gl.TMP_PATH)
    a = len(file_list)
    if a == 0:
        return range_list

    if gl.bools['RANGE_QUERY'] is False and gl.DB != 'GINKO':
        com.mkdirs(gl.TMP_PATH, True)
        return range_list

    s = "Traitement en cours détecté. Tuer ? (o/n)"
    if gl.TEST_RESTART:
        com.log(s)
        com.log_print("n (TEST_RESTART = True)")
    elif com.log_input(s) == 'o':
        com.mkdirs(gl.TMP_PATH, True)
        return range_list

    list_out = modify_restart(range_list, file_list)
    com.log("Liste des plages modifiée.")
    return list_out


def modify_restart(range_list, file_list):
    # modifie la range liste en supprimant les éléments déjà
    # présents dans la file list.
    # on en profite pour supprimer les fichier EC qui pourront causer des pb

    list_out = []
    for elt in range_list:
        comp_elt = elt + gl.FILE_TYPE
        comp_elt_ec = elt + gl.EC + gl.FILE_TYPE
        if comp_elt not in file_list:
            list_out.append(elt)
        if comp_elt_ec in file_list:
            ec_path = gl.TMP_PATH + comp_elt_ec
            os.remove(ec_path)
            com.log("Fichier EC {} supprimé".format(ec_path))

    return list_out


def move_tmp_folder():

    gl.bools["MERGE_OK"] = False
    out_dir = gl.OUT_RG_DIR

    com.log(f"Création du dossier de sortie '{out_dir}'...")
    com.mkdirs(out_dir, True)
    com.log('Dossier de sortie créé')

    file_list = com.get_file_list(gl.TMP_PATH)
    n = len(file_list)
    com.log(f"Déplacement de {n} fichiers vers le dossier de sortie....")
    for elt in file_list:
        cur_dir = gl.TMP_PATH + elt
        target_dir = out_dir + elt
        move(cur_dir, target_dir)
    com.log('Fichers déplacés vers {}'.format(out_dir))


def merge_tmp_files():
    (file_list, out_file, return_bool) = init_merge()
    if return_bool:
        return
    i = 0
    for elt in file_list:
        i += 1
        cur_dir = gl.TMP_PATH + elt
        if i == 1:
            com.merge_files(cur_dir, out_file, remove_header=False)
        else:
            com.merge_files(cur_dir, out_file, remove_header=True)
        os.remove(cur_dir)

    com.log(
        "Fusion et suppression des {} fichiers temporaires terminée".format(
            len(file_list)))


def init_merge():
    gl.bools["MERGE_OK"] = True
    file_list = com.get_file_list(gl.TMP_PATH)
    out_file = gl.OUT_FILE
    if check_ec(file_list) or check_mono(file_list, out_file):
        return ('', '', True)

    if os.path.exists(out_file):
        os.remove(out_file)

    com.log("Fusion et suppression de {} fichiers temporaires...".format(
        len(file_list)))
    return (file_list, out_file, False)


def check_ec(file_list):
    for elt in file_list:
        if gl.EC in elt:
            s = "Fichier EC trouvé ({})."
            s += " Abandon de la fusion des fichiers temporaires."
            com.log(s.format(elt))
            gl.bools["MERGE_OK"] = False
            return True
    return False


def check_mono(file_list, out_file):
    if file_list == ['MONO' + gl.FILE_TYPE]:
        cur_dir = gl.TMP_PATH + file_list[0]
        move(cur_dir, out_file)
        return True
    return False
