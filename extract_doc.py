import pytools.utils as u

IN_DIRS = ['pytools', 'quickstart', 'tests']
OUT_PATH = 'doc.txt'


def main():

    out = []
    for in_dir in IN_DIRS:
        extract_doc_from_dir(in_dir, out)

    u.save_list(out, OUT_PATH)
    u.startfile(OUT_PATH)


def extract_doc_from_dir(in_dir, out):
    file_list = u.list_files(in_dir, walk=True, only_list=['*.py'])
    for i, file in enumerate(file_list, 1):
        extract_doc_from_file(file, out)


def extract_doc_from_file(path, out):
    out.append(path)
    out.append('-------------------------------------------------------------')
    x = u.load_txt(path)
    description = False
    for i, line in enumerate(x):
        if '#' in line or u.like(line, '*"""*"""*'):
            line = line.replace('#', '').strip()
            line = line.replace('"""', '').strip()
            out.append(line)
            continue
        if '"""' in line and description is False:
            line = line.replace('"""', '').strip()
            description = True
            out.append(line)
            continue
        if '"""' in line and description is True:
            line = line.replace('"""', '').strip()
            description = False
            out.append(line)
            continue
        if description is True:
            out.append(line)
    out.append('-------------------------------------------------------------')
    out.append('')
    out.append('')


main()