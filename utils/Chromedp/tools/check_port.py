import os
import random
import socket


def is_open(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, int(port)))
        s.shutdown(2)

        return True
    except:

        return False


def random_port():
    port = random.randint(10000, 20000)
    if is_open('127.0.0.1', port):
        return random_port()
    return port


def killport(port):
    command = '''kill -9 $(netstat -nlp | grep :''' + str(port) + ''' | awk '{print $7}' | awk -F"/" '{ print $1 }')'''
    os.system(command)


if __name__ == '__main__':
    print(random_port())
