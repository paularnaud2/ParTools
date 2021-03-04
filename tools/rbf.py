from common import *
import tools.gl as gl

""
LINE_PER_LINE = True
IN_FILE = 'C:/Py/IN/Extract_LTE_GKO_20200814.csv'
N_READ = 30
""
"""
LINE_PER_LINE = True
IN_FILE = 'C:/Py/IN/Tests/R04'
N_READ = 30
"""
"""
LINE_PER_LINE = False
IN_FILE = 'C:/Py/IN/Tests/C01.xml'
BUFFER_SIZE = 150
N_READ = 30
"""
"""
LINE_PER_LINE = False
IN_FILE = 'C:/Py/IN/Tests/test_sbf_buf.xml'
BUFFER_SIZE = 10
N_READ = 5
"""


def read_big_file():

    init()

    with open(IN_FILE, 'r', encoding='utf-8', errors='ignore') as in_file:

        line = read_file(in_file)
        print(line.strip("\n"))
        while line != "":
            line = read_file(in_file)
            print(line.strip("\n"))
            gl.counters["read"] += 1
            if check_counter(in_file):
                continue
            else:
                break

    log("Fin")


def read_file(in_file):

    if LINE_PER_LINE:
        line = in_file.readline()
    else:
        line = in_file.read(BUFFER_SIZE)
    gl.counters["main"] += 1

    return line


def check_counter(in_file):

    if gl.counters["read"] % N_READ == 0:
        command = input(gl.txt["prompt"])
        print("")
        if len(command) > 0:
            if command == 'q':
                return False
            if command == 'f':
                goto_eof(in_file)
            if command[0].isdigit():
                skip(command, in_file)

    return True


def goto_eof(in_file):

    line = read_file(in_file)
    while line != "":
        line = read_file(in_file)

    bn = big_number(gl.counters["main"] - 1)
    if LINE_PER_LINE:
        s = "Fin du fichier atteint. {} lignes parcourues."
        s = s.format(bn)
    else:
        s = "Fin du fichier atteint. {} buffers de {} caractères parcourus."
        s = s.format(bn, BUFFER_SIZE)

    print(s.format(bn))


def skip(nb, in_file):

    i = 0
    while i < int(nb):
        i += 1
        read_file(in_file)


def init():

    log("Package tools - Lecture de fichier\n", print_date=True)

    gl.counters["main"] = 0
    gl.counters["read"] = 1

    txt = '\n' + "c -> continuer"
    txt += '\n' + "q -> quitter"
    txt += '\n' + "f -> aller à la fin du fichier"
    if LINE_PER_LINE:
        txt += '\n' + "ou entrer le nombre de lignes à passer"
    else:
        txt += '\n' + "ou entrer le nombre de buffers à passer"
    gl.txt["prompt"] = txt
