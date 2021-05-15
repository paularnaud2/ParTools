from . import g
from .log import log


def list_to_dict(list_in, separator='='):
    """Transforms 'list_in' to a dictionary using the 'separator'"""

    out = {}
    for elt in list_in:
        e = elt.split(separator)
        out[e[0]] = e[1]
    return out


def init_kwargs(mod, kwargs):
    """Initializes the gl (global) variables of the module 'mod' with the 'kwargs'
    dictionary (kwargs of a main package function such as sql.download)
    """

    if 'MD' in kwargs:
        if kwargs['MD'] is not None:
            if 'LOG_PATH' in kwargs['MD']:
                g.log_file_initialised = True
                g.log_path = kwargs['MD']['LOG_PATH']

    if len(kwargs) > 0:
        kwargs_log = {
            key: str(value)[:g.MAX_LOG_VAR_CHAR]
            for (key, value) in kwargs.items()
        }
        log(f"Initialising parameters: {kwargs_log}")
        for key in kwargs:
            mod.__getattribute__(key)
            mod.__setattr__(key, kwargs[key])