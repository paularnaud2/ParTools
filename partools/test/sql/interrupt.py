import math
from time import sleep
from multiprocessing import Process
from multiprocessing import Manager

import partools.utils as u

from . import gl
from .main import upload
from .main import download


def upload_interrupted():
    """This function is used to simulate an unexpected interruption of the
    sql.upload function.

    md['T'] is the duration of one insert in ms. As the aim is to
    simulate an unexpected stop, once this duration is received from the
    subprocess, the main process sleeps for this duration before killing
    the subprocess. This is believed to introduce some kind of
    randomness to the moment where the subprocess is killed (we also
    want to test interruption while the the file gl.tmp_file_chunk  is
    being written)
    """

    manager = Manager()
    md = manager.dict()
    md["T"] = False
    md["LOG_PATH"] = u.g.log_path
    u.log("[sql] upload: start", c_out=False)
    p = Process(target=upload, args=(gl.IN, True, md))
    p.start()
    while not md["T"]:
        pass
    u.log("Duration received")

    t = md["T"] / 1000
    sleep(t)
    u.log("Terminating subprocess...")
    p.terminate()
    u.log("Subprocess terminated (upload_interrupted)\n")


def download_interrupted(query, out):
    init_msg = "[sql] download: start"
    kwargs = {"query": query, "out": out, "tr": True}
    interrupt(download, kwargs, init_msg)


def interrupt(function, kwargs, init_msg):
    manager = Manager()
    md = manager.dict()
    md["STOP"] = False
    md["N_STOP"] = math.floor(0.7 * 2900)
    md["LOG_PATH"] = u.g.log_path
    u.log(init_msg, c_out=False)
    kwargs['md'] = md

    p = Process(target=function, kwargs=kwargs)
    p.start()
    while not md["STOP"]:
        pass
    p.terminate()
