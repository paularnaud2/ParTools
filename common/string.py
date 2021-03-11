import re

from math import floor
from time import time
from common import g


def like(in_str, like_string):
    # Oracle equivalent of LIKE operator but with '*' instead of '%'
    # Outputs boolean str LIKE like_string
    # Example: like('Hello World', 'He*o w*d') => True

    if '*' not in like_string:
        return like_string in in_str

    like_string = re.escape(like_string)
    like_string = like_string.replace(r'\*', '(.*)')
    m = re.search(like_string, in_str)
    out = False
    if m:
        out = True

    return out


def get_duration_ms(start_time, end_time=''):
    if end_time == '':
        end_time = time()

    duration = floor((end_time - start_time) * 1000)

    return duration


def get_duration_string(start_time, return_dms=False, end_time=''):
    dms = get_duration_ms(start_time, end_time)
    if dms >= 1000:
        duration_s = dms / 1000
        if duration_s > 60:
            duration_m = duration_s // 60
            duration_s = duration_s % 60
            dm = str(floor(duration_m))
            ds = str(floor(duration_s))
            dstr = f"{dm} minutes and {ds} seconds"
        else:
            dstr = str(duration_s) + " seconds"
    else:
        dstr = str(dms) + " ms"

    if return_dms:
        return (dms, dstr)
    return dstr


def big_number(str_in):
    s = str(str_in)
    position = len(s)
    counter = 0
    out = ''
    while position != 0:
        counter += 1
        position -= 1
        out = s[position] + out
        if counter % 3 == 0 and position != 0:
            out = " " + out
    return (out)


def replace_from_dict(str_in, dict_in):
    for key in dict_in:
        str_in = str_in.replace(g.VAR_DEL + key + g.VAR_DEL, dict_in[key])
    return str_in
