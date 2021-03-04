import os
import qdd.gl as gl
import common as com

from time import time
from qdd.init import set_dirs
from qdd.init import init_tmp_dir
from qdd.init import init_compare_files
from toolDup import del_dup_list
from qdd.csf import compare_sorted_files
from qdd.sort import sort_file
from qdd.functions import check_split
from qdd.functions import compare_headers


def run_qdd(**params):

    com.log("[qdd] run_qdd")
    start_time = time()
    com.init_params(gl, params)
    init_tmp_dir()
    dirs = set_dirs()
    com.log(f"Tri et comparaison des fichiers {dirs['in1']} et {dirs['in2']}")
    com.log_print('|')
    com.check_header(dirs["in1"])
    com.check_header(dirs["in2"])
    compare_headers(dirs["in1"], dirs["in2"])
    sort_file(dirs["in1"], dirs["out1"], True, 1)
    sort_file(dirs["in2"], dirs["out2"], True, 2)
    if not compare_files(dirs["out1"], dirs["out2"], dirs["out"]):
        com.log_print('|')
        check_split(dirs["out"])

    s = "Exécution terminée en {}"
    duration = com.get_duration_ms(start_time)
    s = s.format(com.get_duration_string(duration))
    com.log(s)
    com.send_notif(s, "qdd", duration)
    com.log_print()
    if gl.OPEN_OUT_FILE:
        os.startfile(dirs["out"])


def file_match(in1, in2, del_dup=False, compare=False, err=True, out=''):
    com.log("[qdd] file_match")
    s = f"Comparaison des fichiers {in1} et {in2} en cours..."
    com.log(s)
    ar1 = com.load_csv(in1)
    ar2 = com.load_csv(in2)
    ar1.sort()
    ar2.sort()
    if del_dup:
        ar1 = del_dup_list(ar1)
        ar2 = del_dup_list(ar2)

    res = ar1 == ar2
    if res:
        com.log("Les deux fichiers sont identiques")
    else:
        com.log("Les deux fichiers sont différents.")

    if not res or compare:
        init_compare_files(out)
        com.save_csv(ar1, gl.TMP_1)
        com.save_csv(ar2, gl.TMP_2)
        com.log(f"Comparaison de '{gl.TMP_1}' et '{gl.TMP_2}'...")
        compare_files(gl.TMP_1, gl.TMP_2, gl.OUT_DIR)

    if not res and err:
        os.startfile(gl.OUT_DIR)
        assert res is True
    com.log_print()


def compare_files(in_1, in_2, out):

    start_time = time()
    com.gen_header(in_1, gl.COMPARE_FIELD, out)
    compare_sorted_files(in_1, in_2, out)

    duration = com.get_duration_ms(start_time)
    ds = com.get_duration_string(duration)
    s = f"Comparaison terminée en {ds}"
    com.log(s)
    if gl.counters["diff"] == 0:
        com.log("Les deux fichiers sont identiques")
        return True
    else:
        bn = com.big_number(gl.counters["diff"])
        com.log(f"{bn} écarts trouvés")
        return False
