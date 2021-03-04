import sys
import common as com
import qdd.gl as gl
from qdd.init import init_stf
from qdd.init import init_msf
from qdd.gstf import gen_sorted_temp_files
from qdd.functions import temp_files
from qdd.functions import array_list_not_void
from qdd.fill_al import fill_array_list
from qdd.empty_al import empty_array_list


def sort_file(in_file_dir, out_file_dir, prompt=False, nb=0):
    # La variable nb sert à différentier les fichiers
    # de sortie dans le cadre de qdd

    com.log(f"Début du tri de '{in_file_dir}'.")
    init_stf(in_file_dir, out_file_dir)
    gen_sorted_temp_files(in_file_dir, out_file_dir)
    com.log_print('|')
    nb_files = gl.counters["file"]
    if nb_files > 1:
        s = f"Tri multiple (sur {nb_files} fichiers)"
        s += " et écriture du fichier de sortie en cours..."
        com.log(s)
        merge_sorted_files(out_file_dir)
    finish(out_file_dir, prompt, nb)
    com.log_print('|')


def merge_sorted_files(out_file_dir):

    init_msf()
    while temp_files() or array_list_not_void():
        fill_array_list()
        empty_array_list(out_file_dir)


def finish(out_file_dir, prompt, nb):

    n_dup_key = len(gl.dup_key_list)
    n_dup = len(gl.dup_list)
    bn1 = com.big_number(gl.counters["tot_written_lines_out"])
    bn2 = com.big_number(n_dup)
    s = f"Tri terminé. Fichier de sortie {out_file_dir} généré avec succès"
    s += f"({bn1} lignes écrites, {bn2} doublons écartés)"
    com.log(s)
    if n_dup > 0:
        if nb != 0:
            out_dup = gl.OUT_DUP_FILE + str(nb) + gl.FILE_TYPE
        else:
            out_dup = gl.OUT_DUP_FILE + gl.FILE_TYPE
        com.save_csv(gl.dup_list, out_dup)
        s = "Liste des doublons écrite dans le fichier '{}'"
        s += "\nExemples de doublons (limités à {}) :"
        com.log(s.format(out_dup, gl.MAX_DUP_PRINT))
        com.log_array(gl.dup_list[:gl.MAX_DUP_PRINT])
    if n_dup_key > 0:
        if prompt:
            prompt_dup_key(n_dup_key)
        else:
            com.save_csv(gl.dup_key_list, gl.OUT_DUP_KEY_FILE)
            s = "{} doublons de clé trouvés. Liste écrite dans le fichier '{}'"
            com.log(s.format(n_dup_key, gl.OUT_DUP_KEY_FILE))


def prompt_dup_key(n_dup_key):

    com.log_print('|')
    bn = com.big_number(n_dup_key)
    s = f"Attention : {bn} lignes différentes mais avec la même clé de"
    s += " recherche ont été identifiées."
    s += f"\nExemples de doublons (limités à {gl.MAX_DUP_PRINT}) :"
    com.log_print(s)
    com.log_array(gl.dup_key_list[:gl.MAX_DUP_PRINT])

    s = "\nLa comparaison des fichiers ne va pas fonctionner correctement."
    s += "\na -> sauvegarder la liste des doublons et quitter"
    s += "\nb -> ne pas sauvegarder la liste des doublons et quitter"
    s += "\nc -> sauvegarder la liste des doublons et continuer"
    s += "\nd -> ne pas sauvegarder la liste des doublons et continuer"
    if gl.TEST_PROMPT_DK:
        com.log_print(s)
        com.log_print('c (TEST_PROMPT_DK = True)')
        command = 'c'
    else:
        command = com.log_input(s)
    com.log_print('|')
    if command == 'a':
        com.save_csv(gl.dup_key_list, gl.OUT_DUP_KEY_FILE)
        s = "Liste des doublons de clés écrite dans le fichier '{}'"
        com.log(s.format(gl.OUT_DUP_KEY_FILE))
        sys.exit()
    if command == 'b':
        sys.exit()
    if command == 'c':
        com.save_csv(gl.dup_key_list, gl.OUT_DUP_KEY_FILE)
        s = "Liste des doublons de clés écrite dans le fichier '{}'"
        com.log(s.format(gl.OUT_DUP_KEY_FILE))
