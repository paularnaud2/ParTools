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
    out.append(u.extend_str('', '-', 100))
    x = u.load_txt(path)
    description = False
    n_written = 0
    for i, line in enumerate(x):
        append = False
        if '#' in line or u.like(line, '*"""*"""*'):
            append = True
        elif '"""' in line and description is False:
            description = True
            append = True
        elif '"""' in line and description is True:
            description = False
            append = True
        elif description is True:
            append = True
        if append:
            line = line.strip()
            out.append(line)
            n_written += 1

    if n_written > 0:
        out.append(u.extend_str('', '-', 100))
        out.append('')
        out.append('')
    else:
        del out[-2:]


main()
