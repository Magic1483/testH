import logging
from os import stat
import socket
import sys
import time
import threading
import argparse
from typing_extensions import List

logger = logging.getLogger()
peers = []
RUN_EVENT = threading.Event()

def AddrToMsg(addr):
    """
    """
    s = addr[0]+':'+str(addr[1])
    return str(s).encode('utf8')

def MsgToAddr(addr):
    """
    """
    ip,port = addr.decode('utf8').split(':')
    return (ip,int(port))


def Listen(sock:socket.socket):
    global RUN_EVENT
    while  not RUN_EVENT.is_set():
        data,addr = sock.recvfrom(1024)
        logger.info('REC '+str(data))

def Send(sock:socket.socket,addr):
    global RUN_EVENT
    while  not RUN_EVENT.is_set():
        msg = b'test request'
        sock.sendto(msg,addr)
        logger.info('SEND '+str(msg))
        time.sleep(0.5)


def main(server_host = '83.147.245.51', server_port = 9999):
    global RUN_EVENT
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(b'',(server_host,server_port))      # send req to server

    data,addr = sock.recvfrom(1024)     # rec from server
    logger.info('Get client from server {} {}'.format(addr,data))
    addr = MsgToAddr(data) # peer info

    send_th   = threading.Thread(target=Send,args=(sock,addr))
    listen_th = threading.Thread(target=List,args=(sock,))
    send_th.start()
    listen_th.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info('STOP Service')
        RUN_EVENT.set()


def start():
    if len(sys.argv) < 2:
        print('Usage python peer.py server_ip port:optional\ndefault port 9999')
        return

    ip = sys.argv[1]
    port = 9999
    if len(sys.argv) == 3: port = int(sys.argv[2])

    print('Selected server {}:{}'.format(ip,port))
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
    # main()


if __name__ == '__main__':
    start()
