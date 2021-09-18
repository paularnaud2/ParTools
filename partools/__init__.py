import os

print("CWD:", os.getcwd())


def load_module(name, path):
    # Importing this way is required to force a deployed executable to load
    # from actual file and not from a .pyc statis file generated during the build
    import importlib.util as u

    spec = u.spec_from_file_location(name, path)
    mod = u.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def overwrite_cfg():
    import partools.conf as cfg

    if os.path.exists('PTconf_perso.py'):
        super_path = 'PTconf_perso.py'
        PTconf = load_module('PTconf', super_path)
    elif os.path.exists('PTconf.py'):
        super_path = 'PTconf.py'
        PTconf = load_module('PTconf', super_path)
    else:
        return cfg

    print(PTconf)
    super = PTconf.__dict__
    default = cfg.__dict__
    var_list = []
    for key in super:
        A = key not in PTconf.__builtins__ and '__' not in key
        item = str(super[key])
        B = '<class' not in item and '<module' not in item
        if A and B:
            default[key] = super[key]
            var_list.append(key)
    if not var_list:
        return cfg

    print(f"partools/conf.py overwritten by {super_path}")
    for var in var_list:
        print(var, '=', getattr(cfg, var))
    return cfg


cfg = overwrite_cfg()
