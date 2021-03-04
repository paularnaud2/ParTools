from common import g
from .log import log


def send_notif(msg, package='common', t=0, dur=10):

    if t != 0:
        t = t / 1000
        if t < g.MIN_DUR_NOTIF_TRIGGER:
            return

    try:
        from win10toast import ToastNotifier
    except ModuleNotFoundError:
        s = "Échec de l'envoi de la notification windows."
        s += " Le module win10toast n'est pas installé."
        log(s)
        return

    toaster = ToastNotifier()
    toaster.show_toast("Python - " + package, msg, duration=dur, threaded=True)
    log("Notification Windows envoyée")


def list_to_dict(list_in, separator='='):
    out = {}
    for elt in list_in:
        e = elt.split(separator)
        out[e[0]] = e[1]
    return out


def init_params(mod, params):
    if len(params) > 0:
        log(f"Initialisation des paramètres : {params}")
        for key in params:
            mod.__getattribute__(key)
            mod.__setattr__(key, params[key])

    if 'MD' in params:
        if 'LOG_FILE' in mod.MD:
            g.LOG_FILE_INITIALISED = True
            g.LOG_FILE = mod.MD['LOG_FILE']
