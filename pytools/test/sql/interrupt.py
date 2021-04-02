from time import sleep

from multiprocessing import Process
from multiprocessing import Manager

import pytools.common as com
import pytools.common.g as g

from pytools.test import gl
from .main import upload
from .main import download


def upload_interrupted():
    """This function is used to simulate an unexpected interruption of the
    sql.upload function.

    md['T'] is the duration of one insert in ms. As the aim is to
    simulate an unexpected stop, once this duration is received from the
    subprocess, the main process sleeps for this duration before killing
    the subprocess. This is belieived to introduce some kind of
    randomness to the moment where the subprocess is killed (we also
    wanna test interruption while the the file gl.TMP_FILE_CHUNK  is
    being written)
    """

    manager = Manager()
    md = manager.dict()
    md["T"] = False
    md["LOG_FILE"] = g.LOG_FILE
    com.log("[sql] upload: start", c_out=False)
    p = Process(target=upload, args=(gl.SQL_IN, True, md))
    p.start()
    while not md["T"]:
        pass
    com.log("Duration received")

    t = md["T"] / 1000
    sleep(t)
    com.log("Terminating subprocess...")
    p.terminate()
    com.log("Subprocess terminated (upload_interrupted)\n")


def download_interrupted(query, out):
    manager = Manager()
    md = manager.dict()
    md["STOP"] = False
    md["N_STOP"] = 0.8 * 2900
    md["LOG_FILE"] = g.LOG_FILE
    com.log("[sql] download: start", c_out=False)
    d = {"query": query, "out": out, "tr": True, "md": md}
    p = Process(target=download, kwargs=d)
    p.start()
    while not md["STOP"]:
        pass
    p.terminate()
