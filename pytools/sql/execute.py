from time import time

import pytools.common as com

from . import gl
from .connect import connect
from .init import init
from .functions import get_final_script


@com.log_exeptions
def execute(**kwargs):
    com.log('[sql] execute: start')
    start_time = time()
    com.init_kwargs(gl, kwargs)
    init()
    script = get_final_script(gl.SCRIPT_IN)
    cnx = connect()
    c = cnx.cursor()
    if gl.PROC:
        com.log("Executing proc:")
        com.log_print(script)
        c.execute(script)
        com.log("Proc executed")
    else:
        command_list = script.split(';\n')
        n = len(command_list)
        if command_list[n - 1]:
            command_list[n - 1] = command_list[n - 1].strip(';')
        else:
            command_list = command_list[:-1]
        for command in command_list:
            com.log("Executing command:")
            com.log_print(command)
            c.execute(command)
            com.log("Command executed")
    c.close()
    cnx.commit()
    cnx.close()

    dstr = com.get_duration_string(start_time)
    com.log(f"[sql] execute: end ({dstr})")
    com.log_print()
