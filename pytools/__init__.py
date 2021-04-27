from os.path import realpath
from os.path import exists

if exists('pytools/conf_perso.py'):
    import pytools.conf_perso as cfg
else:
    import pytools.conf as cfg
