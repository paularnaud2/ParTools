from os.path import exists

if exists('PTconf_perso.py'):
    import PTconf_perso as cfg
elif exists('PTconf.py'):
    import PTconf as cfg
else:
    import pytools.conf as cfg
