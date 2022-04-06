import re
import string
import random
import hashlib

from math import floor
from time import time

from . import g


def like(in_str, like_string, case_sensitive=True):
    """Behaves as the LIKE of Oracle SQL (you can match strings with wildcard
    character '*'). Returns the match object that you can access with the group
    function.

    Important note:
    If in_str is multiline and contains 'Hello World'
        - like(in_str, 'Hello World') returns True
        - like(in_str, 'Hel*ld') returns a match object
    If in_str is a one line string (no \n) and contains 'Hello World'
        - like(in_str, 'Hello World') returns True
        - like(in_str, 'Hel*ld') returns None
        - like(in_str, '*Hel*ld*') returns a match object

    Example:
    - m = like('Hello World', 'He*o w*d')
    - m.group(0) => 'Hello World'
    - m.group(1) => 'll'
    """

    if not case_sensitive:
        in_str = in_str.lower()
        like_string = like_string.lower()

    if '*' not in like_string:
        return like_string in in_str

    like_string = re.escape(like_string)
    like_string = like_string.replace(r'\*', '(.*)')
    if '\n' not in in_str:
        like_string = '^' + like_string + '$'
    m = re.search(like_string, in_str)

    return m


def like_list(in_str, like_list, case_sensitive=True):
    """Returns True if in_str matches (using the like function) one of the like_list elements.
    See the like function description for more details."""

    if not isinstance(like_list, list):
        raise Exception('like_list must be of type list')

    for elt in like_list:
        if like(in_str, elt, case_sensitive):
            return elt

    return False


def like_dict(in_str, like_dict, case_sensitive=True, skey=''):
    """Returns the key whose list elt matches (using the like_list function) in_str.
    See the like_list function description for more details."""

    if not isinstance(like_dict, dict):
        raise Exception('like_dict must be of type dict')

    for key in like_dict:
        item = like_dict[key] if not skey else like_dict[key][skey]
        if isinstance(item, str) and like(in_str, item, case_sensitive):
            return key
        if isinstance(item, list) and like_list(in_str, item, case_sensitive):
            return key

    return False


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

    - return_dms: if True, the duration in ms is also output: (dms, dstr).
    If False, only the duration string is output (dstr).
    """

    dms = get_duration_ms(start_time, end_time)
    if dms >= 1000:
        duration_s = dms / 1000
        if duration_s > 120:
            duration_m = duration_s // 60
            duration_s = duration_s % 60
            dm = str(floor(duration_m))
            ds = str(floor(duration_s))
            dstr = f"{dm} minutes and {ds} seconds"
        else:
            duration_s = floor(duration_s * 10) / 10
            dstr = str(duration_s) + " s"
    else:
        dstr = str(dms) + " ms"

    if return_dms:
        return (dms, dstr)
    return dstr


def big_number(int_in):
    """Converts a potentially big number into a lisible string.

    Example:
    - big_number(10000000) returns '10 000 000'.
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

    Example:
    - replace_from_dict('Hello @@VAR@@', {'VAR': 'world'}) returns 'Hello world'
    """

    for key in dict_in:
        str_in = str_in.replace(g.VAR_DEL + key + g.VAR_DEL, str(dict_in[key]))
    return str_in
