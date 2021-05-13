import sys
import warnings

from time import time
from datetime import datetime

from . import g
from . import file
from . import string


def write_log(str_in):

    s = str(str_in)
    g.logs.append(s)
    if not g.log_file_initialised:
        return
    with open(g.log_path, 'a', encoding='utf-8') as in_file:
        in_file.write(s + '\n')


def check_log(in_list, log_match=False):
    """Checks whether the current log file contains the 'in_list' elements.
    If it doesn't, a warning is thrown.

    Args (non-exhaustive)
    ----------------------
    log_match: If True, the matches are printed out in the log file
    """

    log('check_log...')
    txt = file.load_txt(g.log_path, False)
    n_w = 0
    for elt in in_list:
        m = string.like(txt, elt)
        if not m:
            n_w += 1
            s = f"Expression '{elt}' couldn't be found in log file {g.log_path}"
            log(s, c_out=False)
            warnings.warn(s)
        elif str(m) != 'True' and log_match:
            log_print(m)

    if n_w == 0:
        log('check_log ok')
    else:
        log(f'check_log ko ({n_w} warnings)')


def log_print(str_in='', nb_tab=0, c_out=True, dashes=0):
    """Prints something in the current log file (g.log_path)

    Args (non-exhaustive)
    ----------------------
    nb_tab: Number of tab indentations

    c_out: Console out

    dashes: Total length of the input string extended
    with dashes ('-')
    """

    s = str_in
    if nb_tab != 0:
        for i in range(0, nb_tab):
            s = '\t' + s

    if dashes > 0:
        s = string.extend_str(s, '-', dashes)

    with g.verrou:
        if c_out:
            print(s)
        write_log(s)


def log(str_in, level=0, format='%H:%M:%S -', c_out=True):
    """Logs 'str_in' in the current log file (g.log_path)

    Args (non-exhaustive)
    ----------------------
    level: Log level. Current log level set in g.LOG_LEVEL.
    Nothing will be logged if g.LOG_LEVEL < level

    format: Log format

    c_out: Console output
    """

    if g.LOG_LEVEL < level:
        return

    fdate = datetime.now().strftime(format)
    s = f"{fdate} {str_in}"
    log_print(s, c_out=c_out)


def init_log(parent_module='', force_init=False):
    """Initialises a log file

    Args (non-exhaustive)
    ----------------------
    parent_module: Name of the parent module (appears in the
    name of the log file)

    force_init: If True, the log file is initialised even if a
    current log file is already set
    """

    if g.log_file_initialised and not force_init:
        return

    s = datetime.now().strftime('%Y%m%d_%H%M%S')
    if parent_module:
        s += '_' + parent_module
    g.log_path = file.abspath(g.dirs['LOG'] + s + '.txt')
    with open(g.log_path, 'w', encoding='utf-8') as in_file:
        in_file.write('')
    g.logs = []
    g.log_file_initialised = True
    s = f"Log file initialised ({g.log_path})"
    log(s, format='%Y-%m-%d %H:%M:%S -')
    log_print("Python version: " + sys.version)
    log_print()


def step_log(counter, step, what='lines written', nb=0, th_name='DEFAULT'):
    """Logs something only when the 'counter' is a multiple of 'step'

    For simple use, initialise with init_sl_time()

    For multithreaded use, initialise with gen_sl_detail(q_name)

    For more info, check out the README.md file
    """

    if counter % step != 0:
        return False

    detail = g.sl_detail[th_name] if th_name in g.sl_detail else ''
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


def init_sl_time(th_name='DEFAULT'):
    """Initialises the timer for the step_log function (simple use)"""

    with g.verrou:
        g.sl_time_dict[th_name] = time()


def gen_sl_detail(q_name='', th_nb=1, multi_th=False):
    """Initialises the timer for the step_log function (multithread use)"""

    if q_name not in ['', 'MONO'] and multi_th is True:
        detail = f" for query '{q_name}' (connection no. {th_nb})"
    elif q_name not in ['', 'MONO']:
        detail = f" for query '{q_name}'"
    elif multi_th is True:
        detail = f" (thread no. {th_nb})"
    else:
        detail = ''

    th_name = f'{q_name}_{th_nb}'
    with g.verrou:
        g.sl_detail[th_name] = detail

    init_sl_time(th_name)
    return th_name


def log_input(str_in):
    """Same as input but traced in the log file"""

    command = input(str_in)
    write_log(str_in + command)

    return command


def log_array(array, nb_tab=0):
    for elt in array:
        log_print(elt, nb_tab)


def log_dict(dict):
    for key in dict:
        log_print(f'{key}: {dict[key]}')


def log_example(list_in, what="duplicates"):
    if not list_in:
        return

    log_print(f"Examples of {what} (limited to {g.MAX_EXAMPLE_PRINT}):")
    log_array(list_in[:g.MAX_EXAMPLE_PRINT])
