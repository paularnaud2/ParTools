import os
import os.path as p
from shutil import rmtree

from .log import log


def startfile(in_path):
    # Same as os.startfile but with absolute path (more robust)
    os.startfile(p.abspath(in_path))


def delete_folder(dir):
    if p.exists(dir):
        rmtree(dir)
        log(f"Folder {dir} deleted")


def mkdirs(dir, delete=False):
    if p.exists(dir) and not delete:
        return
    if p.exists(dir) and delete:
        delete_folder(dir)
    os.makedirs(dir)
    log(f"Folder {dir} created")


def merge_files(in_path, out_path, remove_header=False):
    with open(in_path, 'r', encoding='utf-8') as in_file:
        with open(out_path, 'a', encoding='utf-8') as out_file:
            i = 0
            for line in in_file:
                i += 1
                if remove_header and i == 1:
                    pass
                else:
                    out_file.write(line)


def get_file_list(in_path):
    try:
        dirs = os.listdir(in_path)
        file_list = [f for f in dirs if p.isfile(p.join(in_path, f))]
    except FileNotFoundError:
        return []

    file_list.sort()
    return file_list


def load_txt(in_path, list_out=True):
    if list_out:
        out = []
    else:
        out = ''

    with open(in_path, 'r', encoding='utf-8') as in_file:
        for line in in_file:
            if list_out:
                out.append(line.strip('\n'))
            else:
                out += line

    return out


def count_lines(in_path):
    with open(in_path, 'r', encoding='utf-8') as in_file:
        i = 0
        for line in in_file:
            i += 1

    return i


def save_list(list, out_path, att='w'):
    with open(out_path, 'w', encoding='utf-8') as out_file:
        for elt in list:
            out_file.write(str(elt).strip("\n") + '\n')
