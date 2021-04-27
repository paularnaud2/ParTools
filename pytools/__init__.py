from os.path import realpath
from os.path import exists

if exists('conf_perso.py'):
    import conf_perso as cfg
else:
    import conf as cfg
