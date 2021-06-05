import subprocess

from .log import log
from .log import log_print


def msg_box(msg, package='utils', dur=0, min_dur_trigger=30, threaded=True):
    """Opens a message box containing the 'msg' input string

    - dur: duration in ms. If input, this value is used to determine if the
    message box should pop out or not. The message box pops out only if
    dur >= min_dur_trigger. This can be useful if you want to use
    this function as an end-process notification but only wants to be notified
    when the process has taken a long enough time.

    - threaded: if true, the message box is open in a parallel process and the
    main script can continue (can be used as a end process notification)
    """
    from multiprocessing import Process
    from tkinter.messagebox import showinfo

    if dur != 0:
        dur = dur / 1000
        if dur < min_dur_trigger:
            return

    title = "Python - " + package
    if threaded:
        p = Process(target=showinfo, args=(title, msg))
        p.start()
    else:
        showinfo(title, msg)


def run_cmd(cmd, input=''):
    """Runs a Windows shell command

    - input: used in the case the command expects the user to input something
    (e.g. Y or N). In this case, a binary string should be used (e.g. b'Y')
    """

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
    """Connects to sqlplus as sysdba and runs the input 'script'"""

    p = subprocess.Popen(
        'sqlplus / as sysdba',
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    (stdout, stderr) = p.communicate(script.encode('utf-8'))

    out = stdout.decode('cp1252', errors="ignore")
    # out = stdout.decode('cp850', errors="ignore")

    log_print(out)
