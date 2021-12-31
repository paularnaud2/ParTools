from . import g
from .log import log


def list_to_dict(list_in, separator='='):
    """Transforms 'list_in' to a dictionary using the 'separator'"""

    out = {}
    for elt in list_in:
        e = elt.split(separator)
        key = e[0].strip()
        value = elt[elt.find(separator) + 1:].strip()
        out[key] = value
    return out


def init_kwargs(mod, kwargs, max_n_char=100):
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
            key: str(value)[:max_n_char]
            for (key, value) in kwargs.items()
        }
        log(f"Initialising parameters: {kwargs_log}")
        for key in kwargs:
            mod.__getattribute__(key)
            mod.__setattr__(key, kwargs[key])
