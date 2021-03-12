import subprocess

from common import g
from .log import log
from .log import log_print
from win10toast import ToastNotifier


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
    if 'MD' in params:
        if 'LOG_FILE' in params['MD']:
            g.LOG_FILE_INITIALISED = True
            g.LOG_FILE = params['MD']['LOG_FILE']

    if len(params) > 0:
        log(f"Initialising parameters: {params}")
        for key in params:
            mod.__getattribute__(key)
            mod.__setattr__(key, params[key])


def run_cmd(cmd, input=''):
    # input variable is used in the case the command expects the user
    # to input something (e.g. Y or N). In this case, a binary
    # string should be used (e.g. b'Y')

    a = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        input=input,
    )
    returncode = a.returncode
    log(f"Shell run over (return code: {returncode}). Shell output:")

    if returncode in [0, 2]:
        out = a.stdout.decode("utf-8", errors="ignore")
        log_print(out)
        return True
    else:
        err = a.stderr.decode("utf-8", errors="ignore")
        log_print(err)
        return False


def run_sqlplus(script):

    p = subprocess.Popen(
        'sqlplus / as sysdba',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    (stdout, stderr) = p.communicate(script.encode('utf-8'))

    out = stdout.decode('cp1252', errors="ignore")
    # out = stdout.decode('cp850', errors="ignore")

    print(out)
