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
