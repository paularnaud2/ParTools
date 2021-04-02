from multiprocessing import Process
from multiprocessing import Manager
from time import sleep


def my_process(id, timeout, md):
    print(f"Process {id} running...")
    sleep(timeout)
    print(f"Process {id} over")
    md[id] = timeout
    return timeout


def run():
    manager = Manager()
    md = manager.dict()
    p1 = Process(target=my_process, args=(1, 3, md))
    p2 = Process(target=my_process, args=(2, 5, md))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("md", md)
    print("Traitement terminé")


if __name__ == '__main__':
    run()
