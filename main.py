from threading import Thread
from os import system
from time import sleep

initialFile = [
    '0',  # 是否重启
    '0',
    '0',
]


def init():
    with open('status', 'w+') as file:
        file.write('\n'.join(initialFile))


def getStatus():
    try:
        with open('status', 'r+') as file:
            status = file.read().split('\n')
    except:
        init()
        status = initialFile
    return status


def writeStatus(status):
    with open('status', 'w+') as file:
        file.write('\n'.join(status))


def closeServer():
    system("ps au | grep ./startup.sh | grep /bin/bash | awk '{print $2}' | xargs kill")


def openServer():
    system('./startup.sh')


if __name__ == '__main__':
    thread = Thread(target=openServer)
    thread.start()
    while True:
        sleep(3)
        status = getStatus()
        if status[0] == '1':
            print('Restarting the server.')
            closeServer()
            sleep(5)
            thread = Thread(target=openServer)
            thread.start()
            status[0] = '0'
            writeStatus(status)
