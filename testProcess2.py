from multiprocessing import Process
from multiprocessing import Manager
from time import sleep
from test import gl


def my_process(timeout, md):
    gl.md = md
    print(f"Process running with timeout set to {timeout}...")
    sleep(timeout)
    print('Timeout 1')
    gl.md['STOP'] = True
    sleep(timeout)
    print('Timeout 2')
    print("Process over")
    return


def run():
    manager = Manager()
    md = manager.dict()
    md['STOP'] = False
    p = Process(target=my_process, args=(3, md))
    p.start()
    while not md['STOP']:
        sleep(0.1)
    print('Stop signal received !')
    p.terminate()
    print("md", md)
    print("Traitement terminé")


if __name__ == '__main__':
    run()
