import re
import string
import random
import hashlib

from math import floor
from time import time

from . import g


def like(in_str, like_string, match_output=False):
    """Behaves as the LIKE of Oracle SQL (you can match strings with wildcard
    character '*')

    Args (non-exhaustive)
    ----------------------
    match_output: if True, the function returns the match

    Example
    -------
    like('Hello World', 'He*o w*d') => True
    """

    if '*' not in like_string:
        return like_string in in_str

    like_string = re.escape(like_string)
    like_string = like_string.replace(r'\*', '(.*)')
    if '\n' not in in_str:
        like_string = '^' + like_string + '$'
    m = re.search(like_string, in_str)
    if not m:
        return False

    return m.group(0)


def hash512(in_str, length=10):
    """Contrary to hash, this hash function is not randomised, meaning it
    always outputs the same string for the same input string"""

    out = hashlib.sha512(in_str.encode('utf-8')).hexdigest()[:length]
    return out


def gen_random_string(length=10):
    """Generates a random string (letters and digits) of length 'length'"""

    letters = string.ascii_letters
    digits = string.digits
    ln = letters + digits
    out = ''.join(random.choice(ln) for i in range(length))
    return out


def extend_str(str_in, char, length, left=False):
    """Extends the string 'str_in' to the length 'length' with the given 'char'"""

    s = str(str_in)
    while len(s) < length:
        s = char + s if left else s + char
    return s


def get_duration_ms(start_time, end_time=None):
    """Gives the duration in ms between 'end_time' and 'start_time'. If 'end_time'
    is not given, the current time is taken."""

    if not end_time:
        end_time = time()

    duration = floor((end_time - start_time) * 1000)

    return duration


def get_duration_string(start_time, return_dms=False, end_time=None):
    """Outputs a string representing the time elapsed between 'end_time' and
    'start_time'. If 'end_time' is not given, the current time is taken.

    Args (non-exhaustive)
    ----------------------
    return_dms: if True, the duration in ms is also output: (dms, dstr).
    If False, only the duration string is output (dstr).
    """

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
            duration_s = floor(duration_s * 10) / 10
            dstr = str(duration_s) + " seconds"
    else:
        dstr = str(dms) + " ms"

    if return_dms:
        return (dms, dstr)
    return dstr


def big_number(int_in):
    """Converts a potentially big number into a lisible string.

    Example
    -------
    big_number(10000000) returns '10 000 000'.
    """

    s = str(int_in)
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
    """Replaces the variables (delimited by '@@') in 'str_in' with the values
    of 'dict_in'.

    Example
    -------
    replace_from_dict('Hello @@VAR@@', {'VAR': 'world'})
    returns 'Hello world'
    """

    for key in dict_in:
        str_in = str_in.replace(g.VAR_DEL + key + g.VAR_DEL, str(dict_in[key]))
    return str_in
