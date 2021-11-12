import time
import os.path as p

import partools.utils as pt
from sel import cfg

from . import g
from . import functions as f


def init_main(func):
    start_time = time.time()
    if not g.start_time:
        g.start_time = start_time

    f.set_main_start_time()

    g.main = func.__name__

    if not pt.g.log_file_initialised:
        pt.init_log(func.__name__)
    f.print_version()
    pt.log(f"[{func._name__}] start")
    g.dir = g.path = f"{g.OUT_DIR}{g.main}/"
    pt.mkdirs(g.dir, cfg.TEST and not cfg.SKIP_LOAD)
    pt.log_print('|')

    return start_time


def init_check(kwargs):

    start_time = time.time()
    g.all_sub_check_ok = True
    start_log = len(pt.g.logs)

    g.env = kwargs['env']
    g.path = f"{g.dir}{g.env}"
    g.check = kwargs['name'] if 'name' in kwargs else g.main
    g.check_key = f'{g.check}_{g.env}'
    g.sum[g.check_key] = {cfg.CHECK_LABEL: g.check}
    g.sum[g.check_key]['Env'] = g.env
    g.sum[g.check_key]['Result'] = 'Failed'
    pt.log(f"[{g.check_key}] start")

    return start_time, start_log


def finish_check(start_time, start_log, passed=True):

    s = f" for {g.env}"
    if passed and g.all_sub_check_ok:
        g.sum[g.check_key]['Result'] = 'Passed'
        pt.log(f"{cfg.CHECK_LABEL} '{g.check}'OK{s}")
    else:
        g.sum[g.check_key]['Result'] = 'Failed'
        pt.log(f"{cfg.CHECK_LABEL} {g.check} NOK{s}")

    dstr = pt.get_duration_string(start_time)
    g.main_dur = pt.get_duration_string(g.start_time)
    pt.log(f"[{g.check_key}] end ({dstr})")
    g.sum[g.check_key]['Duration'] = dstr

    check_log = pt.g.logs[start_log:]
    path = g.path + 'LOG.txt'
    pt.mkdirs(g.dir)
    pt.save_list(check_log, path)

    g.sum[g.check_key]['log'] = p.abspath(path)
    if g.s_dir:
        g.sum[g.check_key]['Screenshots'] = p.abspath(g.s_dir)
        g.s_dir = ''
    else:
        g.sum[g.check_key]['Screenshots'] = ''

    pt.log_print('|')
    g.env = ''
    g.check = ''
    g.check_key = ''


def init_sub_check(func, kwargs):

    start_time = time.time()

    if 'name' in kwargs:
        g.sub_check = kwargs['name']
    else:
        g.sub_check = func.__name__.replace('sub_check_', '')
    g.sub_check = f'{g.check}_{g.sub_check}'
    g.sub_check_key = f'{g.sub_check}{g.env}'
    g.sub_sum[g.sub_check_key] = {cfg.SUBCHECK_LABEL: g.sub_check}
    g.sub_sum[g.sub_check_key]['Env'] = g.env
    g.sub_sum[g.sub_check_key]['Result'] = 'Failed'
    pt.log(f"[{g.sub_check_key}] start")

    return start_time


def finish_sub_check(start_time, passed=True):

    s = f" for {g.env}"
    if passed:
        g.sub_sum[g.sub_check_key]['Result'] = 'Passed'
        pt.log(f"{cfg.SUBCHECK_LABEL} '{g.sub_check}' OK{s}")
    else:
        g.sub_sum[g.sub_check_key]['Result'] = 'Failed'
        pt.log(f"{cfg.SUBCHECK_LABEL} '{g.sub_check}' NOK{s}")
        g.all_sub_check_ok = False

    dstr = pt.get_duration_string(start_time)
    pt.log(f"[{g.sub_check_key}] end ({dstr})")
    g.sub_sum[g.sub_check_key]['Duration'] = dstr

    pt.log_print('|')
    g.sub_check = ''
    g.sub_check_key = ''
