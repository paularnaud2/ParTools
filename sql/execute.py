import common as com
import sql.gl as gl

from sql.init import init
from sql.connect import connect
from sql.functions import get_final_script


@com.log_exeptions
def execute(**params):
    com.log('[sql] execute')
    com.init_params(gl, params)
    init()
    script = get_final_script(gl.SCRIPT_FILE)
    cnx = connect(ENV=gl.ENV, DB=gl.DB)
    c = cnx.cursor()
    if gl.PROC:
        com.log("Execution de la procédure :")
        com.log_print(script)
        c.execute(script)
        com.log("Procédure executée")
    else:
        command_list = script.split(';\n')
        for command in command_list[:-1]:
            com.log("Execution de la commande :")
            com.log_print(command)
            c.execute(command)
            com.log("Commande executée")
    c.close()
    cnx.commit()
    cnx.close()
    com.log_print()
