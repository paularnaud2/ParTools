import sys

from common import g
from common import string
from time import time
from datetime import datetime


def write_log(str_in):
    if not g.LOG_OUTPUT or not g.LOG_FILE_INITIALISED:
        return

    s = str(str_in)
    with open(g.paths['LOG'] + g.LOG_FILE, 'a', encoding='utf-8') as in_file:
        in_file.write(s + '\n')


def log_print(str_in='', nb_tab=0):
    if nb_tab != 0:
        for i in range(0, nb_tab):
            str_in = '\t' + str_in

    with g.verrou:
        print(str_in)
        write_log(str_in)


def log(str_in, level=0, print_date=False, nb_tab=0):
    if g.LOG_LEVEL >= level:
        if print_date:
            s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            s = datetime.now().strftime("%H:%M:%S")
        s = s + " - " + str_in
        log_print(s, nb_tab)


def init_log(parent_module='', force_init=False):
    if g.LOG_FILE_INITIALISED and not force_init:
        return

    g.init_directories()

    s = datetime.now().strftime("%Y%m%d_%H%M%S")
    if parent_module:
        s += '_' + parent_module
    g.LOG_FILE = s + '.txt'
    with open(g.paths['LOG'] + g.LOG_FILE, 'w', encoding='utf-8') as in_file:
        in_file.write('')

    g.LOG_FILE_INITIALISED = True
    log_path = g.paths['LOG'] + g.LOG_FILE
    s = f"Fichier de log initialisé ({log_path})"
    log(s, print_date=True)
    log_print("Version Python : " + sys.version)
    log_print()


def step_log(counter, step, what='lignes écrites', nb=0, th_name='DEFAULT'):
    # Pour une utilisation simple, initialiser avec init_sl_time()
    # Pour une utilisation multi_thread, initialiser avec
    # gen_sl_detail(range_name)

    if counter % step != 0:
        return False

    try:
        detail = g.sl_detail[th_name]
    except KeyError:
        detail = ''

    st = g.sl_time_dict[th_name]
    duration_ms = string.get_duration_ms(st)
    ds = string.get_duration_string(duration_ms)
    bn_1 = string.big_number(step)
    bn_2 = string.big_number(counter)
    if nb == 0:
        s = "{bn1} {what} en {ds}. {bn2} {what} au total{detail}."
        s = s.format(bn1=bn_1, bn2=bn_2, ds=ds, what=what, detail=detail)
    else:
        bn_3 = string.big_number(nb)
        s = what.format(bn_1=bn_1, ds=ds, bn_2=bn_2, bn_3=bn_3)

    log(s)
    init_sl_time(th_name)

    return True


def log_input(str_in):
    command = input(str_in)
    write_log(str_in + command)

    return command


def init_sl_time(th_name='DEFAULT'):
    with g.verrou:
        g.sl_time_dict[th_name] = time()


def gen_sl_detail(range_name, th_nb=1, what='la plage', multi_thread=False):

    th_name = str(range_name) + '_' + str(th_nb)

    if range_name not in ['', 'MONO'] and multi_thread is True:
        detail = ' pour {} {} (thread No.{})'.format(what, range_name, th_nb)
    elif range_name not in ['', 'MONO']:
        detail = ' pour {} {}'.format(what, range_name)
    elif multi_thread is True:
        detail = ' (thread No.{})'.format(th_nb)
    else:
        detail = ''

    with g.verrou:
        g.sl_detail[th_name] = detail

    init_sl_time(th_name)
    return th_name


def log_array(array, nb_tab=0):
    for elt in array:
        log_print(elt, nb_tab)
