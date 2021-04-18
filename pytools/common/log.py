import sys
import warnings
import os.path as p

from time import time
from datetime import datetime

from . import g
from . import file
from . import string


def write_log(str_in):
    if not g.LOG_OUTPUT or not g.LOG_FILE_INITIALISED:
        return

    s = str(str_in)
    with open(g.dirs['LOG'] + g.LOG_FILE, 'a', encoding='utf-8') as in_file:
        in_file.write(s + '\n')


def check_log(in_list, log_match=False):

    log('check_log...')
    lp = g.dirs['LOG'] + g.LOG_FILE
    txt = file.load_txt(lp, False)
    n_w = 0
    for elt in in_list:
        m = string.like(txt, elt)
        if not m:
            n_w += 1
            s = f"Expression '{elt}' couldn't be found in log file {lp}"
            log(s, c_out=False)
            warnings.warn(s)
        elif str(m) != 'True' and log_match:
            log_print(m)

    if n_w == 0:
        log('check_log ok')
    else:
        log(f'check_log ko ({n_w} warnings)')


def log_print(str_in='', nb_tab=0, c_out=True):
    if nb_tab != 0:
        for i in range(0, nb_tab):
            str_in = '\t' + str_in

    with g.verrou:
        if c_out:
            print(str_in)
        write_log(str_in)


def log(str_in, level=0, print_date=False, nb_tab=0, c_out=True):
    if g.LOG_LEVEL < level:
        return

    if print_date:
        s = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        s = datetime.now().strftime("%H:%M:%S")
    s = s + " - " + str(str_in)
    log_print(s, nb_tab, c_out)


def init_log(parent_module='', force_init=False):
    if g.LOG_FILE_INITIALISED and not force_init:
        return

    s = datetime.now().strftime("%Y%m%d_%H%M%S")
    if parent_module:
        s += '_' + parent_module
    g.LOG_FILE = s + '.txt'
    with open(g.dirs['LOG'] + g.LOG_FILE, 'w', encoding='utf-8') as in_file:
        in_file.write('')

    g.LOG_FILE_INITIALISED = True
    log_path = g.dirs['LOG'] + g.LOG_FILE
    log_path = p.abspath(log_path)
    s = f"Log file initialised ({log_path})"
    log(s, print_date=True)
    log_print("Python version: " + sys.version)
    log_print()


def step_log(counter, step, what='lines written', nb=0, th_name='DEFAULT'):
    # For a simple use, initialise with init_sl_time()
    # For multi_thread use, initialise with gen_sl_detail(rg_name)

    if counter % step != 0:
        return False

    try:
        detail = g.sl_detail[th_name]
    except KeyError:
        detail = ''

    st = g.sl_time_dict[th_name]
    dstr = string.get_duration_string(st)
    bn_1 = string.big_number(step)
    bn_2 = string.big_number(counter)
    if nb == 0:
        s = "{bn1} {what} in {dstr}. {bn2} {what} in total{detail}."
        s = s.format(bn1=bn_1, bn2=bn_2, dstr=dstr, what=what, detail=detail)
    else:
        bn_3 = string.big_number(nb)
        s = what.format(bn_1=bn_1, dstr=dstr, bn_2=bn_2, bn_3=bn_3)

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


def gen_sl_detail(q_name='', th_nb=1, multi_th=False):

    th_name = str(q_name) + '_' + str(th_nb)

    if q_name not in ['', 'MONO'] and multi_th is True:
        detail = f" for query '{q_name}' (connection no. {th_nb})"
    elif q_name not in ['', 'MONO']:
        detail = f" for query '{q_name}'"
    elif multi_th is True:
        detail = f" (thread no. {th_nb})"
    else:
        detail = ''

    with g.verrou:
        g.sl_detail[th_name] = detail

    init_sl_time(th_name)
    return th_name


def log_array(array, nb_tab=0):
    for elt in array:
        log_print(elt, nb_tab)


def log_example(list_in, what="duplicates"):
    if not list_in:
        return

    log_print(f"Examples of {what} (limited to {g.MAX_EXAMPLE_PRINT}):")
    log_array(list_in[:g.MAX_EXAMPLE_PRINT])
