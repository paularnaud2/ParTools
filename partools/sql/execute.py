from time import time

import partools.utils as u

from . import gl
from .init import init_gl
from .connect import connect
from .functions import get_final_script


@u.log_exeptions
def execute(**kwargs):
    """Executes a SQL script or a PL/SQL procedure on an Oracle DB

    See README.md for guidance

    See partools/quickstart/sql_execute.py for examples of use
    """

    u.log('[sql] execute: start')
    start_time = time()
    u.init_kwargs(gl, kwargs)
    init_gl()
    script = get_final_script(gl.SCRIPT_IN)
    cnx = connect()
    c = cnx.cursor()
    if gl.PROC:
        u.log("Executing proc:")
        u.log_print(script)
        c.execute(script)
        u.log("Proc executed")
    else:
        command_list = script.split(';\n')
        n = len(command_list)
        if command_list[n - 1]:
            command_list[n - 1] = command_list[n - 1].strip(';')
        else:
            command_list = command_list[:-1]
        for command in command_list:
            u.log("Executing command:")
            u.log_print(command)
            c.execute(command)
            u.log("Command executed")
    c.close()
    cnx.commit()
    cnx.close()

    dstr = u.get_duration_string(start_time)
    u.log(f"[sql] execute: end ({dstr})")
    u.log_print()
