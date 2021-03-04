from common import g
from .log import log
from os import listdir
from os import makedirs
from os.path import join
from os.path import isfile
from os.path import exists
from time import sleep
from shutil import rmtree


def delete_folder(dir):
    log(f"Suppression du dossier {dir}")
    rmtree(dir)
    sleep(g.SLEEP_AFTER_DELETE_FOLDER)
    log(f"Dossier {dir} supprimé")


def mkdirs(dir, delete=False):
    if exists(dir) and not delete:
        return
    if exists(dir) and delete:
        delete_folder(dir)
    log(f"Création du dossier {dir}")
    makedirs(dir)


def merge_files(in_dir, out_dir, remove_header=False):
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        with open(out_dir, 'a', encoding='utf-8') as out_file:
            i = 0
            for line in in_file:
                i += 1
                if remove_header and i == 1:
                    pass
                else:
                    out_file.write(line)


def get_file_list(in_dir):
    try:
        file_list = [f for f in listdir(in_dir) if isfile(join(in_dir, f))]
    except FileNotFoundError:
        return []

    file_list.sort()
    return file_list


def load_txt(in_dir, list_out=True):
    g.counters["txt_read"] = 0
    if list_out:
        out = []
    else:
        out = ''

    with open(in_dir, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            if list_out:
                out.append(line.strip('\n'))
            else:
                out += line
            g.counters["txt_read"] += 1

    return out


def count_lines(in_dir):
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        i = 0
        for line in in_file:
            i += 1

    return i


def save_list(list, out_file_dir):
    with open(out_file_dir, 'w', encoding='utf-8') as out_file:
        for elt in list:
            out_file.write(str(elt).strip("\n") + '\n')


def read_file(in_dir):
    with open(in_dir, 'r', encoding='utf-8') as in_file:
        txt = in_file.read()
    return txt
