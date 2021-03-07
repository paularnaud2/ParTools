from win10toast import ToastNotifier
from common import g
from .log import log


def send_notif(msg, package='common', jdur=0, ndur=10):

    if jdur != 0:
        jdur = jdur / 1000
        if jdur < g.MIN_DUR_NOTIF_TRIGGER:
            return

    toaster = ToastNotifier()
    toaster.show_toast(
        "Python - " + package,
        msg,
        duration=ndur,
        threaded=True,
    )
    log("Windows notification sent")


def list_to_dict(list_in, separator='='):
    out = {}
    for elt in list_in:
        e = elt.split(separator)
        out[e[0]] = e[1]
    return out


def init_params(mod, params):
    if len(params) > 0:
        log(f"Initialising parameters: {params}")
        for key in params:
            mod.__getattribute__(key)
            mod.__setattr__(key, params[key])

    if 'MD' in params:
        if 'LOG_FILE' in mod.MD:
            g.LOG_FILE_INITIALISED = True
            g.LOG_FILE = mod.MD['LOG_FILE']
