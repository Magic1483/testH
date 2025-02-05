import logging
from os import stat
import socket
import sys
import time
import threading
import argparse

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


def main(server_host = '83.147.245.51', server_port = 9999):
    global RUN_EVENT
    window = 100 # offset for port of peer
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    try:
        while True:
            sock.sendto(b'',(server_host,server_port))      # send req to server
            data,addr = sock.recvfrom(1024)     # rec from server
            logger.info('Get self info from server {} {}'.format(addr,data))
            addr = MsgToAddr(data) # peer info
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
    main()


if __name__ == '__main__':
    start()
