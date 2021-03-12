import common as com

import sql.gl as gl

from time import time
from sql.init import init
from sql.connect import connect
from sql.functions import get_final_script


@com.log_exeptions
def execute(**params):
    com.log('[sql] execute: start')
    start_time = time()
    com.init_params(gl, params)
    init()
    script = get_final_script(gl.SCRIPT_FILE)
    cnx = connect(ENV=gl.ENV, DB=gl.DB)
    c = cnx.cursor()
    if gl.PROC:
        com.log("Executing proc:")
        com.log_print(script)
        c.execute(script)
        com.log("Proc executed")
    else:
        command_list = script.split(';\n')
        for command in command_list[:-1]:
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
