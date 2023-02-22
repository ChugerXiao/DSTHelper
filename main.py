from threading import Thread
from os import system, path
from time import sleep
from configparser import ConfigParser


def init(conf):
    with open('status.ini', 'w+'): pass
    conf.add_section('STATUS')
    conf.set('STATUS', 'restart', 'false')
    conf.write(open('status.ini', 'w'))


def closeServer():
    system("ps au | grep ./startup.sh | grep /bin/bash | awk '{print $2}' | xargs kill")


def openServer():
    system('./startup.sh')


if __name__ == '__main__':
    thread = Thread(target=openServer)
    thread.start()
    conf = ConfigParser()
    while True:
        sleep(3)
        if not path.exists('status.ini'): init(conf)
        conf.read('status.ini')
        try:
            restart = conf.get('STATUS', 'restart')
        except:
            restart = 'false'
        if restart == 'true':
            print('Restarting the server.')
            closeServer()
            sleep(5)
            thread = Thread(target=openServer)
            thread.start()
            conf.set('STATUS','restart','false')
            conf.write(open('status.ini', 'w'))
