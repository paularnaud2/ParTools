import importlib.util as u
from os.path import exists


def load_module(name, path):

    spec = u.spec_from_file_location(name, path)
    mod = u.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


if exists('PTconf_perso.py'):
    cfg = load_module('cfg', 'PTconf_perso.py')
elif exists('PTconf.py'):
    cfg = load_module('cfg', 'PTconf.py')
else:
    import partools.conf as cfg

__version__ = '1.0.3'
GITHUB_LINK = 'https://github.com/paularnaud2/ParTools'
GITHUB_ISSUES = GITHUB_LINK + '/issues'

import partools.utils
