import os
import os.path as p
from shutil import rmtree

from .log import log
from .string import like


def startfile(in_path):
    """Same as os.startfile but with absolute path (more robust)"""

    os.startfile(p.abspath(in_path))


def delete_folder(dir):
    """Deletes a folder and its content"""

    if p.exists(dir):
        rmtree(dir)
        log(f"Folder {dir} deleted")


def mkdirs(dir, delete=False):
    """Same as os.makedirs but with a 'delete' option which (if True) deletes
    the folder if it already exists."""

    if p.exists(dir) and not delete:
        return
    if p.exists(dir) and delete:
        delete_folder(dir)
    os.makedirs(dir)
    log(f"Folder {dir} created")


def abspath(path):
    """Same as os.path.abspath but with '/' instead of '\'"""

    out = p.abspath(path).replace('\\', '/')
    return out


def append_file(in_path, out_path, remove_header=False):
    """Appends the 'in_path' file to the 'out_path' file.

    - remove_header: if True, the header of the 'in_path' file is removed
    - before appending
    """

    with open(in_path, 'r', encoding='utf-8') as in_file:
        with open(out_path, 'a', encoding='utf-8') as out_file:
            i = 0
            for line in in_file:
                i += 1
                if remove_header and i == 1:
                    pass
                else:
                    out_file.write(line)


def list_files(in_dir,
               incl_root=True,
               walk=False,
               only_list=[],
               ignore_list=[]):
    """Lists the files of the 'in_dir' directory

    - incl_root: if True, the root is included in each paths (absolute paths)
    - walk: if True, the files of all the subdirectories are listed as well
    - only_list: list of wanted patterns. e.g. ['*.py'] (only these patterns will be output)
    - ignore_list: list of unwanted patterns. e.g. ['*.pyc'] (these patterns won't be output)
    """

    if not p.exists(in_dir):
        return []

    out = []
    for root, dir, files in os.walk(in_dir):
        root = root.strip('/')
        for file in files:
            r = root.replace('\\', '/') + '/' if incl_root else ''
            cur_path = f'{r}{file}'
            if only(cur_path, only_list) and not ignore(cur_path, ignore_list):
                out.append(cur_path)
        if not walk:
            break

    out.sort()
    return out


def only(path, only_list):
    if not only_list:
        return True

    for elt in only_list:
        if like(path, f'{elt}'):
            return True
    return False


def ignore(path, ignore_list):
    for elt in ignore_list:
        if like(path, f'{elt}'):
            return True
    return False


def load_txt(in_path, list_out=True):
    """Loads a text file

    - list_out: if True, a list es output, each element representing a line a the file. If False, a string is output.
    """

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


def save_list(in_list, out_path, att='w'):
    """Saves a list in a file, each element representing a line"""

    with open(out_path, 'w', encoding='utf-8') as out_file:
        for i, elt in enumerate(in_list):
            s = str(elt).strip("\n")
            if i == 0:
                out_file.write(s)
            else:
                out_file.write('\n' + s)


def count_lines(in_path):
    """Counts the number of lines of a file"""

    with open(in_path, 'r', encoding='utf-8') as in_file:
        i = 0
        for line in in_file:
            i += 1

    return i
