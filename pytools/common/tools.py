from . import g
from .log import log


def list_to_dict(list_in, separator='='):
    out = {}
    for elt in list_in:
        e = elt.split(separator)
        out[e[0]] = e[1]
    return out


def init_kwargs(mod, kwargs):
    if 'MD' in kwargs:
        if kwargs['MD'] is not None:
            if 'LOG_FILE' in kwargs['MD']:
                g.LOG_FILE_INITIALISED = True
                g.LOG_FILE = kwargs['MD']['LOG_FILE']

    if len(kwargs) > 0:
        kwargs_log = {
            key: str(value)[:g.MAX_LOG_VAR_CHAR]
            for (key, value) in kwargs.items()
        }
        log(f"Initialising parameters: {kwargs_log}")
        for key in kwargs:
            mod.__getattribute__(key)
            mod.__setattr__(key, kwargs[key])
